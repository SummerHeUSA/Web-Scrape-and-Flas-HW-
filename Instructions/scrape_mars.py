from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/summerhe/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# list of things I need to scrape
# top articles (name and desc)
# 4 images of the hemiscpheres
# weather report
# HTML table of facts
def scrape():

    mars_collections = {}

# news 
    url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2019%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
    resp = requests.get(url)
    data = resp.json()
    listings = pd.DataFrame.from_records(data)
    listings['title'] = listings['items'].map(lambda x : x.get('title'))
    listings["news_descri"]= listings['items'].map(lambda x : x.get('description'))
    # we changed this one to conform with a document definition and avoid a bson error
    mars_collections['news_title'] = listings['title'].tolist()[:1]
    mars_collections['news_description'] = listings['news_descri'].tolist()[:1]
# feature image
    pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    pic_data = requests.get(pic_url)
    soup = BeautifulSoup(pic_data.content, "html.parser")
    pic_link_temp = soup.find('a', {"class":"fancybox"}).attrs.get("data-fancybox-href")
    pic_link = "https://www.jpl.nasa.gov" + pic_link_temp  
    
    mars_collections['featured_pic_line']  = pic_link

    
# weather 
    weather_url = "https://twitter.com/MarsWxReport/status/1098709468945281025"
    weather_data = requests.get(weather_url)
    soup_weather = BeautifulSoup(weather_data.content, "html.parser")
    weather_description= soup_weather.find('p', {"class":"TweetTextSize"}).get_text()
   
    mars_collections['weather_description'] = weather_description
# mars_fact
    df_table = pd.read_html("https://space-facts.com/mars/")[0]
    df_table.to_csv('data.txt', sep ='\t', index = False)
    with open('data.txt', 'r') as myfile:
        data = myfile.read().replace('\n', '')   
    
    mars_collections ["mars_fact"] = data
    

# hemis pics 
    homepage = requests. get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    soup = BeautifulSoup(homepage.content, "html.parser")
    links = soup.find_all('a', {'class':'itemLink'})
    links = ["https://astrogeology.usgs.gov/" + x.attrs.get('href') for x in links]
    
    import os

    def save_page_from_web(url):
        resp = requests.get(url)
        save_name = url.split("/")[-1] + ".html"
        save_path = os.path.join("web_pages/",save_name )
        with open(save_path, "w") as f:
            f.write(resp.text)
    for link in links:
        save_page_from_web(link)
        import glob
    html = glob.glob('web_pages/*.html')
    
    results = []

    for local_file in html:

        with open(local_file, 'r') as f:

            soup = BeautifulSoup(f, "html.parser")
            full_image_link = "https://astrogeology.usgs.gov"+soup.find('img', {'class': 'wide-image'}).attrs.get("src")
            image_name = soup.find('h2', {'class': 'title'}).get_text()
            results.append({
                "image_link": full_image_link,
                "image_name": image_name
            })

    mars_collections['hemisphere_image'] = results
    return mars_collections









