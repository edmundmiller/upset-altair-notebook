"""Display functions for UpSet plots."""


def display(chart):
    """Helper method to display the chart directly.
    
    Args:
        chart: The Altair chart to display
    """
    try:
        chart.display()
    except Exception:  # Be explicit about catching exceptions
        from IPython.display import display as ipython_display
        ipython_display(chart)  # For Jupyter environments 