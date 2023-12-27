from src.algos.algos import *
import pandas as pd
import taipy as tp
from taipy.gui import Gui, Icon, navigate
from src.config.config import scenario_cfg
from taipy.config import Config 

# Load configuration
Config.load('src/config/config.toml')
scenario_cfg = Config.scenarios['customer_segmentation']

# Execute the scenario
tp.Core().run()

def create_first_scenario(scenario_cfg):
    """Create and submit the first scenario."""
    scenario = tp.create_scenario(scenario_cfg)
    tp.submit(scenario)
    return scenario

scenario = create_first_scenario(scenario_cfg)

# read datasets
dataset = scenario.initial_dataset.read()

# print('Hello World 2')