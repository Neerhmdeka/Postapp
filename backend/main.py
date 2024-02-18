from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ai

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

@app.get("/generate")
async def generate(text: str):
    return {"generated_text": ai.generate_text(text)}

@app.post("/publishpost")
async def publish(text_input: TextInput):
    return {"generated_text": ai.generate_text(text_input.text)}
