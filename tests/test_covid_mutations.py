import pytest
import pandas as pd
import json
import re
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

@pytest.fixture
def mutations_spec():
    """Load the mutations reference specification"""
    with open('tests/test_data/covid_variants_upset.json') as f:
        return json.load(f)

def normalize_spec(spec):
    """Normalize specification for comparison by removing variable elements"""
    json_str = json.dumps(spec)
    json_str = re.sub(r'selector\d+', 'selectorXXX', json_str)
    json_str = re.sub(r'"schema": ".*"', '"schema": "<removed>"', json_str)
    return json.loads(json_str)

def test_full_mutations_chart(covid_mutations_data, mutations_spec):
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
    
    spec = normalize_spec(chart.to_dict())
    ref_spec = normalize_spec(mutations_spec)
    
    # Check data structure matches reference
    assert spec['data'] == ref_spec['data']
    
    # Check transforms match reference
    assert spec['vconcat'][0]['layer'][0]['transform'] == ref_spec['data'][3]['transform']
    
    # Check encoding structure
    assert spec['vconcat'][1]['hconcat'][1]['encoding'] == ref_spec['vconcat'][1]['hconcat'][1]['encoding']

def test_subset_mutations_chart(covid_mutations_data):
    """Test the COVID mutations chart with subset of variants"""
    subset_sets = ["Alpha", "Beta", "Gamma", "Delta", "Omicron"]
    
    chart = UpSetAltair(
        data=covid_mutations_data,
        title="Shared Mutations of COVID Variants",
        subtitle=[
            "Story & Data: https://covariants.org/shared-mutations",
            "Altair-based UpSet Plot: https://github.com/hms-dbmi/upset-altair-notebook",
        ],
        sets=subset_sets,
        abbre=["Al", "Be", "Ga", "De", "Om"],
        sort_by="frequency",
        sort_order="ascending",
    )
    
    spec = normalize_spec(chart.to_dict())
    
    # Check set configuration
    color_scale = spec['vconcat'][1]['hconcat'][1]['encoding']['color']['scale']
    assert color_scale['domain'] == subset_sets
    
    # Check transforms handle subset correctly
    transforms = spec['vconcat'][0]['layer'][0]['transform']
    fold_transform = next(t for t in transforms if 'fold' in t)
    assert fold_transform['fields'] == subset_sets 