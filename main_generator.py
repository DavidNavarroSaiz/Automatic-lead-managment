from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException
import random
import requests
from requests.exceptions import Timeout
from hubspot import HubSpotClient

hubspot_client = HubSpotClient()

contact_info = {
    "John Doe": {"email": "john.doe@example.com", "telephone": "+1234567890"},
    "Alice Smith": {"email": "alice.smith@example.com", "telephone": "+1987654321"},
    "Bob Johnson": {"email": "bob.johnson@example.com", "telephone": "+1122334455"},
    "Sarah Williams": {"email": "sarah.williams@example.com", "telephone": "+1555666777"},
    "Michael Brown": {"email": "michael.brown@example.com", "telephone": "+1444333222"},
    "Emily Rodriguez": {"email": "emily.rodriguez@example.com", "telephone": "+1999888777"},
    "Daniel Garcia": {"email": "daniel.garcia@example.com", "telephone": "+1888777666"},
    "Olivia Martinez": {"email": "olivia.martinez@example.com", "telephone": "+1666777888"},
    "Javier Hernandez": {"email": "javier.hernandez@example.com", "telephone": "+1223344556"},
    "Maria Sanchez": {"email": "maria.sanchez@example.com", "telephone": "+1444555666"},
}
lead_messages = [
    "Hello,\n\nI hope this message finds you well. My name is {name}, and I'm interested in learning more about your product. You can reach me at {email} or call me at {telephone}. Looking forward to hearing from you soon.\n\nBest regards,\n{name}",
    "Hi,\n\nMy name is {name}, and I'm reaching out to inquire about your pricing plans. You can contact me at {email} or call me at {telephone}. Any information you can provide would be greatly appreciated. Thank you!\n\nBest regards,\n{name}",
    "Hi there,\n\nI'm {name}, and I've been researching solutions for my business. I believe your product could be a perfect fit. I'm ready to make a purchase and would like to discuss the next steps with you. Please contact me at {email} or call me at {telephone}.\n\nThanks,\n{name}",
    "Hello,\n\nI'm {name}, and I'm interested in learning more about the services you offer. I have a few questions regarding the specifics and would appreciate the opportunity to discuss them further. Could we schedule a call to go over these details? You can reach me at {email} or call me at {telephone}.\n\nLooking forward to your response,\n{name}",
    "Hi,\n\nI came across your company online and wanted to express my interest in learning more about what you offer. My name is {name}, and your solutions seem aligned with the goals of my project. I'm eager to explore how we might collaborate. Please let me know the best way to connect and discuss further. You can contact me at {email} or call me at {telephone}.\n\nBest regards,\n{name}",
    "Hi,\n\nI'm {name}, and I came across your company while researching potential solutions for my project. Your product caught my attention, and I'm eager to learn more about it. Please reach out to me at {email} or call me at {telephone} to discuss further.\n\nBest regards,\n{name}",
    "Hello,\n\nMy name is {name}, and I'm interested in exploring how your services could benefit my business. I'd appreciate the opportunity to connect and discuss potential collaboration opportunities. Feel free to contact me at {email} or call me at {telephone}.\n\nThanks,\n{name}",
    "Hi there,\n\nI'm {name}, and I'm reaching out to inquire about your offerings. Your company seems to align with the goals of my project, and I'm excited to explore how we might work together. Please get in touch with me at {email} or call me at {telephone}.\n\nBest regards,\n{name}",
    "Hello,\n\nI'm {name}, and I'm currently evaluating different solutions for my business needs. Your product has caught my interest, and I'd like to learn more about its features and pricing. Please contact me at {email} or call me at {telephone}.\n\nLooking forward to hearing from you,\n{name}",
    "Hi,\n\nI'm {name}, and I'm excited to explore potential collaboration opportunities with your company. Your services seem to align perfectly with the objectives of my project. I'd appreciate the chance to discuss further. Feel free to reach me at {email} or call me at {telephone}.\n\nBest regards,\n{name}"
]

response_messages =[
    "Hi,Thank you for getting back to me. I'm particularly interested in understanding how your product integrates with existing project management tools. Could you provide more details on its compatibility with platforms like Asana or Trello? Additionally, I'd like to know about any customization options available to tailor the product to our specific project workflows.Looking forward to your insights.Best regards, {name}",
    "Hello,Appreciate your response. Before proceeding further, I'm keen to learn about the pricing structure of your product, especially if there are any tiered plans or additional costs for scaling as our business grows. Additionally, could you elaborate on any enterprise-level features or support options available? Understanding these aspects will help us evaluate the suitability of your product for our long-term needs.Thanks in advance for your assistance.Best regards, {name}",
    "Hi there,Thanks for reaching out. One aspect I'm particularly interested in is how your product handles data security, especially regarding sensitive project information. Could you provide insights into the encryption methods used and any compliance certifications your platform adheres to? Additionally, I'd like to know about integration capabilities with other tools we use, such as Slack and Google Workspace.Looking forward to hearing from you.Best regards,{name}",
    "Hello,Thank you for getting back to me. I'm currently evaluating several options for our project management needs, and pricing is a significant factor in our decision-making process. Along with pricing details, I'm interested in understanding the features included in each plan. Specifically, could you provide a comparison chart outlining the functionalities available in your different pricing tiers? This will help us assess the value proposition of your product.Looking forward to your response.Best regards, {name}",
    "Hi there,Appreciate your prompt response. Before committing to any purchase, our team prefers to explore the product firsthand to ensure it aligns with our requirements. Could you arrange a demo or provide access to a trial version of your software? This would allow us to assess its usability, interface, and suitability for our project management workflows.Thank you in advance for accommodating our request.Best regards, {name}",
 "Hello,Thank you for reaching out. Pricing is certainly a key consideration for us, but we're also interested in understanding the level of customization and support available with your product. Can you provide insights into any customization options for tailoring the software to our specific project needs? Additionally, I'd like to know about the support channels available and the responsiveness of your customer support team.Looking forward to learning more.Best regards, {name}",
]

app = FastAPI()

urlSendLead = "http://localhost:8000/process_lead"

# Endpoint to generate leads with a specific name
@app.get("/generate_lead_specific_name")
async def generate_lead_specific_name(name: str):
    existing_contact = hubspot_client.get_contact_by_name(name)
    if existing_contact:   
        print("contact already exist, generating response message ")

        random_lead_message = random.choice(response_messages)
        
        formatted_message = random_lead_message.format(name=name)
        lead_data = {"lead": formatted_message}

    else:
        print("contact dont exist, generating initial lead message ")
        if name in contact_info:
            contact = contact_info[name]
            email = contact["email"]
            telephone = contact["telephone"]
        else:
            # Default email and telephone when the name is not found
            email = "dcnavarros@unal.edu.co"
            telephone = "+573007751361"
            
        random_lead_message = random.choice(lead_messages)
        
        formatted_message = random_lead_message.format(name=name, email=email, telephone=telephone)
        lead_data = {"lead": formatted_message}
    try:
        response = requests.post(urlSendLead, json=lead_data, timeout=15)  # Timeout set to 15 seconds
        response.raise_for_status()
        return {"message": "Lead generated and sent successfully"}
    except Timeout:
        raise HTTPException(status_code=500, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send lead: {str(e)}")
    
    
# Endpoint to generate leads with a specific name
@app.get("/generate_lead")
async def generate_lead():
    name = random.choice(list(contact_info.keys()))
    existing_contact = hubspot_client.get_contact_by_name(name)
    if existing_contact:   
        
        
        random_lead_message = random.choice(response_messages)
        
        formatted_message = random_lead_message.format(name=name)
        lead_data = {"lead": formatted_message}

    else:
        contact = contact_info[name]
        email = contact["email"]
        telephone = contact["telephone"]

        random_lead_message = random.choice(lead_messages)
        
        formatted_message = random_lead_message.format(name=name, email=email, telephone=telephone)
        lead_data = {"lead": formatted_message}
    try:
        response = requests.post(urlSendLead, json=lead_data, timeout=15)  # Timeout set to 15 seconds
        response.raise_for_status()
        return {"message": "Lead generated and sent successfully"}
    except Timeout:
        raise HTTPException(status_code=500, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send lead: {str(e)}")