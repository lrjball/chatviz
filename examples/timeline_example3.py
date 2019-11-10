from chatviz.utils import load_example_chat_data
from chatviz.plotting import plot_timeline
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [20, 10]
plt.rcParams["font.size"] = 20
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["font.family"] = "Sawasdee"

df = load_example_chat_data()
plot_timeline(
    df, stacked=False, colors="#20639B", tick_step=1, freq="2W", tick_format="%d %b '%y"
)
plt.tight_layout()
plt.show()
