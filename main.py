from typing import Any
from taipy.core.config import ScenarioConfig
from taipy.core.scenario.scenario import Scenario

from src.algos.algos import *
import taipy as tp
from taipy.gui import Gui, Icon, navigate, State
from src.config.config import scenario_cfg
from taipy.config import Config
from src.pages.data_visualization import *
from src.pages.model_manager import *


# Function that is called when there is a change in the menu control
def menu_fct(state: State, var_name: str, var_value: Any):
    """This function handles navigation between pages

    Args:
        state (State): Accessor to the bound variables from callbacks
        var_name (str): Variable name
        var_value (Any): Variable value
    """
    state.page = var_value["args"][0]
    navigate(state, state.page.replace(" ", "-"))


# Create and submit the first scenario
def create_first_scenario(scenario_cfg: ScenarioConfig) -> Scenario:
    """Create and submit the scenario config

    Args:
        scenario_cfg (ScenarioConfig): A scenario config

    Returns:
        Scenario: The created scenario object
    """
    scenario = tp.create_scenario(scenario_cfg)
    tp.submit(scenario)
    return scenario


def on_change(state: State, var_name: str, var_value: Any):
    """Update chart(s) when a variable value changed

    Args:
        state (State): Accessor to the bound variables from callbacks
        var_name (str): Variable name
        var_value (Any): Variable value
    """
    if var_name in ["x_selected_dv", "y_selected_dv"]:
        update_chart_dv(state)
    elif var_name in ["x_selected_mm", "y_selected_mm"]:
        update_chart_mm(state)
        update_dist_df(state)
    elif var_name == "algorithm_selected":
        update_variables(state, var_value)
        update_charts(state, var_value)


def update_charts(state: State, algorithm: str):
    """Update dataframes used for plotting

    Args:
        state (State): Accessor to the bound variables from callbacks
        algorithm (str): Algorithm name
    """
    x_selected_mm = state.x_selected_mm
    state.histo_pred_dataset = creation_histo_pred_dataset(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}")
    )
    state.scatter_pred_dataset = creation_scatter_pred_dataset(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}")
    )
    state.clusters_distribution_dataset = creation_clusters_distribution_dataset(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}")
    )
    (
        state.profiling_dataset_mean,
        state.profiling_dataset_min,
        state.profiling_dataset_max
    ) = creation_profiling_dataset(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}")
    )
    (
        state.distribution_cluster_1,
        state.distribution_cluster_2,
        state.distribution_cluster_3,
        state.distribution_cluster_4
    ) = creation_profiling_dataset_2(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}"), 
        x_selected=x_selected_mm
    )

def update_dist_df(state: State):
    (
        state.distribution_cluster_1,
        state.distribution_cluster_2,
        state.distribution_cluster_3,
        state.distribution_cluster_4
    ) = creation_profiling_dataset_2(
        eval("state.predict_dataset_AC"), 
        x_selected=state.x_selected_mm
    )


def on_init(state: State):
    """Initialize charts

    Args:
        state (State): Accessor to the bound variables from callbacks
    """
    update_chart_dv(state)
    update_chart_mm(state)


def update_variables(state: State, algorithm: str):
    """Update variable(s) when selecting different algorithms

    Args:
        state (State): Accessor to the bound variables from callbacks
        algorithm (str): Algorithm name
    """
    state.silhou_score = calculate_silhouette(
        eval(f"state.predict_dataset_{algorithm_mapper[algorithm]}")
    )


# Load configuration
Config.load("src/config/config.toml")
scenario_cfg = Config.scenarios["customer_segmentation"]

# Execute the core service
tp.Core().run()

# Create and submit a scenario
scenario = create_first_scenario(scenario_cfg)

# Read the preprocessed dataset
ds_scaled = scenario.preprocessed_dataset_scaled.read()
ds_unscaled = scenario.preprocess_dataset_unscaled.read()

# Read the predicted datasets
predictions_AC = scenario.predictions_AC.read()
predictions_KM = scenario.predictions_KM.read()

# Concat predictions
predict_dataset_AC = ds_unscaled.copy()
predict_dataset_AC["Clusters"] = predictions_AC.iloc[:, 0]
predict_dataset_KM = ds_unscaled.copy()
predict_dataset_KM["Clusters"] = predictions_KM.iloc[:, 0]

# Visualization datasets
histo_dataset = creation_histo_dataset(ds_unscaled)
scatter_dataset = creation_scatter_dataset(ds_unscaled)
heatmap_dataset = creation_heatmap_dataset(ds_unscaled)

# Model mangement datasets
histo_pred_dataset = creation_histo_pred_dataset(predict_dataset_AC)
scatter_pred_dataset = creation_scatter_pred_dataset(predict_dataset_AC)
clusters_distribution_dataset = creation_clusters_distribution_dataset(
    predict_dataset_AC
)

# Profiling dataset
profiling_dataset_mean, profiling_dataset_min, profiling_dataset_max = creation_profiling_dataset(
    predict_dataset_AC
)

# Profiling dataset 2
distribution_cluster_1, distribution_cluster_2, distribution_cluster_3, distribution_cluster_4 = creation_profiling_dataset_2(
    predict_dataset_AC
)

# Silhouette score
silhou_score = calculate_silhouette(predict_dataset_AC)

# Columns selection
select_x = ds_unscaled.columns.to_list()
select_y = select_x
# Data visualization page
x_selected_dv = select_x[0]
y_selected_dv = select_y[1]
# Model manager page
x_selected_mm = select_x[0]
y_selected_mm = select_y[1]

# Root page
root_md = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

# Pages navigation
page = "Data Visualization"
menu_lov = [
    ("Data Visualization", Icon("src/images/histogram_menu.svg", "Data Visualization")),
    ("Model Manager", Icon("src/images/model.svg", "Model Manager")),
]

# Define pages structure
pages = {
    "/": root_md,
    "Data-Visualization": data_visualization_md,
    "Model-Manager": model_manager_md,
}

# Run the GUI
if __name__ == "__main__":
    gui = Gui(pages=pages)
    gui.run(title="Customer Segmetation", dark_mode=False, port=8866)
