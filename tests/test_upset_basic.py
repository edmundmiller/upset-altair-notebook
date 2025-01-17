import pytest
import pandas as pd  # Still needed for DataFrame in test_upset_data_validation
import altair as alt
from altair_upset import UpSetAltair

def test_upset_creation(sample_data):
    """Test basic chart creation"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])
    assert isinstance(chart, alt.VConcatChart)

def test_upset_data_validation():
    """Test data validation"""
    with pytest.raises(ValueError):
        UpSetAltair(data=None, sets=["set1"])
    with pytest.raises(ValueError):
        UpSetAltair(data=pd.DataFrame({"a": [1]}), sets=None)

def test_chart_components(sample_data):
    """Test that all chart components are present"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])
    
    assert len(chart.vconcat) == 2  # Should have 2 main components
    assert len(chart.vconcat[1].hconcat) == 2  # Matrix view and horizontal bar chart

def test_error_conditions(sample_data):
    """Test error handling"""
    with pytest.raises(ValueError, match="sort_by must be either 'frequency' or 'degree'"):
        UpSetAltair(data=sample_data, sets=["set1"], sort_by="invalid")

    with pytest.raises(ValueError, match="sort_order must be either 'ascending' or 'descending'"):
        UpSetAltair(data=sample_data, sets=["set1"], sort_order="invalid")

    with pytest.raises(KeyError):
        UpSetAltair(data=sample_data, sets=["nonexistent"]) 