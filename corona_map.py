import pandas as pd
import seaborn as sb
from matplotlib import pyplot as plt
import os

class CovidMap:
    def __init__(self):
        self.currentDirectory = os.path.abspath(os.getcwd())

    def create(self, state):
        # to ignore warnings
        pd.options.mode.chained_assignment = None
        # visualize csv table for now
        df = pd.read_csv(self.currentDirectory + "/covid.csv")

        # df = df[df["state"] == state.title()]
        dfToPlot = df[["state","deaths", "date"]]
        dfToPlot["date"] = pd.to_datetime(dfToPlot["date"])
        # dfToPlot["year"] = dfToPlot["date"].dt.year
        # dfToPlot["month"] = dfToPlot["date"].dt.month
        # dfToPlot["day"] = dfToPlot["date"].dt.dayofyear

        sb.set(style="darkgrid")
        state_chart = sb.lineplot(x="date",
                                y="deaths",
                                hue="state",
                                data = dfToPlot,
                                palette="icefire",
                                ).set_title(f"Corona Deaths By State Over Time")
        plt.xticks(rotation="vertical")
        plt.legend(bbox_to_anchor=(1.02, 1.05), loc=2, borderaxespad=0, fontsize=7, title="States")
        plt.show()
