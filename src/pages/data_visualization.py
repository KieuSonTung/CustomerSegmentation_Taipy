import pandas as pd
from taipy.gui import Markdown

def creation_histo_dataset(ds: pd.DataFrame):
    histo_dataset = ds
    
    return histo_dataset

def creation_scatter_dataset(ds: pd.DataFrame):
    # To_Plot = [ "Income", "Recency", "Customer_For", "Age", "Spent", "Is_Parent"]
    # scatter_dataset = ds[To_Plot]
    scatter_dataset = ds
    
    return scatter_dataset

def creation_heatmap_dataset(ds: pd.DataFrame):
    corr_df= ds.corr()
    corrmat = {
        'Columns': corr_df.columns.tolist(),
        'Index': corr_df.index.tolist(),
        'Values': corr_df.values.tolist()
    }
    
    return corrmat

def update_chart(state):
    global x_selected, y_selected
    x_selected = state.x_selected
    y_selected = state.y_selected

    state.properties_histo = {"x": x_selected}
    state.properties_scatter = {"x": x_selected, "y": y_selected}

    state.histo_dataset = state.histo_dataset
    state.scatter_dataset = state.scatter_dataset
    
    state.scatter_pred_dataset = state.scatter_pred_dataset
    state.histo_pred_dataset = state.histo_pred_dataset
    
    state.properties_scatter_pred = {
        "x": x_selected,
        "y[1]": y_selected+"_1",
        "y[2]": y_selected+"_2",
        "y[3]": y_selected+"_3",
        "y[4]": y_selected+"_4",
        "name[1]": "Cluster 1",
        "name[2]": "Cluster 2",
        "name[3]": "Cluster 3",
        "name[4]": "Cluster 4",
    }
    state.properties_histo_pred = {
        "x[1]": x_selected+"_1",
        "x[2]": x_selected+"_2",
        "x[3]": x_selected+"_3",
        "x[4]": x_selected+"_4",
        "name[1]": "Cluster 1",
        "name[2]": "Cluster 2",
        "name[3]": "Cluster 3",
        "name[4]": "Cluster 4",
    }


dv_graph_selector = ['Histogram', 'Scatter', 'Heatmap']
dv_graph_selected = dv_graph_selector[0]

# Chart properties
properties_histo = {}
properties_scatter = {}


properties_histo_pred = {}
properties_scatter_pred = {}


dv_data_visualization_md = Markdown("src/pages/data_visualization_md.md")