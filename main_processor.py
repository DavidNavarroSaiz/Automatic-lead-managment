from fastapi import FastAPI
from gptProcessor import ChatGPTLeadProcessor
from sendEmail import EmailSender
from hubspot import HubSpotClient
from fastapi import HTTPException
import uvicorn
import json
app = FastAPI()
processor = ChatGPTLeadProcessor() 
hubspot_client = HubSpotClient()

with open("email_data.json", "r") as f:
    email_json = f.read()

# Parse JSON string into dictionary

email_data = json.loads(email_json)

# Retrieve email variables
sender_email = email_data["sender_email"]
receiver_email = email_data["receiver_email"]

# Endpoint to receive leads and print them
@app.post("/process_lead")
async def process_lead(lead_data: dict):
    lead_message = lead_data.get("lead")
    if not lead_message:
        raise HTTPException(status_code=422, detail="Lead message not found in payload")
    gpt_answer = processor.process_data(lead_message)
    structured_data = json.loads(gpt_answer)
    print("structured_data",structured_data)
    name = structured_data["Name"]
    phone_number = structured_data["PhoneNumber"]
    email = structured_data["Email"]
    lead_key_information = structured_data["lead_key_information"]
    user_response = structured_data["Response"]
    # Check if contact already exists in HubSpot
    existing_contact = hubspot_client.get_contact_by_name(name)
    if existing_contact:
        user_messages = existing_contact[0]['properties']['user_messages']
        user_id = existing_contact[0]['id']
        lead_key_information,user_response = processor.process_old_leads(lead_message,user_messages)
        # Format user messages as a history
        formatted_user_messages = f" {user_messages}\n message: {lead_message}\n"
        hubspot_client.update_contact(user_id, key_information=lead_key_information, hs_lead_status="IN_PROGRESS", user_messages=formatted_user_messages)

        
    else:
        new_contact_data = {
            "properties": {
                "email": email,
                "firstname": name,
                'phone' : phone_number,
                'key_information':lead_key_information,
                'hs_lead_status':   'NEW',
                 "user_messages": f"previous messages:\nmessage : {lead_message}\n",  # Format lead message as initial user message
            }
        }
        create_response = hubspot_client.create_contact(new_contact_data)
    
    
    # Send email response
    email_sender = EmailSender(sender_email, receiver_email)
    subject = "Automatic Response Lead Email"
    email_sender.send_email(user_response, subject)
    
    return {"message": user_response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)