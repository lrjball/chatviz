from chatviz.utils import load_example_chat_data
from chatviz.plotting import plot_timeline
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["font.size"] = 20
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["font.family"] = "Sawasdee"

df = load_example_chat_data()
palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
plot_timeline(
    df,
    stacked=True,
    legend=True,
    freq="W",
    tick_format="Week %W, %Y",
    tick_step=1,
    colors=palette,
)
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
plt.tight_layout()
plt.show()
