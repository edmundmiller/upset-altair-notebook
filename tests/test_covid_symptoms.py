import json
import re
import altair as alt
import pandas as pd
from pathlib import Path
from altair_upset import UpSetAltair
from altair_saver import save

def load_test_data():
    """Load the COVID symptoms data"""
    data = pd.read_csv("https://ndownloader.figshare.com/files/22339791")
    return data

def normalize_vega_json(json_str):
    """Normalize the Vega JSON for comparison by:
    1. Normalizing selector IDs that can vary
    2. Normalizing whitespace and formatting
    """
    # Parse and re-serialize to normalize formatting
    if isinstance(json_str, str):
        json_data = json.loads(json_str)
    else:
        json_data = json_str
        
    # Convert back to string with consistent formatting
    normalized = json.dumps(json_data, sort_keys=True, indent=2)
    
    # Normalize selector IDs
    normalized = re.sub(r'selector\d+', 'selectorXXX', normalized)
    
    return normalized

def save_vega_spec(chart, filename):
    """Save the Vega specification for a chart"""
    # Use altair_saver to save in vega format
    save(chart, filename)
    
    # Normalize the saved file
    with open(filename) as f:
        json_str = f.read()
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
    
    # Apply specific configuration to match expected spec
    chart = chart.configure_view(
        stroke=None
    ).configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=16,
        titleFontWeight=400,
        titlePadding=10
    ).configure_legend(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=16,
        titleFontWeight=400,
        padding=20,
        orient="top",
        symbolType="circle",
        symbolSize=325
    ).configure_title(
        fontSize=18,
        fontWeight=400,
        subtitlePadding=10
    ).configure(
        background="white"
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
    
    # Apply specific configuration to match expected spec
    chart = chart.configure_view(
        stroke=None
    ).configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=16,
        titleFontWeight=400,
        titlePadding=10
    ).configure_legend(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=16,
        titleFontWeight=400,
        padding=20,
        orient="top",
        symbolType="circle",
        symbolSize=325
    ).configure_title(
        fontSize=18,
        fontWeight=400,
        subtitlePadding=10
    ).configure(
        background="white"
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
    
    # Save actual spec in Vega format
    debug_dir = Path("tests/debug")
    debug_dir.mkdir(exist_ok=True)
    actual_path = debug_dir / "failed_degree.vg.json"
    save_vega_spec(chart, actual_path)
    
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_degree.vg.json")
    
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
        with open(actual_path) as f:
            actual_json = f.read().strip()
        
        try:
            assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json), \
                "Chart specification does not match snapshot. Run tests with --update-snapshots to update."
        except AssertionError:
            print(f"\nSaved failed spec to: {actual_path}")
            print(f"Expected spec at: {expected_path}")
            raise

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
    
    # Save actual spec in Vega format
    debug_dir = Path("tests/debug")
    debug_dir.mkdir(exist_ok=True)
    actual_path = debug_dir / "failed_frequency.vg.json"
    save_vega_spec(chart, actual_path)
    
    expected_path = Path("tests/test_data/vega/covid_symptoms_by_frequency.vg.json")
    
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
        with open(actual_path) as f:
            actual_json = f.read().strip()
        
        try:
            assert normalize_vega_json(actual_json) == normalize_vega_json(expected_json), \
                "Chart specification does not match snapshot. Run tests with --update-snapshots to update."
        except AssertionError:
            print(f"\nSaved failed spec to: {actual_path}")
            print(f"Expected spec at: {expected_path}")
            raise
