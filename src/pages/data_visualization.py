import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors


#Setting up colors prefrences
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
pallet = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"]
cmap = colors.ListedColormap(["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"])


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

def update_plot(state):
    # global x_selected, y_selected
    # x_selected = state.x_selected
    # y_selected = state.y_selected
    # state.properties_scatter_dataset =  {"x":x_selected,
    #                                      "y":y_selected}
    state.corrmat = state.corrmat


dv_graph_selector = ['Relative', 'Heatmap']
dv_graph_selected = dv_graph_selector[0]

dv_data_visualization_md = """
# Data **Visualization**{: .color-primary}
<|{dv_graph_selected}|toggle|lov={dv_graph_selector}|>

--------------------------------------------------------------------

<|part|render={dv_graph_selected == 'Scatter'}|
### Scatter
|>

<|part|render={dv_graph_selected == 'Heatmap'}|
### Heatmap

<|{heatmap_dataset}|chart|type=heatmap|z=Values|x=Columns|y=Index|height=1000px|width=1700px|>
|>

"""

