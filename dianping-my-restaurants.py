from bs4 import BeautifulSoup
import requests
import time
from http.cookies import SimpleCookie

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


def get_soup(url):
	r = requests.get(url, headers=headers, cookies=cookies)
	html_content = r.text
	print(html_content)
	soup = BeautifulSoup(html_content, "html.parser")
	return soup


def get_restaurant_urls(url):
	print("Reading from " + url)
	urls = list()
	soup = get_soup(url)
	items = soup.find("div", {"class": "pic"})
	print(items)
	for item in items:
		link = item.find("a")
		print(link["href"])
		if link["href"] != "#top":
			urls.append(link["href"])

	return urls


baseUrl = "http://www.dianping.com/malaysia/ch10"
restaurantUrls = list()
restaurantUrls.extend(get_restaurant_urls(baseUrl))

for n in range(2, 51):
	restaurantUrls.extend(get_restaurant_urls(baseUrl + '/p' + str(n)))
	time.sleep(1)

file = open("restaurant.txt", "w")
for url in restaurantUrls:
	file.write(url + "\n")

file.close()
