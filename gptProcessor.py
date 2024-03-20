import os
from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY")
)

class ChatGPTLeadProcessor:

    def __init__(self, lead):
        self.lead = lead

    def generate_response(self):
        """
        Uses ChatGPT to generate a response message based on the lead information.

        Returns:
            str: The generated response message, or an error message if unsuccessful.
        """
        
    # Construct lead information
        lead_content = f"""{self.lead.name} has shown interest in your product/service and has reached out via email regarding the following message:
        {self.lead.message}.

        Lead's contact details:
        - Email: {self.lead.email}
        - Phone: {self.lead.phone}

        """

#         # Define the prompt
#         prompt = [
#             {"role": "system", "content": "You are David, a friendly assistant designed to provide assistance to potential customers."},
#             {"role": "user", "content": lead_content}
#         ]
# # Send the conversation to GPT-3.5 Turbo
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo-1106",
#             messages=prompt,
#             temperature=0.7,
#             max_tokens=200
#         )
#          # Extract message from response
#         gpt_answer = response.choices[0].message.content
        gpt_answer = lead_content
        return gpt_answer


if __name__ == "__main__":
    from pydantic import BaseModel

    # Example usage
    class Lead(BaseModel):
        id: int
        name: str
        email: str
        phone: str
        message: str
    
    lead = Lead(id=1, name="John Doe", email="john@example.com", phone="123-456-7890", message="Interested in your product.")
    processor = ChatGPTLeadProcessor(lead)
    response = processor.generate_response()
    print(response)