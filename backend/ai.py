import openai
from api_key import API_KEY  

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
        raise  # Re-raise the exception to propagate it to the caller
