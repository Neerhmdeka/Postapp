# ai.py
import os
import openai

# Retrieve API key from environment variable
API_KEY = os.environ.get("OPENAI_API_KEY")

# Set OpenAI API key
openai.api_key = API_KEY

model_engine = "gpt-3.5-turbo-0125" 

def generate_text(text):
    try:
        print("Generating text...")
        
        completions = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "user", "content": text}
            ]
        )

        generated_text = completions['choices'][0]['message']['content']
        
        return generated_text
    
    except Exception as e:
        print(f"Error generating text: {e}")
        raise  
