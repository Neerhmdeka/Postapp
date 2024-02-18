from fastapi import FastAPI
from pydantic import BaseModel
import ai

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.get("/generate")
async def generate(text: str):
    return {"generated_text": ai.generate_text(text)}

@app.post("/publishpost")
async def publish(text_input: TextInput):
    return {"generated_text": ai.generate_text(text_input.text)}
