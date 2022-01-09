import requests
from bs4 import BeautifulSoup, SoupStrainer
import pyshorteners
from pushbullet import Pushbullet
import os
import json
import datetime
import select


pb = Pushbullet("o.URzMl8FYm2etEpKKGkA3UNzXKGKnm7Cw")


class PriceAlert():
    def __init__(self):
        self.queryActive = True

    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        url = "https://gamedeals.com.au/search.php?search="
        allProducts = {}
        exclusions = ['store.playstation.au',  'xbox.com.au', 'mightyape.com.au']
        
        try:
            with open('payloads.json') as json_file:
                payloads = json.load(json_file)
            print("Existing payloads found")
        except:
            payloads = {}
            print("Existing payloads not found")
        
        input("\nPress [ENTER] to continue: ")

        while True:
            clear_terminal()
            print("[0] Initiate automatic scrape")
            print("[1] Add games to scrape list")
            print("[2] Remove a game from scrape list")
            print("[3] View games on scrape list")
            print("[4] Write payloads to JSON")
            print("[5] Read JSON file into payloads")
            print("[6] Run a manual scrape")
            print("[Q] Quit")

            selection = input("\nEnter selection: ")

            if selection == "0":
                automatatic_scrape(payloads, url, exclusions, allProducts)
            elif selection == "1": # Add games
                payloads = get_search_payloads(payloads)
            elif selection == "2": # Remove games
                remove_selected_payload(payloads)
            elif selection == "3": # View games
                view_current_payloads(payloads)
            elif selection == "4": # Write to JSON
                write_payloads_to_json(payloads)
            elif selection == "5": # Read from JSON
                payloads = read_json_into_payloads()
            elif selection == "6": # Read from JSON
                scrape(payloads, url, exclusions, allProducts)
                input("\nPress [ENTER] to continue: ") 
            elif selection == "Q" or selection == 'q': # Quit
                exit(0)
            else:
                print("Invalid selection.")
                exit(0)
        





    
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def automatatic_scrape(payloads, url, exclusions, allProducts):
    clear_terminal()
    # Creates a backup before scrape
    write_payloads_to_json(payloads)

    print("Initiating scraping...")
    times = ['00:00:00', '06:00:00', '09:00:00', '12:00:00']
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if current_time in times:
            scrape(payloads, url, exclusions, allProducts)

def scrape(payloads, url, exclusions, allProducts):
    clear_terminal()
    print("Timestamp: " + datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y"))
    print("Querying payloads...")
    print("This will take some time...\n")
    for title in payloads:
        platforms = payloads[title]
        allProducts = query_product(url, title, platforms, exclusions, allProducts)
        allTimeLows = update_all_time_lows(allProducts)
    get_lowest_product(allTimeLows)

    

def read_json_into_payloads():
    clear_terminal()
    fileName = input("Enter JSON file to read from: ")
    try:
        with open(fileName) as json_file:
            data = json.load(json_file)
    except:
        print("Failed to load!")
        input("\nPress [ENTER] to continue: ")
        return
    
    print("Successfully loaded!")
    input("\nPress [ENTER] to continue: ")
    return data

def write_payloads_to_json(payloads):
    clear_terminal()
    try:
        with open('payloads.json', 'w') as fp:
            json.dump(payloads, fp)
        print("Payloads written!")
    except:
        print("Failed to write!")

    input("\nPress [ENTER] to continue: ")

def remove_selected_payload(payloads):
    clear_terminal()
    print("Current Payloads: \n")
    i = 0
    for game in payloads:
        print("[" + str(i) + "] " + game + " -> " + str(payloads[game]))
        i+=1
    print("[Q] Quit" )
    entry = input("\nSelect an entry to remove: ")

    if entry == 'q' or entry == "Q":
        return

    payloads_keys = list(payloads)
    

    try:
        key_to_remove = payloads_keys[int(entry)]
        payloads.pop(key_to_remove)
        print("\n" + key_to_remove + " has been removed.")
    except:
        print("Failed to remove!")

    input("\nPress [ENTER] to continue: ")
    return payloads    

def view_current_payloads(payloads):
    clear_terminal()
    print("Current Payloads: \n")
    for game in payloads:
        print(game + " -> " + str(payloads[game]))

    input("\nPress [ENTER] to continue: ")
    return


def get_search_payloads(payloads):
    clear_terminal()
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

    with open('all-time-lows.json', 'w') as fp:
        json.dump(allProducts, fp)
    return allProducts
        
def query_product(url, searchTerm, platforms, exclusions, finalDict):

    for platform in platforms:
        allProducts = []
        searchTerm = searchTerm.replace(" ", "+")
        k = requests.get(url + searchTerm + "&platform=" + platform).text
        soup=BeautifulSoup(k,'html.parser')
        productList = soup.find_all("a", {"data": "ga_clickthrough_url"})
        for product in productList:
        
            if product.get("data-store") in exclusions:
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

        smsPayload = ""
        for query in allTimeLows:
            lowestPrice = float('inf')
            for product in allTimeLows[query]:
                title = product["title"]
                platf = product["platform"]
                lowestStore = product["store"]
                price = product["price"]
                url = product["url"]

                if price <= lowestPrice:

                    smsPayload = smsPayload + "Title: " + platf + " | " + title + "\n" + "Store: " + lowestStore + "\n" + "Price: " + "$" + str(price) + "\n" + "  URL: " + url + "\n\n"

                    print("###### LOWEST ######")
                    print("Title: " + platf + " | " + title)
                    print("Store: " + lowestStore)
                    print("Price: " + "$" + str(price))
                    print("  URL: " + url)
                    


                    #print("####################")
                    lowestPrice = price
        device = pb.devices[0]
        # Uncomment this to send to phone
        # push = pb.push_sms(device, "+61405991322", smsPayload) 

priceAlert = PriceAlert()
priceAlert.run()