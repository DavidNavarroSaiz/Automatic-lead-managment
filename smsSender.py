from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()

class SMSSender:
    def __init__(self):
        # Twilio API credentials
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        # Initialize Twilio client
        self.client = Client(account_sid, auth_token)

    def send_sms(self, recipient_number, message):
        message = self.client.messages.create(
            body=message,
            from_=self.twilio_phone_number,
            to=recipient_number
        )
        print("SMS sent successfully. SID:", message.sid)

if __name__ == "__main__":
    # Example usage
    sms_sender = SMSSender()

    # Replace with recipient's phone number
    recipient_number = '+573007751361'
    message = "hello"
    sms_sender.send_sms(recipient_number, message)
