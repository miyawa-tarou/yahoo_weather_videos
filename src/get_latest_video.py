# coding: UTF-8
import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import re

with open("min.txt") as m:
    d = csv.reader(m, delimiter=",")
    line = next(d)
    min = int(line[0])
    latest = int(line[1]) + 1 # latestいらなくて？
    max = min

    # IDなしだと最新が取れるのでそこからlatest取得
    url = "https://weather.yahoo.co.jp/weather/video/"
    html = requests.get(url)
    if not html.status_code == requests.codes.ok:
        print("henna request : init")
        sleep(60)
        html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")
    videoList = soup.find_all("div", attrs={"class", "videoDetail"})

    with open("../htdocs/video_list.csv", "a", encoding="utf8") as f:
        writer = csv.writer(f, lineterminator="\n")

        for videoHtml in videoList:
            result = re.match(u"\?c=(\d+)", videoHtml.a.get("href"))
            id = result.group(1)
            print(id)

            url = "https://weather.yahoo.co.jp/weather/video/?c=" + str(id)
            html = requests.get(url)
            if not html.status_code == requests.codes.ok:
                print("henna request :" + str(id))
                sleep(60)
                html = requests.get(url)

            soup = BeautifulSoup(html.content, "html.parser")
            url = soup.find_all("meta", property="og:url")[0].get("content")

            result = re.match(u".*c=(\d+)", url)
            if not result:
                continue

            id = result.group(1)

            if int(id) < min:
                continue

            print("match:" + id)

            title = soup.select("h1")[0].getText()
            time = soup.select("p.dTime")[0].getText()
            t = re.match(u".*配信日時：(.+)", time).group(1)
            caption = soup.select("p.videoCaption")[0].getText()
            nameR = re.match(u".*[(（]気象予報士[・　](.+)[)）]", caption, flags=re.DOTALL)
            if not nameR:
                name = "---"
            else:
                name = nameR.group(1).replace(" ", "").replace("　", "")

            list = [id, title, t, url, name]
            writer.writerow(list)
            if max < int(id):
                max = int(id)

        with open("min.txt", "w") as w:
            max = int(max) + 1
            w.write(str(max) + "," + str(latest))
