import requests
import time
import csv
from http.cookies import SimpleCookie

url = "http://www.dianping.com/overseas/shop/ajax/allReview"
params = {
    "shopId": "",
    "cityId": "2311",  # Singapore
    "categoryURLName": "food",
    "power": "5",
    "cityEnName": "singapore",
    "shopType": "10",
    "_token": "eJyNjVtPgzAAhf9Ln8naQrmUtzFkmQHcBkyjMYZt3ORWoBlM43+3i/jik8lJvpMvJzmfoN+cgYkRQgRLgA+iq4pMNU2XMUaKBE5/nG5I4NgfbGC+YCojiVD0ejN7IX4MRoZQv52ILhOR22ojRiDnnJkQjuO4OBdxw4omW5zaGg55yyClKlapAqR/zWCfXIpkfIurCjIMxEUdigvBcmY8k88ciqwBJkjupzAoyRBEytbVWs9O3SkwJp9HivuB6D4wyNA9hf4SPrge3AZ34+VaYNfKGGG8PK7z9rmz0qbqokeZ1b2zTktnZztugH07Qvzds5NyKOwD5tZytVtB39I98PUNR+5raQ=="
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.dianping.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.dianping.com/shop/9951593',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

raw_data = "cy=2311; _lxsdk_cuid=164e476a159c8-0d29a955cfd024-2711938-1fa400-164e476a15ac8; _lxsdk=164e476a159c8-0d29a955cfd024-2711938-1fa400-164e476a15ac8; _hc.v=945ccfd5-f0ef-5ced-96a6-57b81e5368d1.1532841337; s_ViewType=1; ua=dpuser_4252403616; ctu=0c4ac1d1f837a576bedf3401825fa1532dcac384129922ab18742b378372f91f; __mta=88340260.1532841356020.1532966725733.1533207768798.9; JSESSIONID=2376D714B00477B84DDBE15F56A6B3A4; _thirdu.c=cce17ce5b0b1058454459bc4e82e1b49; lgtoken=08fe9c1c8-b423-4c44-b226-f86a6fcf0845; thirdtoken=91385117C0E327C3C7653E4050175B65; dper=a74568066ab518cd86edf71992682dfcfa816ed7ed2d69cb9ad21f48efcc361f2d51b7bf4b414083dbcac3425b0cebb36cacc3cd80cfd57a853f5906324fabeb23246eae3ed28e1254ca54f9e74b9636dbe4fcdbea91d8444d02b1782a2325e9; ll=7fd06e815b796be3df069dec7836c3df; uamo=85023591; _lxsdk_s=1668764b4ed-5b9-d82-f72%7C%7C82"
cookie = SimpleCookie()
cookie.load(raw_data)

cookies = {}
for key, morsel in cookie.items():
    cookies[key] = morsel.value


def get_reviews_from_api(shop_id):
    params["shopId"] = int(shop_id)
    review_list = list()  # store all the reviews crawled
    dish_list = list()  # store all the dish names crawled

    try:
        print("fetching data - " + shop_id)
        r = requests.get(url, params=params, headers=headers, cookies=cookies)
        # print(r.text)
        resp = r.json()

        dish_list.extend(resp["dishTagStrList"])
        reviews = resp["reviewDataList"]
        for review in reviews:
            restaurant_id = review["shopId"]
            user_id = review["userId"]
            body = review["reviewBody"]
            star = review["star"]["value"]
            add_time = review["addTime"]
            review_list.append([restaurant_id, user_id, body, star, add_time])
            
        # Consolidate all the reviews into csv
        with open("reviews.csv", "a", encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for review in review_list:
                # print(review)
                writer.writerow(review)

    except Exception as e:
        print("Error in requesting from " + shop_id)
        print(e)
        return None


with open("data/restaurant-sg.txt", "r") as restaurant_file:
    for line in restaurant_file:
        print("Crawling start - " + line)
        parts = line.split('/')
        shop_id = parts[len(parts) - 1]
        get_reviews_from_api(shop_id)
        time.sleep(1)
