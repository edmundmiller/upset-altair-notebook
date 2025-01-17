"""Configuration functions for UpSet plots."""
import altair as alt


def configure_chart(chart, width, height):
    """Configure the chart with appropriate settings."""
    return chart.configure_view(
        stroke=None,
        continuousWidth=width,
        continuousHeight=height
    ).configure_title(
        fontSize=18,
        fontWeight=400,
        anchor="start",
        subtitlePadding=10
    ).configure_axis(
        labelFontSize=14,
        labelFontWeight=300,
        titleFontSize=16,
        titleFontWeight=400,
        titlePadding=10
    ).configure_legend(
        titleFontSize=16,
        titleFontWeight=400,
        labelFontSize=14,
        labelFontWeight=300,
        padding=20,
        orient="top",
        symbolType="circle",
        symbolSize=325
    ).configure_concat(
        spacing=0
    )
