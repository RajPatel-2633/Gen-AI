import os
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

system_prompt = '''
  You are an AI assitant who is specified in maths.You should not answer anything that is not related to maths.For a given query help to solve that along with explanation.

  Example:
  Input: 2 + 2
  Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

  Input: 3 * 10
  Output: 3 * 10 is 30 which is calculated by multiplying 3 by 10. Fun Fact you can even multiply 10 * 3, which gives same result
  
  Input: Why is sky blue?
  Output: Bruh? You alright? Is it Maths Query?
  '''

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role":"user",
            "content":"What is a mobile phone?"
        }
    ],
    model="llama-3.1-8b-instant",
    max_completion_tokens=100
)

print(chat_completion.choices[0].message.content)