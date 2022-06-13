import json, datetime, asyncio
import requests
from bs4 import BeautifulSoup

TOKEN = ""
#WebhookのURLを入れる
webhook_url = ""
school_url = "https://www.niihama-nct.ac.jp"
twitter_api_url = "https://api.twitter.com/2"
user_id = ""

async def get_topic(now, old_topic):
    if now.hour%2 == 0 and now.minute == 0:
        res = requests.get(school_url)
        if res.ok:
            soup = BeautifulSoup(res.content,"html.parser")
            topic_anker = soup.find("div",class_="home-main-news-con").find_all("a")
            topic_time = soup.find("div",class_="home-main-news-con").find_all("time")
            topic_link = [topic_anker[i].get("href") for i in range(len(topic_anker))]
            topic_content = [topic_anker[i].text for i in range(len(topic_anker))]
            message = {
                "content":"ホームページからの情報",
                "embeds": [
                    {
                        "title":f"現時点でのトピック",
                        "url":school_url,
                        "fields":[{"name":f"{topic_time[i].text}","value":f"[{topic_content[i]}]({school_url+topic_link[i]})","inline":False} for i in range(len(topic_anker))]
                    }
                ]
            }
            await asyncio.sleep(60)
            if old_topic == message:
                print("[topic]前と被ったのでパス")
                return {}
        else:
            return {}
        print("[topic]送信")
        return message
    else:
        print("[topic]まだその時ではない")
        return{}

async def get_tweet(TOKEN,user_id,now,old_tweet):
    if now.minute%15 == 0:
        headers = {"Accept":"application/json", "Authorization":f"Bearer {TOKEN}"}
        res = json.loads(requests.get(twitter_api_url+f"/users/{user_id}/tweets",headers=headers).text)
        message = {"content": res["data"][0]["text"]}
        await asyncio.sleep(60)
        if old_tweet == message:
            print("[tweet]前と一致したのでパス")
            return {}
        print("[tweet]送信")
        return message
    else:
        print("[tweet]まだその時ではない")
        return{}

async def main():
    old_msg = {"tweet":{},"topic":{}}
    while True:
        print("[main]ループ開始")
        msg_get_task = []
        now = datetime.datetime.now()
        #Twitterから寮食のツイートを取得
        msg_get_task.append(get_tweet(TOKEN, user_id, now, old_msg["tweet"]))        
        #ホームページからトピックを取得
        msg_get_task.append(get_topic(now, old_msg["topic"]))
        msg = await asyncio.gather(*msg_get_task)
        for i in range(len(msg)):
            if msg[i] == {}:
                pass
            else:
                old_msg[list(old_msg)[i]] = msg[i]
                status = requests.post(webhook_url,json.dumps(msg[i]),headers={'Content-Type': 'application/json'})
        print("[main]送信完了 ループ終了")
        await asyncio.sleep(20)

asyncio.run(main())