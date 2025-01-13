"""Core chart creation functionality for UpSet plots."""
import altair as alt
import pandas as pd
from .transforms import (
    preprocess_data,
    create_degree_calculation,
    create_set_mappings,
)
from .config import configure_chart
from .components import (
    create_vertical_bar_chart,
    create_matrix_view,
    create_horizontal_bar_chart,
)
from .selections import create_selections


def UpSetAltair(
    data=None,
    title="",
    subtitle="",
    sets=None,
    abbre=None,
    sort_by="frequency",
    sort_order="ascending",
    width=1200,
    height=700,
    height_ratio=0.6,
    horizontal_bar_chart_width=300,
    color_range=["#55A8DB", "#3070B5", "#30363F", "#F1AD60", "#DF6234", "#BDC6CA"],
    highlight_color="#EA4667",
    glyph_size=200,
    set_label_bg_size=1000,
    line_connection_size=2,
    horizontal_bar_size=20,
    vertical_bar_label_size=16,
    vertical_bar_padding=20,
):
    """Create an UpSet plot using Altair.

    Parameters:
        data (pandas.DataFrame): Tabular data containing the membership of each element (row) in
            exclusive intersecting sets (column).
        title (str): Title of the plot
        subtitle (str or list): Subtitle(s) of the plot
        sets (list): List of set names of interest to show in the UpSet plots.
            This list reflects the order of sets to be shown in the plots as well.
        abbre (list): Abbreviated set names.
        sort_by (str): "frequency" or "degree"
        sort_order (str): "ascending" or "descending"
        width (int): Vertical size of the UpSet plot.
        height (int): Horizontal size of the UpSet plot.
        height_ratio (float): Ratio of height between upper and under views, ranges from 0 to 1.
        horizontal_bar_chart_width (int): Width of horizontal bar chart on the bottom-right.
        color_range (list): Color to encode sets.
        highlight_color (str): Color to encode intersecting sets upon mouse hover.
        glyph_size (int): Size of UpSet glyph (⬤).
        set_label_bg_size (int): Size of label background in the horizontal bar chart.
        line_connection_size (int): width of lines in matrix view.
        horizontal_bar_size (int): Height of bars in the horizontal bar chart.
        vertical_bar_label_size (int): Font size of texts in the vertical bar chart on the top.
        vertical_bar_padding (int): Gap between a pair of bars in the vertical bar charts.

    Returns:
        altair.vegalite.v4.api.VConcatChart: An Altair chart object
    """
    # Input validation
    if (data is None) or (sets is None):
        raise ValueError(
            "Both data and sets parameters are required. "
            "Please provide a pandas DataFrame and a list of set names."
        )

    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"data must be a pandas DataFrame, got {type(data)}")

    if not isinstance(sets, list):
        raise TypeError(f"sets must be a list of column names, got {type(sets)}")

    if sort_by not in ["frequency", "degree"]:
        raise ValueError("sort_by must be either 'frequency' or 'degree'")

    if sort_order not in ["ascending", "descending"]:
        raise ValueError("sort_order must be either 'ascending' or 'descending'")

    if (height_ratio < 0) or (1 < height_ratio):
        height_ratio = 0.5
        print("height_ratio set to 0.5")

    # Process data and create mappings
    processed_data = preprocess_data(data, sets, abbre, sort_by, sort_order)
    degree_calculation = create_degree_calculation(sets)
    set_to_abbre, set_to_order = create_set_mappings(sets, processed_data["abbre"])

    # Create selections
    selections = create_selections()
    legend_selection, color_selection, opacity_selection = selections

    # Create base chart with transformations
    base = (
        alt.Chart(alt.Data(values=processed_data["data"].to_dict("records"), name="source"))
        .transform_filter(legend_selection)
        .transform_pivot(
            "set",
            op="max",
            groupby=["intersection_id", "count"],
            value="is_intersect",
        )
        .transform_aggregate(
            count="sum(count)",
            groupby=sets,
        )
        .transform_calculate(degree=degree_calculation)
        .transform_filter("datum.degree != 0")
        .transform_window(
            intersection_id="row_number()",
            frame=[None, None],
        )
        .transform_fold(sets, as_=["set", "is_intersect"])
        .transform_lookup(
            lookup="set", from_=alt.LookupData(set_to_abbre, "set", ["set_abbre"])
        )
        .transform_lookup(
            lookup="set", from_=alt.LookupData(set_to_order, "set", ["set_order"])
        )
    )

    # Calculate dimensions
    dimensions = {
        "vertical_bar_chart_height": height * height_ratio,
        "matrix_height": height - (height * height_ratio),
        "matrix_width": width - horizontal_bar_chart_width,
        "vertical_bar_size": min(
            30,
            width / len(processed_data["data"]["intersection_id"].unique()) - vertical_bar_padding,
        ),
    }

    # Create chart components
    vertical_bar_chart = create_vertical_bar_chart(
        base, dimensions, color_selection, sort_by, sort_order, vertical_bar_label_size
    )

    matrix_view = create_matrix_view(
        base,
        dimensions,
        color_selection,
        opacity_selection,
        glyph_size,
        line_connection_size,
        vertical_bar_label_size,
        sort_by,
        sort_order,
    )

    horizontal_bar_chart = create_horizontal_bar_chart(
        base,
        horizontal_bar_chart_width,
        color_range,
        sets,
        horizontal_bar_size,
        vertical_bar_label_size,
    )

    # Compose final chart
    chart = (
        alt.vconcat(
            vertical_bar_chart,
            alt.hconcat(matrix_view, horizontal_bar_chart),
            spacing=20,
        )
        .resolve_scale(y="shared")
        .add_params(legend_selection)
        .properties(autosize={"type": "fit", "contains": "padding"})
    )

    # Configure and return
    chart = configure_chart(chart, width, height)
    if title:
        chart = chart.properties(
            title=alt.Title(
                text=title, subtitle=subtitle if subtitle else None, anchor="start"
            )
        )

    return chart 