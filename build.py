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

.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 100px;
    margin-top: 10px;
}}

/* NEW: wrapper per image + d-spacing label */
.gallery-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.gallery-item .d-label {{
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 6px;
}}

.gallery img {{
    width: 100%;
    height: 400px;          /* Controls size → increase if needed */
    object-fit: contain;    /* Prevent cropping */
    background: #fafafa;    /* Fill empty space when aspect ratio differs */
    padding: 10px;          /* Adds clean spacing */
    border-radius: 6px;
    border: 1px solid #ccc;
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
    cif_name = filename if filename.lower().endswith(".xyz") else filename + ".xyz"
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
                     data-type="xyz"
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

    # ---------- All images gallery (SUMMARY) ----------
    # Collect plane images for gallery, WITH d-spacing
    plane_images = []
    for hkl in hkls:
        image = hkl.get("image")
        if image:
            img_fs = os.path.join(base_dir, image.lstrip("/"))
            if os.path.exists(img_fs):
                plane_images.append({
                    "src": image.lstrip("/"),
                    "d": hkl.get("distance", "N/A"),
                    "plane": hkl.get("plane", [0, 0, 0])
                })

    # Add gallery if at least one image
    if plane_images:
        html += """<div><strong>Plane Images:</strong></div>"""
        html += """<div class="gallery">"""
        for entry in plane_images:
            src = entry["src"]
            d = entry["d"]
            plane = entry["plane"]
            html += f'''
                <div class="gallery-item">
                    <div class="d-label">
                        Plane ({plane[0]}, {plane[1]}, {plane[2]}): distance = {d} Å
                    </div>
                    <img src="{src}" alt="plane thumbnail">
                </div>
            '''
        html += "</div>"

    # ---------- HKL sections (detailed, as before) ----------
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
                     style="max-width: 50%; border-radius: 6px; margin-top: 5px;">
                """

        html += """
            </div>
        """

    html += """
        </div>  <!-- end file content -->
    </div>      <!-- end card -->
    """

# -------- JS: collapsible + unit cell + 2×2×2 --------
html += """
<script>
// Collapsible logic
var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        content.style.display = (content.style.display === "block") ? "none" : "block";
    });
}

// Helper: wait for model, then add unit cell + replicate
function enhanceViewerWhenReady(viewer, id) {
    var tries = 0;
    var maxTries = 20;      // ~20 * 300ms = 6 seconds max
    var interval = setInterval(function() {
        var model = null;
        try {
            model = viewer.getModel();
        } catch (e) {
            model = null;
        }

        if (model) {
            clearInterval(interval);

            try {
                viewer.addUnitCell();
            } catch (e) {
                console.warn("addUnitCell failed for", id, e);
            }

            try {
                viewer.replicateUnitCell(2, 2, 2);
            } catch (e) {
                console.warn("replicateUnitCell failed for", id, e);
            }

            viewer.zoomTo();
            viewer.render();
        } else {
            tries += 1;
            if (tries >= maxTries) {
                clearInterval(interval);
                console.warn("No model loaded for viewer", id, "after", maxTries, "tries.");
            }
        }
    }, 300);
}

// Once 3Dmol auto-viewers are initialized, schedule enhancement
window.addEventListener("load", function() {
    if (typeof $3Dmol === "undefined" || !$3Dmol.viewers) {
        console.warn("3Dmol not ready or no viewers found.");
        return;
    }

    document.querySelectorAll(".viewer_3Dmoljs").forEach(function(div) {
        var id = div.id;
        var viewer = $3Dmol.viewers && $3Dmol.viewers[id];
        if (!viewer) {
            console.warn("No 3Dmol viewer found for div id:", id);
            return;
        }

        // Wait for model to exist, then add box + 2x2x2
        enhanceViewerWhenReady(viewer, id);
    });
});
</script>
</body>
</html>
"""

# -------- Write HTML --------
with open("index.html", "w") as f:
    f.write(html)

print("Website generated successfully: index.html")