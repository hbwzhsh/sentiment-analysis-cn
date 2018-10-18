from bs4 import BeautifulSoup
import requests
import time


def get_soup(url):
	r = requests.get(url)
	html_content = r.text
	soup = BeautifulSoup(html_content, "html.parser")
	return soup


def get_restaurant_urls(url):
	print("Reading from " + url)
	urls = list()
	soup = get_soup(url)
	items = soup.find("div", {"id": "searchList"})
	links = items.findAll("a", {"class": "BL"})
	for link in links:
		if link["href"] != "#top":
			urls.append("http://www.dianping.com" + link["href"])
	return urls


baseUrl = "http://www.dianping.com/singapore/food"
restaurantUrls = list()
restaurantUrls.extend(get_restaurant_urls(baseUrl))

for n in range(2, 51):
	restaurantUrls.extend(get_restaurant_urls(baseUrl + '/p' + str(n)))
	time.sleep(1)

file = open("restaurant.txt", "w")
for url in restaurantUrls:
	file.write(url + "\n")

file.close()
