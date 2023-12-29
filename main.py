from src.algos.algos import *
import pandas as pd
import taipy as tp
from taipy.gui import Gui, Icon, navigate
from src.config.config import scenario_cfg
from taipy.config import Config 
from src.pages.data_visualization import *


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

def on_change(state, var_name, var_value):
    if var_name in ['x_selected', 'y_selected']:
        update_chart(state)
        
def on_init(state):
    update_chart(state)


scenario = create_first_scenario(scenario_cfg)

# read dataset
ds = scenario.preprocessed_dataset.read()

# run model
results = scenario.trained_model.read()
pred = results['Clusters']

# visualization
histo_dataset = creation_histo_dataset(ds)
scatter_dataset = creation_scatter_dataset(ds)
heatmap_dataset = creation_heatmap_dataset(ds)

# Columns selection
select_x = ds.drop("Response", axis=1).columns.to_list()
select_y = select_x
x_selected = select_x[0]
y_selected = select_y[1]

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
    gui.run(title="Customer Segmetation", dark_mode=False, port=8866, use_reloader=True)