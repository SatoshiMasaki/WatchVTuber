from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import re
import random
import webbrowser

"""
minicalendar_viewer
>list1 スケジュール表
>full_hr 区切り

<li>00時00分～
    <img src="https:" alt="face.png" title="face.png" width="25" height="25" loading="lazy">
    <a class="ext" href="https://twitter.com/" rel="nofollow">笹木咲
    <img src="https://cdn.wikiwiki.jp/to/w/common/image/plus/ext.png?v=4" alt="" title="" class="ext 
    pukiwiki-open-uri" data-href="https://twitter.com/saku_sasaki/status/1383435601165254662" data-frame="_blank">
    </a> at:YouTube ポケモンピンボール
</li>


selenium.common.exceptions.InvalidSelectorException: Message: invalid selector: Unable to locate an element with the xpath expression //div[@class='holodule navbar-text' and contains(text(), 4/20)] because of the following error:
SyntaxError: Failed to execute 'evaluate' on 'Document': The string '//div[@class='holodule navbar-text' and contains(text(), 4/20)]' is not a valid XPath expression.
  (Session info: headless chrome=89.0.4389.128)
"""

driver_pass = "chromedriver.exe"
nijisanji_url = "https://wikiwiki.jp/nijisanji/%E9%85%8D%E4%BF%A1%E4%BA%88%E5%AE%9A%E3%83%AA%E3%82%B9%E3%83%88"
hololive_url = "https://schedule.hololive.tv/"
pattern_midnight = re.compile(".*0[0-5]時[0-9]{2}分～.*")
pattern_noon = re.compile(".*(0[6-9])*(1[0-7])*時[0-9]{2}分～ .*")
pattern_night = re.compile(".*(1[8-9])*(2[0-3])*時[0-9]{2}分～ .*")
pattern_border = re.compile(".*border: 3px red solid.*")
pattern_border_another = re.compile(".*border: 3px solid red.*")


def getHoloSchedule():
    """
    div.holodule
    >div.holodule navbar-text

                                04/19
                                (月)

    親の親の兄弟要素が予定表

    予定枠のaタグにboaderが指定されていれば配信中？
    """
    def check_exist_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    now = datetime.datetime.now()
    today_sentence = "{}/{}".format(now.month, now.day)
    target_live = []

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get(hololive_url)
    time.sleep(5)

    container = driver.find_element_by_xpath(
        "//div[@class='holodule navbar-text' and contains(text(), '{}')]".format(today_sentence)
    )

    if now.hour < 6:
        now_hour_label = 0
    elif now.hour < 12:
        now_hour_label = 1
    elif now.hour < 18:
        now_hour_label = 2
    else:
        now_hour_label = 3

    container = container.find_element_by_xpath(
        "parent::node()/parent::node()/parent::node()/parent::div[@class='container']"
    )
    for _ in range(now_hour_label):
        container = container.find_element_by_xpath(
            "following-sibling::div"
        )

    container = container.find_element_by_xpath("div/div[2]/div")
    container_size = len(container.find_elements_by_xpath("div"))

    for i in range(container_size):
        a_tag = container.find_element_by_xpath("div[{}]/a".format(i + 1))
        if pattern_border.match(a_tag.get_attribute("style")) or \
                pattern_border_another.match(a_tag.get_attribute("style")):
            target_live.append(a_tag.get_attribute("href"))

    if len(target_live) == 0:
        print("現在配信中のライバーはいません。")
        time.sleep(10)
    else:
        webbrowser.open(target_live[random.randint(0, len(target_live) - 1)])


def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    now_hour = datetime.datetime.now().hour
    schedule_data = None

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get(nijisanji_url)
    time.sleep(5)

    html = driver.page_source.encode('utf-8')
    page_data = BeautifulSoup(html, "html.parser")

    calender = page_data.find(class_="minicalendar_viewer")
    mini_tables = calender.find_all(class_="list1")

    for table in mini_tables:
        if now_hour < 6:
            if pattern_midnight.match(str(table.find("li"))):
                schedule_data = table.find_all("li")
        elif now_hour < 18:
            if pattern_midnight.match(str(table.find("li"))):
                schedule_data = table.find_all("li")
        else:
            if pattern_midnight.match(str(table.find("li"))):
                schedule_data = table.find_all("li")

    container = []
    for data, i in enumerate(schedule_data):
        if int(data.text[0:2]) == now_hour:
            container.append(i)


if __name__ == '__main__':
    getHoloSchedule()
