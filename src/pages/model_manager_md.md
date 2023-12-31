# **Model**{: .color-primary} Manager

<|layout|columns=3 2 2 2|
<|{mm_graph_selected}|toggle|lov={mm_graph_selector}|>

<|{algorithm_selected}|selector|dropdown=True|lov={algorithm_selector}|label=Algorithm|>
|>

<|part|render={mm_graph_selected == 'Histogram'}|
### Histogram
<|{x_selected_mm}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{histo_pred_dataset}|chart|type=histogram|rebuild|properties={properties_histo_pred}|layout={histo_layout}|options={histo_options}|>
|>

<|part|render={mm_graph_selected == 'Scatter'}|
### Scatter
<|layout|columns= 1 2|
<|{x_selected_mm}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{y_selected_mm}|selector|lov={select_y}|dropdown=True|label=Select y|>
|>

<|{scatter_pred_dataset}|chart|type=scatter|rebuild|properties={properties_scatter_pred}|mode=markers|>
|>

<|part|render={mm_graph_selected == 'Metrics'}|
### Metrics
<|layout|columns= 1 2 1|
<|part|>

<|part|
**Silhouette Score**
<br/>
<|{silhou_score:.4f}|indicator|value={silhou_score}|min=-1|max=1|>

<|{clusters_distribution_dataset}|chart|type=pie|values=count|labels=Clusters|title=Clusters Distribution|>
|>

<|part|>
|>
|>

<|part|render={mm_graph_selected == 'Profiling'}|
### Profiling
**Mean**
<|{profiling_dataset_mean}|table|>

**Min**
<|{profiling_dataset_min}|table|>

**Max**
<|{profiling_dataset_max}|table|>
|>