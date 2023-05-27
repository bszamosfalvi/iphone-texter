import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

#twilio stuff
account_sid = "YOUR_TWILIO_SID_HERE"
auth_token = 'YOUR_TWILIO_AUTH_TOKEN_HERE'
client = Client(account_sid, auth_token)



URL = "https://iphonechecker.herokuapp.com/q/10023/i14ProMax/unlocked"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

job_elements = soup.find_all("div", class_="PhonesInStore_store__ESR7V")

relevant_stores = job_elements[:4]

for store in relevant_stores:
    store_name = store.find("h4")
    store_name = store_name.text

    phones = store.find_all("div", class_="ms-TooltipHost root-155")

    for phone in phones:
        string = phone.text
        string[string.find('iPhone'):]

        phone_name = string[:string.find(':')][1:]

        if "TB" in phone_name or "512GB" in phone_name:
            continue
    
        phone_name = string[:string.find(':')][1:]
        availability = string[string.find(':'):][2:]

        if availability == "Available Today" or availability == "Available Tomorrow":
            text = store_name + " " + phone_name + " " + availability
            message = client.messages \
                .create(
                    body= text,
                    from_='YOUR_PHONE_NUMBER_HERE',
                    to='TARGET_PHONE_NUMBER_HERE'
                )
            
