# backend/main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from openai import OpenAI

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Never share publicly
)

chat_log = [{
    'role': 'system',
    'content': 'You are a very helpful AI.'
}]

@app.post("/")
async def chat(user_input: Annotated[str, Form()]):
    chat_log.append({'role': 'user', 'content': user_input})

    response = client.chat.completions.create(
        model="openai/gpt-4o",
        messages=chat_log,
        max_tokens=500,
        temperature=0.6,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "ChatBot",
        }
    )

    bot_response = response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': bot_response})
    return bot_response
