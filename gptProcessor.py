import os
from openai import OpenAI
import openai
from dotenv import load_dotenv
load_dotenv()

import json


class ChatGPTLeadProcessor:

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def process_data(self,lead):
        """
        Uses ChatGPT to generate a response message based on the lead information.

        Returns:
            str: The generated response message, or an error message if unsuccessful.
        """
        


        system_prompt = """Ignore spaces and dots. Extract the following information in JSON format:

            {
            "Name": "",
            "PhoneNumber": "",
            "Email": "",
            "lead_key_information": "none",
            "Response": ""
            }


            Instructions:

            - Look for and extract the following key information:
            - Name: Extract the name mentioned in the lead message.
            - PhoneNumber: Extract the phone number mentioned in the lead message.
            - Email: Extract the email addresses mentioned in the lead message.
            - lead_key_information: Identify any key information mentioned in the lead message and provide a brief summary. If no key information is found, set this field to "none" but put efforts to find useful information in the lead.
            - response:  you are a friendly assistant designed to provide assistance to potential customers and you are processing customer lead. let the customer know that you will comunicate her/ him soon
            - your company is called SouthDesk and your name is David 
            Ensure accurate extraction of information and provide a helpful and friendly response to the user.

            customer Lead:

            """
            # Define the prompt
        prompt = [
            {"role": "system", "content":system_prompt },
            {"role": "user", "content": lead}
        ]
    # Send the conversation to GPT-3.5 Turbo
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=prompt,
            temperature=0.4,
            max_tokens=200
        )
            # Extract message from response
        gpt_answer = response.choices[0].message.content
        response_dict = json.loads(gpt_answer)
        # Convert the dictionary back to JSON for consistency
        return json.dumps(response_dict)


if __name__ == "__main__":
    lead = "Hi,\n\nI'm Maria Sanchez, and I'm excited to explore potential collaboration opportunities with your company. Your services seem to align perfectly with the objectives of my project. I'd appreciate the chance to discuss further. Feel free to reach me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nMaria"

    processor = ChatGPTLeadProcessor()
    response = processor.process_data(lead)
    print(response)