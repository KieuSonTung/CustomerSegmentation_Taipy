import pandas as pd
from taipy.gui import Markdown, State


def creation_histo_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for plotting a histogram

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    histo_dataset = ds

    return histo_dataset


def creation_scatter_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for plotting a scatter plot

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    scatter_dataset = ds

    return scatter_dataset


def creation_heatmap_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for plotting a correlation matrix

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    corr_df = ds.corr()
    corrmat = {
        "Columns": corr_df.columns.tolist(),
        "Index": corr_df.index.tolist(),
        "Values": corr_df.values.tolist(),
    }

    return corrmat


def update_chart_dv(state: State):
    """Update the variables and dataframes based on the selected x and y

    Args:
        state (State): Accessor to the bound variables from callbacks
    """
    x_selected_dv = state.x_selected_dv
    y_selected_dv = state.y_selected_dv

    state.properties_histo = {"x": x_selected_dv}
    state.properties_scatter = {"x": x_selected_dv, "y": y_selected_dv}

    state.histo_dataset = state.histo_dataset
    state.scatter_dataset = state.scatter_dataset


# Chart selection
dv_graph_selector = ["Histogram", "Scatter", "Heatmap"]
dv_graph_selected = dv_graph_selector[0]

# Chart properties
properties_histo = {}
properties_scatter = {}

# Page creation
data_visualization_md = Markdown("src/pages/data_visualization_md.md")
