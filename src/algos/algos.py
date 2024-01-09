# Importing the Libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score
import warnings
import sys
import datetime as dt

if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)


def preprocess_dataset(initial_dataset: pd.DataFrame, date: dt.datetime = "None"):
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
    initial_dataset["Dt_Customer"] = pd.to_datetime(
        initial_dataset["Dt_Customer"], format="%d-%m-%Y"
    )
    dates = [i.date() for i in initial_dataset["Dt_Customer"]]

    d1 = max(dates)

    days = []
    for i in dates:
        delta = d1 - i
        days.append(delta)

    initial_dataset["Customer_For"] = days
    initial_dataset["Customer_For"] = pd.to_numeric(
        initial_dataset["Customer_For"], errors="coerce"
    )

    # Age of customer today
    initial_dataset["Age"] = 2021 - initial_dataset["Year_Birth"]

    # Total spendings on various items
    initial_dataset["Spent"] = (
        initial_dataset["MntWines"]
        + initial_dataset["MntFruits"]
        + initial_dataset["MntMeatProducts"]
        + initial_dataset["MntFishProducts"]
        + initial_dataset["MntSweetProducts"]
        + initial_dataset["MntGoldProds"]
    )

    # Deriving living situation by marital status"Alone"
    initial_dataset["Living_With"] = initial_dataset["Marital_Status"].replace(
        {
            "Married": "Partner",
            "Together": "Partner",
            "Absurd": "Alone",
            "Widow": "Alone",
            "YOLO": "Alone",
            "Divorced": "Alone",
            "Single": "Alone",
        }
    )

    # Feature indicating total children living in the household
    initial_dataset["Children"] = (
        initial_dataset["Kidhome"] + initial_dataset["Teenhome"]
    )

    # Feature for total members in the householde
    initial_dataset["Family_Size"] = (
        initial_dataset["Living_With"].replace({"Alone": 1, "Partner": 2})
        + initial_dataset["Children"]
    )

    # Feature pertaining parenthood
    initial_dataset["Is_Parent"] = np.where(initial_dataset.Children > 0, 1, 0)

    # Segmenting education levels in three groups
    initial_dataset["Education"] = initial_dataset["Education"].replace(
        {
            "Basic": "Undergraduate",
            "2n Cycle": "Undergraduate",
            "Graduation": "Graduate",
            "Master": "Postgraduate",
            "PhD": "Postgraduate",
        }
    )

    # Calculate Frequency
    initial_dataset.loc[:, 'Frequency'] = initial_dataset[['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']].sum(axis=1)

    # For clarity
    initial_dataset = initial_dataset.rename(
        columns={
            "MntWines": "Wines",
            "MntFruits": "Fruits",
            "MntMeatProducts": "Meat",
            "MntFishProducts": "Fish",
            "MntSweetProducts": "Sweets",
            "MntGoldProds": "Gold",
        }
    )

    # Dropping some of the redundant features
    to_drop = [
        "Marital_Status",
        "Dt_Customer",
        "Z_CostContact",
        "Z_Revenue",
        "Year_Birth",
        "ID",
    ]
    initial_dataset = initial_dataset.drop(to_drop, axis=1)

    # Dropping the outliers by setting a cap on Age and income.
    initial_dataset = initial_dataset[(initial_dataset["Age"] < 90)]
    initial_dataset = initial_dataset[(initial_dataset["Income"] < 600000)]

    # Label encoding
    s = initial_dataset.dtypes == "object"
    object_cols = list(s[s].index)

    LE = LabelEncoder()
    for i in object_cols:
        initial_dataset[i] = initial_dataset[[i]].apply(LE.fit_transform)

    # Creating a subset of dataframe by dropping the features on deals accepted and promotions
    cols_del = [
        "AcceptedCmp3",
        "AcceptedCmp4",
        "AcceptedCmp5",
        "AcceptedCmp1",
        "AcceptedCmp2",
        "Complain",
        "Response",
    ]
    initial_dataset = initial_dataset.drop(cols_del, axis=1)
    initial_dataset = initial_dataset.reset_index(drop=True)
    unscaled_ds = initial_dataset.copy()

    # Scaling
    scaler = StandardScaler()
    scaler.fit(initial_dataset)
    scaled_ds = pd.DataFrame(
        scaler.transform(initial_dataset), columns=initial_dataset.columns
    )

    return scaled_ds, unscaled_ds


def train_model_AC(ds: pd.DataFrame):
    """Fit and predict a dataframe using the Aggolomerative Clustering model

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        ndarray: Predictions
    """
    AC = AgglomerativeClustering(n_clusters=4)
    yhat_AC = AC.fit_predict(ds)

    return yhat_AC


def train_model_KM(ds: pd.DataFrame):
    """Fit and predict a dataframe using the KMeans model

    Args:
        ds (pd.DataFrame): A dataframe

    Returns:
        ndarray: Prediction
    """
    KM = KMeans(n_clusters=4)
    yhat_KM = KM.fit_predict(ds)

    return yhat_KM


def calculate_silhouette(ds: pd.DataFrame) -> float:
    """Calculate the silhouette score of a given dataframe

    Args:
        ds (pd.DataFrame): A dataframe with labels

    Returns:
        float: The silhouette score
    """
    labels = ds["Clusters"]
    X = ds.drop(columns="Clusters")
    score = silhouette_score(X, labels)

    return score
