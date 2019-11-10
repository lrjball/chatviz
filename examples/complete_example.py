import matplotlib.pyplot as plt

from chatviz import visualize_chat
from chatviz.utils import STOPWORDS


def configure_matplotlib():
    plt.rcParams["figure.figsize"] = (30, 40)
    plt.rc("font", size=18)
    plt.rc("axes", titlesize=25)
    plt.rc("axes", labelsize=22)
    plt.rc("xtick", labelsize=20)
    plt.rc("ytick", labelsize=20)
    plt.rc("legend", fontsize=30)
    plt.rc("figure", titlesize=50)
    plt.rcParams["font.family"] = "Humor Sans"


if __name__ == "__main__":
    configure_matplotlib()
    from chatviz.utils import load_example_chat_data

    df = load_example_chat_data()
    actors = [
        "John Cleese",
        "Eric Idle",
        "Michael Palin",
        "Terry Jones",
        "Graham Chapman",
    ]
    palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
    colors = {n: c for (n, c) in zip(actors, palette)}

    visualize_chat(
        df,
        title="Monty Python Flying Circus: Series 1",
        colors=colors,
        stopwords=STOPWORDS,
        timeline_stacked=True,
        timeline_freq="D",
        timeline_tick_format="%d %b '%y",
    )
    plt.show()
