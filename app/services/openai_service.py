import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_psychology_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "system",
            "content": "Você é um psicólogo profissional respondendo de forma empática e útil."
        }, {
            "role": "user",
            "content": prompt
        }]
    )
    return response.choices[0].message['content'].strip()