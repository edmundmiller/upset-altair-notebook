"""Selection creation functions for UpSet plots."""
import altair as alt


def create_selections():
    """Create the selections used in the UpSet plot."""
    legend_selection = alt.selection_point(
        name="legend",
        fields=["set"],
        bind="legend"
    )
    
    color_selection = alt.selection_point(
        name="hover",
        fields=["intersection_id"],
        on="mouseover",
        empty=False
    )
    
    opacity_selection = alt.selection_point(
        name="opacity",
        fields=["intersection_id"]
    )
    
    return legend_selection, color_selection, opacity_selection 