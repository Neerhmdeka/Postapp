# main.py
from fastapi import FastAPI, HTTPException, Request
from ai import generate_text
from linkedin_automation import LinkedinAutomate
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load environment variables from .env file
load_dotenv()

# Initialize OAuth client
oauth = OAuth()

# Configure LinkedIn OAuth 2.0 settings with all required scopes
linkedin = oauth.register(
    name='linkedin',
    client_id=os.environ.get('LINKEDIN_CLIENT_ID'),
    client_secret=os.environ.get('LINKEDIN_CLIENT_SECRET'),
    authorize_url='https://www.linkedin.com/oauth/v2/authorization',
    authorize_params=None,
    access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:8000/auth/linkedin/callback',
    client_kwargs={'scope': ['r_liteprofile', 'r_emailaddress', 'w_member_social', 'w_share']}  # Specify required scopes
)

# Define a Pydantic model for text input
class TextInput(BaseModel):
    text: str

# Endpoint to generate text
@app.post("/generate-text")
async def generate_text_endpoint(text_input: TextInput):
    try:
        generated_text = generate_text(text_input.text)
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to publish post to LinkedIn
@app.post("/publish-post")
async def publish_post_to_linkedin(text_input: TextInput):
    try:
        # Check if access token is available
        access_token = os.environ.get("LINKEDIN_ACCESS_KEY")
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token is required")

        # Generate text
        generated_text = generate_text(text_input.text)

        # Publish post to LinkedIn
        linkedin = LinkedinAutomate(yt_url="https://www.youtube.com/watch?v=Mn6gIEM33uU",
                                    title="Filtering, Searching, Ordering in Django Rest Framework Part 22",
                                    description=generated_text)
        linkedin.main_func(generated_text)
        return {"message": "Post published to LinkedIn successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to redirect users to LinkedIn OAuth 2.0 authorization page
@app.get("/auth/linkedin")
async def auth_linkedin(request: Request):
    redirect_uri = request.url_for('auth_linkedin_callback')
    return await linkedin.authorize_redirect(request, redirect_uri)

# Endpoint to handle OAuth 2.0 callback from LinkedIn
@app.get("/auth/linkedin/callback")
async def auth_linkedin_callback(request: Request):
    token = await linkedin.authorize_access_token(request)
    # Store token securely or use it to access LinkedIn API
    return RedirectResponse(url="/", status_code=302)

# Define a simple handler for the root URL
@app.get("/")
async def root():
    return {"message": "Welcome to PostApp!"}
