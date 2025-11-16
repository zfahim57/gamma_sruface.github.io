import json
import os

DATA = "data.json"
pwd = os.getcwd()
with open(DATA, "r") as f:
    data = json.load(f)

for file_entry in data["files"]:
    base = file_entry["filename"]  # e.g. "4-(n-hexyloxy)benzoic-acid"
    hkls = file_entry.get("hkls", [])

    for hkl in hkls:
        h, k, l = hkl["plane"]
        # force a consistent image path for this plane
        temp_path = os.path.join("images", base)
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        else:
            pass

                