import requests
import time
import json
from bs4 import BeautifulSoup
from mail_to_sms import MailToSMS
from discord_webhook import DiscordWebhook


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
    sendDiscord("\n"+time.strftime('%a %H:%M:%S') + " " + message, "log")

    if(int(ats) > 0):
        sendDiscord(message, "online")

def checkInstore(zip, name, sku, link):
    url = 'https://availability.dickssportinggoods.com/ws/v2/omni/stores?addr={}&radius=100&uom=imperial&lob=dsg&sku={}&res=locatorsearch&qty=1'.format(zip, sku)
    try:
        r = requests.get(url, timeout=5, headers=header, proxies=proxies).json()
    except:
        checkInstore(zip, name, sku, link)
        return

    if 'data' not in r:
        return

    if(len(r['data']['results']) == 0):
        return

    result = r['data']['results'][0]
    location = result['store']['zip']
    qty = result['skus'][0]['qty']

    message = "Curbside\nItem: {}\nAvailability: {}\nzipcode: {}\n{}".format(name, str(qty), location, link)
    print("\n", time.strftime('%a %H:%M:%S'), message)
    sendDiscord("\n" + time.strftime('%a %H:%M:%S') +  message, "log")
    if '97236' in zip:
        sendDiscord(message, "pdx")
    elif '94806' in zip:
        sendDiscord(message, "sfo")
    elif '98402' in zip:
        sendDiscord(message, "sea")
    else:
        print("SOMETHING WRONG {}".format(zip))

def sendDiscord(message, condition):
    if "online" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695662753104265286/cZZEdE8oL_02IsWONpLjQ6onU4fsd74GciKMlF5CPLYMixeZTaF86ZT9qNeN9TyA8SqP', content=message)
        response = webhook.execute()
    elif "pdx" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695662589895639070/_SUd1uygVjsYJFS-sUmVtiEsaUckvjNU9x4KzEn_kLcrrjzZZkX1vHJpm42y6hwwnjdu', content=message)
        response = webhook.execute()
    elif "sfo" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695662684410216580/FUmxam-i3lVbVJkoeBlxoFLQwR7hpNPRafJou0nTWBtPKhLj8eJt_5mT_Kz3Ixn5Gk3k', content=message)
        response = webhook.execute()
    elif "sea" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695861616394371124/LsQ5W5clniFWOTYl5FmyHK7rMvoEV0qR9LZnpf2ZKQd8I_jMWgEXfY4o4eRezkKJFye_', content=message)
        response = webhook.execute()
    elif "log" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695470195896221776/t_MGwZ3214BEHF2JboM3TkH8cf3mOSwrePeQSOyH15PN32tBYc2lIS-dpTy79w62xllI', content=message)
        response = webhook.execute()
    elif "low" in condition:
        webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695671741262987364/56Aoni56NQM5g2N6J_VtZh3NqRdyPc2Lv6kzOEwFGOiW7S4MB-eS7m6O9kdc6sqlVUBv', content=message)
        response = webhook.execute()


if __name__ == "__main__":
    main()
