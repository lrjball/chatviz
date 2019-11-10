import requests as req
import pandas as pd
from bs4 import BeautifulSoup
import re


def get_all_links():
    links = []
    link = "http://montypython.50webs.com/scripts"
    r = req.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    for sub_link in soup.find_all("a")[3:]:
        link2 = "/".join([link, sub_link["href"]])
        if link2.endswith("/"):
            link2 = link2[:-1]
        r2 = req.get(link2)
        soup2 = BeautifulSoup(r2.text, "html.parser")
        for sub_link2 in soup2.find_all("a")[3:-2]:
            links.append("/".join([link2, sub_link2["href"]]))
    return links


def get_film_data(link):
    r = req.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    data = []
    for i in soup.find_all("p"):
        if i.find_all(attrs=["name"]):
            name = i.contents[0].string.replace(":", "").strip()
            try:
                text = i.contents[1].string
            except IndexError:
                text = ""
            data.append([name, text])
    return data


def save_film_script(title, fname):
    all_links = get_all_links()
    all_links = [link for link in all_links if title in link]
    all_links = sorted(all_links, key=lambda x: int(re.sub("[^0-9]", "", x)))
    all_data = []
    for link in all_links:
        print(link)
        all_data += get_film_data(link)
    df = pd.DataFrame(all_data, columns=["name", "text"])
    print(df["name"].value_counts())
    df.to_csv(fname)


def get_series_data(link):
    r = req.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    data = []
    try:
        names = [
            n.string.strip().lower().replace(".", "").replace("-", "")
            for n in soup.find_all("dt")
        ]
    except AttributeError:
        return None
    actors = [n.string.strip() for n in soup.find_all("dd") if n.string is not None]
    cast_dict = {n: a for (n, a) in zip(names, actors)}
    for i in soup.find_all("p"):
        if i.find_all(attrs=["name"]):
            name = (
                i.contents[0]
                .string.replace(":", "")
                .strip()
                .lower()
                .replace(".", "")
                .replace("-", "")
            )
            try:
                text = i.contents[1].string
            except IndexError:
                text = ""
            try:
                data.append([cast_dict[name], text])
            except:
                found = False
                for key in cast_dict.keys():
                    if (name in key) or (key in name):
                        data.append([cast_dict[key], text])
                        found = True
                        break
                if not found:
                    print(f"{name} not found in {list(cast_dict.keys())}")
    return data


if __name__ == "__main__":
    all_links = get_all_links()
    title = "Series_4"
    fname = "series_4.csv"
    all_links = [link for link in all_links if title in link]
    all_links = sorted(all_links, key=lambda x: int(re.sub("[^0-9]", "", x)))
    all_dfs = []
    for ind, link in enumerate(all_links):
        print(ind, link)
        data = get_series_data(all_links[ind])
        if data is not None:
            data = pd.DataFrame(data, columns=["name", "text"])
            all_dfs.append(data)
        else:
            print("Didnt work for this one!")
    df_all = pd.concat(all_dfs)

    def fix_typos(string):
        string = string.replace(":", "").strip()
        return string.replace("Plain", "Palin").replace("Wytech", "Wyech")

    df_all["name"] = [fix_typos(n) for n in df_all["name"]]
    print(df_all["name"].value_counts())
    df_all.to_csv(fname)
