"""
Test the functions used for loading data from sources like Facebook, WhatsApp,
SMS.
"""

from chatviz.load_data import prep_facebook_data, prep_whatsapp_data, prep_sms_data
import pathlib
import pandas as pd


def test_prep_facebook_data():
    fb_filename = pathlib.Path(__file__) / ".." / "test_data" / "fb_data.json"
    df = prep_facebook_data(fb_filename.resolve())
    expected_df = pd.DataFrame(
        [
            ["1970-01-01 00:00:00", "Customer", "Good Morning"],
            [
                "1970-01-01 00:00:05",
                "Owner",
                "Good morning, Sir. Welcome to the National Cheese Emporium!",
            ],
            ["1970-01-01 00:00:08", "Customer", "Ah thank you my good man."],
            ["1970-01-01 00:00:10", "Owner", "What can I do for you, Sir?"],
            [
                "1970-01-01 00:00:12",
                "Customer",
                "Well, I was, uh, sitting in the public library on Thurmon "
                "Street just now, skimming through 'Rogue Herrys' by Hugh "
                "Walpole, and I suddenly came over all peckish.",
            ],
        ],
        columns=["date", "name", "text"],
    )
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    assert expected_df.equals(df)


def test_prep_whatsapp_data():
    wa_filename = pathlib.Path(__file__) / ".." / "test_data" / "wa_data.txt"
    df = prep_whatsapp_data(wa_filename.resolve())
    expected_df = pd.DataFrame(
        [
            ["1970-01-01 00:01:00", "Owner", "Peckish, sir?"],
            ["1970-01-01 00:01:00", "Customer", "Esuriant."],
            ["1970-01-01 00:01:00", "Owner", "Eh?"],
            ["1970-01-01 00:01:00", "Customer", "'Ee I were all 'ungry-like!"],
            ["1970-01-01 00:02:00", "Owner", "Ah, hungry!"],
        ],
        columns=["date", "name", "text"],
    )
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    assert expected_df.equals(df)


def test_prep_sms_data():
    sms_filename = pathlib.Path(__file__) / ".." / "test_data" / "sms_data.xml"
    df = prep_sms_data(sms_filename.resolve())
    expected_df = pd.DataFrame(
        [
            [
                "1970-01-01 00:02:40",
                "Customer",
                "In a nutshell. And I thought to myself, 'a little fermented "
                "curd will do the trick', so, I curtailed my Walpoling "
                "activites, sallied forth, and infiltrated your place of "
                "purveyance to negotiate the vending of some cheesy "
                "comestibles!",
            ],
            ["1970-01-01 00:03:00", "Owner", "Come again?"],
            ["1970-01-01 00:03:10", "Customer", "I want to buy some cheese."],
        ],
        columns=["date", "name", "text"],
    )
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    assert expected_df.equals(df)
