import pytest
import pandas as pd
import json
from altair_upset import UpSetAltair

@pytest.fixture
def covid_symptoms_data():
    """Load the COVID symptoms data"""
    return pd.read_csv("https://ndownloader.figshare.com/files/22339791")

@pytest.fixture
def reference_spec():
    """Load the reference specification"""
    with open('tests/test_data/sort_by_degree_covid_symptoms.json') as f:
        return json.load(f)

def test_basic_symptoms_chart(covid_symptoms_data, reference_spec):
    """Test Example 1 from the documentation"""
    chart = UpSetAltair(
        data=covid_symptoms_data,
        title="Symptoms Reported by Users of the COVID Symptom Tracker App",
        subtitle=[
            "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=["Shortness of Breath", "Diarrhea", "Fever", "Cough", "Anosmia", "Fatigue"],
        abbre=["B", "D", "Fe", "C", "A", "Fa"],
        sort_by="degree",
        sort_order="ascending",
    )
    
    spec = chart.to_dict()
    
    # Check against reference
    assert spec['title']['text'] == reference_spec['title']['text']
    assert spec['title']['subtitle'] == reference_spec['title']['subtitle']
    
    # Check data transformations
    transforms = spec['vconcat'][0]['layer'][0]['transform']
    ref_transforms = reference_spec['data'][3]['transform']
    assert len(transforms) == len(ref_transforms)

def test_custom_symptoms_chart(covid_symptoms_data):
    """Test Example 2 with custom options"""
    chart = UpSetAltair(
        data=covid_symptoms_data,
        title="Symptoms Reported by Users of the COVID Symptom Tracker App",
        subtitle=[
            "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=["Shortness of Breath", "Diarrhea", "Fever", "Cough", "Anosmia", "Fatigue"],
        abbre=["B", "D", "Fe", "C", "A", "Fa"],
        sort_by="degree",
        sort_order="ascending",
        width=900,
        height=500,
        height_ratio=0.65,
        color_range=["#F0E442", "#E69F00", "#D55E00", "#CC79A7", "#0072B2", "#56B4E9"],
        highlight_color="#777",
        horizontal_bar_chart_width=200,
        glyph_size=100,
        set_label_bg_size=650,
        line_connection_size=1,
        horizontal_bar_size=16,
        vertical_bar_label_size=12,
        vertical_bar_padding=14,
    )
    
    spec = chart.to_dict()
    
    # Check custom dimensions
    assert spec['width'] == 900
    assert spec['height'] == 500
    
    # Check custom colors
    color_scale = spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']
    assert color_scale['range'] == ["#F0E442", "#E69F00", "#D55E00", "#CC79A7", "#0072B2", "#56B4E9"] 