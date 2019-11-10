import matplotlib.pyplot as plt

from chatviz.plotting import plot_donuts
from chatviz.utils import load_example_chat_data

plt.rcParams["font.size"] = 25
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["figure.figsize"] = [12, 30]
plt.rcParams["font.family"] = "Purisa"

df = load_example_chat_data()
fig, ax = plt.subplots(3, 1)
palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
plot_donuts(df, show_ylabels=True, ax=ax, colors=palette)
plt.subplots_adjust(hspace=0.4, top=0.95, bottom=0)
plt.show()
