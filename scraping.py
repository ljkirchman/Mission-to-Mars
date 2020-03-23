# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

# Set the executable path and initialize the chrome browser in splinter
# executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path="/usr/local/bin/chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser)
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
# Define the function mars_news
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #  Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p


### Featured Images
# Define the function mars_news
def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')


    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    
    except AttributeError:
        return None
   
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Convert html table into a pandas dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)
    
    # Convert dataframe back to an html file
    return df.to_html()

def hemispheres(browser):
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # List to contain image urls
    image_urls = []
    # How many elements are in the page that contain what we want
    links = browser.find_by_css("a.product-item h3")

    # Click the link, find the sample anchor, return the href
    for i in range(len(links)):
        data = {}

        # Index and click
        browser.find_by_css("a.product-item h3")[i].click()

        # Retrieve and append img_url and title
        sample = browser.find_link_by_text('Sample').first
        data['img_url'] = sample['href']
        data['title'] = browser.find_by_css('h2.title').text

        # Append each dictionary data to list
        image_urls.append(data)

        # Goes back and repeats for the loop
        browser.back()

    return image_urls
    
    # Close session
    browser.quit()

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())



