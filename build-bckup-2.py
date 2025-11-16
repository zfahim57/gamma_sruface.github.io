import json
import os

# Load JSON
with open("data.json") as f:
    data = json.load(f)

print("JSON keys:", data.keys())

# Build HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Gamma Surface Calculations</title>
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
</style>
</head>

<body>
<h1>Gamma Surface Calculations</h1>
<h2>A collection of surface calculations for various molecular crystals using different force field styles.</h2>
"""

for project in data["files"]:
    html += f"""
    <div class="card">
        <button class="collapsible file-toggle">{project['filename']}</button>
        <div class="content">
            <p><strong>SMILES:</strong> {project['smiles']}</p>
    """
    #status = project["Status"] 
    status,img_count = "Bad", 0
    # Add collapsible HKL sections
    base_dir = os.path.dirname(os.path.abspath(__file__))  # put this near the top, after imports
    for i,hkl in enumerate(project["hkls"]):
        plane = hkl["plane"]
        d = hkl["d_spacing"]
        dist = hkl["distance"]
        image = hkl.get("image")  # e.g. "images/9,10-DCA/plane_1_-1_-1.jpg"

        html += f"""
            <button class="collapsible plane-toggle">
                Plane: ({plane[0]}, {plane[1]}, {plane[2]})
            </button>
            <div class="content">
                <p><strong>d-spacing:</strong> {d} Å</p>
                <p><strong>distance:</strong> {dist}</p>
        """

        if image:
            # turn web path into local filesystem path
            img_fs = os.path.join(base_dir, image.lstrip("/"))
            if os.path.exists(img_fs):
                img_count += 1
                html += f"""
                <p><strong>Image:</strong></p>
                <img src="{image}"
                    alt="Plane ({plane[0]}, {plane[1]}, {plane[2]})"
                    style="max-width: 100%; border-radius: 6px; margin-top: 5px;">
                """
            else:
                print(f"⚠ Image file not found, skipping: {img_fs}")

        html += """
            </div>
        """
    if img_count == len(project["hkls"]):
        status = "Good"
    elif img_count < len(project["hkls"]) and img_count > 0:
        status = "Partial"
    else:
        status = "Bad"
    html += f"""
            <p><strong>Status:</strong> {status}</p>
        </div>  <!-- end file content -->
    </div>      <!-- end card -->
    """

html += """
<script>
var coll = document.getElementsByClassName("collapsible");
for (var i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}
</script>
</body>
</html>
"""

# Write output HTML
with open("index.html", "w") as f:
    f.write(html)

print("Website generated successfully: index.html")