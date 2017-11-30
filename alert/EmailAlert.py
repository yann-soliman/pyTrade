import os

from sendgrid import sendgrid, Email
from sendgrid.helpers.mail import Content, Mail


class EmailAlert:
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')

    def send_message(self, message):
        sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email("zh@mf.com")
        subject = "ALERTE PRIORITÉ BITCOIN"
        to_email = Email("yann.soliman@gmail.com")
        content = Content("text/plain", message)
        mail = Mail(from_email, subject, to_email, content)
        sg.client.mail.send.post(request_body=mail.get())
