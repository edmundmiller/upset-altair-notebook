import json
import re
import altair as alt
import pandas as pd
from pathlib import Path
from altair_upset import UpSetAltair

def load_test_data():
    """Load the COVID symptoms data"""
    data = pd.read_csv("https://ndownloader.figshare.com/files/22339791")
    return data

def normalize_vega_json(json_str):
    """Normalize the Vega JSON for comparison by:
    1. Removing schema URLs that may change with versions
    2. Normalizing selector IDs that can vary
    3. Normalizing whitespace and formatting
    """
    # Parse and re-serialize to normalize formatting
    if isinstance(json_str, str):
        json_data = json.loads(json_str)
    else:
        json_data = json_str
        
    # Remove schema URLs
    if "$schema" in json_data:
        json_data["$schema"] = "<removed>"
    
    # Convert back to string with consistent formatting
    normalized = json.dumps(json_data, sort_keys=True, indent=2)
    
    # Normalize selector IDs
    normalized = re.sub(r'selector\d+', 'selectorXXX', normalized)
    
    return normalized

def save_vega_spec(chart, filename):
    """Save the Vega specification for a chart"""
    with alt.data_transformers.enable(consolidate_datasets=False):
        json_str = chart.to_json()
    
    # Normalize and save
    normalized = normalize_vega_json(json_str)
    with open(filename, 'w') as f:
        f.write(normalized)

def create_symptoms_by_degree_chart(data):
    """Create the symptoms chart sorted by degree"""
    # Configure Altair to match previous version
    alt.themes.enable('default')
    
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
    
    # Apply specific configuration to match previous version
    chart = chart.configure(
        background="white",
    )
    
    return chart

def create_symptoms_by_frequency_chart(data):
    """Create the symptoms chart sorted by frequency"""
    # Configure Altair to match previous version
    alt.themes.enable('default')
    
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
    
    # Apply specific configuration to match previous version
    chart = chart.configure(
        background="white",
    )
    
    return chart

def test_symptoms_by_degree_chart(update_snapshots=False):
    # Create the chart
    data = load_test_data()
    chart = create_symptoms_by_degree_chart(data)
    
    # Test specific chart properties
    chart_dict = chart.to_dict()
    assert chart_dict['title']['text'] == "Symptoms Reported by Users of the COVID Symptom Tracker App"
    assert chart_dict['title']['subtitle'] == [
        "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
        "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
    ]
    
    # Generate actual spec
    with alt.data_transformers.enable(consolidate_datasets=False):
        actual_json = chart.to_json()
    
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_degree_vega.json")
    
    if update_snapshots:
        save_vega_spec(chart, expected_path)
    else:
        if not expected_path.exists():
            save_vega_spec(chart, expected_path)
            raise AssertionError(
                f"Missing snapshot file {expected_path}. New snapshot has been created."
            )
        
        # Load and compare
        with open(expected_path) as f:
            expected_json = f.read().strip()
        
        assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json), \
            "Chart specification does not match snapshot. Run tests with --update-snapshots to update."

def test_symptoms_by_frequency_chart(update_snapshots=False):
    # Create the chart
    data = load_test_data()
    chart = create_symptoms_by_frequency_chart(data)
    
    # Test specific chart properties
    chart_dict = chart.to_dict()
    assert chart_dict['title']['text'] == "Symptoms Reported by Users of the COVID Symptom Tracker App"
    assert chart_dict['title']['subtitle'] == [
        "Story & Data: https://www.nature.com/articles/d41586-020-00154-w",
        "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
    ]
    
    # Generate actual spec
    with alt.data_transformers.enable(consolidate_datasets=False):
        actual_json = chart.to_json()
    
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_frequency_vega.json")
    
    if update_snapshots:
        save_vega_spec(chart, expected_path)
    else:
        if not expected_path.exists():
            save_vega_spec(chart, expected_path)
            raise AssertionError(
                f"Missing snapshot file {expected_path}. New snapshot has been created."
            )
        
        # Load and compare
        with open(expected_path) as f:
            expected_json = f.read().strip()
        
        assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json), \
            "Chart specification does not match snapshot. Run tests with --update-snapshots to update."
