from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# HTML class names.
PRODUCT_CLASS = "product-thumbnail grid-33 tablet-grid-33 mobile-grid-50 grid-1600" #div tag
PRODUCT_LINK_CLASS = "product-thumbnail__link" # a tag, append neimanmarcus.com to front
PRODUCT_NAME_CLASS = "name" # span tag
PRODUCT_PRICE_CLASS = "product-thumbnail__sale-price" # div tag
PRODUCT_BRAND_CLASS = "designer" # span tag
NEXT_PAGE_CLASS = "arrow-button--right" # a tag, link in href attribute

# First pages.
WOMENS_SHOES = "https://www.neimanmarcus.com/c/shoes-all-designer-shoes-cat47190746?navpath=cat000000_cat000141_cat47190746&source=leftNav"

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()
df_neiman = pd.DataFrame(columns=["item_brand", "item_name", "item_price", "item_link"])


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

    for article in soup.find_all("div", class_=PRODUCT_CLASS):
        try:
            item_brand = article.find("span", class_=PRODUCT_BRAND_CLASS).text
            print(item_brand)
            item_name = article.find("span", class_=PRODUCT_NAME_CLASS).text
            print(item_name)
            price_tag = article.find("div", PRODUCT_PRICE_CLASS)
            if price_tag.find("span", class_="price"):
                for price in price_tag.find_all("span", class_="price"):
                    item_price = price.text
            else:
                item_price = price_tag.span.text
            print(item_price)
            item_link = "https://www.neimanmarcus.com" + article.find("a", class_=PRODUCT_LINK_CLASS)["href"]
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
        if soup.find("a", class_=NEXT_PAGE_CLASS):
            link = soup.find("a", class_=NEXT_PAGE_CLASS)
            curURL = "https://www.neimanmarcus.com" + link["href"]
            print("current URL: " + curURL)
        if curURL == tempURL:
            break
    dataframe.to_csv("../data/neiman_marcus.csv")
    return dataframe

    driver.quit()

# Execute for all women's shoes on Neiman Marcus.
# fetch_all(WOMENS_SHOES, df_neiman)