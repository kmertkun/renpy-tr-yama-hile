"""Inject translated chunk JSON back into a Ren'Py tl template.

usage: tl_inject.py <template_tl_dir> <chunks_dir> <out_tl_dir>
Entries whose translation is missing or breaks a placeholder keep the English text.
"""
import os, re, sys, json, glob, shutil

tpl_dir, chunks_dir, out_dir = sys.argv[1:4]
QUOTE = re.compile(r'"((?:[^"\\]|\\.)*)"')
VARS = re.compile(r'\[[^\[\]]*\]')
TAGS = re.compile(r'\{[^{}]*\}')
PCT = re.compile(r'%(?:\([^)]*\))?[sdif]')
BS = chr(92)

src = {}
tr = {}
for f in sorted(glob.glob(os.path.join(chunks_dir, "chunk_[0-9][0-9].json"))):
    for e in json.load(open(f, encoding="utf-8")):
        src[e["k"]] = e["en"]
    out = f[:-5] + ".tr.json"
    if os.path.exists(out):
        try:
            tr.update(json.load(open(out, encoding="utf-8")))
        except Exception as ex:
            print("BAD JSON", out, ex)


def sig(s):
    # "[[" and "{{" are escaped literal brackets, not variables/tags
    s = s.replace("[[", "\x00").replace("{{", "\x01")
    tags = sorted(t for t in TAGS.findall(s) if not t.startswith("{#"))
    return sorted(VARS.findall(s)), tags, sorted(PCT.findall(s)), s.count(BS + "n")


def escape(s):
    return re.sub(r'(?<!\\)"', BS + BS + '"', s)


ok = 0; missing = []; broken = []
use = {}
for k, en in src.items():
    t = tr.get(k)
    if not isinstance(t, str) or not t.strip():
        missing.append(k); continue
    t = t.replace("\r", "").replace("\n", BS + "n")
    # {#...} disambiguation tags must survive as-is at the start
    m = re.match(r'(\{#[^}]*\})', en)
    if m and not t.startswith(m.group(1)):
        t = m.group(1) + t
    if sig(en) != sig(t):
        broken.append((k, en, t)); continue
    use[k] = escape(t); ok += 1

if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
for dp, _, fs in os.walk(tpl_dir):
    for f in fs:
        if not f.endswith(".rpy"):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, tpl_dir).replace("\\", "/")
        lines = open(p, encoding="utf-8-sig").read().split("\n")
        for i, l in enumerate(lines):
            k = "%s:%d" % (rel, i)
            if k in use:
                qs = list(QUOTE.finditer(l))
                m = qs[-1] if len(qs) > 1 else qs[0]
                lines[i] = l[:m.start(1)] + use[k] + l[m.end(1):]
        dst = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write("﻿" + "\n".join(lines))

print("translated", ok, "of", len(src), "| missing", len(missing), "| placeholder mismatch (kept English)", len(broken))
for k, en, t in broken[:15]:
    print("  BROKEN", k, "\n     EN:", en, "\n     TR:", t)
json.dump({"missing": missing, "broken": broken}, open(os.path.join(chunks_dir, "inject_report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
