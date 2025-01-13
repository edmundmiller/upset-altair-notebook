import altair as alt
import pandas as pd
from altair_upset import UpSetAltair

# Create sample COVID variant data with more realistic intersections
df = pd.DataFrame(
    {
        "Alpha": [1, 1, 1, 0, 1, 0, 1, 0],  # 5 occurrences
        "Beta": [1, 0, 1, 1, 0, 1, 1, 0],  # 5 occurrences
        "Gamma": [0, 1, 1, 1, 0, 1, 1, 0],  # 5 occurrences
        "Delta": [0, 0, 1, 1, 1, 1, 1, 0],  # 5 occurrences
        "Omicron": [0, 0, 0, 1, 1, 1, 1, 1],  # 5 occurrences
    }
)

# Create visualization
chart = UpSetAltair(
    data=df,
    title="Shared Mutations of COVID Variants",
    subtitle=[
        "Example UpSet plot showing shared mutations between COVID variants",
        "Created with altair-upset",
    ],
    sets=["Alpha", "Beta", "Gamma", "Delta", "Omicron"],
    abbre=["α", "β", "γ", "δ", "o"],  # Using Greek letters for better readability
    sort_by="frequency",
    sort_order="descending",  # Show largest intersections first
    width=800,  # Adjusted for better display
    height=600,
    color_range=[
        "#5778a4",
        "#e49444",
        "#d1615d",
        "#85b6b2",
        "#6a9f58",
    ],  # Color-blind friendly palette
)

# Save the chart
chart.save("covid_variants_upset.html")
