import pytest
import pandas as pd
from altair_upset import UpSetAltair

def test_sorting_options(sample_data):
    """Test different sorting options"""
    chart_freq = UpSetAltair(
        data=sample_data, 
        sets=["set1", "set2", "set3"], 
        sort_by="frequency"
    )
    spec_freq = chart_freq.to_dict()
    assert "transform" in spec_freq["vconcat"][0]["layer"][0]

    chart_degree = UpSetAltair(
        data=sample_data, 
        sets=["set1", "set2", "set3"], 
        sort_by="degree"
    )
    spec_degree = chart_degree.to_dict()
    assert "transform" in spec_degree["vconcat"][0]["layer"][0]

def test_selections(sample_data):
    """Test selection configurations"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])
    spec = chart.to_dict()

    assert "params" in spec
    legend_sel = next(p for p in spec["params"] if p["name"] == "legend")
    assert legend_sel["bind"] == "legend"

def test_duplicate_width_signal():
    """Test that the chart doesn't create duplicate width signals."""
    data = {
        'set': ['A', 'B', 'A&B'],
        'value': [1, 1, 1],
        'is_intersect': [0, 0, 1],
        'set_order': [0, 1, 0],
        'intersection_id': [0, 1, 2],
        'set_abbre': ['A', 'B', 'AB']
    }
    df = pd.DataFrame(data)
    
    chart = UpSetAltair(data=df, sets=["set"])
    chart_dict = chart.to_dict()
    
    def count_width_properties(obj):
        width_props = []
        if isinstance(obj, dict):
            if 'width' in obj:
                width_props.append(obj['width'])
            for value in obj.values():
                width_props.extend(count_width_properties(value))
        elif isinstance(obj, list):
            for item in obj:
                width_props.extend(count_width_properties(item))
        return width_props
    
    width_props = count_width_properties(chart_dict)
    assert len(width_props) <= 4 