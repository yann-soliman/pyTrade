import os

from sendgrid import sendgrid, Email
from sendgrid.helpers.mail import Content, Mail


class EmailAlert:
    def __init__(self):
        self.api_key = "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"

    def send_simple_message(self):
        sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email("test@example.com")
        subject = "Hello World from the SendGrid Python Library!"
        to_email = Email("yann.soliman@gmail.com")
        content = Content("text/plain", "Hello, Email!")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        print(os.environ.get('SENDGRID_API_KEY'))
