import pytest
import pandas as pd
import altair as alt
from altair_upset import UpSetAltair


@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame(
        {"set1": [1, 0, 1, 1], "set2": [1, 1, 0, 1], "set3": [0, 1, 1, 1]}
    )


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


def test_height_ratio_validation(sample_data):
    """Test height ratio validation"""
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        height_ratio=1.5,  # Should be capped at 0.5
    )
    assert isinstance(chart, alt.VConcatChart)


def test_abbreviations(sample_data):
    """Test abbreviation handling"""
    # Test mismatched lengths
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        abbre=["a", "b"],  # Should fall back to using full names
    )
    assert isinstance(chart, alt.VConcatChart)

    # Test matching lengths
    chart = UpSetAltair(
        data=sample_data, sets=["set1", "set2", "set3"], abbre=["a", "b", "c"]
    )
    assert isinstance(chart, alt.VConcatChart)


def test_chart_components(sample_data):
    """Test that all chart components are present"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])

    # Check for vertical bar chart
    assert len(chart.vconcat) == 2  # Should have 2 main components

    # Check for matrix view and horizontal bar chart
    assert len(chart.vconcat[1].hconcat) == 2


def test_sorting_options(sample_data):
    """Test different sorting options"""
    # Test frequency sorting
    chart_freq = UpSetAltair(
        data=sample_data, sets=["set1", "set2", "set3"], sort_by="frequency"
    )
    assert isinstance(chart_freq, alt.VConcatChart)

    # Test degree sorting
    chart_degree = UpSetAltair(
        data=sample_data, sets=["set1", "set2", "set3"], sort_by="degree"
    )
    assert isinstance(chart_degree, alt.VConcatChart)


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
    assert isinstance(chart, alt.VConcatChart)


def test_title_and_subtitle(sample_data):
    """Test title and subtitle handling"""
    # Test with string subtitle
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        title="Test Title",
        subtitle="Test Subtitle",
    )
    assert isinstance(chart, alt.VConcatChart)

    # Test with list subtitle
    chart = UpSetAltair(
        data=sample_data,
        sets=["set1", "set2", "set3"],
        title="Test Title",
        subtitle=["Line 1", "Line 2"],
    )
    assert isinstance(chart, alt.VConcatChart)


@pytest.mark.xfail(reason="Test broken")
def test_chart_structure(sample_data):
    """Test the detailed chart structure"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])
    spec = chart.to_dict()

    # Check data source structure
    assert "data" in spec
    assert spec["data"]["name"] == "source"
    assert isinstance(spec["data"]["values"], list)

    # Check transformations
    transforms = spec["vconcat"][0]["layer"][0]["transform"]
    transform_types = [t.get("type", "") for t in transforms]
    assert "pivot" in transform_types
    assert "aggregate" in transform_types
    assert "calculate" in transform_types

    # Check encodings
    vertical_bar = spec["vconcat"][0]
    matrix = spec["vconcat"][1]["hconcat"][0]
    horizontal_bar = spec["vconcat"][1]["hconcat"][1]

    assert "encoding" in vertical_bar
    assert "encoding" in matrix
    assert "encoding" in horizontal_bar


def test_selections(sample_data):
    """Test selection configurations"""
    chart = UpSetAltair(data=sample_data, sets=["set1", "set2", "set3"])
    spec = chart.to_dict()

    # Check legend selection
    assert "params" in spec
    legend_sel = next(p for p in spec["params"] if p["name"] == "legend")
    assert legend_sel["bind"] == "legend"

    # TODO Check hover selection
    # hover_sel = next(p for p in spec["params"] if p["name"] == "hover")


def test_error_conditions(sample_data):
    """Test error handling"""
    # Test invalid sort_by
    with pytest.raises(
        ValueError, match="sort_by must be either 'frequency' or 'degree'"
    ):
        UpSetAltair(data=sample_data, sets=["set1"], sort_by="invalid")

    # Test invalid sort_order
    with pytest.raises(
        ValueError, match="sort_order must be either 'ascending' or 'descending'"
    ):
        UpSetAltair(data=sample_data, sets=["set1"], sort_order="invalid")

    # Test missing columns
    with pytest.raises(KeyError):
        UpSetAltair(data=sample_data, sets=["nonexistent"])


def test_configuration(sample_data):
    """Test chart configuration options"""
    chart = UpSetAltair(
        data=sample_data, sets=["set1", "set2", "set3"], width=800, height=600
    )
    spec = chart.to_dict()

    # Check view configuration
    assert spec["config"]["view"]["continuousWidth"] == 800
    assert spec["config"]["view"]["continuousHeight"] == 300

    # Check other configurations
    assert spec["config"]["axis"]["labelFontSize"] == 14
    assert spec["config"]["legend"]["symbolType"] == "circle"
