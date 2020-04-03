import sys
import requests
import time
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

class bestbuy:

    def __init__(self, url, proxy):
        self.url = url
        self.proxy = proxy

    def checkStock(self):
        s = requests.Session()
        getheaders = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
            'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }

        try:
            r = requests.get(self.url, proxies=self.proxy, timeout=6, headers=getheaders)
            bsObj = BeautifulSoup(r.text, 'html.parser')
            title = bsObj.find("div", {"class": "sku-title"})
            button = bsObj.find("div", {"class": "fulfillment-add-to-cart-button"})

            if title is None or title.text is None:
                return

            if button is None or button.text is None:
                return

            message = title.text + " : " + button.text
            print(time.strftime('%a %H:%M:%S'), message)
            self.sendDiscord(time.strftime('%a %H:%M:%S') + "\n" +  message, 'log')

            if 'Add to Cart' in button.text:
                self.sendDiscord(message, 'online')
        #except requests.exceptions.HTTPError as errh:
            #print ("Http Error:",errh)
        #except requests.exceptions.ConnectionError as errc:
            #print ("Error Connecting:",errc)
        #except requests.exceptions.Timeout as errt:
            #print ("Timeout Error:",errt)
        #except requests.exceptions.RequestException as err:
            #print ("OOps: Something Else",err)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return

    def sendDiscord(self, message, condition):
        if "online" in condition:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695662985510912072/GQnZfJj58Qz52hnb-MjxnFfSA6N9DuiROiZjwJCxc8zuTb-M8T4CjnlrnJqrHzDgV0dy', content=message)
            response = webhook.execute()
        elif "log" in condition:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695682182949240982/RcrE4o2UNz1_8ZyWqz8yHzDKN316zjs41Y6Oiyt7wzOXn77q9HBhX8o2voqlJmQbQBuE', content=message)
            response = webhook.execute()



proxy = {
  "http": "http://108.59.14.203:13010",
  "https": "108.59.14.203:13010",
}

urls = [
    'https://www.bestbuy.com/site/bowflex-selecttech-552-adjustable-dumbbells-black/5845062.p?skuId=5845062',
    'https://www.bestbuy.com/site/bowflex-selecttech-560-adjustable-dumbbells-black/6405085.p?skuId=6405085',
    'https://www.bestbuy.com/site/nordictrack-55-lb-select-a-weight-adjustable-dumbbell-pair-blue-black/6343462.p?skuId=6343462',
    'https://www.bestbuy.com/site/nordictrack-50-lb-adjustable-dumbbell-black/6343458.p?skuId=6343458',
]

items = []
for url in urls:
    item = bestbuy(url, proxy)
    items.append(item)

while True:
    for item in items:
        item.checkStock()

