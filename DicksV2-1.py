import sys
import requests
import time
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

class dicks:

    def __init__(self, url, proxy):
        self.url = url
        self.proxy = proxy
        self.count = 0

    def checkStock(self):
        try:
            r = requests.get(self.url, proxies=self.proxy, timeout=3)
            bsObj = BeautifulSoup(r.text, 'html.parser')
            label = bsObj.find("span", {'class':'ship-mode-message'})
            title = bsObj.find("h1", {'class':'title'})

            message = title.text + " : " + label.text
            print(time.strftime('%a %H:%M:%S'), message, self.count)
            #self.sendDiscord(time.strftime('%a %H:%M:%S') + " " +  message + " " + str(self.count), "log")

            if label is None:
               return

            if 'Ship to Me' in label.text:
                self.count = self.count + 1
                if(self.count == 3):
                    self.sendDiscord(message + "\n" + self.url, "online")
            else:
                self.count = 0
        #except requests.exceptions.HTTPError as errh:
            #print ("Http Error:",errh)
        #except requests.exceptions.ConnectionError as errc:
            #print ("Error Connecting:",errc)
        #except requests.exceptions.Timeout as errt:
            #print ("Timeout Error:",errt)
        #except requests.exceptions.RequestException as err:
            #print ("OOps: Something Else",err)
        except:
            #print("Unexpected error:", sys.exc_info()[0])
            return

    def sendDiscord(self, message, condition):
        if "online" in condition:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695676188621930587/4b3UpCQlbZAU9M0eSgyLzX22VkzfJjnlPamZKjAtFqp6yUkPNcuRLIM69UavkRyQqwG2', content=message)
            response = webhook.execute()
        elif "log" in condition:
            webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/695680553541697578/utZKtsGNvDlbQsh_HAH9bBV09uRoqMf9C8dUn0SVMh-Mq79qG_cCM_kGArtWlkMQPUae', content=message)
            response = webhook.execute()


def main():
    proxy = {
      "http": "http://108.59.14.203:13010",
      "https": "108.59.14.203:13010",
    }

    urls = [
        'https://www.dickssportinggoods.com/p/bowflex-selecttech-552-dumbbells-16bfxuslcttchdmbbslc/16bfxuslcttchdmbbslc',
        'https://www.dickssportinggoods.com/p/powerblock-50-lbadjustable-dumbbell-set-19pwkupwrblcksprtslc/19pwkupwrblcksprtslc'
    ]

    items = []

    for url in urls:
        item = dicks(url, proxy)
        items.append(item)

    while True:
        for item in items:
            item.checkStock()

if __name__ == "__main__":
    main()



