from fastapi import FastAPI
from pydantic import BaseModel
from gptProcessor import ChatGPTLeadProcessor
from sendEmail import EmailSender
from fastapi import HTTPException
import json
app = FastAPI()
processor = ChatGPTLeadProcessor() 
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
    
    print(f"Received Lead: {lead_message}")
    response = processor.process_data(lead_message)
    # Parse the JSON string into a dictionary
    response_dict = json.loads(response)
    # Access the properties of the dictionary
    print("name: ", response_dict["Name"])
    print("PhoneNumber: ", response_dict["PhoneNumber"])
    print("Email: ", response_dict["Email"])
    print("lead_key_information: ", response_dict["lead_key_information"])
    print("Response: ", response_dict["Response"])


    email_sender = EmailSender(sender_email, receiver_email)
    subject = "Automatic Response Lead Email"
    email_sender.send_email(response_dict["Response"], subject)
    
    return {"message": response_dict}
