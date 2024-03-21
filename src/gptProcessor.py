import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ChatGPTLeadProcessor:
    def __init__(self):
        # Initialize the OpenAI client with the API key from environment variables
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def process_data(self, lead):
        """
        Uses ChatGPT to generate a response message based on the lead information.

        Args:
            lead (str): The lead information provided by the user.

        Returns:
            str: The generated response message, or an error message if unsuccessful.
        """
        # Define the system prompt for data processing
        system_prompt = """Extract the following information in JSON format:
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
              - response: You are a friendly assistant designed to provide assistance to potential customers, and you are processing customer lead. Let the customer know that you will communicate with them soon.
              - Your company is called SouthDesk, and your name is David.
              
            Ensure accurate extraction of information and provide a helpful and friendly response to the user.

            Customer Lead:
            """
        
        # Construct the prompt with system and user messages
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": lead}
        ]

        # Send the conversation to GPT-3.5 Turbo
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=prompt,
            temperature=0.4,
            max_tokens=200
        )
        
        # Extract message from response and process JSON
        gpt_answer = response.choices[0].message.content
        start_index = gpt_answer.index('{')
        end_index = gpt_answer.rindex('}') + 1  # Include the closing curly bracket
        gpt_answer = gpt_answer[start_index:end_index]
        response_dict = json.loads(gpt_answer.strip())
        
        # Convert the dictionary back to JSON for consistency
        return json.dumps(response_dict)

    def process_old_leads(self, lead, previous_messages):
        """
        Uses ChatGPT to generate a response message based on the lead information.

        Args:
            lead (str): The lead information provided by the user.
            previous_messages (str): Previous conversation messages for context.

        Returns:
            tuple: A tuple containing lead key information and a response message.
        """

        # Define the system prompt for processing old leads
        system_prompt = """
            Extract the desired information in JSON format:
            {
                "lead_key_information": "",
                "response": ""
            }

            Instructions:
            - Extract key information and respond to customer leads in a friendly manner.
            - lead_key_information: Identify and summarize any key information mentioned in the customer lead, ignoring the name and email.
            - response: As a friendly assistant representing SouthDesk with the name David, reassure the customer that their inquiry has been received and will be addressed promptly.
            - Use previous messages to generate contextually appropriate responses and key information.
            """

        system_prompt += "\nPrevious Messages:\n" + previous_messages

        # Construct the prompt with system and user messages
        prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Customer Lead: " + lead} 
        ]

        # Send the conversation to GPT-3.5 Turbo
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=prompt,
            temperature=0.6,
            max_tokens=200
        )

        # Extract message from response and process JSON
        gpt_answer = response.choices[0].message.content
        start_index = gpt_answer.index('{')
        end_index = gpt_answer.rindex('}') + 1  # Include the closing curly bracket
        gpt_answer = gpt_answer[start_index:end_index]
        response_dict = json.loads(gpt_answer.strip())
        
        # Return lead key information and response message
        return response_dict['lead_key_information'], response_dict['response']


if __name__ == "__main__":
    lead = "Hi,\n\nI'm Maria Sanchez, and I'm excited to explore potential collaboration opportunities with your company. Your services seem to align perfectly with the objectives of my project. I'd appreciate the chance to discuss further. Feel free to reach me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nMaria"

    processor = ChatGPTLeadProcessor()
    # response = processor.process_data(lead)
    previous_messages =  "Hi,\n\nI came across your company online and wanted to express my interest in learning more about what you offer. My name is Emily Rodriguez, and your solutions seem aligned with the goals of my project. I'm eager to explore how we might collaborate. Please let me know the best way to connect and discuss further. You can contact me at dcnavarros@unal.edu.co or call me at +573007751361.\n\nBest regards,\nEmily Rodriguez"
    lead= "Hi there,Thanks for reaching out. One aspect I'm particularly interested in is how your product handles data security, especially regarding sensitive project information. Could you provide insights into the encryption methods used and any compliance certifications your platform adheres to? Additionally, I'd like to know about integration capabilities with other tools we use, such as Slack and Google Workspace.Looking forward to hearing from you.Best regards,Olivia Martinez"
    response = processor.process_old_leads(lead,previous_messages)
