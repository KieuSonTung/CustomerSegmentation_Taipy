
import pandas as pd
# import sys
# sys.path.append("src/utils")
from src.utils.utils import AppPath
from taipy.gui import Markdown


def creation_scatter_dataset(ds: pd.DataFrame):
    To_Plot = [ "Income", "Recency", "Customer_For", "Age", "Spent", "Is_Parent"]
    scatter_dataset = ds[To_Plot]
    
    return scatter_dataset

def creation_heatmap_dataset(ds: pd.DataFrame):
    corr_df= ds.corr()
    corrmat = {
        'Columns': corr_df.columns.tolist(),
        'Index': corr_df.index.tolist(),
        'Values': corr_df.values.tolist()
    }
    
    return corrmat

def read_data(file_path: str = AppPath.DATA_FILE_PATH) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    # data = data.drop(["Unnamed: 0", "ID"], axis=1)
    data["Dt_Customer"] = pd.to_datetime(data["Dt_Customer"], errors="coerce")
    return data

def update_chart(state):
    global x_selected, y_selected
    x_selected = state.x_selected
    y_selected = state.y_selected

    state.properties_histo = {"x": x_selected}
    state.properties_scatter = {"x": x_selected, "y": y_selected}

    state.data = state.data


dv_graph_selector = ['Histogram', 'Scatter', 'Heatmap']
dv_graph_selected = dv_graph_selector[0]

# Read the data
data = read_data()

# Columns selection
select_x = data.drop("Response", axis=1).columns.to_list()
select_y = select_x
x_selected = select_x[0]
y_selected = select_y[0]

# Chart properties
properties_histo = {}
properties_scatter = {}


dv_data_visualization_md = Markdown("src/pages/data_visualization_md.md")