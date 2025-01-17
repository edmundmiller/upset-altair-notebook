import pandas as pd
import altair as alt
from altair_upset import UpSetAltair

# Create sample dataset
def create_sample_data():
    """Create a simple dataset with set memberships"""
    data = {
        'Set A': [1, 1, 1, 0, 0, 1, 0, 1],
        'Set B': [0, 1, 1, 1, 0, 0, 1, 1],
        'Set C': [0, 0, 1, 1, 1, 0, 1, 1],
        'Set D': [0, 0, 0, 1, 1, 1, 1, 1]
    }
    return pd.DataFrame(data)

# Create COVID symptoms dataset
def load_covid_data():
    """Load the COVID symptoms dataset"""
    return pd.read_csv("https://ndownloader.figshare.com/files/22339791")

def visualize_upset(data, sets, title="UpSet Plot", **kwargs):
    """
    Create and display an UpSet plot with given parameters
    
    Parameters:
        data: pandas DataFrame
        sets: list of set names
        title: str, plot title
        **kwargs: additional parameters for UpSetAltair
    """
    plot = UpSetAltair(
        data=data,
        sets=sets,
        title=title,
        subtitle=[""],
        **kwargs
    )
    return plot

if __name__ == "__main__":
    # Example 1: Simple dataset
    print("Generating simple dataset visualization...")
    simple_data = create_sample_data()
    simple_sets = ['Set A', 'Set B', 'Set C', 'Set D']
    
    simple_plot = visualize_upset(
        simple_data,
        simple_sets,
        title="Simple UpSet Plot Example",
        abbre=['A', 'B', 'C', 'D'],
        sort_by="frequency",
        sort_order="descending",
        width=800,
        height=500
    )
    
    # Save the plot
    simple_plot.save("simple_upset.html")
    
    # Example 2: COVID dataset
    print("Generating COVID dataset visualization...")
    covid_data = load_covid_data()
    covid_sets = [
        "Shortness of Breath", 
        "Diarrhea", 
        "Fever", 
        "Cough", 
        "Anosmia", 
        "Fatigue"
    ]
    
    covid_plot = visualize_upset(
        covid_data,
        covid_sets,
        title="COVID Symptoms UpSet Plot",
        abbre=['SoB', 'D', 'F', 'C', 'A', 'Fa'],
        sort_by="degree",
        sort_order="ascending",
        width=1000,
        height=600,
        color_range=["#55A8DB", "#3070B5", "#30363F", "#F1AD60", "#DF6234", "#BDC6CA"]
    )
    
    # Save the plot
    covid_plot.save("covid_upset.html")
    
    print("Visualizations have been saved as HTML files.")
    print("Open 'simple_upset.html' and 'covid_upset.html' in your browser to view them.") 