import json
import os

# Load JSON
with open("data.json") as f:
    data = json.load(f)

print("JSON keys:", data.keys())

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gamma Surface Calculations</title>

<!-- JSmol core (already present in your jsmol/ folder) -->
<script type="text/javascript" src="jsmol/JSmol.min.js"></script>

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
.cif-viewer {{
    width: 100%;
    height: 400px;
    min-height: 400px;
    border-radius: 6px;
    border: 1px solid #ddd;
    margin-top: 5px;
    display: none;
    background-color: #ffffff;
}}
.view-cif-btn {{
    margin-top: 10px;
    padding: 6px 10px;
    font-size: 14px;
    border-radius: 4px;
    border: 1px solid #aaa;
    background-color: #eee;
    cursor: pointer;
}}
.view-cif-btn:hover {{
    background-color: #ddd;
}}
</style>

</head>

<body>
<h1>Gamma Surface Calculations</h1>
<h2>A collection of surface calculations for various molecular crystals using different force field styles.</h2>
"""

base_dir = os.path.dirname(os.path.abspath(__file__))

for idx, project in enumerate(data["files"]):

    # ---- compute status ----
    img_count = 0
    total_hkls = len(project["hkls"])

    for hkl in project["hkls"]:
        image = hkl.get("image")
        if image:
            img_fs = os.path.join(base_dir, image.lstrip("/"))
            if os.path.exists(img_fs):
                img_count += 1

    if img_count == total_hkls:
        status = "All Available"
    elif img_count > 0:
        status = "Partial"
    else:
        status = "Bad"

    # ---- CIF path in ./cif/ ----
    cif_name = project["filename"]
    if not cif_name.lower().endswith(".cif"):
        cif_name = cif_name + ".cif"
    cif_web_path = f"cif/{cif_name}"

    viewer_id = f"cif-viewer-{idx}"

    html += f"""
    <div class="card">
        <button class="collapsible file-toggle">
            {project['filename']} — <span style="color:#555;">({status})</span>
        </button>

        <div class="content">
            <p><strong>SMILES:</strong> {project['smiles']}</p>

            <div class="cif-viewer-container">
                <button class="view-cif-btn"
                        data-cif="{cif_web_path}"
                        data-target="{viewer_id}">
                    View CIF structure
                </button>
                <div id="{viewer_id}" class="cif-viewer"></div>
            </div>
    """

    # --- HKL sections ---
    for hkl in project["hkls"]:
        plane = hkl["plane"]
        d = hkl["d_spacing"]
        dist = hkl["distance"]
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

# ---- JS: collapsibles + JSmol viewers ----
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

// Tell JSmol we will inject applets dynamically
Jmol.setDocument(0);

var jsmolApplets = {};

document.addEventListener("DOMContentLoaded", function() {
    var buttons = document.querySelectorAll(".view-cif-btn");

    buttons.forEach(function(btn) {
        btn.addEventListener("click", function() {
            var cifUrl   = this.getAttribute("data-cif");
            var targetId = this.getAttribute("data-target");
            var viewerDiv = document.getElementById(targetId);

            // Toggle open/close
            if (viewerDiv.dataset.open === "true") {
                viewerDiv.style.display = "none";
                viewerDiv.dataset.open = "false";
                this.textContent = "View CIF structure";
                return;
            }

            viewerDiv.style.display = "block";
            viewerDiv.dataset.open = "true";
            this.textContent = "Hide CIF structure";

            // Initialize JSmol applet only once
            if (!viewerDiv.dataset.initialized) {
                viewerDiv.dataset.initialized = "true";

                var appletName = targetId + "_applet";

                // Here we follow JSmol's own pattern: put the load
                // script directly in Info.script, and use getAppletHtml().
                var Info = {
                    width: "100%",
                    height: "100%",
                    use: "HTML5",
                    j2sPath: "jsmol/j2s",
                    disableInitialConsole: true,
                    script:
                        "load " + cifUrl + ";" +
                        "set forcePacked true;" +
                        "set unitcell on;" +
                        "select *;" +
                        "wireframe 0.15;" +
                        "spacefill 25%;" +
                        "zoom 110;"
                };

                var applet = Jmol.getApplet(appletName, Info);
                jsmolApplets[targetId] = applet;

                // Insert the applet HTML into the div
                viewerDiv.innerHTML = Jmol.getAppletHtml(applet);
            }
        });
    });
});
</script>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("Website generated successfully: index.html")