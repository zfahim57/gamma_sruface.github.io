import json
import os

class GammaJSON:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self.load()
        self.all_keys = self.data.keys()
        self.all_files = [f["filename"] for f in self.data["files"]]
    # -----------------------------
    # Load + Save
    # -----------------------------
    def load(self):
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"{self.filename} not found.")

        with open(self.filename, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)
        print(f"✔ Saved changes to {self.filename}")


    # -----------------------------
    # File-level operations
    # -----------------------------
    def strip_all_extensions(self):
        for f in self.data["files"]:
            if f["filename"].endswith(".cif"):
                f["filename"] = f["filename"][:-4]
        print("✔ Removed .cif from all filenames")

    def list_files(self):
        print("\nFiles in dataset:\n")
        for i, file in enumerate(self.data["files"]):
            print(f"{i+1}. {file['filename']}")
        print()

    def add_file(self, filename, path, smiles):
        entry = {
            "filename": filename,
            "path": path,
            "smiles": smiles,
            "hkls": []
        }
        self.data["files"].append(entry)
        print(f"✔ Added file: {filename}")

    def add_info(self, filename, key, value):
        for f in self.data["files"]:
            if f["filename"] == filename:
                f[key] = value
                print(f"✔ Added info to {filename}: {key} = {value}")
                return
        print(f"⚠ File not found: {filename}")

    def add_image_hkl(self, filename):
        for f in self.data["files"]:
            base = f["filename"]
            planes = f["hkls"]
            for plane in planes:
                plane_path = os.path.join("/images", base, f"plane_{plane['plane'][0]}_{plane['plane'][1]}_{plane['plane'][2]}.jpg")
                self.add_info(filename, f"image_plane_{plane['plane'][0]}_{plane['plane'][1]}_{plane['plane'][2]}", plane_path)
        print("✔ Added image paths to all HKLs")

    def delete_file(self, filename):
        before = len(self.data["files"])
        self.data["files"] = [f for f in self.data["files"] if f["filename"] != filename]
        after = len(self.data["files"])

        if before == after:
            print(f"⚠ No such file: {filename}")
        else:
            print(f"✔ Deleted: {filename}")

    

    def update_smiles(self, filename, new_smiles):
        for f in self.data["files"]:
            if f["filename"] == filename:
                f["smiles"] = new_smiles
                print(f"✔ Updated SMILES for {filename}")
                return
        print(f"⚠ File not found: {filename}")


    # -----------------------------
    # HKL-level operations
    # -----------------------------
    def add_hkl(self, filename, plane, d_spacing, distance_list):
        for f in self.data["files"]:
            if f["filename"] == filename:
                entry = {
                    "plane": plane,
                    "d_spacing": d_spacing,
                    "distance": distance_list
                }
                f["hkls"].append(entry)
                print(f"✔ Added HKL to {filename}: plane={plane}")
                return

        print(f"⚠ File not found: {filename}")



# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    db = GammaJSON("data.json")
    
    # Show existing files
    #for struct in db.all_files:
    #    db.add_info(struct, "Status", "Good")
    #print("Status info added to all files.")
    #db.save()

    # Adding Image paths to all HKLs
    #for struct in db.all_files:
    #    db.add_image_hkl(struct)
    #db.save()

    # Delete a file
    #db.delete_file("4-chlorobenzonitrile")
    #db.save()
    db.delete_file("4-(n-hexyloxy)benzoic-acid")
    db.delete_file("4-NBA")
    db.delete_file("4-FBN")
    db.save()