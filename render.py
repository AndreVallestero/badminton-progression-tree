import pandas as pd
import graphviz
import random
import cairosvg
from PIL import Image
import io
from collections import defaultdict
import os

CSV_PATH = "badminton_technique_dag.csv"
OUTPUT = "badminton_technique_dag"

df = pd.read_csv(CSV_PATH)

# Mapping of technique to category
technique_to_category = dict(zip(df["Technique"], df["Category"]))

# Organize techniques by category
category_techniques = defaultdict(list)
for _, row in df.iterrows():
    category_techniques[row["Category"]].append(row["Technique"])

width = 9999
max_width = 2496

while width > max_width:
    categories = list(category_techniques.keys())
    random.shuffle(categories)

    for category in categories:
        random.shuffle(category_techniques[category])

    # Create the Graphviz DAG
    dot = graphviz.Digraph(format="svg")

    # Randomly vary graph-level attributes
    rankdirs = ["LR"]
    splines = ["polyline", "ortho", "true"]
    ranksep = round(random.uniform(0.5, 2), 2)
    nodesep = round(random.uniform(0.5, 2), 2)

    dot.attr(rankdir=random.choice(rankdirs),
            splines=random.choice(splines),
            nodesep=str(nodesep),
            ranksep=str(ranksep),
            concentrate="true")

    # Add clusters per category
    for category in categories:
        with dot.subgraph(name=f"cluster_{category}") as sub:
            sub.attr(label=category, style='filled', color='lightgrey')
            for technique in category_techniques[category]:
                sub.node(technique)

    # Add edges (dependencies)
    for _, row in df.iterrows():
        target = row["Technique"]
        for dep_col in ["Dependency 1", "Dependency 2", "Dependency 3", "Dependency 4"]:
            source = row.get(dep_col)
            if pd.notna(source):
                dot.edge(source, target)

    # Render
    dot.render(filename="temp", cleanup=True)
    png_bytes = cairosvg.svg2png(url='temp.svg')
    image = Image.open(io.BytesIO(png_bytes))
    width = image.size[1]
    if width > max_width:
        print("too large, retrying")

# Save
print("solution found")
if os.path.exists("badminton_technique_dag.svg"):
    os.remove("badminton_technique_dag.svg")
os.rename('temp.svg', 'badminton_technique_dag.svg')
with open('badminton_technique_dag.png', 'wb') as f:
    f.write(png_bytes)

