import pandas as pd
import numpy as np

# import sys
# sys.path.append("src/utils")
from src.utils.utils import AppPath
from taipy.gui import Markdown
from sklearn.metrics import silhouette_score

mm_algorithm_selector = ['Agglomerative', 'KMeans']
mm_algorithm_selected = 'Agglomerative'

mm_pie_color_dict_4 = {"piecolorway":["#00D08A","#81F1A0","#F3C178","#FE913C"]}


def calculate_silhouette(ds: pd.DataFrame, algo):
    table = ds.copy()
    table = table[table["algo"] == algo]
    silhouette_avg = silhouette_score(table.drop(["labels", "algo"], axis=1), table["labels"])

    return silhouette_avg

def create_distribution_dataset(ds: pd.DataFrame, algo):
    table = ds.copy()
    table = table[table["algo"] == algo]
    distribution_dataset = pd.DataFrame({
        "values": table["labels"].value_counts().values,
        "labels": table["labels"].value_counts().index.values
    })
    return distribution_dataset

def update_algorithm(state):
    global mm_algorithm_selected
    mm_algorithm_selected = state.mm_algorithm_selected
    
    state.silhouette = state.silhouette
    state.distribution_dataset = state.distribution_dataset

dv_model_management_md = Markdown("src/pages/model_management_md.md")