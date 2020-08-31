from chatviz import visualize_chat
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
from chatviz.utils import STOPWORDS
import pytest
import pathlib


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


@pytest.mark.mpl_image_compare(style="default")
def test_five_members():
    configure_matplotlib()
    file_path = pathlib.Path(__file__) / ".." / "test_data" / "series_1.csv"
    df = pd.read_csv(file_path.resolve(), index_col=0, parse_dates=["date"])
    actors = [
        "John Cleese",
        "Eric Idle",
        "Michael Palin",
        "Terry Jones",
        "Graham Chapman",
    ]
    df = df[df["name"].isin(actors)]
    palette = ["#20639B", "#3CAEA3", "#F6D55C", "#ED553B", "#173F5F"]
    colors = {n: c for (n, c) in zip(actors, palette)}

    return visualize_chat(
        df,
        title="Monty Python Flying Circus: Series 1",
        colors=colors,
        stopwords=STOPWORDS,
        timeline_stacked=True,
        timeline_freq="D",
        timeline_tick_format="%d %b '%y",
    )


@pytest.mark.mpl_image_compare(style="default")
def test_two_members():
    configure_matplotlib()
    file_path = pathlib.Path(__file__) / ".." / "test_data" / "series_1.csv"
    df = pd.read_csv(file_path.resolve(), index_col=0, parse_dates=["date"])
    actors = ["John Cleese", "Eric Idle"]
    df = df[df["name"].isin(actors)]
    palette = ["#20639B", "#3CAEA3"]
    colors = {n: c for (n, c) in zip(actors, palette)}

    return visualize_chat(
        df,
        title="Monty Python Flying Circus: Series 1",
        colors=colors,
        stopwords=STOPWORDS,
        timeline_stacked=False,
        timeline_freq="W",
        timeline_tick_format="%d/%M/%Y",
        timeline_tick_step=1,
        timeline_color="#F6D55C",
    )


@pytest.mark.mpl_image_compare(style="default")
def test_one_member():
    configure_matplotlib()
    file_path = pathlib.Path(__file__) / ".." / "test_data" / "series_1.csv"
    df = pd.read_csv(file_path.resolve(), index_col=0, parse_dates=["date"])
    actors = ["John Cleese"]
    df = df[df["name"].isin(actors)]
    palette = ["#20639B"]

    return visualize_chat(
        df,
        title="Monty Python Flying Circus: Series 1",
        colors=palette,
        stopwords=STOPWORDS,
        timeline_stacked=False,
        timeline_freq="W",
        timeline_tick_format="%d/%M/%Y",
        timeline_tick_step=1,
        timeline_color="#F6D55C",
    )


if __name__ == "__main__":
    test_two_members()
