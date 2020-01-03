import pandas as pd

macys = pd.read_csv("data/macys.csv")
nm = pd.read_csv("data/neiman_marcus.csv")
nordstrom = pd.read_csv("data/nordstrom.csv")

macys["item"] = macys["item_brand"] + " " + macys["item_name"]
nm["item"] = nm["item_brand"] + " " + nm["item_name"]