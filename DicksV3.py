import config
import requests
import time

#get SKUs, Products name from URL
links = []
skus = []
names = []
with open('links.txt','r') as f:
    for line in f:
        link = line.strip()
        links.append(link)

        r = requests.get(link)
        bsObj = BeautifulSoup(r.text, 'html.parser')

        name = bsObj.find("h1", {'itemprop':'name'}).text
        names.append(name)

        sku = bsObj.find("ul", {"class":"product-numbers"}).findAll("li")[1].find("span").text
        skus.append(sku)

def main():
    while True:
        for i in range(len(links)):
            checkOnlineInventory(names[i], skus[i], links[i])

            for zip in zips:
                checkInstore(zip, names[i], skus[i], links[i])


def checkOnlineInventory(name, sku, link):
    url = 'https://availability.dickssportinggoods.com/v1/inventoryapis/searchinventory?location=0&sku={}'.format(sku)

    try:
        r = requests.get(url, timeout=6, headers=config.header, proxies=config.proxy).json()
    except:
        checkOnlineInventory(name, sku, link)
        return

    ats = r['data']['skus'][0]['atsqty']
    message = "Online\nItem: {}\navailable to ship: {}\n{}".format(name, ats, link)
    print("\n",time.strftime('%a %H:%M:%S'), message)

    if(int(ats) > 0):
        checkStock(link)

def checkStock(link):
    try:
        r = requests.get(link, proxies=config.proxy, timeout=6, headers=config.header)
        bsObj = BeautifulSoup(r.text, 'html.parser')
        title = bsObj.find("div", {"class": "sku-title"})
        button = bsObj.find("div", {"class": "fulfillment-add-to-cart-button"})

        if title is None or title.text is None:
            return

        if button is None or button.text is None:
            return

        message = title.text + " : " + button.text
        print(time.strftime('%a %H:%M:%S'), message)

        #if 'Add to Cart' in button.text:
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return

if __name__ == "__main__":
    main()
