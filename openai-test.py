import os
from dotenv import load_dotenv
from openai import OpenAI

# Get the API key from environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


#Set up OpenAI client
client = OpenAI()


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)