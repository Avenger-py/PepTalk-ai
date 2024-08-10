from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse 
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from prompt import sys_prompt
from typing import Union
import google.generativeai as genai
import os


genai.configure(api_key="os.environ["GEMINI_API_KEY"]")

app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")
templates = Jinja2Templates(directory="../templates")

prompt = ""
response = ""

def get_response(prompt, sys_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash',system_instruction=sys_prompt)
    situation = f"<Situation>\n{prompt}"
    response = model.generate_content(situation)
    return response.text


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    global response
    return templates.TemplateResponse("index.html", {"request": request, "response": response})


@app.post("/generate")
async def generate(request: Request, userInput: str = Form(default=".")):
    global prompt
    global response
    prompt = userInput
    try:
        response = get_response(prompt, sys_prompt)
    except:
        pass
        # response = "Error: either API calls are exhausted or an error occured. Please try again."
    return RedirectResponse(url="/", status_code=303)

# @app.get("/", response_class=HTMLResponse)
