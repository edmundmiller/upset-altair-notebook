import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        "set1": [1, 0, 1, 1], 
        "set2": [1, 1, 0, 1], 
        "set3": [0, 1, 1, 1]
    }) 