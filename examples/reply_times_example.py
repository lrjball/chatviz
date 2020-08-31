from chatviz.utils import load_example_chat_data
from chatviz.plotting import plot_reply_times
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["font.size"] = 25
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["font.family"] = "Sawasdee"

df = load_example_chat_data()
palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
plot_reply_times(df, colors=palette, show_ylabels=True)
plt.tight_layout(pad=2.5)
plt.title("Average Reply Times")
plt.show()
