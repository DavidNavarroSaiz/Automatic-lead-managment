from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException
import random
import requests
from requests.exceptions import Timeout


lead_messages = [
    "Hello,\n\nI hope this message finds you well. My name is John Doe, and I'm interested in learning more about your product. You can reach me at dcnavarros@unal.edu.co or call me at +573007751361. Looking forward to hearing from you soon.\n\nBest regards,\nJohn",
    
    "Hi,\n\nMy name is Alice Smith, and I'm reaching out to inquire about your pricing plans. You can contact me at dcnavarros@unal.edu.co or call me at +573007751361. Any information you can provide would be greatly appreciated. Thank you!\n\nBest regards,\nAlice",

    "Hi there,\n\nI'm Bob Johnson, and I've been researching solutions for my business. I believe your product could be a perfect fit. I'm ready to make a purchase and would like to discuss the next steps with you. Please contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nThanks,\nBob",

    "Hello,\n\nI'm Sarah Williams, and I'm interested in learning more about the services you offer. I have a few questions regarding the specifics and would appreciate the opportunity to discuss them further. Could we schedule a call to go over these details? You can reach me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nLooking forward to your response,\nSarah",

    "Hi,\n\nI came across your company online and wanted to express my interest in learning more about what you offer. My name is Michael Brown, and your solutions seem aligned with the goals of my project. I'm eager to explore how we might collaborate. Please let me know the best way to connect and discuss further. You can contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nMichael",
    
    "Hi,\n\nI'm Emily Rodriguez, and I came across your company while researching potential solutions for my project. Your product caught my attention, and I'm eager to learn more about it. Please reach out to me at dcnavarros@unal.edu.co or call me at +573007751361 to discuss further.\n\nBest regards,\nEmily",

    "Hello,\n\nMy name is Daniel Garcia, and I'm interested in exploring how your services could benefit my business. I'd appreciate the opportunity to connect and discuss potential collaboration opportunities. Feel free to contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nThanks,\nDaniel",

    "Hi there,\n\nI'm Olivia Martinez, and I'm reaching out to inquire about your offerings. Your company seems to align with the goals of my project, and I'm excited to explore how we might work together. Please get in touch with me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nOlivia",

    "Hello,\n\nI'm Javier Hernandez, and I'm currently evaluating different solutions for my business needs. Your product has caught my interest, and I'd like to learn more about its features and pricing. Please contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nLooking forward to hearing from you,\nJavier",

    "Hi,\n\nI'm Maria Sanchez, and I'm excited to explore potential collaboration opportunities with your company. Your services seem to align perfectly with the objectives of my project. I'd appreciate the chance to discuss further. Feel free to reach me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nMaria"
]


# Define a Pydantic model for Lead

app = FastAPI()

urlSendLead = "http://localhost:8000/process_lead"
# Endpoint to generate leads

@app.get("/generate_lead")
async def generate_lead():
    if lead_messages:
        random_lead = random.choice(lead_messages)
        lead_data = {"lead": random_lead}
        try:
            response = requests.post(urlSendLead, json=lead_data, timeout=15)  # Timeout set to 5 seconds
            response.raise_for_status()
            return {"message": "Lead generated and sent successfully"}
        except Timeout:
            raise HTTPException(status_code=500, detail="Request timed out")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send lead: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="No leads available")
