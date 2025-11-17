import json
import os

# -------- Load JSON --------
with open("data.json") as f:
    data = json.load(f)

print("JSON keys:", data.keys())

# -------- HTML header --------
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gamma Surface Calculations</title>

<!-- 3Dmol.js: no install needed -->
<script src="https://3Dmol.org/build/3Dmol-min.js"></script>
<script src="https://3Dmol.org/build/3Dmol.ui-min.js"></script>

<style>
body {{
    font-family: Arial, sans-serif;
    padding: 2rem;
}}
.card {{
    padding: 1rem 1.5rem;
    background: #f7f7f7;
    border-radius: 10px;
    margin-bottom: 1rem;
}}
.collapsible {{
    background-color: #eee;
    color: #333;
    cursor: pointer;
    padding: 10px 15px;
    width: 100%;
    border: none;
    text-align: left;
    margin-top: 5px;
    border-radius: 6px;
    font-size: 15px;
}}
.active, .collapsible:hover {{
    background-color: #ccc;
}}
.content {{
    padding: 10px 15px;
    display: none;
    overflow: hidden;
    background-color: #f9f9f9;
    border-left: 3px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
}}
.file-toggle {{
    font-weight: bold;
    font-size: 16px;
    margin-top: 10px;
}}
.plane-toggle {{
    margin-left: 10px;
    font-size: 14px;
}}
.cif-viewer-container {{
    margin-top: 10px;
}}

/* 3Dmol viewer must have fixed size and position:relative */
.cif-viewer {{
    width: 100%;
    height: 400px;
    min-height: 400px;
    border-radius: 6px;
    border: 1px solid #ddd;
    margin-top: 5px;
    background-color: #ffffff;
    position: relative;
}}
</style>

</head>

<body>
<h1>Gamma Surface Calculations</h1>
<h2>A collection of surface calculations for various molecular crystals using different force field styles.</h2>
"""

base_dir = os.path.dirname(os.path.abspath(__file__))

# -------- Loop over projects --------
for idx, project in enumerate(data.get("files", [])):

    hkls = project.get("hkls", [])
    total_hkls = len(hkls)

    # compute status from images
    img_count = 0
    for hkl in hkls:
        image = hkl.get("image")
        if image:
            img_fs = os.path.join(base_dir, image.lstrip("/"))
            if os.path.exists(img_fs):
                img_count += 1

    if total_hkls > 0 and img_count == total_hkls:
        status = "All Available"
    elif img_count > 0:
        status = "Partial"
    else:
        status = "Bad"

    # CIF path in ./cif/
    filename = project.get("filename", f"file_{idx}")
    cif_name = filename if filename.lower().endswith(".cif") else filename + ".cif"
    cif_web_path = f"cif/{cif_name}"
    cif_fs_path = os.path.join(base_dir, cif_web_path)

    viewer_id = f"cif-viewer-{idx}"

    html += f"""
    <div class="card">
        <button class="collapsible file-toggle">
            {filename} — <span style="color:#555;">({status})</span>
        </button>

        <div class="content">
            <p><strong>SMILES:</strong> {project.get('smiles', 'N/A')}</p>

            <div class="cif-viewer-container">
    """

    # ---- Only add 3Dmol viewer if CIF actually exists ----
    if os.path.exists(cif_fs_path):
        html += f"""
                <div id="{viewer_id}"
                     class="viewer_3Dmoljs cif-viewer"
                     data-href="{cif_web_path}"
                     data-type="cif"
                     data-backgroundcolor="0xffffff"
                     data-style="stick">
                </div>
        """
    else:
        html += f"""
                <p style="color:#a00; font-style:italic;">
                    CIF file not found: {cif_web_path}
                </p>
        """

    html += """
            </div>  <!-- end cif-viewer-container -->
    """

    # HKL sections
    for hkl in hkls:
        plane = hkl.get("plane", [0, 0, 0])
        d = hkl.get("d_spacing", "N/A")
        dist = hkl.get("distance", "N/A")
        image = hkl.get("image")

        html += f"""
            <button class="collapsible plane-toggle">
                Plane: ({plane[0]}, {plane[1]}, {plane[2]})
            </button>

            <div class="content">
                <p><strong>d-spacing:</strong> {d} Å</p>
                <p><strong>distance:</strong> {dist}</p>
        """

        if image:
            img_fs = os.path.join(base_dir, image.lstrip("/"))
            if os.path.exists(img_fs):
                web_path = image.lstrip("/")
                html += f"""
                <p><strong>Image:</strong></p>
                <img src="{web_path}"
                     alt="Plane"
                     style="max-width: 100%; border-radius: 6px; margin-top: 5px;">
                """

        html += """
            </div>
        """

    html += """
        </div>  <!-- end file content -->
    </div>      <!-- end card -->
    """

# -------- JS: only collapsible logic --------
html += """
<script>
// Collapsible logic only
var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        content.style.display = (content.style.display === "block") ? "none" : "block";
    });
}
</script>

</body>
</html>
"""

# -------- Write HTML --------
with open("index.html", "w") as f:
    f.write(html)

print("Website generated successfully: index.html")