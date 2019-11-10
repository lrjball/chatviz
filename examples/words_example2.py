from chatviz.utils import load_example_chat_data, STOPWORDS
from chatviz.plotting import plot_words
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [30, 15]
plt.rcParams["font.size"] = 35
plt.rcParams["axes.titlesize"] = 40
plt.rcParams["font.family"] = "Sawasdee"

df = load_example_chat_data()
palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
plot_words(
    df,
    colors=palette,
    show_titles=True,
    stopwords=None,
    top_n=5
)

plt.suptitle('Most Used Words', size=50)
plt.subplots_adjust(top=0.85, wspace=1.0)
plt.show()
