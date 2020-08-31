from chatviz.utils import load_example_chat_data
from chatviz.plotting import plot_days_radar
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [15, 15]
plt.rcParams["font.size"] = 20
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["font.family"] = "Sawasdee"
plt.rcParams["legend.loc"] = "upper left"

df = load_example_chat_data()
palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
plot_days_radar(df, colors=palette, legend=True)

legend = plt.gca().get_legend()
legend.set_bbox_to_anchor((1.0, 1.1))  # move the legend to the right

plt.suptitle("Distribution of Message Dates", size=50)
plt.subplots_adjust(top=0.95, wspace=1.0, right=0.75)
plt.show()
