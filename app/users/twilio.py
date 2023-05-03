import os
from twilio.rest import Client
# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACf72ad4611cfecee26bd5a1c9a5b699f5"
auth_token = "a4069f4b74baca268bc0d4bc24a04838"
client = Client(account_sid, auth_token)


def send_message(message,phone):
    
    message = client.messages.create(
    body=f"REZA SAFARKHANI / code is :  {message}",
    from_="+447380316598",
    to=str(phone)
    )
    print(message.sid)