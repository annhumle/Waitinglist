import requests
from bs4 import BeautifulSoup 
import schedule
import time
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
last_send_time = []

def is_open():
    page = requests.get("https://findbolig.nu/da-dk/udlejere")
    if not page.status_code == 200:
        if check_if_sms(3600):
            send_sms(["4542436150"], "Shit, vi er blokeret!")
            last_send_time.append(datetime.now()) 
        
        return

    soup = BeautifulSoup(page.content, "html.parser")
    tds = soup.find_all("td")[2:]
    status = tds[1::2]
    for s in status:
        if not "Lukket" in s:
            return True
    return True

def job():
    if is_open():
        logging.info("List is open")
        if check_if_sms(120):
            send_sms(["4542436150", "4531450399", "4552115035", "4531446415"], "Ventelisten er åben")
            last_send_time.append(datetime.now()) 
    else:
        logging.info("list is closed")

def check_if_sms(delay):
    return not len(last_send_time) or (datetime.now() - last_send_time[-1]).seconds > delay
    
def send_sms(recipients, message):
    token="sbQJTYgFQue-5pNajzisBWwQdStSacAjsvuOK5I1twSTVkAGkCGInaDGlL5tEWq6"
    
    payload = {
        "sender": "Ventelisten",
        "message": message,
        "recipients": [
            {"msisdn": recipient_number}
            for recipient_number in recipients
        ],
    }

    resp = requests.post(
     "https://gatewayapi.com/rest/mtsms",
     json=payload,
     auth=(token, ""),
    )
    resp.raise_for_status

def main():
    schedule.every(300).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
