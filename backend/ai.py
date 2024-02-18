import openai
from api_key import API_KEY  

openai.api_key = API_KEY

model_engine = "gpt-3.5-turbo-0125" 

def generate_text(text):
    print("Generating text...")

    completions = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "user", "content": text}
        ]
    )

    generated_text = completions['choices'][0]['message']['content']

    return generated_text
