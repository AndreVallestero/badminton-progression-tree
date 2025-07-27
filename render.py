import pandas as pd
import graphviz
import random
import cairosvg
from PIL import Image
import io
from collections import defaultdict
import os

CSV_PATH = "badminton_skill_dag.csv"
OUTPUT = "badminton_skill_dag"

df = pd.read_csv(CSV_PATH)

# Mapping of skill to category
skill_to_category = dict(zip(df["Skill"], df["Category"]))

# Organize skills by category
category_skills = defaultdict(list)
for _, row in df.iterrows():
    category_skills[row["Category"]].append(row["Skill"])

width = 99999
max_width = 2200

while width > max_width:
    categories = list(category_skills.keys())
    random.shuffle(categories)

    for category in categories:
        random.shuffle(category_skills[category])

    # Create the Graphviz DAG
    dot = graphviz.Digraph(format="svg", engine='dot')


    # Randomly vary graph-level attributes
    rankdirs = ["LR"]
    splines = ["true"]
    ranksep = round(random.uniform(0.5, 2), 2)
    nodesep = round(random.uniform(0.5, 2), 2)

    dot.attr(rankdir=random.choice(rankdirs),
            splines=random.choice(splines),
            nodesep=str(nodesep),
            ranksep=str(ranksep),
            concentrate="true",
            compound="true",
            searchsize="1000")

    # Add clusters per category
    for category in categories:
        with dot.subgraph(name=f"cluster_{category}") as sub:
            sub.attr(label=category, style='filled', color='lightgrey')
            for skill in category_skills[category]:
                sub.node(skill)

    # Add edges (dependencies)
    for _, row in df.iterrows():
        target = row["Skill"]
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
if os.path.exists("badminton_skill_dag.svg"):
    os.remove("badminton_skill_dag.svg")
os.rename('temp.svg', 'badminton_skill_dag.svg')
with open('badminton_skill_dag.png', 'wb') as f:
    f.write(png_bytes)

