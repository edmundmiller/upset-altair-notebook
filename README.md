# Altair UpSet

Create UpSet plots using Altair.

## Installation

With uv:
```bash
uv pip install altair-upset
```

With pip:
```bash
pip install altair-upset
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/altair-upset.git
cd altair-upset
```

2. Create a virtual environment and install dependencies:
```bash
uv venv
uv pip install -e ".[dev]"
```

3. Start Jupyter for development:
```bash
uv run --with jupyter jupyter lab
```

## Testing

Run the tests with:
```bash
uv pip install -e ".[test]"
uv run pytest
```

For coverage report:
```bash
uv run pytest --cov=altair_upset --cov-report=term-missing
```

## Usage

```python
import altair_upset as au
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'set1': [1, 0, 1],
    'set2': [1, 1, 0],
    'set3': [0, 1, 1]
})

# Create UpSet plot
chart = au.UpSetAltair(
    data=data,
    title="Sample UpSet Plot",
    sets=["set1", "set2", "set3"]
)

# Display the chart
chart.show()
```
