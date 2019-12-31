from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tqdm import tqdm

# HTML class names.
ITEM_CLASS = "_1AOd3 QIjwE" # article tag
ITEM_DESCRIPTION_CLASS = "YbtDD _18N5Q" # div tag
ITEM_PRICE_CLASS = "_3wu-9" # span tag
ITEM_COLOR_CLASS = "_2jA_i _3moH9" # div tag
NEXTPAGE_BUTTON_CLASS = "_2WIqd" # a tag

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()
df_nordstrom = pd.DataFrame(columns=["item_name", "item_price", "item_color", "item_link"])


def fetch_page(pageURL, dataframe):
    '''
    Fetches data from a single html page.
    Relevant only to Nordstrom.
    :param pageURL: http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe and a BeatifulSoup object of corresponding page
    '''
    driver.get(pageURL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for article in soup.find_all("article", class_=ITEM_CLASS):
        try:
            item_name = article.h3.a.text
            item_price = article.find("div", class_=ITEM_DESCRIPTION_CLASS) \
                    .find("span", class_=ITEM_PRICE_CLASS).text
            item_color = []
            if article.find("div", class_=ITEM_COLOR_CLASS):
                for color in article.find("div", class_=ITEM_COLOR_CLASS).div.ul.find_all("li"):
                    item_color.append(color.button.span.text)
            item_link = "https://shop.nordstrom.com" + article.h3.a["href"]
            dataframe = dataframe.append({"item_name": item_name,
                                          "item_price": item_price,
                                          "item_color": item_color,
                                          "item_link": item_link}, ignore_index=True)
        except:
            print("fetch failed.")
    return dataframe, soup


def fetch_all(mainURL, dataframe):
    '''
    Fetch all pages starting from the given https address.
    Stores into `nordstrom.csv` everytime the page changes.
    Relevant only to Nordstrom and page must have next button.
    :param mainURL: starting http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe
    '''
    curURL = mainURL
    next_link = True
    pbar = tqdm(total=1200)
    while next_link:
        dataframe, soup = fetch_page(curURL, dataframe)
        next_link = soup.find("a", class_="_2WIqd")["href"]
        curURL = "https://shop.nordstrom.com/c/all-women" + next_link
        dataframe.to_csv("nordstrom.csv")
        pbar.update(1)
    pbar.close()
    return dataframe

    driver.quit()

# Parent page for women's items.
URL = "https://shop.nordstrom.com/c/all-women?breadcrumb=Home%2FWomen%2FAll%20Women" # first page URL

# Execute for all women's wear on Nordstrom.
fetch_all(URL, df_nordstrom)