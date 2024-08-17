import openai
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv("apikey.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(prompt="Call me an Uber ride type \"Plus\" in Berkeley at zipcode 94704 in 10 minutes", model="gpt-3.5-turbo", functions=[]):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            functions = functions,
            function_call = "auto"
        )
        return completion.choices[0].message.content    
    except Exception as e:
        print(e, model, prompt)