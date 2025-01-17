import pytest
from altair_upset import UpSetAltair

def test_height_ratio_validation(sample_data):
    """Test height ratio validation"""
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        height_ratio=1.5,  # Should be capped at 0.5
    )
    spec = chart.to_dict()
    assert "config" in spec

def test_abbreviations(sample_data):
    """Test abbreviation handling"""
    # Test mismatched lengths
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        abbre=["a", "b"],  # Should fall back to using full names
    )
    spec = chart.to_dict()
    assert "config" in spec

    # Test matching lengths
    chart = UpSetAltair(
        data=sample_data, 
        sets=["set1", "set2", "set3"], 
        abbre=["a", "b", "c"]
    )
    spec = chart.to_dict()
    assert "config" in spec

def test_chart_customization(sample_data):
    """Test customization options"""
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        width=800,
        height=600,
        color_range=["#ff0000", "#00ff00", "#0000ff"],
        highlight_color="#999999",
        glyph_size=150,
        horizontal_bar_size=15,
    )
    spec = chart.to_dict()
    assert spec["config"]["view"]["continuousWidth"] == 800
    assert spec["config"]["view"]["continuousHeight"] == 300

def test_title_and_subtitle(sample_data):
    """Test title and subtitle handling"""
    # Test with string subtitle
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        title="Test Title",
        subtitle="Test Subtitle",
    )
    spec = chart.to_dict()
    assert "title" in spec

    # Test with list subtitle
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        title="Test Title",
        subtitle=["Line 1", "Line 2"],
    )
    spec = chart.to_dict()
    assert "title" in spec 