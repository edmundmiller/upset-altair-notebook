import altair as alt
import pandas as pd
from altair_upset import UpSetAltair

# Create sample COVID variant data
df = pd.DataFrame({
    "Alpha": [1, 1, 0, 0, 1],
    "Beta":  [1, 0, 1, 0, 1],
    "Gamma": [0, 1, 1, 0, 1],
    "Delta": [0, 0, 1, 1, 1],
    "Omicron": [0, 0, 0, 1, 1]
})

# Create visualization
chart = UpSetAltair(
    data=df,
    title="Shared Mutations of COVID Variants",
    subtitle=[
        "Example UpSet plot showing shared mutations between COVID variants",
        "Created with altair-upset"
    ],
    sets=["Alpha", "Beta", "Gamma", "Delta", "Omicron"],
    abbre=["Al", "Be", "Ga", "De", "Om"],
    sort_by="frequency",
    sort_order="ascending",
)

# Save the chart
chart.save("covid_variants_upset.html") 