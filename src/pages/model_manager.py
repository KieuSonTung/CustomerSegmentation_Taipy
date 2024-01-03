import pandas as pd
from taipy.gui import Markdown, State


def creation_histo_pred_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for plotting a histogram

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    histo_pred_dataset = ds.copy()
    histo_pred_dataset["Clusters"] = histo_pred_dataset["Clusters"] + 1
    dfs = []

    for col in histo_pred_dataset.columns:
        if col != "Clusters":
            dfs.append(
                histo_pred_dataset.pivot(columns="Clusters", values=col).add_prefix(
                    col + "_"
                )
            )

    dfs.append(histo_pred_dataset)
    histo_pred_dataset = pd.concat(dfs, axis=1)

    return histo_pred_dataset


def creation_scatter_pred_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for plotting a scatter plot

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    scatter_pred_dataset = ds.copy()
    scatter_pred_dataset["Clusters"] = scatter_pred_dataset["Clusters"] + 1
    dfs = []

    for col in scatter_pred_dataset.columns:
        if col != "Clusters":
            dfs.append(
                scatter_pred_dataset.pivot(columns="Clusters", values=col).add_prefix(
                    col + "_"
                )
            )

    dfs.append(scatter_pred_dataset)
    scatter_pred_dataset = pd.concat(dfs, axis=1)

    return scatter_pred_dataset


def creation_clusters_distribution_dataset(ds: pd.DataFrame) -> pd.DataFrame:
    """Create a dataset for ploting a clusters distribution plot

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        pd.DataFrame: A dataframe
    """
    clusters_distribution_dataset = ds.copy()
    clusters_distribution_dataset["Clusters"] = (
        clusters_distribution_dataset["Clusters"] + 1
    )

    clusters_distribution_dataset = (
        clusters_distribution_dataset["Clusters"].value_counts().reset_index()
    )
    clusters_distribution_dataset["Clusters"] = clusters_distribution_dataset[
        "Clusters"
    ].apply(lambda x: "Cluster " + str(x))

    return clusters_distribution_dataset


def update_chart_mm(state: State):
    """Update variables and dataframes based on the selected x and y

    Args:
        state (State): Accessor to the bound variables from callbacks
    """
    x_selected_mm = state.x_selected_mm
    y_selected_mm = state.y_selected_mm

    state.scatter_pred_dataset = state.scatter_pred_dataset
    state.histo_pred_dataset = state.histo_pred_dataset

    state.properties_scatter_pred = {
        "x": x_selected_mm,
        "y[1]": y_selected_mm + "_1",
        "y[2]": y_selected_mm + "_2",
        "y[3]": y_selected_mm + "_3",
        "y[4]": y_selected_mm + "_4",
        "name[1]": "Cluster 1",
        "name[2]": "Cluster 2",
        "name[3]": "Cluster 3",
        "name[4]": "Cluster 4",
    }
    state.properties_histo_pred = {
        "x[1]": x_selected_mm + "_1",
        "x[2]": x_selected_mm + "_2",
        "x[3]": x_selected_mm + "_3",
        "x[4]": x_selected_mm + "_4",
        "name[1]": "Cluster 1",
        "name[2]": "Cluster 2",
        "name[3]": "Cluster 3",
        "name[4]": "Cluster 4",
    }


# Chart selection
mm_graph_selector = ["Histogram", "Scatter", "Metrics"]
mm_graph_selected = mm_graph_selector[0]

# Algorithm selection
algorithm_selector = ["AgglomerativeClustering", "KMeans"]
algorithm_selected = algorithm_selector[0]

# Algorithm mapper
algorithm_mapper = {"AgglomerativeClustering": "AC", "KMeans": "KM"}

# Chart properties
properties_histo_pred = {}
properties_scatter_pred = {}

# Layout settings for the histogram plot
histo_layout = {"barmode": "overlay"}

# Options for the histogram plot
histo_options = [{"opacity": 0.3}]

# Page creation
model_manager_md = Markdown("src/pages/model_manager_md.md")
