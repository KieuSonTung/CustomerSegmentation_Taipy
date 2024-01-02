# **Model**{: .color-primary} Manager

<|{mm_graph_selected}|toggle|lov={mm_graph_selector}|>

<|part|render={mm_graph_selected == 'Histogram'}|
### Histogram
<|{x_selected_mm}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{histo_pred_dataset}|chart|type=histogram|rebuild|properties={properties_histo_pred}|>
|>

<|part|render={mm_graph_selected == 'Scatter'}|
### Scatter
<|layout|columns= 1 2|
<|{x_selected_mm}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{y_selected_mm}|selector|lov={select_y}|dropdown=True|label=Select y|>
|>

<|{scatter_pred_dataset}|chart|type=scatter|rebuild|properties={properties_scatter_pred}|mode=markers|>
|>