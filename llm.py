import os   #to access environment variables
from dotenv import load_dotenv   #to load variables in .env file
from google import genai   #to access tools to communicate with gemini
import json
load_dotenv()    #to load the API key

client= genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )       #to connect gemini API key 


#to choose the model
MODEL="gemini-3.5-flash-lite"  


#define a function to send a prompt
def ask_ai(prompt):
    response=client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text

#to create json response function
def ask_ai_json(prompt):
    response= client.models.generate_content(
        model=MODEL, 
        contents=prompt,
        config={
            "response_mime_type":"application/json"
        }
    )
    return json.loads(response.text)