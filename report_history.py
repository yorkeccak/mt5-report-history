from matplotlib import pyplot as plt
import pandas as pd

FILE_EXTENSION = "ReportHistory.xlsx"
NEXT_TABLE = "Orders"


class Data:
    def __init__(self, xlsx_file_extension):
        self.file = pd.read_excel(xlsx_file_extension, usecols="A:O", skiprows=6)

        self.closed_position_time = pd.to_datetime(self.get_column("Time"))
        self.closed_position_profits = self.get_column("Profit")
        self.cumulative_profits = self.get_cumulative_profits(
            self.closed_position_profits
        )

    def table_length(self, table):
        for i, element in enumerate(table):
            if element == NEXT_TABLE or str(element) == "nan":
                return i

    def get_column(self, column_name):
        return self.file[column_name][: self.table_length(self.file[column_name])]

    def get_cumulative_profits(self, profits):
        cumulative_profits = []

        for i in range(len(profits)):
            if i == 0:
                cumulative_profits.append(round(profits[i], 2))
            else:
                cumulative_profits.append(
                    round(profits[i] + cumulative_profits[i - 1], 2)
                )
        return cumulative_profits

    def plot_cumulative_profits(self):
        plt.plot(self.closed_position_time, self.cumulative_profits)
        plt.title("Cumulative P/L")
        plt.show()

        # matplotlib.pyplot.yscale("log")

    def plot_wins_or_losses(self, wins_or_losses):
        trades = self.closed_position_profits.copy()
        time = self.closed_position_time.copy()

        for i, element in enumerate(self.closed_position_profits):
            if wins_or_losses == "Wins" and element < 0:
                trades.pop(i)
                time.pop(i)
            if wins_or_losses == "Losses" and element > 0:
                trades.pop(i)
                time.pop(i)

        plt.plot(time, trades, linestyle="", marker="o")
        plt.title(wins_or_losses)
        plt.show()


data = Data(FILE_EXTENSION)
data.plot_cumulative_profits()
data.plot_wins_or_losses("Wins")
data.plot_wins_or_losses("Losses")
