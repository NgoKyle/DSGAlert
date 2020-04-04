# Changes to be made before use:
    #     . Make the necessary changes in the URL.
    #     . Update your "User-Agent" in headers.
    #     . Enable Google Apps passwords for mail, and update it in the code on line 54
    #     . Update your email from which the mail has to be sent.
    #     . Update your email to which you want the mail to be sent.
    #     . Make whatever changes you want to the message.
    #     . Change the frequency at which you want to run the script.
    #     . You are all done! You can run this script now!

#   . If you want to run this script on startup in Windows, make a batch file
#   Learn how to make a batch file from here https://datatofish.com/batch-python-script/
#   Now, open Run, and execute this 'shell:common startup' and paste your batch file in there.

# Library to run the program over time.
import time

# Libraries required for the web-scraping.
import requests
from bs4 import BeautifulSoup

# Get data
data = {}

# You can use any Amazon product's URL.
url = 'https://www.amazon.com/Stack-52-Instructions-Included-Adjustable/dp/B07PMY84H5/ref=sr_1_3?dchild=1&keywords=bowflex+selecttech&qid=1585965871&sr=8-3'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0', 'if-modified-since': 'Fri, 05 Jan 2018 11',
    'if-none-match': '"42f-562062e8ef580-gzip"', 'upgrade-insecure-requests': '1',
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

def checkAvailablity():
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(soup)

        # The data is stored in a div with ID as 'availability'
        availablity = soup.find('div', {'id':'availabilityInsideBuyBox_feature_div'})
        print(availablity)
        """
        availablity = availablity.split('\n')
        if availablity[0] == "In stock.":
            price = soup.find(id='priceblock_ourprice')
            print("price: " + price)
        """


checkAvailablity()
