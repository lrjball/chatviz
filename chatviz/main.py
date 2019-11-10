import matplotlib.pyplot as plt
from chatviz.utils import _build_color_dict
from chatviz.plotting import (
    plot_donuts,
    plot_reply_times,
    plot_timeline,
    plot_hours_radar,
    plot_days_radar,
    plot_words,
    plot_legend,
)


def visualize_chat(
    df,
    title,
    colors="default",
    timeline_freq="MS",
    timeline_tick_format="%b '%y",
    timeline_tick_step=6,
    timeline_color="default",
    timeline_stacked=False,
    top_n_words=10,
    stopwords=None,
):
    """
    Creates a series of plots given a dataframe of messages.

    The plots created are:

    1. 3 donut plots showing the number of messages, words and characters used
       by each person in the chat.
    2. A bar chart showing the average time to reply in hours for each person.
    3. A timeline showing the number of messages over time, can optionally be
       split down to per person.
    4. Bar charts showing the most used words by each person.
    5. 2 radar plots showing the number of messages sent at each hour and day
       respectively for each person.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe of messages. Must have the columns
        ['date', 'name', 'text'].
    title : str
        The title for the plot.
    colors : {'default'} or list of str or dict
        The colors to be used for each person in the chat. Should be either
        'default' in which case the default color scheme is used, a list of
        colors the same length as the number of names in df['name'], or a dict
        which maps each name to a color. For more info about color options,
        see `here <https://matplotlib.org/2.0.2/api/colors_api.html>`_.
    timeline_freq: str
        The offset string for the resample frequency in the timeline plot. See `here
        <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects>`_
        for more. The default is 'MS', which will generate a monthly plot.
    timeline_tick_format : str
        The format string for the x tick labels in the timeline plot, which are dates.
        The default is '%b \'%y' which gives for example `Jan '19`.
    timeline_tick_step : int
        The number of steps between the ticks on the x-axis for the timeline
        plot. By default this is 6, so every 6 bars will have an x-tick label.
    timeline_color : str
        Only applicable if timeline_stacked is False. In this case, the timeline
        plot will only be one color, which may want to be different from `colors`
        as these are per person. Default is 'default' which will just use matplotlibs
        default color.
    timeline_stacked : bool
        If True, then a stacked bar chart will be created for the timeline plot,
        with one color per person involved in the chat. If False (default),
        will just plot one colored bar with the overall count.
    top_n_words : int
        The number of top words to include in the words bar chart. Default is 10.
    stopwords : None or iterable
        If given, then these words will be removed from the words bar charts.
        If None, all words will be kept (Note: this will lead to poor results
        as 'the', 'and', 'a', 'is' etc. will be the top words. A stopword list
        is recommended).

    Returns
    -------
    plt.figure
        A matplotlib figure with all of the message plots on it.

    Examples
    --------

    This example visualizes the script from Monty Python Flying Circus
    Series 1. In just a few lines we can used chatviz to create a sophisticated
    infographic. Note: The dates have been randomly created for this example.

    .. plot:: ../examples/complete_example.py
    """
    fig = plt.figure()
    gs = fig.add_gridspec(
        4, 4, height_ratios=[0.2, 0.5, 0.2, 0.2], hspace=0.6, wspace=0.5
    )

    color_dict = _build_color_dict(colors, df)

    gsdonuts = gs[0, :3].subgridspec(1, 3)
    ax_donuts = [
        fig.add_subplot(gsdonuts[0]),
        fig.add_subplot(gsdonuts[1]),
        fig.add_subplot(gsdonuts[2]),
    ]
    plot_donuts(df, ax=ax_donuts, colors=color_dict)

    ax_legend = fig.add_subplot(gs[0, 3])
    # plot_reply_times(df, ax=ax_reply, colors=color_dict)
    plot_legend(color_dict, ax=ax_legend)

    ax_timeline = fig.add_subplot(gs[1, :])

    plot_timeline(
        df,
        ax=ax_timeline,
        colors=color_dict if timeline_stacked else [timeline_color],
        freq=timeline_freq,
        tick_format=timeline_tick_format,
        tick_step=timeline_tick_step,
        stacked=timeline_stacked,
    )

    gswords = gs[2, :].subgridspec(1, len(set(df["name"])), wspace=1.3)
    ax_words_title = fig.add_subplot(gswords[:])
    ax_words_title.set_title("Most Used Words", y=1.1)
    if len(color_dict) > 1:
        ax_words_title.axis(False)
    ax_words = [fig.add_subplot(gswords[i]) for i in range(len(set(df["name"])))]
    plot_words(df, ax=ax_words, colors=color_dict, top_n=top_n_words, stopwords=stopwords)

    gsradar = gs[3, 2:].subgridspec(1, 2)
    ax_radar_title = fig.add_subplot(gsradar[:])
    ax_radar_title.set_title("Distribution of Message Times", y=1.2)
    ax_radar_title.axis(False)
    hour_radar_ax = fig.add_subplot(gsradar[0], polar=True)
    plot_hours_radar(df, ax=hour_radar_ax, colors=colors)
    day_radar_ax = fig.add_subplot(gsradar[1], polar=True)
    plot_days_radar(df, ax=day_radar_ax, colors=color_dict)

    gsreply = gs[3, :2].subgridspec(1, 2)
    ax_reply_title = fig.add_subplot(gsreply[:])
    ax_reply_title.axis(False)
    ax_reply_title.set_title("Average Time to Reply", y=1.2)
    ax_reply = fig.add_subplot(gs[3, :2])
    plot_reply_times(df, ax=ax_reply, colors=color_dict)

    fig.suptitle(title, y=0.95)
    return fig


# TODO: add a quickstart and a gallery with a few examples
# TODO: upload to github and pypi
