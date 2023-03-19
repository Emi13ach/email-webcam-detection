import os
import ssl
import smtplib
from email.message import EmailMessage
import imghdr


def send_email(image_path):
    HOST = "smtp.gmail.com"
    PORT = 465
    USERNAME = "eb.pythoncode@gmail.com"
    PASSWORD = os.getenv("GMAIL_PASSWORD")
    RECEIVER = 'eb.pythoncode@gmail.com'

    email_message = EmailMessage()
    email_message["Subject"] = "Motion detector."
    email_message.set_content("Motion has been detected.")

    with open(image_path, "rb") as image:
        content = image.read()

    email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None, content))

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=HOST, port=PORT, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, RECEIVER, email_message.as_string())


if __name__ == '__main__':
    send_email("images/01.png")
