from bs4 import BeautifulSoup
import requests
import json
import datetime

#WebhookのURLを入れる
webhook_url = ""
url = "https://www.niihama-nct.ac.jp"
headers = {'Content-Type': 'application/json'}

res = requests.get(url)
if not res.ok:
    print("Error")
else:
    now = datetime.datetime.now()
    now_time_str= f"{now.year}年{now.month}月{now.day}日{now.hour}時{now.minute}分"
    soup = BeautifulSoup(res.content,"html.parser")
    news_anker = soup.find("div",class_="home-main-news-con").find_all("a")
    news_time = soup.find("div",class_="home-main-news-con").find_all("time")
    news_link = [news_anker[i].get("href") for i in range(len(news_anker))]
    news_content = [news_anker[i].text for i in range(len(news_anker))]
    send_message = {
        "content":"ホームページからの情報",
        "embeds": [
            {
                "title":f"{now_time_str}時点でのトピック",
                "url":url,
                "fields":[{"name":f"{news_time[i].text}","value":f"[{news_content[i]}]({url+news_link[i]})","inline":False} for i in range(len(news_anker))]
            }
        ]
    }
    requests.post(webhook_url,json.dumps(send_message),headers=headers)