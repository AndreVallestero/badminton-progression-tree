import pandas as pd
import graphviz
from collections import defaultdict

CSV_PATH = "badminton_technique_dag.csv"
OUTPUT_SVG = "badminton_technique_dagz"

df = pd.read_csv(CSV_PATH)

technique_to_category = dict(zip(df["Technique"], df["Category"]))
categories = list(df["Category"].unique())

category_techniques = defaultdict(list)
for _, row in df.iterrows():
    category_techniques[row["Category"]].append(row["Technique"])

dot = graphviz.Digraph(format="svg")
#dot.attr(rankdir="TD", splines="true", nodesep="1", ranksep="2", concentrate="true")
dot.attr(rankdir="LR", splines="true", nodesep=".5", ranksep=".5", concentrate="true")

for category in categories:
    with dot.subgraph(name=f"cluster_{category}") as sub:
        sub.attr(label=category, style='filled', color='lightgrey')
        for technique in category_techniques[category]:
            sub.node(technique)

for _, row in df.iterrows():
    target = row["Technique"]
    for dep_col in ["Dependency 1", "Dependency 2", "Dependency 3"]:
        source = row.get(dep_col)
        if pd.notna(source):
            dot.edge(source, target)

dot.render(filename=OUTPUT_SVG, cleanup=True)
print(f"Graph saved as: {OUTPUT_SVG}")
