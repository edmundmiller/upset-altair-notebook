"""Configuration functions for UpSet plots."""
import altair as alt


def configure_chart(chart, width, height, legend_orient="top-left", legend_symbol_size=30):
    """Configure the top level properties of the UpSet plot.
    
    Args:
        chart (alt.Chart): The chart to configure
        width (int): Chart width
        height (int): Chart height
        legend_orient (str): Legend orientation
        legend_symbol_size (int): Size of legend symbols
    
    Returns:
        alt.Chart: Configured chart
    """
    return (
        chart.configure_view(stroke=None, continuousWidth=width)
        .configure_title(
            fontSize=20,
            fontWeight=500,
            anchor="start",
            subtitleColor="#3A3A3A",
            subtitleFontSize=14,
            subtitlePadding=10,
        )
        .configure_axis(
            labelFontSize=14,
            labelFontWeight=300,
            titleFontSize=16,
            titleFontWeight=400,
            titlePadding=10,
        )
        .configure_legend(
            titleFontSize=16,
            titleFontWeight=400,
            labelFontSize=14,
            labelFontWeight=300,
            padding=20,
            orient=legend_orient,
            symbolType="circle",
            symbolSize=legend_symbol_size,
        )
        .configure_concat(spacing=0)
        .properties(autosize={"type": "fit", "contains": "padding"})
    ) 