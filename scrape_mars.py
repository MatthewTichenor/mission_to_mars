from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scraping():
	#Get the info from the NASA News Webpage
	url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
	response = requests.get(url)
	bsoup = BeautifulSoup(response.text, "html.parser")

	#news_title = bsoup.find("div", class_="content_title")["target":"_self"].text.strip()
	#news_p = bsoup.find("div", class_="image_and_description_container").text.strip()

	news_title = bsoup.find("div", class_="content_title").text.strip()
	news_p = bsoup.find("div", class_="image_and_description_container").text.strip()

	print(news_title)
	print(news_p)

	# GEt the featured image of Jet propulsion Lab
	executable_path = {"executable_path": "chromedriver.exe"}
	browser = Browser("chrome", **executable_path, headless=True)
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)

	#Using soup to get the image link
	html = browser.html
	bsoup = BeautifulSoup(html, "html.parser")
	image = bsoup.find("article", class_="carousel_item")
	featured_image_url = "https://www.jpl.nasa.gov" + image["style"][23:75]
	print(featured_image_url)

	#Get the info from twitter
	url = "https://twitter.com/marswxreport?lang=en"
	response = requests.get(url)
	bsoup = BeautifulSoup(response.text, "html.parser")

	mars_weather = bsoup.find("div", class_="js-tweet-text-container").text.strip()

	print(mars_weather)

	#Facts

	url = "https://space-facts.com/mars/"
	table = pd.read_html(url)
	#table
	df = table[0]
	df.columns = ["Facts", "Answers"]
	df.head(20)
	dictionary = df.to_dict('list')
	dictionary = {str(key): value for key, value in  dictionary.items()}
	dictionary

	# GEt the images from the hemispheres -.-
	executable_path = {"executable_path": "chromedriver.exe"}
	browser = Browser("chrome", **executable_path, headless=True)
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)
	html = browser.html
	bsoup = BeautifulSoup(html, 'html.parser')
	hemisphere_image_urls = []
	dict = {}
	url = 'https://astrogeology.usgs.gov'

	image = bsoup.find_all('a', class_='itemLink product-item')
	for i in image:
	    if(i.get_text() != ''):

	        browser.visit(url + i['href'])    
	        
	        html = browser.html
	        bsoup = BeautifulSoup(html, 'html.parser')
	        
	        componentlnk = bsoup.find('div', class_='downloads').find('a')['href']
	        dict = {'title': i.get_text(),
	                'img_url' : componentlnk}        

	        hemisphere_image_urls.append(dict)

	        
	        browser.back()
	

	mars_data = {"news_title": news_title,"news_p": news_p,"featured_image_url": featured_image_url,"table" : dictionary,"hemisphere_image_urls" : hemisphere_image_urls,"Weather" : mars_weather}
	return mars_data