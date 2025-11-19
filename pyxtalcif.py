import numpy as np
from pyxtal import pyxtal
from ase.io import write
import json
import os

def load_cif(file_path, file_name, smiles, output_path):
    print(f"→ Loading CIF for {file_name} with SMILES: {smiles}")
    cif = file_name + '.cif'
    cif = os.path.join(file_path, cif)
    xtal = pyxtal(molecular=True)
    try:
        xtal.from_seed(cif, [x+'.smi' for x in smiles.split('.')])
        print(f"✔ Loaded {cif} successfully.")
    except Exception as e:
        print(f"⚠ Error loading {cif}: {e}")
        return
    xtal_to_ase = xtal.to_ase()
    #atoms = xtal_to_ase.get_positions()

    output_path = os.path.join(output_path, file_name + '.xyz')
    write(output_path, xtal_to_ase)
    print(f"✔ Saved converted CIF to {output_path}.")

if __name__ == "__main__":
    file_path = os.getcwd()
    file_path = os.path.join(file_path, 'cif')
    output_path = os.path.join(file_path, 'converted_cifs')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    db = "data.json"
    with open(db, "r") as f:
        data = json.load(f)
    for file_entry in data["files"]:
        filename = file_entry["filename"]
        smiles = file_entry["smiles"]
        load_cif(file_path, filename, smiles, output_path)
    print("✔ Converted all CIFs using pyxtal and saved to 'converted_cifs' folder.")
