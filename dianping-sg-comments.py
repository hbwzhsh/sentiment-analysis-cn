import requests
from bs4 import BeautifulSoup
from http.cookies import SimpleCookie

proxies = {
	"http": "http://37.59.250.98",
}
headers = {
	'Host': 'www.dianping.com',
	'Referer': '',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
	'Accept-Encoding': 'gzip, deflate'
}

raw_data = "cy=2311; cye=singapore; _lxsdk_cuid=164e476a159c8-0d29a955cfd024-2711938-1fa400-164e476a15ac8; _lxsdk=164e476a159c8-0d29a955cfd024-2711938-1fa400-164e476a15ac8; _hc.v=945ccfd5-f0ef-5ced-96a6-57b81e5368d1.1532841337; s_ViewType=1; dper=a74568066ab518cd86edf71992682dfc9f319a811019bd44349b10a34e92a4b03792193a4eebf2ec129b40a00e209c0d5c587ec3af3ea5226063297014c74d195a28eee62fb23182908b2431fade58572313efd53e79214f13313e81d202182c; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_4252403616; ctu=0c4ac1d1f837a576bedf3401825fa1532dcac384129922ab18742b378372f91f; uamo=85023591; __mta=88340260.1532841356020.1532843168352.1532843227201.3; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; _lxsdk_s=%7C%7C0"
cookie = SimpleCookie()
cookie.load(raw_data)

cookies = {}
for key, morsel in cookie.items():
	cookies[key] = morsel.value


def get_soup(url, prev_url):
	headers["Referer"] = prev_url
	r = requests.get(url, headers = headers, cookies = cookies, proxies = proxies)
	html_content  = r.text
	print(str(r.text))

	soup = BeautifulSoup(html_content, "html.parser")
	return soup


def get_reviews(url, prev_url):
	print("Reading from " + url)
	soup = get_soup(url, prev_url)
	shop_name = soup.find("a", {"class": "shop-name"})

	items = soup.find("div", {"class": "reviews-items"})
	authors = items.findAll("a", {"class": "name"})
	review_words = items.findAll("div", {"class": "review-words"})
	dates = items.findAll("span", {"class": "time"})
	stars = items.findAll("span", {"class": "sml-rank-stars"})

	reviews = list()
	for n in range(0, len(review_words)):
		reviews.append({
			"shop_name": shop_name.text,
			"author": authors[n].text,
			"review_words": review_words[n].text,
			"date": dates[n].text,
			"stars": stars[n].get('class', [])
		})
	return reviews


# read url files
restaurantURLs = list()

file = open("reviews.csv", "w")
for review in get_reviews("http://www.dianping.com/shop/9951593/review_all/p2", "http://www.dianping.com/shop/9951593"):
	file.write(review["shop_name"] + "\n")
	file.write(review["author"] + "\n")
	file.write(review["review_words"] + "\n")
	file.write(review["date"] + "\n")
	file.write(str(review["stars"]) + "\n")
	file.write("\n\n")

file.close()

# restaurantUrls = list()
# restaurantUrls.extend(getRestaurantURLs(baseUrl))

# for n in range(2,51):
# 	restaurantUrls.extend(getRestaurantURLs(baseUrl + '/p' + str(n)))
# 	time.sleep(1)