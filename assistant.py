from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv("APIKEY")
client = OpenAI()


def ai_bot(request):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"You are a fact check bot check check the following "
                                        f"information and give a brief summary of the topic: {request}"}
        ]
    )
    response = str(completion.choices[0].message)
    return response[31:-71]
