import requests
import time
import json
from bs4 import BeautifulSoup
from mail_to_sms import MailToSMS
from discord_webhook import DiscordWebhook


skus = {
    "16380346": "PowerBlock 50 lb. Adjustable Dumbbell Set",
    "11465449": "Bowflex SelectTech 552 Dumbbells",
    "10836482": "Fitness Gear 25 lb Rubber Hex Dumbbell",
    "10404947": "Fitness Gear 20 lb Cast Hex Dumbbell",
    "10836480": "Fitness Gear 20 lb Rubber Hex Dumbbell",
    "10836482": "Fitness Gear 25 lb Rubber Hex Dumbbell",
    "17683555": "Fitness Gear 65 cm Premium Stability Ball"
}

links = []
skus = []
names = []
proxies = {
  "http": "http://108.59.14.203:13010",
  "https": "108.59.14.203:13010",
}

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
    'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

#get SKUs, Products name from URL
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

#get Zipcode for curbside pickup
with open('zipcode.txt','r') as f:
    zips = f.read().splitlines()

def main():
    while True:
        for i in range(len(links)):
            checkOnlineInventory(names[i], skus[i], links[i])

            for zip in zips:
                checkInstore(zip, names[i], skus[i], links[i])


def checkOnlineInventory(name, sku, link):
    url = 'https://availability.dickssportinggoods.com/v1/inventoryapis/searchinventory?location=0&sku={}'.format(sku)

    try:
        r = requests.get(url, timeout=6, headers=header, proxies=proxies).json()
    except:
        checkOnlineInventory(name, sku, link)
        return

    ats = r['data']['skus'][0]['atsqty']
    message = "Online\nItem: {}\navailable to ship: {}\n{}".format(name, ats, link)
    print("\n",time.strftime('%a %H:%M:%S'), message)

    if(int(ats) > 0):
        sendDiscord(message)

def checkInstore(zip, name, sku, link):
    url = 'https://availability.dickssportinggoods.com/ws/v2/omni/stores?addr={}&radius=100&uom=imperial&lob=dsg&sku={}&res=locatorsearch&qty=1'.format(zip, sku)
    try:
        r = requests.get(url, timeout=5, headers=header, proxies=proxies).json()
    except:
        checkInstore(zip, name, sku, link)
        return

    if 'data' not in r:
        return

    #print("SKU: {} results: {}".format(sku, r['data']['results']))
    if(len(r['data']['results']) == 0):
        return

    result = r['data']['results'][0]
    location = result['store']['zip']
    qty = result['skus'][0]['qty']

    message = "Curbside\nItem: {}\nAvailability: {}\nzipcode: {}\n{}".format(name, str(qty), location, link)
    print("\n", time.strftime('%a %H:%M:%S'), message)
    sendDiscord(message)

def sendDiscord(message):
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695383280794599454/4rJHjEH0l6JYGgVeGvPgKyOJSjlRmPeCGjdEFPHiMnGkolC1Dtetfuiv4PKD6vLzIpj1', content=message)
    response = webhook.execute()

if __name__ == "__main__":
    main()
