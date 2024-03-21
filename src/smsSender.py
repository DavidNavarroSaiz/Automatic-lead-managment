from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class SMSSender:
    def __init__(self):
        """
        Initializes the SMSSender with Twilio API credentials.
        """
        # Retrieve Twilio API credentials from environment variables
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

        # Initialize Twilio client
        self.client = Client(account_sid, auth_token)

    def send_sms(self, recipient_number, message):
        """
        Sends an SMS message using Twilio.

        Args:
            recipient_number (str): The phone number of the message recipient.
            message (str): The message content.

        Returns:
            str: The Twilio message SID if the message is sent successfully.
        """
        # Send the SMS message
        message = self.client.messages.create(
            body=message,
            from_=self.twilio_phone_number,
            to=recipient_number
        )
        # Print success message with the message SID
        return message.sid

if __name__ == "__main__":
    # Example usage
    sms_sender = SMSSender()

    # Example recipient phone number and message
    recipient_number = '+573007751361'
    message = "Hello, this is a test message."

    # Send the SMS
    sms_sender.send_sms(recipient_number, message)
