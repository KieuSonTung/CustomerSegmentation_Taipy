import sys
sys.path.append('/Users/kieusontung/Library/CloudStorage/OneDrive-Personal/Work/Viettel/HoaPhat/CustomerSegmentation/src')

from algos.algos import *
from taipy import Config, Scope


##############################################################################################################################
# Creation of the datanodes
##############################################################################################################################

path_to_csv = 'src/data/data.csv'

# path for csv and file_path for pickle
initial_dataset_cfg = Config.configure_data_node(id="initial_dataset",
                                             path=path_to_csv,
                                             storage_type="csv",
                                             has_header=True
                                             )

date_cfg = Config.configure_data_node(id="date", default_data="None")

preprocessed_dataset_cfg = Config.configure_data_node(id="preprocessed_dataset")

# the final datanode that contains the processed data
trained_model_cfg = Config.configure_data_node(id="trained_model")


##############################################################################################################################
# Creation of the tasks
##############################################################################################################################

# initial_dataset --> preprocess dataset --> preprocessed_dataset
task_preprocess_dataset_cfg = Config.configure_task(id="preprocess_dataset",
                                                    input=[initial_dataset_cfg, date_cfg],
                                                    function=preprocess_dataset,
                                                    output=preprocessed_dataset_cfg)

# preprocessed_dataset --> create train_model data --> trained_model
task_train_model_cfg = Config.configure_task(id="train_model",
                                                input=preprocessed_dataset_cfg,
                                                function=train_model,
                                                output=trained_model_cfg)


##############################################################################################################################
# Creation of the scenario
##############################################################################################################################

scenario_cfg = Config.configure_scenario(
    id='customer_segmentation',
    task_configs=[
        task_preprocess_dataset_cfg,
        task_train_model_cfg
    ]
)

Config.export('src/config/config.toml')
print('config.toml created')