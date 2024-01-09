import sys

sys.path.append("src/algos")

from algos import preprocess_dataset, train_model_AC, train_model_KM
from taipy import Config


##############################################################################################################################
# Creation of the datanodes
##############################################################################################################################

path_to_csv = "src/data/data.csv"

# path for csv and file_path for pickle
initial_dataset_cfg = Config.configure_data_node(
    id="initial_dataset", path=path_to_csv, storage_type="csv", has_header=True
)

date_cfg = Config.configure_data_node(id="date", default_data="None")

preprocessed_dataset_scaled_cfg = Config.configure_data_node(
    id="preprocessed_dataset_scaled"
)
preprocessed_dataset_unscaled_cfg = Config.configure_data_node(
    id="preprocess_dataset_unscaled"
)

# the final data nodes that contains the processed data
predictions_AC_cfg = Config.configure_csv_data_node(id="predictions_AC")
predictions_KM_cfg = Config.configure_csv_data_node(id="predictions_KM")

##############################################################################################################################
# Creation of the tasks
##############################################################################################################################

# initial_dataset --> preprocess_dataset --> [preprocessed_dataset_scaled, preprocessed_dataset_unscaled]
task_preprocess_dataset_cfg = Config.configure_task(
    id="preprocess_dataset",
    input=[initial_dataset_cfg, date_cfg],
    function=preprocess_dataset,
    output=[preprocessed_dataset_scaled_cfg, preprocessed_dataset_unscaled_cfg],
)

# preprocessed_dataset --> train_model --> predict_dataset
task_train_model_AC_cfg = Config.configure_task(
    id="train_model_AC",
    input=preprocessed_dataset_scaled_cfg,
    function=train_model_AC,
    output=predictions_AC_cfg,
)

task_train_model_KM_cfg = Config.configure_task(
    id="train_model_KM",
    input=preprocessed_dataset_scaled_cfg,
    function=train_model_KM,
    output=predictions_KM_cfg,
)

##############################################################################################################################
# Creation of the scenario
##############################################################################################################################

scenario_cfg = Config.configure_scenario(
    id="customer_segmentation",
    task_configs=[
        task_preprocess_dataset_cfg,
        task_train_model_AC_cfg,
        task_train_model_KM_cfg,
    ],
)

Config.export("src/config/config.toml")
print("config.toml created")
