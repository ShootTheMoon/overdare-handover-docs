"""manifest.json -> overdare_create_instances `itemsFile` payloads.

Run with plain system python (no Blender needed).

    python make_items.py collision      # ready now, needs no import
    python make_items.py meshes         # needs meshids.json from the bulk import

Coordinate convention baked into the manifest (VERIFY with ONE part first):
    blender (bx,by,bz)      -> engine (bx, bz, -by)          FBX is written Y-up
    blender size (sx,sy,sz) -> engine size (sx, sz, sy)      Y is height
    blender yaw about +Z    -> engine orientation [0, yaw, 0]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(HERE, "manifest.json")
CHUNK = 200          # overdare_create_instances itemsFile limit


def load():
    return json.load(open(MAN, encoding="utf-8"))


def collision_items(m):
    """Invisible engine Parts. MeshPart has no CollisionFidelity in OVERDARE, so these
       carry every collision and every raycast in the map -- including the ground probe
       TeamServer.snapToGround uses to seat spawns, which is why canQuery stays true."""
    out = []
    for i, c in enumerate(m["collision"]):
        out.append({
            "className": "Part",
            "name": "%s_%03d" % (c["name"].split(".")[0], i),
            "props": {
                "position": c["engine_pos"],
                "size": c["size"],
                "orientation": [0, c["yaw_deg"], 0],
                "anchored": True, "mobility": "Static",
                "transparency": 1,
                "canCollide": True, "canQuery": True, "canTouch": False,
                "castShadow": False, "locked": True,
                "material": "Plastic",
            },
        })
    return out


def mesh_items(m, meshids, texids):
    """One MeshPart per placement. CanCollide is false on every one: the invisible
       boxes above do the physics, exactly as JSN_Sangok does it."""
    out, missing = [], []
    for rec in m["meshes"]:
        mid = meshids.get(rec["mesh"])
        if not mid:
            missing.append(rec["mesh"])
            continue
        tex = texids.get(rec["mesh"])
        for i, inst in enumerate(rec["instances"]):
            props = {
                "position": inst["engine_pos"],
                "orientation": [0, inst["yaw_deg"], 0],
                "meshId": mid,
                "anchored": True, "mobility": "Static",
                "canCollide": False, "canQuery": False, "canTouch": False,
                "locked": True,
            }
            if tex:
                props["raw"] = {"TextureId": tex}
            out.append({
                "className": "MeshPart",
                "name": "%s_%02d" % (rec["mesh"], i),
                "props": props,
            })
    if missing:
        print("  !! no meshId yet for %d meshes: %s" % (len(missing), missing[:6]))
    return out


def write(tag, items):
    paths = []
    for i in range(0, len(items), CHUNK):
        part = items[i:i + CHUNK]
        p = os.path.join(HERE, "items_%s_%02d.json" % (tag, i // CHUNK))
        json.dump(part, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        paths.append((os.path.basename(p), len(part)))
    return paths


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "collision"
    m = load()
    idpath = os.path.join(HERE, "meshids.json")
    ids = json.load(open(idpath, encoding="utf-8")) if os.path.exists(idpath) else {}
    if which == "collision":
        rows = write("col", collision_items(m))
    elif which == "meshes":
        rows = write("mesh", mesh_items(m, ids.get("mesh", {}), ids.get("tex", {})))
    else:
        raise SystemExit("usage: make_items.py [collision|meshes]")
    for f, n in rows:
        print("%-32s %4d items" % (f, n))
