from openai import OpenAI
from typing import List
from pydantic import BaseModel
import streamlit as st

config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "max_tokens": 1024,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

class Messages:
  def __init__(self):
    self.messages = []

  def add_message(self, role : str, content : str, type : str = "text"):
    self.messages.append({"role": role, "content": content, "type": type})
    
  def get_messages(self):
    return self.messages
  
  def clear(self):
    self.messages = []
    
  def compose_system_message(self, prompt : str):
    return [{"role": "system", "content": prompt}] + self.messages


client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

def infenrence(messages : Messages, system_prompt : str):
  response = client.chat.completions.create(
    model=config["model"],
    messages=messages.compose_system_message(system_prompt),
    **config
  )
  return response.choices[0].message.content

class Prompt(BaseModel):
  role : str
  content : str
  type : str = "text"

def talk(prompt : Prompt, system_prompt : str):
  messages = Messages()
  messages.add_message(prompt.role, prompt.content, prompt.type)
  res = infenrence(messages, system_prompt)
  messages.add_message("assistant", res)
  return res


