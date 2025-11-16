import json

DATA = "data.json"

with open(DATA, "r") as f:
    data = json.load(f)

for file_entry in data["files"]:
    base = file_entry["filename"]  # e.g. "4-(n-hexyloxy)benzoic-acid"
    hkls = file_entry.get("hkls", [])

    for hkl in hkls:
        h, k, l = hkl["plane"]
        # force a consistent image path for this plane
        hkl["image"] = f"images/{base}/plane_{h}_{k}_{l}.jpg"

print("✔ Rewrote all HKL image paths based on filename + plane")

with open(DATA, "w") as f:
    json.dump(data, f, indent=4)

print(f"✔ Saved fixed JSON to {DATA}")