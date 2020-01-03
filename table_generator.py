import pandas as pd

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

# Process item identifier string (brand + name) for unity.
def clean_identifier(col):
    temp = col.str.replace("[^a-zA-Z]", "")
    temp = temp.str.lower()
    temp = temp.str.replace("women", "")
    temp = temp.str.replace("men", "")
    temp = temp.str.replace("createdformacys", "")
    return temp

macys["item"] = clean_identifier(macys["item"])
nm["item"] = clean_identifier(nm["item"])
nordstrom["item"] = clean_identifier(nordstrom["item"])

# Create table of overlapping items
macys_nm = pd.merge(macys, nm, on="item")
macys_nord = pd.merge(macys, nordstrom, on="item")
nm_nord = pd.merge(nm, nordstrom, on="item")

output = pd.merge(pd.merge(macys_nm, macys_nord, on="item", how="outer"), nm_nord, on="item", how="outer")
output.to_csv("output.csv")