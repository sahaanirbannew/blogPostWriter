from fastapi.responses import JSONResponse 
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, HTTPException, Form, Response, Header, Depends, Request 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from business_logic_layer.logger import logger, log_exception
from business_logic_layer.config import Config 
from presentation_layer.input import Input_Payload
from typing import Optional 
import json
logger.info("Imports are working... ")

config = Config() 
lang = config.admin.language
print(lang)
security = HTTPBearer()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('messages.json') as f:                # load the messages from the messages.json file 
    messages = json.load(f)

def get_response(message_code, message_type, response = None, lang = lang, messages = messages):
    """
    Get the response for the given message code and message type
    """
    if message_code.startswith("E"):
        logger.error(f"Error: {messages[message_code][lang]}") 
    else:
        logger.info(f"Message: {messages[message_code][lang]}")
    
    response = JSONResponse(content={"message": messages[message_code][lang], "status": message_type}) 
    return response

def get_cookie_details(request):
    """
    Get the cookie details from the request object
    """
    try:
        jwt_token = request.cookies.get("jwt_token") 
    except Exception as e:
        return get_response("E001", "error")
    
    try:
        refresh_token = request.cookies.get("refresh_token") 
    except Exception as e:
        return get_response("E002", "error")
    
    try:
        user_id = request.cookies.get("user_id") 
    except Exception as e:
        return get_response("E003", "error")
    
    return jwt_token, refresh_token, user_id

@app.get("/")
async def read_root():
    return {
        "message": "Hello World"
    };

@app.get("/read-image")
async def read_image(request: Request,        # Request object
                       payload: Optional[Input_Payload] = None): 
    
    print(Input_Payload) 
    return "response to the UI"