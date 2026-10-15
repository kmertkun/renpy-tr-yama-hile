import os, re, sys

ext = sys.argv[1]
tl = os.path.join(ext, "tl")


def blocks(lang):
    out = {}
    d = os.path.join(tl, lang)
    for dp, _, fs in os.walk(d):
        for f in fs:
            if not f.endswith(".rpy"):
                continue
            txt = open(os.path.join(dp, f), encoding="utf-8-sig").read()
            for m in re.finditer(r'# (game/[^\n]+):(\d+)\ntranslate \w+ (\w+):\n((?:    [^\n]*\n|\n)*)', txt):
                if m.group(3) == "strings":
                    continue
                o = re.search(r'# original: ([^\n]*)', m.group(4))
                out[m.group(3)] = (m.group(1), int(m.group(2)), o.group(1) if o else "")
    return out


tr = blocks("turkish")
src_cache = {}
for ref in ["spanish", "russian", "french"]:
    other = blocks(ref)
    missing = [k for k in other if k not in tr]
    live = 0; stale = 0; samples = []
    for k in missing:
        fn, ln, orig = other[k]
        path = os.path.join(ext, fn[len("game/"):])
        if path not in src_cache:
            src_cache[path] = open(path, encoding="utf-8-sig").read() if os.path.exists(path) else ""
        q = re.search(r'"((?:[^"\\]|\\.)*)"', orig)
        needle = q.group(1) if q else orig
        if needle and needle in src_cache[path]:
            live += 1
            if len(samples) < 8:
                samples.append((fn, ln, needle[:80]))
        else:
            stale += 1
    print(ref, "missing-in-turkish:", len(missing), "still in source:", live, "stale:", stale)
    for s in samples:
        print("   ", s)
