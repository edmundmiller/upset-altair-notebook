"""Configuration functions for UpSet plots."""
import altair as alt


def configure_chart(chart, width, height):
    """Configure the chart with appropriate settings."""
    return (
        chart.configure_view(
            strokeWidth=0,
            width=width,
            height=height
        )
        .configure_title(
            fontSize=20,
            fontWeight=500,
            anchor="start",
            subtitleColor="#3A3A3A",
            subtitleFontSize=14,
            subtitlePadding=10
        )
        .configure_axis(
            labelFontSize=14,
            labelFontWeight=300,
            titleFontSize=16,
            titleFontWeight=400,
            titlePadding=10
        )
        .configure_legend(
            titleFontSize=16,
            titleFontWeight=400,
            labelFontSize=14,
            labelFontWeight=300,
            padding=20,
            orient="top",
            symbolType="circle",
            symbolSize=325
        )
        .configure_concat(
            spacing=0
        )
        .properties(
            background="white"
        )
    )
