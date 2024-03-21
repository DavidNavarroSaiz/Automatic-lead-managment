import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class EmailSender:
    def __init__(self, sender_email, receiver_email):
        """
        Initializes the EmailSender with sender and receiver email addresses.

        Args:
            sender_email (str): The sender's email address.
            receiver_email (str): The recipient's email address.
        """
        self.receiver_email = receiver_email
        self.sender_email = sender_email
        self.password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, message, subject):
        """
        Sends an email using SMTP.

        Args:
            message (str): The email message content.
            subject (str): The email subject.

        Returns:
            None
        """
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject

        # Attach message to email
        msg.attach(MIMEText(message, 'plain'))

        # Connect to SMTP server (Gmail)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())

if __name__ == "__main__":
    # Example usage
    sender_email = "example@gmail.com"
    receiver_email = "recipient@example.com"
    email_subject = "Test Subject"
    email_message = "Hello, this is a test email."

    email_sender = EmailSender(sender_email, receiver_email)
    email_sender.send_email(email_message, email_subject)
