from src.algos.algos import *
import pandas as pd
import taipy as tp
from taipy.gui import Gui, Icon, navigate
from src.config.config import scenario_cfg
from taipy.config import Config 
from src.pages.data_visualization import *
from src.pages.model_management import *


# Load configuration
Config.load('src/config/config.toml')
scenario_cfg = Config.scenarios['customer_segmentation']

# Execute the scenario
tp.Core().run()

# Function that is called when there is a change in the menu control
def menu_fct(state, var_name, var_value):
    state.page = var_value['args'][0]
    navigate(state, state.page.replace(" ", "-"))

# Create and submit the first scenario
def create_first_scenario(scenario_cfg):
    scenario = tp.create_scenario(scenario_cfg)
    tp.submit(scenario)
    return scenario

scenario = create_first_scenario(scenario_cfg)

# read dataset
ds = scenario.preprocessed_dataset.read()

# run model
results = scenario.trained_model.read()
pred = results['Clusters']

# visualization
heatmap_dataset = creation_heatmap_dataset(ds)

# model management


root_md = """
<|toggle|theme|>
<|menu|label=Menu|lov={menu_lov}|on_action=menu_fct|>
"""

menu_lov = [
    ("Data Visualization", Icon('src/images/histogram_menu.svg', 'Data Visualization'))
]

# Define pages
pages = {
    "/": root_md,
    "Data-Visualization": dv_data_visualization_md
}

# Run the GUI
if __name__ == '__main__':
    gui = Gui(pages=pages)
    gui.run(title="Customer Segmetation", dark_mode=False, port=8866)