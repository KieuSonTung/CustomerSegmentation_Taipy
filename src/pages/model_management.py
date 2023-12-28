import pandas as pd
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt

# pallete
pal = ["#682F2F","#B9C0C9", "#9F8A78","#F3AB60"]

# elbow method to identify k - number of clusters
def kelbow_plot(data: pd.DataFrame):
    print('Elbow Method to determine the number of clusters to be formed:')
    Elbow_M = KElbowVisualizer(KMeans(), k=10)
    Elbow_M.fit(data)
    Elbow_M.show()

#Plotting countplot of clusters
def clusters_countplot(data: pd.DataFrame):
    pl = sns.countplot(x=data["Clusters"], palette= pal)
    pl.set_title("Distribution Of The Clusters")
    plt.show()

def scatter_plot(data: pd.DataFrame):
    pl = sns.scatterplot(data=data, x=data["Spent"], y=data["Income"], hue=data["Clusters"], palette=pal)
    pl.set_title("Cluster's Profile Based On Income And Spending")
    plt.legend()
    plt.show()

def joint_plot(data: pd.DataFrame, attr: str):
    plt.figure()
    sns.jointplot(x=data[attr], y=data["Spent"], hue=data["Clusters"], palette=pal)
    plt.show()