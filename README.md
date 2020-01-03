# 👚 Webscraper for Price Comparison

Project was motivated by a student project at [Forkaia incubator](https://www.forkaia.com/) building a shopping assistant application for professional women. The algorithm automatizes web scraping process from three online stores: Nordstrom, Macy's and Neiman Marcus, and generates a csv file containing the list of all overlapping items and their prices.

## 🕸️ Webscraping

Python `beatifulsoup4` and `selenium` packages were used for processing HTML files and automatic browsing. Within the `scripts` folder are Python scripts used for the webscraping process. The scripts share three methods: `fetch_url`, `fetch_page`, and `fetch_all`.

1. The `fetch_url` method returns the http address of an item category's first shopping page. The only parameter is the item category represented by pre-defined strings.
2. The `fetch_page` takes in the http address of a single shopping page and a dataframe. The method fills the dataframe with information of listed items such as item name, price and link.
3. The `fetch_all` methods also takes in the https address of a shopping page and a dataframe. The method automatically moves on to next page and calls `fetch_page` method until it reaches the very end.
