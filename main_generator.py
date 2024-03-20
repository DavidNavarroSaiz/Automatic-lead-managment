from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException
import random
import requests
from requests.exceptions import Timeout


# Define a Pydantic model for Lead
class Lead(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    message: str

# Sample mock lead data
mock_leads = [
    Lead(id=1, name="John Doe", email="john@example.com", phone="123-456-7890", message="Interested in your product."),
    Lead(id=2, name="Jane Smith", email="jane@example.com", phone="987-654-3210", message="Looking for more information."),
    Lead(id=3, name="Alice Johnson", email="alice@example.com", phone="555-123-4567", message="Needs a pricing quote."),
    Lead(id=4, name="Bob Williams", email="bob@example.com", phone="444-789-0123", message="Ready to buy!"),
]

app = FastAPI()

urlSendLead = "http://localhost:8000/process_lead"
# Endpoint to generate leads
@app.get("/generate_lead")
async def generate_lead():
    if mock_leads:
        random_lead = random.choice(mock_leads)
        # Send the generated lead to another API service
        try:
            response = requests.post(urlSendLead, json=random_lead.model_dump(), timeout=5)  # Timeout set to 5 seconds
            response.raise_for_status()
            return {"message": "Lead generated and sent successfully"}
        except Timeout:
            raise HTTPException(status_code=500, detail="Request timed out")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send lead: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail="No leads available")