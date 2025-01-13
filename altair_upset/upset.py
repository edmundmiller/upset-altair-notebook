import altair as alt
import pandas as pd


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
    if (data is None) or (sets is None):
        raise ValueError("No data and/or a list of sets are provided")

    if (height_ratio < 0) or (1 < height_ratio):
        height_ratio = 0.5
        print("height_ratio set to 0.5")

    if abbre is not None and len(sets) != len(abbre):
        abbre = None
        print(
            "Dropping the `abbre` list because the lengths of `sets` and `abbre` are not identical."
        )

    # Data Preprocessing
    data = data.copy()
    data["count"] = 0
    data = data[sets + ["count"]]
    data = data.groupby(sets).count().reset_index()

    data["intersection_id"] = data.index
    data["degree"] = data[sets].sum(axis=1)
    data = data.sort_values(
        by=["count"], ascending=True if sort_order == "ascending" else False
    )

    data = pd.melt(data, id_vars=["intersection_id", "count", "degree"])
    data = data.rename(columns={"variable": "set", "value": "is_intersect"})

    if abbre is None:
        abbre = sets

    set_to_abbre = pd.DataFrame(
        [[sets[i], abbre[i]] for i in range(len(sets))], columns=["set", "set_abbre"]
    )
    set_to_order = pd.DataFrame(
        [[sets[i], 1 + sets.index(sets[i])] for i in range(len(sets))],
        columns=["set", "set_order"],
    )

    # Calculate degree
    degree_calculation = "+".join(
        [f"(isDefined(datum['{s}']) ? datum['{s}'] : 0)" for s in sets]
    )

    # Selections
    legend_selection = alt.selection_point(name="legend", bind="legend", fields=["set"])

    color_selection = alt.selection_point(
        name="hover",
        fields=["intersection_id"],
        on="mouseover",
        empty=False,  # Changed from "none" to False to keep previous selection when moving away
    )

    # Styles
    vertical_bar_chart_height = height * height_ratio
    matrix_height = height - vertical_bar_chart_height
    matrix_width = width - horizontal_bar_chart_width

    vertical_bar_size = min(
        30,
        width / len(data["intersection_id"].unique().tolist()) - vertical_bar_padding,
    )

    main_color = "#3A3A3A"
    brush_color = alt.condition(
        "!hover.intersection_id || hover.intersection_id === datum.intersection_id",
        alt.value(main_color),
        alt.value(highlight_color),
    )

    is_show_horizontal_bar_label_bg = len(abbre[0]) <= 2
    horizontal_bar_label_bg_color = (
        "white" if is_show_horizontal_bar_label_bg else "black"
    )

    x_sort = alt.Sort(
        field="count" if sort_by == "frequency" else "degree", order=sort_order
    )
    tooltip = [
        alt.Tooltip("max(count):Q", title="Cardinality"),
        alt.Tooltip("degree:Q", title="Degree"),
    ]

    # Add opacity selection that was missing
    opacity_selection = alt.selection_point(name="opacity", fields=["intersection_id"])

    # Update base chart with proper transformations
    base = (
        alt.Chart(data)
        .transform_filter(legend_selection)
        .transform_pivot(
            # Right before this operation, columns should be:
            # `count`, `set`, `is_intersect`, (`intersection_id`, `degree`, `set_order`, `set_abbre`)
            # where (fields with brackets) should be dropped and recalculated later.
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
        .transform_window(
            # This was missing - it ensures proper set ordering
            set_order="distinct(set)",
            frame=[None, 0],
            sort=[{"field": "set_order"}],
        )
    )

    # Vertical bar chart
    vertical_bar = (
        base.mark_bar(color=main_color, size=vertical_bar_size)
        .encode(
            x=alt.X(
                "intersection_id:N",
                axis=alt.Axis(grid=False, labels=False, ticks=False, domain=True),
                sort=x_sort,
                title=None,
            ),
            y=alt.Y(
                "max(count):Q",
                axis=alt.Axis(grid=False, tickCount=3, orient="right"),
                title="Intersection Size",
            ),
            color=brush_color,
            tooltip=tooltip,
        )
        .properties(width=matrix_width, height=vertical_bar_chart_height)
    )

    vertical_bar_text = vertical_bar.mark_text(
        color=main_color, dy=-10, size=vertical_bar_label_size
    ).encode(text=alt.Text("count:Q", format=".0f"))

    vertical_bar_chart = (vertical_bar + vertical_bar_text).add_params(color_selection)

    # Matrix view
    matrix_view = (
        alt.layer(
            # Background rectangles for alternating rows
            base.mark_rect()
            .transform_filter("datum.set_order % 2 == 1")
            .encode(
                x=alt.value(0),
                x2=alt.value(matrix_width),
                y=alt.Y(
                    "set_order:N",
                    axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                    title=None,
                ),
                color=alt.value("#F7F7F7"),
            ),
            # Background circles
            base.mark_circle(size=glyph_size, opacity=1).encode(
                x=alt.X(
                    "intersection_id:N",
                    axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                    sort=x_sort,
                    title=None,
                ),
                y=alt.Y(
                    "set_order:N",
                    axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                    title=None,
                ),
                color=alt.value("#E6E6E6"),
            ),
            # Set labels
            base.mark_text(
                align="right", baseline="middle", dx=-10, size=vertical_bar_label_size
            ).encode(
                x=alt.value(0),
                y=alt.Y("set_order:N", title=None),
                text="set_abbre:N",
            ),
            # Connection lines
            base.mark_rule(color="#E6E6E6", size=line_connection_size).encode(
                x=alt.X(
                    "intersection_id:N",
                    axis=alt.Axis(grid=False, labels=False, ticks=False),
                    sort=x_sort,
                ),
                y=alt.Y("set_order:N", title=None),
                detail="intersection_id:N",
                strokeWidth=alt.condition(
                    "datum.is_intersect == 1",
                    alt.value(line_connection_size),
                    alt.value(0),
                ),
                opacity=alt.condition(opacity_selection, alt.value(1), alt.value(0.6)),
            ),
            # Intersection circles
            base.mark_circle(size=glyph_size)
            .transform_filter("datum.is_intersect == 1")
            .encode(
                x=alt.X("intersection_id:N", sort=x_sort),
                y="set_order:N",
                color=brush_color,
                tooltip=tooltip,
                opacity=alt.condition(opacity_selection, alt.value(1), alt.value(0.6)),
            ),
        )
        .properties(width=matrix_width, height=matrix_height)
        .add_params(color_selection, opacity_selection)
    )

    # Horizontal bar chart
    horizontal_bars = (
        base.mark_bar(size=horizontal_bar_size)
        .transform_filter("datum.is_intersect == 1")
        .encode(
            x=alt.X(
                "sum(count):Q", axis=alt.Axis(grid=False, tickCount=3), title="Set Size"
            ),
            y=alt.Y(
                "set_order:N",
                axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                title=None,
            ),
            color=alt.Color(
                "set:N", scale=alt.Scale(domain=sets, range=color_range), legend=None
            ),
        )
        .properties(width=horizontal_bar_chart_width)
    )

    # Combine all views
    chart = (
        alt.vconcat(
            vertical_bar_chart, alt.hconcat(matrix_view, horizontal_bars), spacing=20
        )
        .resolve_scale(y="shared")
        .add_params(legend_selection)
    )

    # Apply configuration
    chart = _upset_top_level_configuration(chart)

    # Add title and subtitle
    if title:
        chart = chart.properties(
            title=alt.Title(
                text=title, subtitle=subtitle if subtitle else None, anchor="start"
            )
        )

    return chart


def _upset_top_level_configuration(
    base, legend_orient="top-left", legend_symbol_size=30
):
    """Configure the top level properties of the UpSet plot.

    Internal helper function.
    """
    return (
        base.configure_view(stroke=None)
        .configure_title(fontSize=18, fontWeight=400, subtitlePadding=10)
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
    )
