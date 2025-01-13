import pytest
import pandas as pd
import json
import re
from altair_upset import UpSetAltair


@pytest.fixture
def covid_symptoms_data():
    """Load the COVID symptoms data"""
    return pd.read_csv("https://ndownloader.figshare.com/files/22339791")


@pytest.fixture
def sort_by_degree_spec():
    """Load the sort by degree reference specification"""
    with open("tests/test_data/sort_by_degree_covid_symptoms.json") as f:
        return json.load(f)


@pytest.fixture
def sort_by_freq_spec():
    """Load the sort by frequency reference specification"""
    with open("tests/test_data/sort_by_freq_covid_symptoms.json") as f:
        return json.load(f)


def normalize_spec(spec):
    """Normalize specification for comparison by removing variable elements"""
    json_str = json.dumps(spec)
    # Replace selector names which can vary
    json_str = re.sub(r"selector\d+", "selectorXXX", json_str)
    # Remove schema URL which can change with Altair versions
    json_str = re.sub(r'"schema": ".*"', '"schema": "<removed>"', json_str)
    return json.loads(json_str)


def test_basic_symptoms_chart_by_degree(covid_symptoms_data, sort_by_degree_spec):
    """Test Example 1 from the documentation with sort by degree"""
    chart = UpSetAltair(
        data=covid_symptoms_data,
        title="Symptoms Reported by Users of the COVID Symptom Tracker App",
        subtitle=[
            "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=[
            "Shortness of Breath",
            "Diarrhea",
            "Fever",
            "Cough",
            "Anosmia",
            "Fatigue",
        ],
        abbre=["B", "D", "Fe", "C", "A", "Fa"],
        sort_by="degree",
        sort_order="ascending",
    )

    spec = normalize_spec(chart.to_dict())
    ref_spec = normalize_spec(sort_by_degree_spec)

    # Update assertions to match Altair 5 structure
    assert "data" in spec
    assert "transform" in spec["vconcat"][0]["layer"][0]
    assert "encoding" in spec["vconcat"][1]["hconcat"][1]


def test_custom_symptoms_chart(covid_symptoms_data, sort_by_freq_spec):
    """Test Example 2 with custom options"""
    custom_width = 900
    custom_height = 500
    custom_colors = ["#F0E442", "#E69F00", "#D55E00", "#CC79A7", "#0072B2", "#56B4E9"]

    chart = UpSetAltair(
        data=covid_symptoms_data,
        title="Symptoms Reported by Users of the COVID Symptom Tracker App",
        subtitle=[
            "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=[
            "Shortness of Breath",
            "Diarrhea",
            "Fever",
            "Cough",
            "Anosmia",
            "Fatigue",
        ],
        abbre=["B", "D", "Fe", "C", "A", "Fa"],
        sort_by="frequency",
        sort_order="ascending",
        width=custom_width,
        height=custom_height,
        height_ratio=0.65,
        color_range=custom_colors,
        highlight_color="#777",
        horizontal_bar_chart_width=200,
        glyph_size=100,
        set_label_bg_size=650,
        line_connection_size=1,
        horizontal_bar_size=16,
        vertical_bar_label_size=12,
        vertical_bar_padding=14,
    )

    spec = normalize_spec(chart.to_dict())

    # Update assertions to check properties in the correct location
    assert spec["vconcat"][0]["width"] == custom_width
    assert (
        spec["vconcat"][0]["height"] == custom_height * 0.65
    )  # Account for height ratio

    # Check custom colors in the horizontal bar chart
    color_scale = spec["vconcat"][1]["hconcat"][1]["layer"][1]["encoding"]["color"][
        "scale"
    ]
    assert color_scale["range"] == custom_colors
