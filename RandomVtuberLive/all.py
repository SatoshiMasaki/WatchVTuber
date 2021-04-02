import requests
from bs4 import BeautifulSoup
import random
import webbrowser
import re


def getLiveURL():
    url = "https://virtual-youtuber.userlocal.jp/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    tableTag = soup.find(class_="table-live-schedules")
    now_time = tableTag.find("div", class_="hour").string
    row_content = tableTag.find_all("tr", class_=re.compile(r"row-content.*"))

    target_url = []
    for row in row_content:
        try:
            if row.find("div", class_="hour").string == now_time:
                target_url.append(row.find("a", target="_blank").get("href"))
            else:
                break
        except AttributeError as a:
            print(a)
            print("{}のためtarget_urlに追加します".format(now_time))
            print(row)
            target_url.append(row.find("a", target="_blank").get("href"))

    # SHOWROOMなどYouTube以外のサイトの場合URLの貼られ方が異なるため調整
    finally_url = target_url[random.randint(0, len(target_url) - 1)]
    if re.match(r"https://", finally_url):
        webbrowser.open(finally_url)
    else:
        webbrowser.open("https://virtual-youtuber.userlocal.jp/" + finally_url)


if __name__ == '__main__':
    getLiveURL()
