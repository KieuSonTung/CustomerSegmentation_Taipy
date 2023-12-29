# Data **Visualization**{: .color-primary}

<|{dv_graph_selected}|toggle|lov={dv_graph_selector}|>

<|part|render={dv_graph_selected == 'Histogram'}|
### Histogram
<|{x_selected}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{histo_dataset}|chart|type=histogram|rebuild|properties={properties_histo}|>
|>

<|part|render={dv_graph_selected == 'Scatter'}|
### Scatter
<|layout|columns= 1 2|
<|{x_selected}|selector|lov={select_x}|dropdown=True|label=Select x|>

<|{y_selected}|selector|lov={select_y}|dropdown|label=Select y|>
|>

<|{scatter_dataset}|chart|type=scatter|rebuild|properties={properties_scatter}|mode=markers|>
|>

<|part|render={dv_graph_selected == 'Heatmap'}|
### Heatmap

<|{heatmap_dataset}|chart|type=heatmap|z=Values|x=Columns|y=Index|height=1000px|width=1700px|>
|>