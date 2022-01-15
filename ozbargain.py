import requests
from bs4 import BeautifulSoup, SoupStrainer
import pyshorteners

url = "https://www.ozbargain.com.au/search/node/hard%20drive"
k = requests.get(url).text
soup=BeautifulSoup(k,'html.parser')
productList = soup.find_all("dt", {"class": "title"})

for product in productList:
    for tag in product:
        for x in tag:
            if "expired" not in str(x):
                print(x)
            

