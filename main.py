from webscrapper import Webscrapper
import requests
import time
import os

class BitcoinNotifier:

    def __init__(self):
        self.API_KEY = 'jz1oAdWOPOvEiK7eW_oAyy1JPmlUcl86KTDA7RESAyV'
        self.BITCOIN_PRICE_THRESHOLD = 10000
        self.IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/' + self.API_KEY
        self.tempThreshold = 0
        self.bitcoin = Webscrapper()

    def clear(self):
        return os.system('cls')
    
    def intro(self):
        self.clear()
        print("Threshold: The value where it will begins taking effect.")
        print("If the current value is below the treshold for more than 30 minutes,")
        print("It will send you a SMS message")
        input("Press enter to continue ...")
        self.clear()
        print("Enter bitcoin price threshold:")
        print(f"Current: {self.BITCOIN_PRICE_THRESHOLD} (Press Enter to keep current value)")
        self.tempThreshold = input("Threshold (Numbers): ")

        if self.tempThreshold.isnumeric():
            self.tempThreshold = int(self.tempThreshold)
            self.BITCOIN_PRICE_THRESHOLD = self.tempThreshold

    def main(self):
        try:
            with open('.config', 'r+') as f:
                self.BITCOIN_PRICE_THRESHOLD = int(f.readline())
                self.intro()
                f.seek(0)
                f.write(f'{self.tempThreshold}')
                f.truncate()           
        except FileNotFoundError:
            with open('.config', 'w') as f:
                self.intro()
                f.write(f'{self.BITCOIN_PRICE_THRESHOLD}')

        bitcoin_history = []
        switch = True


        while True:
            price = self.get_latest_bitcoin_price()   
            self.clear()

            print("Current Price: " + str(price))
            print("Current Threshold: " + str(self.BITCOIN_PRICE_THRESHOLD))
            print("Current bitcoint history below from threshold: " + str(bitcoin_history))
            print("If it's below for more than a minute, you will receive an SMS")
            # Save price if is below threshold into history
            if price < self.BITCOIN_PRICE_THRESHOLD:
                bitcoin_history.append(price)
            else:
                bitcoin_history = []

            if len(bitcoin_history) == 5:
                pass
                # Send a notification of the actual price
                self.post_ifttt_webhook('bitcoin_price_emergency', price)
            # If history still not empty it calculate the avarage
            # of the history to assign new threshold
            elif len(bitcoin_history) >= 10:
                switch = True
                avarage = 0
                for price in bitcoin_history:
                    avarage += price
                avarage = avarage / len(bitcoin_history)
                self.BITCOIN_PRICE_THRESHOLD = avarage * 0.98
                bitcoin_history = []


            if price > 10000 and switch:
                switch = False
                self.BITCOIN_PRICE_THRESHOLD = 10000

            time.sleep(5 * 60)

    def get_latest_bitcoin_price(self):
        return self.bitcoin.getPrice()

    def post_ifttt_webhook(self, event, value):
        # The payload that will be sent to IFTTT service
        data = {'value1': value}
        # Inserts our desired event
        ifttt_event_url = self.IFTTT_WEBHOOKS_URL.format(event)
        # Sends a HTTP POST request to the webhook URL
        requests.post(ifttt_event_url, json=data)


if __name__ == '__main__':
    program = BitcoinNotifier()
    program.main()
