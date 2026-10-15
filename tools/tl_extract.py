"""Extract translatable text from a Ren'Py tl/<lang> template into JSON chunks.

usage: tl_extract.py <tl_lang_dir> <out_dir> <num_chunks>
"""
import os, re, sys, json

tl_dir, out_dir, nchunks = sys.argv[1], sys.argv[2], int(sys.argv[3])
QUOTE = re.compile(r'"((?:[^"\\]|\\.)*)"')
WORD = re.compile(r'[A-Za-z]')

entries = []  # dict(k, f, line, who, t)

for dp, _, fs in os.walk(tl_dir):
    for f in sorted(fs):
        if not f.endswith(".rpy"):
            continue
        path = os.path.join(dp, f)
        rel = os.path.relpath(path, tl_dir).replace("\\", "/")
        lines = open(path, encoding="utf-8-sig").read().split("\n")
        in_strings = False
        for i, l in enumerate(lines):
            s = l.strip()
            if l.startswith("translate "):
                in_strings = l.rstrip().endswith(" strings:")
                continue
            if not s or s.startswith("#"):
                continue
            if in_strings:
                if s.startswith("new "):
                    m = QUOTE.search(s)
                    if m and WORD.search(m.group(1)):
                        entries.append(dict(k="%s:%d" % (rel, i), f=rel, who="", t=m.group(1)))
                continue
            # dialogue line inside translate block
            if l.startswith("    "):
                qs = list(QUOTE.finditer(l))
                if not qs:
                    continue
                m = qs[-1] if len(qs) > 1 else qs[0]
                # with two strings the first one is the speaker name
                who = l[:qs[0].start()].strip() if len(qs) == 1 else qs[0].group(1)
                if WORD.search(m.group(1)):
                    entries.append(dict(k="%s:%d" % (rel, i), f=rel, who=who, t=m.group(1)))

total = sum(len(e["t"]) for e in entries)
print("entries", len(entries), "chars", total)

os.makedirs(out_dir, exist_ok=True)
# split by size, keeping whole files together where possible
target = total / nchunks
chunks = [[]]; size = 0; last_f = None
for e in entries:
    if size >= target and e["f"] != last_f and len(chunks) < nchunks:
        chunks.append([]); size = 0
    chunks[-1].append(e); size += len(e["t"]); last_f = e["f"]
for n, c in enumerate(chunks, 1):
    data = [{"k": e["k"], "who": e["who"], "en": e["t"].replace(chr(92) + chr(34), chr(34))} for e in c]
    json.dump(data, open(os.path.join(out_dir, "chunk_%02d.json" % n), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("chunk_%02d" % n, len(c), "entries", sum(len(e["t"]) for e in c), "chars", c[0]["f"], "->", c[-1]["f"])
