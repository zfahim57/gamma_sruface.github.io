import json

DATA = "data.json"

with open(DATA, "r") as f:
    data = json.load(f)

for file_entry in data["files"]:
    hkls = file_entry.get("hkls", [])
    seen = {}
    new_hkls = []

    for hkl in hkls:
        plane = tuple(hkl["plane"])  # (h, k, l)
        if plane not in seen:
            # first time we see this plane → keep it
            seen[plane] = hkl
            new_hkls.append(hkl)
        else:
            # duplicate plane → merge info into the first one
            existing = seen[plane]

            # merge distance lists (unique values, same order)
            d_old = existing.get("distance", [])
            d_new = hkl.get("distance", [])
            merged = list(dict.fromkeys(d_old + d_new))
            existing["distance"] = merged

            # if existing has no image but new one does, keep it
            if "image" not in existing and "image" in hkl:
                existing["image"] = hkl["image"]

    file_entry["hkls"] = new_hkls

with open(DATA, "w") as f:
    json.dump(data, f, indent=4)

print("✔ Deduplicated HKLs by plane in data.json")