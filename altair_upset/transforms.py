"""Data transformation functions for UpSet plots."""
import pandas as pd


def preprocess_data(data, sets, abbre, sort_by, sort_order):
    """Preprocess the input data for the UpSet plot.
    
    Args:
        data (pd.DataFrame): Input data
        sets (list): List of set names
        abbre (list): List of abbreviated set names
        sort_by (str): Sort method ('frequency' or 'degree')
        sort_order (str): Sort order ('ascending' or 'descending')
    
    Returns:
        dict: Processed data and abbreviations
    """
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

    if len(sets) != len(abbre):
        abbre = sets
        print(
            "Dropping the `abbre` list because the lengths of `sets` and `abbre` are not identical."
        )

    return {"data": data, "abbre": abbre}


def create_degree_calculation(sets):
    """Create the degree calculation formula for Vega-Lite.
    
    Args:
        sets (list): List of set names
    
    Returns:
        str: Degree calculation formula
    """
    return "+".join([f"(isDefined(datum['{s}']) ? datum['{s}'] : 0)" for s in sets])


def create_set_mappings(sets, abbre):
    """Create mappings for set abbreviations and orders.
    
    Args:
        sets (list): List of set names
        abbre (list): List of abbreviated set names
    
    Returns:
        tuple: (set_to_abbre DataFrame, set_to_order DataFrame)
    """
    set_to_abbre = pd.DataFrame(
        [[sets[i], abbre[i]] for i in range(len(sets))], columns=["set", "set_abbre"]
    )
    set_to_order = pd.DataFrame(
        [[sets[i], 1 + sets.index(sets[i])] for i in range(len(sets))],
        columns=["set", "set_order"],
    )
    return set_to_abbre, set_to_order 