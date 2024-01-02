# **Model**{: .color-primary} Manager

<|layout|columns=2 2|

<|{mm_algorithm_selected}|selector|lov={mm_algorithm_selector}|dropdown|label=Algorithm|>

<br/> **Number of datapoints:** <|{number_of_data_points}|>
{: .text-right}
|>

-----------------------------------------------------------------


### **Silhouette score**{: .text-center}

<|{silhouette}|indicator|value={silhouette}|min=-1|max=1|>

### **Data distribution**{: .text-center}

<|{distribution_dataset}|chart|title=Data distribution by clusters|values=values|labels=labels|type=pie|layout={mm_pie_color_dict_4}|>
