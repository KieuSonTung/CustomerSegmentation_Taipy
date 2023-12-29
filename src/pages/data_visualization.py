
import pandas as pd
from src.utils.utils import AppPath
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


dv_graph_selector = ['Histogram', 'Scatter', 'Heatmap']
dv_graph_selected = dv_graph_selector[0]

# Chart properties
properties_histo = {}
properties_scatter = {}


dv_data_visualization_md = Markdown("src/pages/data_visualization_md.md")