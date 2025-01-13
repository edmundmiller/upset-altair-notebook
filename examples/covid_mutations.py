import json
from urllib.request import urlopen
import re
import pandas as pd
from altair_upset.upset import UpSetAltair

# Retreived on Nov 30, 2021
res = urlopen(
    "https://raw.githubusercontent.com/hodcroftlab/covariants/master/scripts/mutation_comparison.py"
)

# Read and decode the content
content = res.read().decode()

# Extract the JSON part (everything between the first { and last })
json_str = re.search(r"\{.*\}", content, re.DOTALL).group()

# Clean up the JSON string
# Remove Python-style comments
json_str = re.sub(r"#.*$", "", json_str, flags=re.MULTILINE)
# Ensure property names are double-quoted
json_str = re.sub(r"(\w+):", r'"\1":', json_str)
# Remove trailing commas
json_str = re.sub(r",(\s*[}\]])", r"\1", json_str)

try:
    json_data = json.loads(json_str)
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {str(e)}")
    print("First 500 characters of processed JSON:")
    print(json_str[:500])
    raise

# Restructure and get unique mutations
unique_mutations = set()
for name in json_data:
    mutations = json_data[name]["nonsynonymous"]
    json_data[name] = mutations
    unique_mutations.update(mutations)

unique_vars = list(json_data.keys())
unique_mutations = list(unique_mutations)

unique_vars, json_data, unique_mutations

# Generate data for UpSet
data = {}
for i, m in enumerate(unique_mutations):
    for v in unique_vars:
        if i == 0:
            data[v] = []
        data[v].append(1 if m in json_data[v] else 0)

df = pd.DataFrame(data)

# Rename columns to match variant names
df = df.set_axis(
    [
        "Alpha",
        "Beta",
        "Gamma",
        "Delta",
        "Kappa",
        "Omicron",
        "Eta",
        "Iota",
        "Lambda",
        "Mu",
        "-",
    ],
    axis=1,
)
df = df.drop("-", axis=1)
df

chart = UpSetAltair(
    data=df.copy(),
    title="Shared Mutations of COVID Variants",
    subtitle=[
        "Story & Data: https://covariants.org/shared-mutations",
        "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
    ],
    sets=[
        "Alpha",
        "Beta",
        "Gamma",
        "Delta",
        "Eta",
        "Iota",
        "Kappa",
        "Lambda",
        "Mu",
        "Omicron",
    ],
    abbre=["Al", "Be", "Ga", "De", "Et", "Io", "Ka", "La", "Mu", "Om"],
    sort_by="frequency",
    sort_order="ascending",
    color_range=[
        "#5778a4",
        "#e49444",
        "#d1615d",
        "#85b6b2",
        "#6a9f58",
        "#e7ca60",
        "#a87c9f",
        "#f1a2a9",
        "#967662",
        "#b8b0ac",
    ],
    set_label_bg_size=650,
)

chart.save("covid_mutations_upset.html")

UpSetAltair(
    data=df.copy(),
    title="Shared Mutations of COVID Variants",
    subtitle=[
        "Story & Data: https://covariants.org/shared-mutations",
        "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
    ],
    sets=["Alpha", "Beta", "Gamma", "Delta", "Omicron"],
    abbre=["Al", "Be", "Ga", "De", "Om"],
    sort_by="frequency",
    sort_order="ascending",
)
