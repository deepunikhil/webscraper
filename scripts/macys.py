from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# HTML class names.
ITEM_CLASS = "cell productThumbnailItem" # li tag
ITEM_NAME_CLASS = "productDescLink" # a tag
PRICE_CLASS = "regular originalOrRegularPriceOnSale" # span tag
DISCOUNT_PRICE_CLASS = "discount" # span tag
COLORS_CLASS = "color swatch" # li tag

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()
df_macys = pd.DataFrame(columns=["item_name", "item_price", "item_color", "item_link"])


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

    for article in soup.find_all("li", class_=ITEM_CLASS):
        try:
            item_name = article.find("a", class_=ITEM_NAME_CLASS).text
            print(item_name)
            if article.find("span", PRICE_CLASS):
                item_price = article.find("span", PRICE_CLASS).text
            if article.find("span", DISCOUNT_PRICE_CLASS):
                item_price = article.find("span", DISCOUNT_PRICE_CLASS).text
            print(item_price)
            item_color = []
            if article.find("ul", class_=COLORS_CLASS):
                for color in article.find_all("li", class_=COLORS_CLASS):
                    item_color.append(color.li.div.title)
            print(item_color)
            item_link = "https://www.macys.com" + article.find("a", class_=ITEM_NAME_CLASS)["href"]
            print(item_link)
            # dataframe = dataframe.append({"item_name": item_name,
            #                               "item_price": item_price,
            #                               "item_color": item_color,
            #                               "item_link": item_link}, ignore_index=True)
        except:
            None
    return dataframe, soup

fetch_page("https://www.macys.com/shop/shoes/all-womens-shoes?id=56233&edge=hybrid", df_macys)


# def fetch_all(mainURL, dataframe):
#     '''
#     Fetch all pages starting from the given https address.
#     Stores into `nordstrom.csv` everytime the page changes.
#     Relevant only to Nordstrom and page must have next button.
#     :param mainURL: starting http address
#     :param dataframe: pandas dataframe for data storage
#     :return: manipulated dataframe
#     '''
#     curURL = mainURL
#     while True:
#         tempURL = curURL
#         dataframe, soup = fetch_page(curURL, dataframe)
#         nav_links = soup.find_all("a", class_=NEXTPAGE_BUTTON_CLASS)
#         for link in nav_links:
#             if link.span.text == "Next":
#                 curURL = mainURL + link["href"]
#                 print("current URL: " + curURL)
#         if curURL == tempURL:
#             break
#     dataframe.to_csv("nordstrom.csv")
#     return dataframe
#
#     driver.quit()
#
# # Execute for all women's shoes on Nordstrom.
# fetch_all(WOMENS_SHOES, df_nordstrom)