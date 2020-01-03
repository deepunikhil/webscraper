import pandas as pd
from scripts import macys as mc, neiman_marcus as nm, nordstrom as ns

# Compares price for given category. Generate output.csv.
def compare_price(CATEGORY):
    '''
    Generate output.csv file comparing item price for the given category
    :param CATEGORY: Item category in string format
    :return: None
    '''
    generate_data(CATEGORY)
    generate_joined_output()
    return


def generate_data(CATEGORY):
    '''
    Generates csv files in data folder depending on category selected.
    :param CATEGORY: Item category in string format
    :return: None
    '''
    if CATEGORY not in ["women's shoes", "women's clothing", "men's shoes", "men's clothing", "handbags"]:
        print("CATEGORY must be one of the following: women's shoes, women's clothing, men's shoes, men's clothing, handbags")
        return
    mc.fetch_page(mc.fetch_url(CATEGORY), pd.DataFrame(columns=["item_brand", "item_name", "item_price", "item_link"]))
    nm.fetch_page(nm.fetch_url(CATEGORY), pd.DataFrame(columns=["item_brand", "item_name", "item_price", "item_link"]))
    ns.fetch_page(ns.fetch_url(CATEGORY), pd.DataFrame(columns=["item_name", "item_price", "item_link"]))
    return


def clean_identifier(col):
    '''
    Process item identifier string (brand + name) for unity.
    '''
    temp = col.str.replace("[^a-zA-Z]", "")
    temp = temp.str.lower()
    temp = temp.str.replace("women", "")
    temp = temp.str.replace("men", "")
    temp = temp.str.replace("createdformacys", "")
    return temp


def generate_joined_output():
    '''
    Generates joined csv file based on csv files in data folder
    :return: None
    '''
    # Read generated csv files.
    macys = pd.read_csv("data/macys.csv")
    nm = pd.read_csv("data/neiman_marcus.csv")
    nordstrom = pd.read_csv("data/nordstrom.csv")

    # Combine item brand and item name. Rename columns.
    macys["item"] = macys["item_brand"] + " " + macys["item_name"]
    macys = macys[["item", "item_price", "item_link"]]
    macys.columns = ["item", "macys_price", "macys_link"]

    nm["item"] = nm["item_brand"] + " " + nm["item_name"]
    nm = nm[["item", "item_price", "item_link"]]
    nm.columns = ["item", "nm_price", "nm_link"]

    nordstrom = nordstrom[["item_name", "item_price", "item_link"]]
    nordstrom.columns = ["item", "nordstrom_price", "nordstrom_link"]

    macys["item"] = clean_identifier(macys["item"])
    nm["item"] = clean_identifier(nm["item"])
    nordstrom["item"] = clean_identifier(nordstrom["item"])

    # Create table of overlapping items
    macys_nm = pd.merge(macys, nm, on="item")
    macys_nord = pd.merge(macys, nordstrom, on="item")
    nm_nord = pd.merge(nm, nordstrom, on="item")

    output = pd.merge(pd.merge(macys_nm, macys_nord, on="item", how="outer"), nm_nord, on="item", how="outer")
    output.to_csv("output.csv")
    return