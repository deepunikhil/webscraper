from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# HTML class names.
ITEM_CLASS = "cell productThumbnailItem" # li tag
ITEM_NAME_CLASS = "productDescLink" # a tag
ITEM_BRAND_CLASS = "productBrand" # div tag
PRICE_CLASS = "regular" # span tag
DISCOUNT_PRICE_CLASS = "discount" # span tag
NEXTPAGE_BUTTON_CLASS = "next-page" #li tag

# First pages.
WOMENS_SHOES = "https://www.macys.com/shop/shoes/all-womens-shoes?id=56233"
WOMENS_CLOTHING = "https://www.macys.com/shop/womens-clothing/all-womens-clothing?id=188851&cm_sp=us_hdr-_-women-_-188851_all-women%27s-clothing_COL1"
MENS_SHOES = "https://www.macys.com/shop/mens-clothing/shop-all-mens-footwear?id=55822&edge=hybrid"
MENS_CLOTHING = "https://www.macys.com/shop/mens-clothing/all-mens-clothing?id=197651&cm_sp=us_hdr-_-men-_-197651_all-men%27s-clothing_COL1"
HANDBAGS = "https://www.macys.com/shop/handbags-accessories/all-handbags?id=27686&edge=hybrid"

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()


def fetch_url(CATEGORY):
    if CATEGORY == "women's shoes":
        return WOMENS_SHOES
    elif CATEGORY == "women's clothing":
        return WOMENS_CLOTHING
    elif CATEGORY == "men's shoes":
        return MENS_SHOES
    elif CATEGORY == "men's clothing":
        return MENS_CLOTHING
    elif CATEGORY == "handbags":
        return HANDBAGS


def fetch_page(pageURL, dataframe):
    '''
    Fetches data from a single html page.
    Relevant only to Macy's.
    :param pageURL: http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe and a BeatifulSoup object of corresponding page
    '''
    driver.delete_all_cookies()
    driver.get(pageURL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for article in soup.find_all("li", class_=ITEM_CLASS):
        try:
            item_brand = article.find("div", class_=ITEM_BRAND_CLASS).text.lstrip().rstrip()
            print(item_brand)
            item_name = article.find("a", class_=ITEM_NAME_CLASS)["title"][1:]
            print(item_name)
            item_price = None
            if article.find("span", PRICE_CLASS):
                item_price = article.find("span", PRICE_CLASS).text
            if article.find("span", DISCOUNT_PRICE_CLASS):
                item_price = article.find("span", DISCOUNT_PRICE_CLASS).text
            item_price = item_price.\
                    replace(" ", "").replace("\t", "").replace("\n", "").replace("Sale", "").replace("Now", "")
            print(item_price)
            item_link = "https://www.macys.com" + article.find("a", class_=ITEM_NAME_CLASS)["href"]
            print(item_link)
            dataframe = dataframe.append({"item_brand": item_brand,
                                          "item_name": item_name,
                                          "item_price": item_price,
                                          "item_link": item_link}, ignore_index=True)
        except:
            None
    return dataframe, soup


def fetch_all(mainURL, dataframe):
    '''
    Fetch all pages starting from the given https address.
    Stores into `../data/macys.csv` everytime the page changes.
    Relevant only to Macy's and page must have next button.
    :param mainURL: starting http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe
    '''
    curURL = mainURL
    while True:
        tempURL = curURL
        dataframe, soup = fetch_page(curURL, dataframe)
        if soup.find("li", class_=NEXTPAGE_BUTTON_CLASS):
            link = soup.find("li", class_=NEXTPAGE_BUTTON_CLASS)
            curURL = "https://www.macys.com" + link.div.a["href"]
            print("current URL: " + curURL)
        if curURL == tempURL:
            break
    dataframe.to_csv("../data/macys.csv")
    return dataframe

    driver.quit()