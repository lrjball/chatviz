"""
test the individual plots on some dummy data.
"""
from chatviz.plotting import (
    plot_donuts,
    plot_timeline,
    plot_days_radar,
    plot_hours_radar,
    plot_words,
    plot_legend,
    plot_reply_times,
)
from chatviz.utils import STOPWORDS, _map_colors, load_example_chat_data
import pandas as pd
import pathlib
import matplotlib.pyplot as plt
import pytest


def generate_dummy_data(n_members=5):
    df = load_example_chat_data()
    # file_path = pathlib.Path(__file__) / ".." / "test_data" / "series_1.csv"
    # df = pd.read_csv(file_path.resolve(), index_col=0, parse_dates=["date"])
    members = list(df["name"].value_counts().index)
    return df[df["name"].isin(members[:n_members])]


@pytest.mark.mpl_image_compare(style="default")
def test_donuts():
    df = generate_dummy_data()
    plt.rcParams["font.size"] = 12
    plt.rcParams["axes.titlesize"] = 20

    plot_donuts(df, show_ylabels=True)
    fig = plt.gcf()
    fig.subplots_adjust(wspace=0.5)
    fig.set_size_inches(20, 10)
    return fig


@pytest.mark.mpl_image_compare(style="default")
def test_timeline():
    df = generate_dummy_data()
    plot_timeline(
        df, stacked=True, legend=True, freq="2D", tick_format="%d/%M", tick_step=3
    )
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_nonstacked_timeline():
    df = generate_dummy_data()
    plot_timeline(
        df,
        stacked=False,
        freq="W",
        tick_format="Week %W %Y",
        tick_step=1,
        colors="blue",
    )
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_days_radar():
    df = generate_dummy_data()
    plot_days_radar(df, legend=True)
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_hours_radar():
    df = generate_dummy_data()
    plot_hours_radar(df, legend=True)
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_plot_words():
    df = generate_dummy_data(3)
    plot_words(df, top_n=20, stopwords=None, show_titles=True)
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_plot_words_without_stopwords():
    df = generate_dummy_data(3)
    plot_words(df, top_n=10, stopwords=STOPWORDS, show_titles=True)
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_plot_legend():
    plot_legend({"Blue": "b", "Green": "g", "Cyan": "c", "Magenta": "m"})
    return plt.gcf()


@pytest.mark.mpl_image_compare(style="default")
def test_plot_reply_times():
    df = generate_dummy_data(10)
    plot_reply_times(df, show_ylabels=True)
    return plt.gcf()


def test_map_colors():
    df = pd.DataFrame(["a", "b", "a", "b", "d", "c"], columns=["name"])
    colors = _map_colors(["b", "g", "y", "r"], df)
    assert colors == ["b", "g", "b", "g", "r", "y"]
