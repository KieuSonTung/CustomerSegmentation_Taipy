import pandas as pd
from taipy.gui import Markdown


def creation_histo_pred_dataset(ds: pd.DataFrame):
    histo_pred_dataset = ds.copy()
    histo_pred_dataset["Clusters"] = histo_pred_dataset["Clusters"] + 1
    dfs = []
    
    for col in histo_pred_dataset.columns:
        if col != "Clusters":
            dfs.append(histo_pred_dataset.pivot(columns='Clusters', values=col).add_prefix(col + "_"))
            
    dfs.append(histo_pred_dataset)
    histo_pred_dataset = pd.concat(dfs, axis=1)
    
    return histo_pred_dataset

def creation_scatter_pred_dataset(ds: pd.DataFrame):
    scatter_pred_dataset = ds.copy()
    scatter_pred_dataset["Clusters"] = scatter_pred_dataset["Clusters"] + 1
    dfs = []
    
    for col in scatter_pred_dataset.columns:
        if col != "Clusters":
            dfs.append(scatter_pred_dataset.pivot(columns='Clusters', values=col).add_prefix(col + "_"))
            
    dfs.append(scatter_pred_dataset)
    scatter_pred_dataset = pd.concat(dfs, axis=1)
    
    return scatter_pred_dataset

mm_graph_selector = ['Histogram', 'Scatter']
mm_graph_selected = mm_graph_selector[0]

algorithm_selector = ['AC']
algorithm_selected = algorithm_selector[0]

model_manager_md = Markdown("src/pages/model_manager_md.md")
