"""Selection-related functions for UpSet plots."""
import altair as alt


def create_selections():
    """Create the interactive selections for the UpSet plot.
    
    Returns:
        tuple: (legend_selection, color_selection, opacity_selection)
    """
    legend_selection = alt.selection_point(name="legend", bind="legend", fields=["set"])

    color_selection = alt.selection_point(
        name="hover",
        fields=["intersection_id"],
        on="mouseover",
        empty=False,  # Keep previous selection when moving away
    )

    opacity_selection = alt.selection_point(name="opacity", fields=["intersection_id"])

    return legend_selection, color_selection, opacity_selection 