from bs4 import BeautifulSoup
import requests
import json
import datetime
import time

#WebhookのURLを入れる
webhook_url = "https://discord.com/api/webhooks/984428325835505684/jIRww8J4vTCCqrGlZ3V9v2QISgGQastiMt2LxdLbGqz9lQCbUL7hvVBoYDC79D_iSzCk"
url = "https://www.niihama-nct.ac.jp"
headers = {'Content-Type': 'application/json'}

while True:
    now = datetime.datetime.now()
    if now.hour%4==0 and now.minute==30:
        res = requests.get(url)
        if not res.ok:
            print("Error")
            requests.post(webhook_url,json.dumps({"content":"Error 取得に失敗しました"}),headers=headers)
        else:
            print("Send")
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
            time.sleep(60)
