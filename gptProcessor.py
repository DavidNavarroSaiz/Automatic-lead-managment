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
            "lead_key_information": "",
            "Response": ""
            }


            Instructions:

            - Look for and extract the following key information:
            - Name: Extract the name mentioned in the lead message.
            - PhoneNumber: Extract the phone number mentioned in the lead message.
            - Email: Extract the email addresses mentioned in the lead message.
            - lead_key_information: Identify any key information mentioned in the lead message and provide a brief summary. 
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
        print("gpt_answer",gpt_answer)
        response_dict = json.loads(str(gpt_answer).strip())
        # Convert the dictionary back to JSON for consistency
        return json.dumps(response_dict)
    def extract_lead_and_response(self, response_string):
        # Split the response string into lines
        lines = response_string.strip().split('\n')
        
        # Initialize variables to store lead_key_information and response
        lead_key_information = ""
        response = ""
        
        # Iterate through the lines to extract lead_key_information and response
        for line in lines:
            # Check if the line starts with "lead_key_information"
            if line.startswith("lead_key_information:"):
                # Extract lead_key_information by removing the prefix
                lead_key_information = line.split(":")[1].strip()
            # Check if the line starts with "response"
            elif line.startswith("response:"):
                # Extract response by removing the prefix
                response = line.split(":")[1].strip()

        return lead_key_information, response

    def process_old_leads(self,lead, previous_messages):
        
        """
        Uses ChatGPT to generate a response message based on the lead information.

        Returns:
            str: The generated response message, or an error message if unsuccessful.
        """
        
        print("previous_messages",previous_messages)

        system_prompt = """
            Extract key information and respond to customer leads in a friendly manner.
            {
            "lead_key_information": "",
            "response": ""
            }
            Instructions:
            - lead_key_information: Identify and summarize any key information mentioned in the customer lead, you can ignore the name
            - response: As a friendly assistant representing SouthDesk with the name David, reassure the customer that their inquiry has been received and will be addressed promptly.
            - Use previous messages to generate contextually appropriate responses and key information.

          

            """

        system_prompt += "previous messages \n" + previous_messages


        prompt = [
            {"role": "system", "content": system_prompt },
            {"role": "user", "content": "customer Lead:" + lead} 
        ]
    # Send the conversation to GPT-3.5 Turbo
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=prompt,
            temperature=0.6,
            max_tokens=200
        )
            # Extract message from response
        gpt_answer = response.choices[0].message.content
        
        print("\n gpt_answer old leads \n ",gpt_answer)
        # Splitting the response into lead_key_information and response
        split_response = gpt_answer.split("response:")
        lead_key_information = split_response[0].strip()
        response_text = "response:" + split_response[1].strip()

        return lead_key_information, response_text



if __name__ == "__main__":
    lead = "Hi,\n\nI'm Maria Sanchez, and I'm excited to explore potential collaboration opportunities with your company. Your services seem to align perfectly with the objectives of my project. I'd appreciate the chance to discuss further. Feel free to reach me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nMaria"

    processor = ChatGPTLeadProcessor()
    # response = processor.process_data(lead)
    previous_messages =  "Hi,\n\nI came across your company online and wanted to express my interest in learning more about what you offer. My name is Emily Rodriguez, and your solutions seem aligned with the goals of my project. I'm eager to explore how we might collaborate. Please let me know the best way to connect and discuss further. You can contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nEmily Rodriguez"
    lead= "Hi there,Thanks for reaching out. One aspect I'm particularly interested in is how your product handles data security, especially regarding sensitive project information. Could you provide insights into the encryption methods used and any compliance certifications your platform adheres to? Additionally, I'd like to know about integration capabilities with other tools we use, such as Slack and Google Workspace.Looking forward to hearing from you.Best regards,Olivia Martinez"
    response = processor.process_old_leads(lead,previous_messages)
    print(response)