import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from a .env file
load_dotenv()
SYSTEM_PROMPT = "You're a text message generator AI, understand user query very deeply, think of most common and possible variables in the message and then wrap them around {{var}} likewise. RETURN ONLY 1 TOP BEST MESSAGE, AND JUST REPLY THE MESSAGE"

# Configure the Gemini API with the key from the environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=api_key)

# Initialize the FastAPI router
router = APIRouter(tags=['Message Generator'])

# Pydantic model for the incoming request body
class Prompt(BaseModel):
    prompt: str

@router.post('/api/generate-message')
def generate_message(prompt: Prompt):
    """
    Generates a message using the Gemini API based on the provided prompt.
    """
    try:
        print("HERE")
        # The model initialization remains the same
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
        
        # Generate content synchronously
        response = model.generate_content(prompt.prompt)

        # Return the generated text in the response
        return {"message": response.text}
    except Exception as e:
        # 1. Print the full error to the console for debugging
        print(f"An error occurred with the Gemini API: {e}")
        
        # 2. Create the JSON error message for the client
        error_message = {"detail": f"Failed to generate message. Error: {e}"}
        
        # 3. Return a JSONResponse with a 500 status code
        return JSONResponse(status_code=500, content=error_message)
