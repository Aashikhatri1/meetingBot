
import openai
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

model ='gpt-3.5-turbo-1106'

instructions = """You are to analyze a conversation of a sales representative and score it based on specific criteria. Also take into consideration the time constraint. You should answer in the JSON format as below. Provide all the fields. Write true if that indicator is there, else write false. 
{
  "Greetings": True/False,
  "Name": True/False,
  "Title and Roles": True/False,
  "Responsibilities": True/False,
  "Agenda Setup for the meeting": True/False,
  "Rapport Building": True/False,
  "Company Offerings / Services": True/False,
  "Company Stats - Revenue / Global Presence / Employee Strength": True/False,
  "Product Demo/ Information": {
    "Let me show you": True/False,
    "Features": True/False
  },
  "Challenges and Pain Points": True/False,
  "Ongoing and upcoming projects or initiatives": True/False,
  "Current vendors/ service providers": True/False,
  "Current Platforms or tools being used": True/False,
  "Follow-up conversations/ next steps": True/False,
  "Follow-up Date and Time": True/False,
  "Proposed POC": True/False,
  "Decision Maker": True/False,
  "Addressing Objections": True/False,
  "Providing Explanations and References": True/False,
  "Offering Solutions to overcome objections": True/False
}"""

def gpt_response(indicators, diarisation):
    indicators =str(indicators)
    diarisation = str(diarisation)
    conversation = [
        {
            "role": "system",
            "content": instructions,
        },
    {
            "role": "system",
            "content": indicators,
        },
        {
            "role": "system",
            "content": diarisation,
        },
    ]
    # Call to OpenAI chat API
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        api_key=openai_api_key,  # Use the API key from the environment variable
    )

    # Get the answer from OpenAI
    answer = (response.get("choices", [{}])[0])
    # print("Received answer from OpenAI:", answer)
    content = answer.get("message", {}).get("content", "")

    #print("Extracted content:", content)
    return content