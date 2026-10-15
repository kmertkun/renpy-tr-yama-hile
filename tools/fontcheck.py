"""Check whether TrueType/OpenType fonts contain Turkish glyphs (cmap only)."""
import struct, sys

CHARS = "çÇğĞıİöÖşŞüÜ"


def cmap_chars(path):
    data = open(path, "rb").read()
    num = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num):
        tag, _, off, ln = struct.unpack(">4sIII", data[12 + 16 * i: 28 + 16 * i])
        tables[tag] = off
    base = tables[b"cmap"]
    n = struct.unpack(">H", data[base + 2: base + 4])[0]
    found = set()
    for i in range(n):
        pid, eid, off = struct.unpack(">HHI", data[base + 4 + 8 * i: base + 12 + 8 * i])
        sub = base + off
        fmt = struct.unpack(">H", data[sub: sub + 2])[0]
        if fmt == 4:
            segx2 = struct.unpack(">H", data[sub + 6: sub + 8])[0]
            seg = segx2 // 2
            ends = struct.unpack(">%dH" % seg, data[sub + 14: sub + 14 + segx2])
            starts = struct.unpack(">%dH" % seg, data[sub + 16 + segx2: sub + 16 + 2 * segx2])
            for s, e in zip(starts, ends):
                for c in CHARS:
                    if s <= ord(c) <= e:
                        found.add(c)
        elif fmt == 12:
            ngroups = struct.unpack(">I", data[sub + 12: sub + 16])[0]
            for g in range(ngroups):
                s, e, _ = struct.unpack(">III", data[sub + 16 + 12 * g: sub + 28 + 12 * g])
                for c in CHARS:
                    if s <= ord(c) <= e:
                        found.add(c)
    return found


for p in sys.argv[1:]:
    try:
        f = cmap_chars(p)
        miss = "".join(c for c in CHARS if c not in f)
        print(p.split("/")[-1], "OK" if not miss else "MISSING: " + miss)
    except Exception as ex:
        print(p, "error", ex)
