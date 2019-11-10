import json
import xml.etree.ElementTree as ET

import pandas as pd


def prep_facebook_data(filename):
    """
    Processes a Facebook chat file into a neat DataFrame.

    Chat history can be downloaded from Facebook as JSON. See `here
    <https://www.facebook.com/help/www/1701730696756992>`_ for how to download
    Facebook chat data in JSON format.

    Parameters
    ----------
    filename : Union[int, str, bytes, PathLike]
        The path to the JSON chat file.

    Returns
    -------
    pd.DataFrame
        A DataFrame with all of the necessary columns
        i.e. ['date', 'name', 'text'].
    """
    with open(filename, "r") as f:
        data = json.load(f)
    df = pd.read_json(json.dumps(data["messages"]))
    df = df[pd.notnull(df["content"])]
    df["date"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
    df = df.rename(columns={"content": "text", "sender_name": "name"})
    return df[["date", "name", "text"]]


def prep_sms_data(filename):
    """
    Processes an SMS chat file into a neat DataFrame.

    Chat history can be downloaded as XML using the app `SMS Backup & Restore`.
    See `here <https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en_GB>`_
    for Android.

    Parameters
    ----------
    filename : Union[int, str, bytes, PathLike]
        The path to the XML chat file.

    Returns
    -------
    pd.DataFrame
        A DataFrame with all of the necessary columns
        i.e. ['date', 'name', 'text'].

    Warnings
    --------
    If your chat data is from a different app then this may not work as
    column names will be different, but this function can be used as a basis
    for any file manipulations on XML data before passing the dataframe to
    the main function.
    """
    with open(filename, "rb") as f:
        etree = ET.parse(f)
    df = pd.DataFrame([doc.attrib for doc in etree.iter("sms")])
    df = df.rename(columns={"body": "text", "type": "name"})
    df["date"] = pd.to_datetime(df["date"].astype(int), unit="ms")
    return df[["date", "name", "text"]]


def prep_whatsapp_data(filename):
    """
    Processes a WhatsApp chat file into a neat DataFrame.

    Chat history can be downloaded from WhatsApp as a text file. See `here
    <https://faq.whatsapp.com/en/wp/22548236>`_ for how to download
    WhatsApp chat data as a .txt file.

    Parameters
    ----------
    filename : Union[int, str, bytes, PathLike]
        The path to the JSON chat file.

    Returns
    -------
    pd.DataFrame
        A DataFrame with all of the necessary columns
        i.e. ['date', 'name', 'text'].
    """
    data = []
    with open(filename, "r") as f:

        for line in list(f)[1:]:
            line = line.strip()
            if line.endswith("<Media omitted>"):
                continue
            try:
                date, rest = line.split(" - ", 1)
            except ValueError:
                continue
            name, text = rest.split(": ", 1)
            data.append([date, name, text])
    df = pd.DataFrame(data, columns=["date", "name", "text"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)
    return df
