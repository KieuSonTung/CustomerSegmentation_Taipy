import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors


#Setting up colors prefrences
sns.set(rc={"axes.facecolor":"#FFF9ED","figure.facecolor":"#FFF9ED"})
pallet = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"]
cmap = colors.ListedColormap(["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#9F8A78", "#F3AB60"])


def relative_plot(ds: pd.DataFrame):
    To_Plot = [ "Income", "Recency", "Customer_For", "Age", "Spent", "Is_Parent"]
    plt.title("Reletive Plot Of Some Selected Features: A Data Subset")
    plt.figure()
    sns.pairplot(ds[To_Plot], hue= "Is_Parent",palette= (["#682F2F","#F3AB60"]))

    plt.show()

def correlation_matrix(ds: pd.DataFrame):
    #correlation matrix
    corrmat= ds.corr()
    plt.figure(figsize=(20,20))  
    sns.heatmap(corrmat, annot=True, cmap=cmap, center=0)

