from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for Lead
class Lead(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    message: str

# Endpoint to receive leads and print them
@app.post("/process_lead")
async def process_lead(lead: Lead):
    print(f"Received Lead: {lead}")
    
    
    return {"message": "Lead received successfully"}
