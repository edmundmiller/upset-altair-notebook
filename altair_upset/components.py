"""Component creation functions for UpSet plots."""
import altair as alt


def create_vertical_bar_chart(
    base, dimensions, color_selection, sort_by, sort_order, vertical_bar_label_size
):
    """Create the vertical bar chart component."""
    main_color = "#3A3A3A"
    highlight_color = "#EA4667"
    brush_color = alt.condition(
        color_selection, alt.value(main_color), alt.value(highlight_color)
    )

    x_sort = alt.Sort(
        field="count" if sort_by == "frequency" else "degree",
        order=sort_order
    )

    tooltip = [
        alt.Tooltip("max(count):Q", title="Cardinality"),
        alt.Tooltip("degree:Q", title="Degree"),
    ]

    vertical_bar = (
        base.mark_bar(color=main_color, size=dimensions["vertical_bar_size"])
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
        .properties(
            height=dimensions["vertical_bar_chart_height"],
            width=dimensions["matrix_width"]
        )
    )

    vertical_bar_text = vertical_bar.mark_text(
        color=main_color,
        dy=-10,
        size=vertical_bar_label_size
    ).encode(
        text=alt.Text("count:Q", format=".0f")
    )

    return (vertical_bar + vertical_bar_text).add_params(color_selection)


def create_matrix_view(
    base,
    dimensions,
    color_selection,
    opacity_selection,
    glyph_size,
    line_connection_size,
    vertical_bar_label_size,
    sort_by,
    sort_order,
):
    """Create the matrix view component."""
    main_color = "#3A3A3A"
    highlight_color = "#EA4667"
    brush_color = alt.condition(
        color_selection, alt.value(main_color), alt.value(highlight_color)
    )

    x_sort = alt.Sort(
        field="count" if sort_by == "frequency" else "degree",
        order=sort_order
    )

    tooltip = [
        alt.Tooltip("max(count):Q", title="Cardinality"),
        alt.Tooltip("degree:Q", title="Degree"),
    ]

    # Create a filtered view for intersecting sets only
    intersection_base = base.transform_filter("datum.is_intersect == 1")

    # Add aggregation for min and max set_order
    intersection_base = intersection_base.transform_aggregate(
        min_set_order='min(set_order)',
        max_set_order='max(set_order)',
        groupby=['intersection_id']
    )

    # Create a base chart with data
    base_chart = alt.Chart(base.data)

    # Create the layered chart
    matrix_view = alt.layer(
        # Background rectangles for alternating rows
        base_chart.mark_rect()
        .transform_filter("datum.set_order % 2 == 1")
        .encode(
            x=alt.value(0),
            x2=alt.value(dimensions["matrix_width"]),
            y=alt.Y(
                "set_order:N",
                axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                title=None,
            ),
            color=alt.value("#F7F7F7"),
        ),
        # Background circles
        base_chart.mark_circle(size=glyph_size, opacity=1).encode(
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
        base_chart.mark_text(
            align="right",
            baseline="middle",
            dx=-10,
            size=vertical_bar_label_size
        ).encode(
            x=alt.value(0),
            y=alt.Y("set_order:N", title=None),
            text="set_abbre:N",
        ),
        # Connection lines - only between intersecting dots
        base_chart.mark_rule(color="#E6E6E6", size=line_connection_size)
        .transform_filter("datum.is_intersect == 1")
        .transform_aggregate(
            min_set_order='min(set_order)',
            max_set_order='max(set_order)',
            groupby=['intersection_id']
        )
        .encode(
            x=alt.X(
                "intersection_id:N",
                axis=alt.Axis(grid=False, labels=False, ticks=False),
                sort=x_sort,
            ),
            y="min_set_order:Q",
            y2="max_set_order:Q",
            opacity=alt.condition(opacity_selection, alt.value(1), alt.value(0.6)),
        ),
        # Intersection circles
        base_chart.mark_circle(size=glyph_size)
        .transform_filter("datum.is_intersect == 1")
        .encode(
            x=alt.X("intersection_id:N", sort=x_sort),
            y="set_order:N",
            color=brush_color,
            tooltip=tooltip,
            opacity=alt.condition(opacity_selection, alt.value(1), alt.value(0.6)),
        ),
    ).properties(
        height=dimensions["matrix_height"],
        width=dimensions["matrix_width"]
    ).add_params(color_selection, opacity_selection)

    return matrix_view


def create_horizontal_bar_chart(
    base,
    horizontal_bar_chart_width,
    color_range,
    sets,
    horizontal_bar_size,
    vertical_bar_label_size,
):
    """Create the horizontal bar chart component."""
    # Create a base chart with data
    base_chart = alt.Chart(base.data)

    horizontal_bars = (
        base_chart.mark_bar(size=horizontal_bar_size)
        .transform_filter("datum.is_intersect == 1")
        .encode(
            x=alt.X(
                "sum(count):Q",
                axis=alt.Axis(grid=False, tickCount=3),
                title="Set Size",
            ),
            y=alt.Y(
                "set_order:N",
                axis=alt.Axis(grid=False, labels=False, ticks=False, domain=False),
                title=None,
            ),
            color=alt.Color(
                "set:N",
                scale=alt.Scale(domain=sets, range=color_range),
                legend=None,
            ),
        )
    )

    horizontal_bar_labels = (
        base_chart.mark_text(
            align="right",
            baseline="middle",
            dx=-10,
            size=vertical_bar_label_size
        )
        .encode(
            x=alt.value(0),
            y=alt.Y("set_order:N", title=None),
            text="set_abbre:N",
        )
    )

    return alt.layer(horizontal_bar_labels, horizontal_bars).properties(
        width=horizontal_bar_chart_width
    )