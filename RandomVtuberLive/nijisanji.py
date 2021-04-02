import requests
from bs4 import BeautifulSoup
import random
import webbrowser
import re


def getNijisanjiURL():
    url = "https://virtual-youtuber.userlocal.jp/office/nijisanji_all"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    tableTag = soup.find(class_="table-live-schedules")
    now_time = tableTag.find("div", class_="hour").string
    row_content = tableTag.find_all("tr", class_=re.compile(r"row-content.*"))

    target_url = []
    target_live_title = []
    for row in row_content:
        try:
            if row.find("div", class_="hour").string == now_time:
                target_url.append(row.find("a", target="_blank").get("href"))
                target_live_title.append(row.find("a", target="_blank").string)
            else:
                break
        except AttributeError:
            target_url.append(row.find("a", target="_blank").get("href"))
            target_live_title.append(row.find("a", target="_blank").string)

    while True:
        random_i = random.randint(0, len(target_url) - 1)
        if target_live_title[random_i] != re.compile(r".*プレミア.*"):  # プレミア公開は配信ではないため避ける
            webbrowser.open("https://virtual-youtuber.userlocal.jp/" + target_url[random_i])
            break


if __name__ == '__main__':
    getNijisanjiURL()
