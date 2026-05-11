import os
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is the Sky Blue?",
        }
    ],
    model="llama-3.1-8b-instant",
    max_completion_tokens=50
)

print(chat_completion.choices[0].message.content)