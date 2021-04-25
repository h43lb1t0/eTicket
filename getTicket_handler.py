#script by Tom Ole Haelbich, with major help from Andreas Schröder
from logger import log, debug
import requests
import json
import time
import random

class getTicket:

    def __init__(self):
        with open("config.json") as config_file:
            self.config = json.load(config_file)
        self.order_url = self.config["orderUrl"]
        self.event = self.config["event"]
        self.event_no = self.config["eventNo"]
        self.email = self.config["Email"]
        self.ammount = self.config["ammount"]

    def order_ticket(self,no=0):
        session = requests.Session()
        log("Request entry page")
        response = session.get(self.order_url)
        log(f"got response nwith code {response.status_code}")

        data = {
            'email': self.email,
            'lang': 'de',
            'format': '',
            'eventnr': self.event_no,
            'orderid': '',
            'tktlist': '{"0":0}',
            'tkt_status': 'booking',
            'order_price': '0',
            'guestlist': '',
            'message': '',
            'promo_code': '',
            'promo_unit': '',
            'promo_value': '0',
            'task': 'step1',
            'test_code':'',} 

        headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://eveeno.com',
        'Referer': self.order_url,}

        log(f"Posting ticket request no. {no+1}/{self.ammount}")

        response = session.post(
            self.order_url,
            data = data,
            headers=headers
        )

    def main(self):
        log(f"approximate time to order the tickets: {round((self.config['minRan'] * self.ammount)/60)}min - {round((self.config['maxRan'] * self.ammount)/60)}min")
        for no in range(self.ammount):
            self.order_ticket(no)
            sleeptime = random.randrange(self.config["minRan"],self.config["maxRan"])
            if no+1 < self.ammount:
                log(f"sleep for {sleeptime} seconds \n")
                time.sleep(sleeptime)



#ticket = getTicket()
#ticket.main()