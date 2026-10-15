import sys, zlib, pickle, os
src, out = sys.argv[1], sys.argv[2]
with open(src,'rb') as f:
    hdr = f.readline().split()
    off = int(hdr[1],16); key = int(hdr[2],16)
    f.seek(off); idx = pickle.loads(zlib.decompress(f.read()))
    for name, parts in idx.items():
        data = b''
        for p in parts:
            o, l = p[0]^key, p[1]^key
            pre = p[2] if len(p)>2 else b''
            if isinstance(pre,str): pre = pre.encode('latin1')
            f.seek(o); data += pre + f.read(l-len(pre))
        dst = os.path.join(out, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst,'wb').write(data)
        print(name)
