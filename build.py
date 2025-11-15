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
<title>{data['main']['name']}</title>
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
</style>
</head>

<body>
<h1>{data['main']['name']}</h1>
<p>{data['main']['description']}</p>
<p><strong>Author:</strong> {data['main']['author']}</p>
"""

for project in data["files"]:
    html += f"""
    <div class="card">
        <h2>{project['filename']}</h2>
        <p>{project['smiles']}</p>
        <strong>Status: </strong>
    </div>
    """

html += """
</body>
</html>
"""

# Write output HTML
with open("index.html", "w") as f:
    f.write(html)

print("Website generated successfully: index.html")