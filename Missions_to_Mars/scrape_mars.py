# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# splinter
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# scrape data
def scrape():

    # scrape news title and paragraph
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    mars_news = bs(html, 'html.parser')

    # Extract the text of the title
    news_html = mars_news.select_one('ul.item_list li.slide')
    news_title = news_html.find('div', class_="content_title").text

    # Extract the text of the paragraph
    news_paragraph = news_html.find('div', class_="article_teaser_body").text




    # JPL Mars Space Images - Featured Image
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(mars_image_url)

    #follow path to image
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')

    #store as var
    image_html = browser.html

    # Create a Beautiful Soup object
    mars_image = bs(image_html, 'html.parser')

    # find scraped image
    find_image = mars_image.find(class_="main_image")

    # home url 
    nasa_url = 'https://www.jpl.nasa.gov'

    scrape_image_url = nasa_url + find_image["src"]

    # Mars Facts
    space_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(space_facts_url)
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ['Description','Value']
    
    # convert to_html
    mars_info = mars_facts_df.to_html(header=True, index=True)

    # Mars Hemispheres

    # image urls and hemisphere url
    mars_urls = []
    astropedia_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    astropedia_main_url = "https://astrogeology.usgs.gov"

    browser.visit(astropedia_url)

    # make some soup
    mars_hem = browser.html
    bowl_of_soup = bs(mars_hem, 'html.parser')

    # Find the text in soup
    find_text = bowl_of_soup.find_all('div', class_='item')

    # loop to list image urls
    for x in find_text:
        title = x.find("h3").text 
        hem_image_url = x.find('a', class_='itemLink product-item')["href"]  
        browser.visit(astropedia_main_url + hem_image_url) 
        hem_image_html = browser.html   
        mars_soup = bs(hem_image_html,"html.parser")   
        full_url = astropedia_main_url + mars_soup.find("img",class_="wide-image")["src"]
        mars_urls.append({"title":title,"full_url":full_url})

    # package in a dictionary
    mars_stuff = {

        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "scrape_image_url": scrape_image_url,
        "mars_info": mars_info,
        "mars_urls": mars_urls
    }

    browser.quit()

    return mars_stuff