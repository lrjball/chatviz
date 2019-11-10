import re
from collections import Counter

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from chatviz.utils import _map_colors, _build_color_dict


def plot_timeline(
    df,
    ax=None,
    freq="MS",
    colors="default",
    tick_format="%b '%y",
    tick_step=6,
    stacked=False,
    legend=False,
):
    """
    Creates a bar chart of number of messages over time.

    The size of the bins in the bar chart can be adjusted via `freq`, and there
    are other options to control whether or not to create a stacked bar chart.
    See the examples below for more information.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['date', 'text'], as
        well as a 'name' columns if stacked=True.
    ax : plt.Axes or None
        The axes to plot onto. If None (default), will create a new axes.
    freq: str
        The offset string for the resample frequency. See `the pandas documentation
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects>`_
        for all options. The default is 'MS', which will generate a monthly plot.
    colors : {'default'} or str or list of str or dict
        The colors to be used for each person in the chat. Should be either:

        - 'default' in which case the default color scheme is used.
        - a list of colors the same length as the number of names in df['name']
          when `stacked=True`.
        - a single color string when `stacked=False`.
        or

        - a dict which maps each name to a color.
        If `stacked=False` and multiple colors are passed, then the first one will
        be used.
        For more info about the possible color strings,
        see `the matplotlib documentation <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    tick_format : str
        The format string for the x tick labels, which are dates. The default
        is '%b \'%y' which gives for example `Jan '19`. For more information
        about datetime format strings, `see the datetime documentation
        <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_.
    tick_step : int
        The number of steps between the ticks on the x-axis. By default this
        is 6, so every 6 bars will have an x-tick label.
    stacked : bool
        If True, then a stacked bar chart will be created, with one color per
        person involved in the chat. If False (default), will just plot one
        colored bar with the overall count.
    legend : bool
        If True, will add a legend to the plot when stacked=True.
        Default is False.

    Returns
    -------
    plt.Axes
        The bar chart axes plot.

    Examples
    --------

    This first example shows how to plot a stacked timeline with each bar being
    2 days, and every third bar having a label on it, which is formatted as
    day/month/year.

    .. plot:: ../examples/timeline_example.py
       :width: 800px

    The second example shows how the frequency can be change to plot weekly
    bars, with the labels now being on every bar and showing the week number
    and year.

    .. plot:: ../examples/timeline_example2.py
       :width: 800px

    The third example shows the plot with `stacked=False`, so the bars are
    only in one color.

    .. plot:: ../examples/timeline_example3.py
       :width: 800px


    .. note:: You may need to alter the font sizes and other parameters using
              `plt.rcParams` to get a suitable plot.
    """
    if ax is None:
        ax = plt.subplot(111)
    df2 = df.copy()
    if stacked:
        df2 = (
            df2.groupby([pd.Grouper(key="date", freq=freq), "name"])
            .count()
            .unstack("name")
            .fillna(0)
            .resample(freq)
            .sum()
        )
        color_dict = _build_color_dict(colors, df)
        cats = list(color_dict.keys())[::-1]
        df2 = df2.reindex(cats, axis=1, level=1)
        df2["text"].plot(
            kind="bar",
            stacked=True,
            width=0.75,
            color=_map_colors(colors, df2["text"].transpose()),
            ax=ax,
            rot=45,
        )
    else:
        df2 = df2.resample(freq, on="date").count()
        df2["text"].plot(
            kind="bar",
            width=0.75,
            color=list(_build_color_dict(colors, df).values())[0],
            ax=ax,
            rot=45,
        )
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xticks(list(range(len(df2)))[::tick_step])
    ax.set_xticklabels([item.strftime(tick_format) for item in df2.index[::tick_step]])
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.set_title("Message Timeline")
    ax.xaxis.labelpad = 20
    ax.yaxis.labelpad = 20
    if stacked:
        if legend:
            patches = [
                mpatches.Patch(facecolor=c, label=n) for n, c in color_dict.items()
            ]
            ax.legend(handles=patches, loc="upper right")
        else:
            ax.get_legend().remove()
    return ax


def plot_one_donut(df, title, ax, colors, show_ylabels=False):
    def func(pct, allvals):
        absolute = int(pct / 100.0 * np.sum(allvals))
        return "{:d}".format(absolute)

    color_dict = _build_color_dict(colors, df)
    df = df.loc[list(color_dict.keys())[::-1]]
    ax.pie(
        df["text"],
        wedgeprops=dict(width=0.3),
        labels=df.index if show_ylabels else None,
        colors=_map_colors(color_dict, df),
        startangle=90,
        autopct=lambda pct: func(pct, df),
        pctdistance=0.45,
    )
    ax.set_title(f"Number of {title}\nTotal: {df.sum().iloc[0]}")
    return ax


def plot_donuts(df, ax=None, colors="default", show_ylabels=False):
    """
    Creates a plot of 3 donut charts.

    The donut charts contain the following info:

    1. The number of messages per person.
    2. The number of words per person.
    3. The number of characters per person.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['date', 'text',
        'name'].
    ax : plt.Axes or None
        This should be an iterable of 3 axes, such as the one generated from
        _, ax = plt.subplots(1, 3). If None (default), will create 3 new axes.
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either:

        - 'default' in which case the default color scheme is used
        - a list of colors the same length as the number of names in df['name']
        or

        - a dict which maps each name to a color.
        For more info about the possible color strings,
        see `the matplotlib documentation <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    show_ylabels : bool
        If True, will show names around the donut. If False (default), then they
        will be hidden.

    Returns
    -------
    array of plt.Axes objects
        An array of length 3.

    Examples
    --------

    .. plot:: ../examples/donuts_example.py
       :width: 500px
    """

    if ax is None:
        _, ax = plt.subplots(1, 3)
    pie_messages = df.groupby("name").count()[["text"]]
    ax[0] = plot_one_donut(pie_messages, "messages", ax[0], colors, show_ylabels)

    pie_words = df.groupby("name")[["text"]].aggregate(
        lambda x: sum(
            len(re.sub(r"[^a-zA-Z0-9]+", " ", i).strip().split()) for i in x.fillna("")
        )
    )
    ax[1] = plot_one_donut(pie_words, "words", ax[1], colors, show_ylabels)

    pie_chars = df.groupby("name")[["text"]].aggregate(
        lambda x: sum(len(i) for i in x.fillna(""))
    )
    ax[2] = plot_one_donut(pie_chars, "characters", ax[2], colors, show_ylabels)
    return ax


def _create_reply_time_df(df):
    """
    Calculates the per person reply times in hours.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['date', 'name'].

    Returns
    -------
    pd.Series
        A series with the reply times in hours for each person in df['name'].
    """
    reply_times = []
    last_time = None
    last_person = None
    for d, n in df[["date", "name"]].values:
        if last_time is None:
            last_time = d
            last_person = n
            continue
        if n != last_person:
            reply_time = d - last_time
            last_person = n
            last_time = d
            reply_times.append([reply_time, n])
    if not reply_times:
        return None
    reply_df = pd.DataFrame(reply_times, columns=["reply_time", "name"])
    reply_df["reply_seconds"] = reply_df["reply_time"].dt.total_seconds()
    reply_data = reply_df.groupby("name")["reply_seconds"].mean() / 3600
    reply_data.name = "reply_hours"
    return reply_data


def plot_reply_times(df, ax=None, colors="default", show_ylabels=False):
    """
    Creates a horizontal bar chart showing the average reply time in hours
    for each person in the chat.

    Reply time for person A is calculated as the time at which a message was
    sent minus the time of the last message sent by someone other than
    person A.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['date', 'name'].
    ax : plt.Axes or None
        The axes to plot onto. If None (default), will create a new axes.
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either:

        - 'default' in which case the default color scheme is used
        - a list of colors the same length as the number of names in df['name']
        or

        - a dict which maps each name to a color.
        For more info about the possible color strings,
        see `the matplotlib documentation <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    show_ylabels : bool
        If True, will show names around the donut. If False (default), then they
        will be hidden.

    Returns
    -------
    plt.Axes
        The horizontal bar chart axes plot.

    Examples
    --------

    .. plot:: ../examples/reply_times_example.py
       :width: 800px
    """
    if ax is None:
        ax = plt.subplot(111)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    reply_data = _create_reply_time_df(df)
    if reply_data is None:
        ax.axis("off")
        return ax
    color_dict = _build_color_dict(colors, df)
    reply_data = reply_data[list(color_dict.keys())[::-1]]
    reply_data.plot(kind="barh", color=_map_colors(color_dict, reply_data), ax=ax)
    ax.set_ylabel("")
    if not show_ylabels:
        ax.set_yticklabels([])
    ax.set_xlabel("Hours")
    return ax


def _word_counts(df, stopwords):
    """
    Gets the word counts for each person in the df.

    Lower cases the words and removes all punctuation and numbers except '_'.
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['name', 'text'].

    Returns
    -------
    dict
        A dictionary of (name, Counter), where the Counter contains word counts.
    """
    df2 = df.copy()

    def clean_text(s):
        return re.sub(r"[^a-z_]+", " ", s.lower()).strip().split()

    if stopwords is None:
        stopwords = set()
    else:
        stopwords = set(clean_text(" ".join(stopwords)))
    df2["words"] = (
        df2["text"]
        .fillna("")
        .apply(lambda x: [w for w in clean_text(x) if w not in stopwords])
    )
    count_dicts = {
        name: Counter(sub_df["words"].sum()) for (name, sub_df) in df2.groupby("name")
    }
    return count_dicts


def plot_words(
    df, ax=None, top_n=10, stopwords=None, colors="default", show_titles=False
):
    """
    Plots a bar chart per person with their top words used.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['name', 'text'].
    ax : plt.Axes or None
        This should be an iterable of M axes, where M is the number of unique
        names in df['name']. If None (default), will create M new axes, via
        _, ax = plt.subplots(1, M).
    top_n : int
        The number of top words to include. Default is 10.
    stopwords : None or iterable
        If given, then these words will be removed from the plots. If None,
        all words will be kept (Note: this will lead to poor results as 'the',
        'and', 'a', 'is' etc. will be the top words. A stopword list is
        recommended).
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either
        'default' in which case the default color scheme is used, a list of
        colors the same length as the number of names in df['name'], or a dict
        which maps each name to a color. For more info about color options,
        see `here <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    show_titles : bool
        If True, will show names about each plot. If False (default), then they
        will be hidden.

    Returns
    -------
    array of plt.Axes
        The horizontal bar chart axes plots, one for each person in the chat.

    Examples
    --------

    .. plot:: ../examples/words_example.py
       :width: 800px


    The example below shows the results without stopwords being removed. In
    most cases the results with be better by removing stopwords, either using
    the `chatviz.utils.STOPWORDS` or a custom list of stopwords.

    .. plot:: ../examples/words_example2.py
       :width: 800px
    """
    counts = _word_counts(df, stopwords)
    if ax is None:
        _, ax = plt.subplots(1, len(counts))
    color_dict = _build_color_dict(colors, df)
    for ind, (name, color) in enumerate(color_dict.items()):
        name_counts = counts.get(name, Counter())
        top_words = name_counts.most_common(top_n)
        ax[ind].barh(
            [i[0] for i in top_words][::-1],
            [i[1] for i in top_words][::-1],
            color=color,
        )
        ax[ind].spines["right"].set_visible(False)
        ax[ind].spines["top"].set_visible(False)
        if show_titles:
            ax[ind].set_title(name)
    return ax


def plot_radar(df, ax=None, colors="default", legend=False):
    """
    Creates a radar plot from the given dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        This should be a dataframe where each index is a 'radar' area to be
        plotted, and each column is a category to plot, starting on the x-axis
        and going round the circle in the order of df.columns.
    ax : plt.Axes or None
        This should be a polar axes. If None (default), one will be created
        with ax = plt.subplot(polar=True).
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either
        'default' in which case the default color scheme is used, a list of
        colors the same length as the number of names in df['name'], or a dict
        which maps each name to a color. For more info about color options,
        see `here <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    legend : bool
        If True, will add a legend to the plot. Default is False.

    Returns
    -------
    matplotlib.axes._subplots.PolarAxesSubplot
        A radar plot with one area per index of the dataframe.
    """
    n_cols = len(df.columns)
    if ax is None:
        ax = plt.subplot(polar=True)

    angles = [n / float(n_cols) * 2 * np.pi for n in range(n_cols)]
    angles += angles[:1]  # repeat first value to go full circle

    color_dict = _build_color_dict(colors, df)
    for ind, (name, row) in enumerate(df.fillna(0).iterrows()):
        values = list(row)
        values += values[:1]
        ax.plot(angles, values, linewidth=3, linestyle="solid", color=color_dict[name])
        ax.fill(angles, values, color_dict[name], alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(list(df.columns))
    ax.set_rlabel_position(0)
    ax.set_yticklabels([str(int(i)) for i in ax.get_yticks()[:-2]])

    ax.tick_params(axis="both", colors="grey")
    ax.tick_params(axis="y", labelrotation=45)
    ax.tick_params(axis="x", pad=20)
    if legend:
        patches = [mpatches.Patch(color=c, label=n) for (n, c) in color_dict.items()]
        ax.legend(handles=patches)
    return ax


def plot_days_radar(df, ax=None, colors="default", legend=False):
    """
    Creates a radar plot showing the number of messages per day for each
    person in the chat.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['name', 'date'].
    ax : plt.Axes or None
        This should be a polar axes. If None (default), one will be created
        with ax = plt.subplot(polar=True).
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either
        'default' in which case the default color scheme is used, a list of
        colors the same length as the number of names in df['name'], or a dict
        which maps each name to a color. For more info about color options,
        see `here <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    legend : bool
        If True, will add a legend to the plot. Default is False.

    Returns
    -------
    matplotlib.axes._subplots.PolarAxesSubplot
        A radar plot with one area per person in the chat.

    See Also
    --------
    plot_hours_radar

    Examples
    --------

    This example shows how to create a radar plot showing how many messages are
    sent on each day by each chat participant. It shows that for this dummy
    dataset, `John Cleese` sends most of his messages on a Sunday, whereas
    `Michael Palin` sends most of his on a Monday.

    .. plot:: ../examples/radar_day_example.py
       :width: 800px
    """
    df = df.copy()
    df["label"] = df["date"].dt.dayofweek
    days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
    df = (
        df.groupby(["name", "label"], as_index=False)["text"]
        .count()
        .pivot(index="name", columns="label", values="text")
    )
    df = df.rename(columns={i: days[i] for i in df.columns})
    return plot_radar(df, ax=ax, colors=colors, legend=legend)


def plot_hours_radar(df, ax=None, colors="default", legend=False):
    """
    Creates a radar plot showing the number of messages per hour for each
    person in the chat.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns ['name', 'date'].
    ax : plt.Axes or None
        This should be a polar axes. If None (default), one will be created
        with ax = plt.subplot(polar=True).
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either
        'default' in which case the default color scheme is used, a list of
        colors the same length as the number of names in df['name'], or a dict
        which maps each name to a color. For more info about color options,
        see `here <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    legend : bool
        If True, will add a legend to the plot. Default is False.

    Returns
    -------
    matplotlib.axes._subplots.PolarAxesSubplot
        A radar plot with one area per person in the chat.

    See Also
    --------
    plot_days_radar

    Examples
    --------
    .. plot:: ../examples/radar_hour_example.py
       :width: 800px
    """
    df = df.copy()
    df["label"] = df["date"].dt.hour
    hours = (
        ["12am"]
        + ["{}am".format(i) for i in range(1, 12)]
        + ["12pm"]
        + ["{}pm".format(i) for i in range(1, 12)]
    )
    df = (
        df.groupby(["name", "label"], as_index=False)["text"]
        .count()
        .pivot(index="name", columns="label", values="text")
    )
    df = df.rename(columns={i: hours[i] for i in df.columns})
    return plot_radar(df, ax=ax, colors=colors, legend=legend)


def plot_legend(color_dict, ax=None):
    if ax is None:
        ax = plt.subplot(111)

    patches = [mpatches.Patch(facecolor=c, label=n) for n, c in color_dict.items()]
    ax.legend(handles=patches, loc="center", frameon=False)
    ax.axis("off")
    return ax
