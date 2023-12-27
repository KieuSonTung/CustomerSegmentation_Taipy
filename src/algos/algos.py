#Importing the Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from matplotlib.colors import ListedColormap
from sklearn import metrics
import warnings
import sys
import datetime as dt
from sklearn.model_selection import train_test_split
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)


def preprocess_dataset(initial_dataset: pd.DataFrame, date: dt.datetime="None"):
    """This function preprocess the dataset to be used in the model

    Args:
        initial_dataset (pd.DataFrame): the raw format when we first read the data

    Returns:
        pd.DataFrame: the preprocessed dataset for classification
    """
    print("\n     Preprocessing the dataset...")

    # remove na values
    initial_dataset = initial_dataset.dropna()

    # create feature "Customer_For" - how long has the user been a customer
    initial_dataset['Dt_Customer'] = pd.to_datetime(initial_dataset['Dt_Customer'], format='%d-%m-%Y')
    dates = [i.date() for i in initial_dataset['Dt_Customer']]
    
    d1 = max(dates)
    
    days = []
    for i in dates:
        delta = d1 - i
        days.append(delta)
    
    initial_dataset['Customer_For'] = days
    initial_dataset['Customer_For'] = pd.to_datetime(initial_dataset['Customer_For'], errors='coerce')

    #Age of customer today 
    initial_dataset["Age"] = 2021-initial_dataset["Year_Birth"]

    #Total spendings on various items
    initial_dataset["Spent"] = initial_dataset["MntWines"]+ initial_dataset["MntFruits"]+ initial_dataset["MntMeatProducts"]+ initial_dataset["MntFishProducts"]+ initial_dataset["MntSweetProducts"]+ initial_dataset["MntGoldProds"]

    #Deriving living situation by marital status"Alone"
    initial_dataset["Living_With"]=initial_dataset["Marital_Status"].replace({"Married":"Partner", "Together":"Partner", "Absurd":"Alone", "Widow":"Alone", "YOLO":"Alone", "Divorced":"Alone", "Single":"Alone",})

    #Feature indicating total children living in the household
    initial_dataset["Children"]=initial_dataset["Kidhome"]+initial_dataset["Teenhome"]

    #Feature for total members in the householde
    initial_dataset["Family_Size"] = initial_dataset["Living_With"].replace({"Alone": 1, "Partner":2})+ initial_dataset["Children"]

    #Feature pertaining parenthood
    initial_dataset["Is_Parent"] = np.where(initial_dataset.Children> 0, 1, 0)

    #Segmenting education levels in three groups
    initial_dataset["Education"]=initial_dataset["Education"].replace({"Basic":"Undergraduate","2n Cycle":"Undergraduate", "Graduation":"Graduate", "Master":"Postgraduate", "PhD":"Postgraduate"})

    #For clarity
    initial_dataset=initial_dataset.rename(columns={"MntWines": "Wines","MntFruits":"Fruits","MntMeatProducts":"Meat","MntFishProducts":"Fish","MntSweetProducts":"Sweets","MntGoldProds":"Gold"})

    #Dropping some of the redundant features
    to_drop = ["Marital_Status", "Dt_Customer", "Z_CostContact", "Z_Revenue", "Year_Birth", "ID"]
    initial_dataset = initial_dataset.drop(to_drop, axis=1)

    #Dropping the outliers by setting a cap on Age and income. 
    initial_dataset = initial_dataset[(initial_dataset["Age"]<90)]
    initial_dataset = initial_dataset[(initial_dataset["Income"]<600000)]

    # label encoding
    s = (initial_dataset.dtypes == 'object')
    object_cols = list(s[s].index)

    LE = LabelEncoder()
    for i in object_cols:
        initial_dataset[i] = initial_dataset[[i]].apply(LE.fit_transform)

    # creating a copy of data
    ds = initial_dataset.copy()
    
    # creating a subset of dataframe by dropping the features on deals accepted and promotions
    cols_del = ['AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1','AcceptedCmp2', 'Complain', 'Response']
    ds = ds.drop(cols_del, axis=1)
    
    # scaling
    scaler = StandardScaler()
    scaler.fit(ds)
    scaled_ds = pd.DataFrame(scaler.transform(ds),columns= ds.columns)

    return initial_dataset


def dimensionality_reduction(ds: pd.DataFrame, n_components=3):
    pca = PCA(n_components=n_components)
    pca.fit(ds)

    cols = [f'col{i+1}' for i in range(n_components)]
    PCA_ds = pd.DataFrame(pca.transform(ds), columns=(cols))

    return PCA_ds

def train_model(ds: pd.DataFrame):
    AC = AgglomerativeClustering(n_clusters=4)

    yhat_AC = AC.fit_predict(ds)
    ds['Clusters'] = yhat_AC

    return ds

# def visualize_clusters(ds: pd.DataFrame):
#     x = ds["col1"]
#     y = ds["col2"]
#     z = ds["col3"]

#     cmap = colors.ListedColormap(["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"])

#     fig = plt.figure(figsize=(10,8))
#     ax = plt.subplot(111, projection='3d', label="bla")
#     ax.scatter(x, y, z, s=40, c=ds["Clusters"], marker='o', cmap=cmap)
#     ax.set_title("The Plot Of The Clusters")
#     plt.show()