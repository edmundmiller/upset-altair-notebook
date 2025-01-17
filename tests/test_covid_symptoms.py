import json
import re
import altair as alt
import pandas as pd
from pathlib import Path
from altair_upset import UpSetAltair

def load_test_data():
    """Load the COVID symptoms data"""
    # Use the same data source as the other tests
    data = pd.read_csv("https://ndownloader.figshare.com/files/22339791")
    return data

def normalize_vega_json(json_str):
    """Normalize the Vega JSON for comparison by:
    1. Removing schema URLs that may change with versions
    2. Normalizing selector IDs that can vary
    """
    # Remove schema URLs
    json_str = re.sub(r'"\$schema": ".*"', '"$schema": "<removed>"', json_str)
    # Normalize selector IDs
    json_str = re.sub(r'selector\d+', 'selectorXXX', json_str)
    return json_str

def create_symptoms_by_degree_chart(data):
    """Create the symptoms chart sorted by degree"""
    chart = UpSetAltair(
        data=data,
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
        sort_by="degree",
        sort_order="ascending",
    )
    return chart

def create_symptoms_by_frequency_chart(data):
    """Create the symptoms chart sorted by frequency"""
    chart = UpSetAltair(
        data=data,
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
        sort_by="frequency",
        sort_order="ascending",
    )
    return chart

def test_symptoms_by_degree_chart():
    # Create the chart
    data = load_test_data()
    chart = create_symptoms_by_degree_chart(data)
    
    # Test specific chart properties
    chart_dict = chart.to_dict()
    assert chart_dict['title']['text'] == "Symptoms Reported by Users of the COVID Symptom Tracker App"
    assert chart_dict['background'] == "white"
    
    # Compare full Vega specification
    with alt.data_transformers.enable(consolidate_datasets=False):
        actual_json = chart.to_json()
    
    # Load expected Vega JSON
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_degree_vega.json")
    with open(expected_path) as f:
        expected_json = f.read()
    
    # Compare normalized JSONs
    assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json)

def test_symptoms_by_frequency_chart():
    # Create the chart
    data = load_test_data()
    chart = create_symptoms_by_frequency_chart(data)
    
    # Test specific chart properties
    chart_dict = chart.to_dict()
    assert chart_dict['title']['text'] == "Symptoms Reported by Users of the COVID Symptom Tracker App"
    assert chart_dict['background'] == "white"
    
    # Compare full Vega specification
    with alt.data_transformers.enable(consolidate_datasets=False):
        actual_json = chart.to_json()
    
    # Load expected Vega JSON
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_frequency_vega.json")
    with open(expected_path) as f:
        expected_json = f.read()
    
    # Compare normalized JSONs
    assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json)
