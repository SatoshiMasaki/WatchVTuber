from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import re
import random
import webbrowser


driver_pass = "chromedriver.exe"
nijisanji_url = "https://nijisanji.net/lives/"
hololive_url = "https://schedule.hololive.tv/"
pattern_midnight = re.compile(".*0[0-5]時[0-9]{2}分～.*")
pattern_noon = re.compile(".*(0[6-9])*(1[0-7])*時[0-9]{2}分～ .*")
pattern_night = re.compile(".*(1[8-9])*(2[0-3])*時[0-9]{2}分～ .*")
pattern_border = re.compile(".*border: 3px red solid.*")
pattern_border_another = re.compile(".*border: 3px solid red.*")


def getHoloSchedule():
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


def getNijiSchedule():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    now_on_live_flag = False

    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    driver.get(nijisanji_url)
    time.sleep(5)

    try:
        driver.find_element_by_xpath("//span[@class='ui mini horizontal label pink']")
        now_on_live_flag = True
    except NoSuchElementException:
        print("現在配信中のライバーはいません。")
        time.sleep(10)

    if now_on_live_flag:
        items = driver.find_elements_by_xpath(
            "//span[@class='ui mini horizontal label pink']/parent::a"
        )

        webbrowser.open(
            items[random.randint(0, len(items)) - 1].get_attribute("href")
        )


if __name__ == '__main__':
    container = [getNijiSchedule, getHoloSchedule]
    container[random.randint(0, 1)]()
