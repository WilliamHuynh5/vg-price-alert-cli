import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import pyshorteners


class PriceAlert():
    def __init__(self):
        self.queryActive = True

    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        url = "https://gamedeals.com.au/search.php?search="
        allProducts = {}
        digitalStores = ['store.playstation.au', 'nintendo.com.au', 'xbox.com.au']
        payloads = get_search_payloads()

        for title in payloads:
            platforms = payloads[title]
            allProducts = query_product(url, title, platforms, digitalStores, allProducts)
            allTimeLows = update_all_time_lows(allProducts)
        get_lowest_product(allTimeLows)

    
def get_search_payloads():
    payloads = {}
    while True:
        try:
            search = input("Enter game: ").lower()
            platformStr = input("Enter platform(s): ").lower()
            platforms = process_platforms_input(platformStr)
            payloads[search] = platforms
            print("     Added: " + search)
            print("     Platf: " + platformStr.replace(" " , " | "))
        except EOFError:
            print("/..EOF../")
            print("Querying...\n")
            break

    return payloads

def process_platforms_input(platformsStr):
    platforms = platformsStr.split(" ")
    if "xbox" in platforms:
        platforms.pop(platforms.index("xbox"))
        platforms.append("xbox-one")
        platforms.append("xbox-series-x")

    return platforms

def update_all_time_lows(allProducts):
    for product in allProducts:
        allProducts[product] = sorted(allProducts[product], key = lambda i: (i['price']))

    return allProducts
        
def query_product(url, searchTerm, platforms, digitalStores, finalDict):


    for platform in platforms:
        allProducts = []
        searchTerm = searchTerm.replace(" ", "+")
        k = requests.get(url + searchTerm + "&platform=" + platform).text
        soup=BeautifulSoup(k,'html.parser')
        productList = soup.find_all("a", {"data": "ga_clickthrough_url"})
        for product in productList:
        
            if product.get("data-store") in digitalStores:
                continue
        
            store = product.get("data-store")
            title = product.getText()
            price = float(product.get("data-curprice"))
            platform = product.get("data-platform")
            prevPrice = product.get("data-prvprice")
            produrl = product.get("href")
            
            prodDict = {"title": title, "platform": platform, "store": store, "price": price, "url": produrl}

            allProducts.append(prodDict)


        key = searchTerm.replace("+", " ") + " | " + platform
        finalDict[key] = allProducts
    return finalDict

def get_lowest_product(allTimeLows):
        for query in allTimeLows:
            lowestPrice = float('inf')
            for product in allTimeLows[query]:
                title = product["title"]
                platf = product["platform"]
                lowestStore = product["store"]
                price = product["price"]
                url = product["url"]

                if price <= lowestPrice:
                    print("###### LOWEST ######")
                    print("Title: " + platf + " | " + title)
                    print("Store: " + lowestStore)
                    print("Price: " + "$" + str(price))
                    print("  URL: " + url)
                    
                    #print("####################")
                    lowestPrice = price

priceAlert = PriceAlert()
priceAlert.run()