import os
import requests


class EmailAlert:
    def __init__(self):
        self.domain = os.environ.get('MAILGUN_DOMAIN')
        self.api_key = os.environ.get('MAILGUN_API_KEY')

    def send_simple_message(self):
        return requests.post(
            "https://api.mailgun.net/v3/" + self.domain + "/messages",
            auth=("api", self.api_key),
            data={"from": "Excited User <mailgun@" + self.domain + ">",
                  "to": ["yann.soliman@gmail.com", "yann.soliman@gmail.com"],
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomness!"})
