from fastapi import FastAPI, HTTPException
from src.gptProcessor import ChatGPTLeadProcessor
from src.sendEmail import EmailSender
from src.hubspot import HubSpotClient
from src.smsSender import SMSSender
import uvicorn
import json

# Load email configuration from JSON file
with open("./src/send_data.json", "r") as f:
    email_json = f.read()

# Parse JSON string into dictionary
email_data = json.loads(email_json)

# Retrieve email variables
sender_email = email_data["sender_email"]
receiver_email = email_data["receiver_email"]
recipient_number = email_data["recipient_number"]

# Initialize FastAPI app
app = FastAPI()

# Initialize processors and senders
processor = ChatGPTLeadProcessor()
hubspot_client = HubSpotClient()
email_sender = EmailSender(sender_email, receiver_email)
sms_sender = SMSSender()

# Endpoint to receive leads and process them
@app.post("/process_lead")
async def process_lead(lead_data: dict):
    """
    Endpoint to receive leads, process them, and send responses via email and SMS.

    Args:
        lead_data (dict): A dictionary containing the lead message.

    Returns:
        dict: A dictionary containing the response message.
    """
    
    try:
        # Extract lead message from payload
        lead_message = lead_data.get("lead")
        if not lead_message:
            raise HTTPException(status_code=422, detail="Lead message not found in payload")

        # Process lead message with GPT processor
        gpt_answer = processor.process_data(lead_message)
        structured_data = json.loads(gpt_answer)

        # Extract relevant information from processed lead data
        name = structured_data["Name"]
        phone_number = structured_data["PhoneNumber"]
        email = structured_data["Email"]
        lead_key_information = structured_data["lead_key_information"]
        user_response = structured_data["Response"]

        # Check if contact already exists in HubSpot
        existing_contact = hubspot_client.get_contact_by_email(email)
        if existing_contact:
            user_messages = existing_contact[0]['properties']['user_messages']
            user_id = existing_contact[0]['id']
            # Process old leads and update contact
            lead_key_information, user_response = processor.process_old_leads(lead_message, user_messages)
            # Format user messages as a history
            formatted_user_messages = f"{user_messages}\n message: {lead_message}\n"
            hubspot_client.update_contact(user_id, key_information=lead_key_information, hs_lead_status="IN_PROGRESS", user_messages=formatted_user_messages)
            message = f"The lead of {email} was correctly updated"

        else:
            # Create new contact in HubSpot
            new_contact_data = {
                "properties": {
                    "email": email,
                    "firstname": name,
                    'phone': phone_number,
                    'key_information': lead_key_information,
                    'hs_lead_status': 'NEW',
                    "user_messages": f"previous messages:\nmessage : {lead_message}\n",  # Format lead message as initial user message
                }
            }
            _ = hubspot_client.create_contact(new_contact_data)
            message = f"The lead of {email} was correctly created"
        # Send SMS response
        sms_sender.send_sms(recipient_number, user_response)

        # Send email response
        subject = f"Response for Lead: {name}"
        email_sender.send_email(user_response, subject)
        print("message",message)
        return {"message": message}
    except Exception as e:
        # Handle exceptions
        message = "An error occurred: " + str(e)
        return {"message": message}

# Run FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
