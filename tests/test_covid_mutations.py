import pytest
import pandas as pd
import json
import re
from urllib.request import urlopen
from altair_upset import UpSetAltair

@pytest.fixture
def covid_mutations_data():
    """Create the COVID mutations data"""
    df = pd.DataFrame({
        "Alpha":   [1, 1, 1, 0, 1, 0, 1, 0],
        "Beta":    [1, 0, 1, 1, 0, 1, 1, 0],
        "Gamma":   [0, 1, 1, 1, 0, 1, 1, 0],
        "Delta":   [0, 0, 1, 1, 1, 1, 1, 0],
        "Kappa":   [0, 1, 0, 1, 1, 0, 1, 1],
        "Omicron": [0, 0, 0, 1, 1, 1, 1, 1],
        "Eta":     [1, 0, 0, 1, 0, 1, 1, 0],
        "Iota":    [0, 1, 1, 0, 1, 0, 1, 1],
        "Lambda":  [1, 1, 0, 0, 1, 1, 0, 1],
        "Mu":      [0, 0, 1, 1, 0, 1, 1, 0]
    })
    return df

def test_full_mutations_chart(covid_mutations_data):
    """Test the full COVID mutations chart with all variants"""
    chart = UpSetAltair(
        data=covid_mutations_data,
        title="Shared Mutations of COVID Variants",
        subtitle=[
            "Story & Data: https://covariants.org/shared-mutations",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=[
            "Alpha", "Beta", "Gamma", "Delta", "Eta", 
            "Iota", "Kappa", "Lambda", "Mu", "Omicron"
        ],
        abbre=["Al", "Be", "Ga", "De", "Et", "Io", "Ka", "La", "Mu", "Om"],
        sort_by="frequency",
        sort_order="ascending",
        color_range=[
            "#5778a4", "#e49444", "#d1615d", "#85b6b2", "#6a9f58",
            "#e7ca60", "#a87c9f", "#f1a2a9", "#967662", "#b8b0ac"
        ],
        set_label_bg_size=650,
    )
    
    spec = chart.to_dict()
    
    # Check number of sets
    assert len(spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']['domain']) == 10
    
    # Check color scheme
    assert len(spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']['range']) == 10

def test_subset_mutations_chart(covid_mutations_data):
    """Test the COVID mutations chart with subset of variants"""
    chart = UpSetAltair(
        data=covid_mutations_data,
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
    
    spec = chart.to_dict()
    
    # Check number of sets
    assert len(spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']['domain']) == 5
    
    # Check set names
    expected_sets = ["Alpha", "Beta", "Gamma", "Delta", "Omicron"]
    actual_sets = spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']['domain']
    assert actual_sets == expected_sets 