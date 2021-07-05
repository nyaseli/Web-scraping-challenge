from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import time


def scrape():
    path = {"executable_path":r"C:\Users\nyase\Downloads\chromedriver_win32\chromedriver.exe"}
    driver = Browser('chrome',**path)

    driver.visit("https://redplanetscience.com/")
    time.sleep(2)
    text = driver.html
    search = bs(text,"html.parser")

    heading = search.find_all('div',class_ = "content_title")

    news_title = heading[0].text

    paragraph = search.find_all('div',class_ = "article_teaser_body")
    news_p = paragraph[0].text

    driver.visit("https://spaceimages-mars.com/")
    text = driver.html
    search = bs(text,"html.parser")
    image = search.find_all('img',class_ = "headerimage fade-in")
    text = image[0]["src"]

    featured_image_url = "https://spaceimages-mars.com/"+text

    data = pd.read_html("https://galaxyfacts-mars.com/")

    table = data[1]
    table.columns = ["Name", "Facts"]

    html_table = table.to_html()

    driver.visit("https://marshemispheres.com/")
    text = driver.html
    search = bs(text,"html.parser")
    hemi = search.find_all('div',class_ = "collapsible results")
    hemis = hemi[0].find_all('h3')
    names = []
    for i in hemis:
        txt = i.text
        names.append(txt)

    hemis = hemi[0].find_all('a')
    links = []
    for i in hemis:
        txt = i['href']
        links.append(txt)

    links = list(set(links))

    hemilinks = []
    for i in links:
        hemilinks.append("https://marshemispheres.com/"+i)

    result = {}
    for link in hemilinks:
        driver.visit(link)
        text = driver.html
        search = bs(text,"html.parser")
        image = search.find_all('img',class_ = "wide-image")
        text = image[0]["src"]
        img = "https://marshemispheres.com/"+text
        name = [i for i in names if i.split()[0].lower() in link][0]
        result[name] = img

    hemisphere_image_urls = []
    for name , image in result.items():
        hemi = {'title':name,"img_url":image}
        hemisphere_image_urls.append(hemi)
    mars_data = {
        "news_title": news_title,
        "news_p": news_p, 
        "featured_image_url":featured_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls 
    }
    driver.quit()
    return mars_data

