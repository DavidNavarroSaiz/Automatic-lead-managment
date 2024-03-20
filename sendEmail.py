import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()
class EmailSender():
    def __init__(self,sender_email,receiver_email):
        self.receiver_email = receiver_email
        self.sender_email = sender_email
        self.password = os.getenv("EMAIL_PASSWORD")
# Function to send email
    def send_email(self, message,subject):

        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] =  self.receiver_email
        msg['Subject'] = subject

        # Attach message to email
        msg.attach(MIMEText(message, 'plain'))

        # Connect to SMTP server (Gmail)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            
if __name__ == "__main__":
    # Replace with your email credentials
    sender_email = "dcnavarros97@gmail.com"
    receiver_email = "dcnavarros@unal.edu.co"

    # Initialize EmailSender object
    email_sender = EmailSender(receiver_email, sender_email)

    # Test sending email
    message = "This is a test email sent from Python."
    subject = "Test Email"
    email_sender.send_email(message, subject)

    print("Email sent successfully.")