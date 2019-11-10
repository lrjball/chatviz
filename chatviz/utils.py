import pathlib

import pandas as pd

STOPWORDS = [
    "and",
    "of",
    "in",
    "it",
    "of",
    "you",
    "a",
    "s",
    "i",
    "the",
    "we",
    "what",
    "yes",
    "no",
    "t",
    "is",
    "to",
    "that",
    "m",
    "on",
    "be",
    "there",
    "for",
    "me",
    "he",
    "are",
    "do",
    "was",
    "with",
    "this",
    "at",
    "have",
    "not",
    "ve",
    "but",
    "get",
    "your",
    "don",
    "can",
    "they",
    "er",
    "so",
    "ll",
    "if",
    "my",
    "all",
    "here",
    "he",
    "she",
    "his",
    "hers",
    "him",
    "her",
    "want",
    "now",
    "got",
    "as",
    "re",
    "up",
    "right",
    "about",
    "one",
    "know",
    "just",
    "like",
    "about",
    "then",
    "how",
    "oh",
    "well",
    "how",
    "an",
    "from",
    "been",
    "yeah",
    "mr",
    "will",
    "would",
    "off",
    "going",
    "look",
    "out",
    "d",
    "really",
    "who",
    "think",
    "come",
    "good",
    "see",
    "sir",
    "ah",
    "ha",
    "very",
    "only",
    "could",
    "why",
    "had",
    "them",
    "am",
    "by",
    "go",
    "any",
    "our",
    "mean",
    "say",
    "were",
    "did",
    "these",
    "into",
    "must",
    "take",
    "where",
    "or",
    "when",
    "has",
]


def _build_color_dict(colors, df):
    """
    Builds the color dict from colors.

    If already a dict then just returns that, otherwise will create a dict
    by zipping the colors iterable and the sorted unique names in df['name'].
    """
    if isinstance(colors, dict):
        return colors
    if df.index.name == "name":
        col = df.index
    else:
        col = df["name"]
    sorted_names = sorted(set(col))
    if colors == "default":
        colors = ["C{}".format(i) for i in range(len(sorted_names))]
    elif isinstance(colors, str):
        return {"color": colors}
    return {n: c for (n, c) in zip(sorted_names, colors)}


def _map_colors(colors, df):
    color_dict = _build_color_dict(colors, df)
    if df.index.name == "name":
        col = df.index
    else:
        col = df["name"]
    return [color_dict[n] for n in col]


def load_example_chat_data():
    fname = pathlib.Path(__file__) / ".." / "data" / "mpfc1_example_data.csv"
    return pd.read_csv(fname.resolve(), index_col=0, parse_dates=["date"])
