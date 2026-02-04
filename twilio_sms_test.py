import os
from twilio.rest import Client

# Load credentials from environment variables
account_sid = "AC7a2f6b425702a24219395198913e7cf7"
auth_token = "73464fc4c4cd3cee7458bdecf0e0b8c6"

print(f"Account SID: '{account_sid}'")
print(f"Auth Token: '{auth_token}'")

client = Client(account_sid, auth_token)

from_number = '+12365067497'  # Your Twilio number, formatted with country code
to_number = '+16047038779'    # Your mobile number, formatted with country code

message = client.messages.create(
    body='Hello from Clawdbot - Twilio SMS test!',
    from_=from_number,
    to=to_number
)

print(f"Message sent with SID: {message.sid}")
