import os, re, sys, json

root = sys.argv[1]
QUOTE = re.compile(r'"((?:[^"\\]|\\.)*)"')
WORD = re.compile(r'[a-zA-Z]{3}')


def scan(lang):
    d = os.path.join(root, lang)
    ids = set(); strings = {}; same_dlg = []; same_str = []
    for dp, _, fs in os.walk(d):
        for f in fs:
            if not f.endswith(".rpy"):
                continue
            p = os.path.join(dp, f); rel = os.path.relpath(p, d)
            lines = open(p, encoding="utf-8-sig").read().split("\n")
            i = 0; cur = None; orig = None
            while i < len(lines):
                l = lines[i]; s = l.strip()
                m = re.match(r'translate \w+ (\w+):\s*$', l)
                if m:
                    cur = None if m.group(1) == "strings" else m.group(1)
                    if cur:
                        ids.add(cur)
                    orig = None
                elif s.startswith("old "):
                    o = s[4:]
                    n = lines[i + 1].strip()[4:] if i + 1 < len(lines) else ""
                    strings[o] = n
                    if o == n and WORD.search(o):
                        same_str.append((rel, o))
                    i += 1
                elif cur and s.startswith("# original:"):
                    orig = s[len("# original:"):].strip()
                elif cur and orig is not None and s and not s.startswith("#"):
                    q = QUOTE.search(l); oq = QUOTE.search(orig)
                    if q and oq and oq.group(1) == q.group(1) and WORD.search(q.group(1)):
                        same_dlg.append((rel, cur, q.group(1)))
                    orig = None
                i += 1
    return ids, strings, same_dlg, same_str


res = {}
for lang in ["turkish", "spanish", "russian", "french"]:
    res[lang] = scan(lang)
    ids, st, sd, ss = res[lang]
    print(lang, "dialog", len(ids), "strings", len(st), "untranslated dlg", len(sd), "untranslated str", len(ss))
ids, st, sd, ss = res["turkish"]
print("dialog ids missing vs spanish:", len(res["spanish"][0] - ids), " strings missing:", len(set(res["spanish"][1]) - set(st)))
json.dump({"dlg": sd, "str": ss}, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for x in sd[:15]:
    print("D", x)
for x in ss[:30]:
    print("S", x)
