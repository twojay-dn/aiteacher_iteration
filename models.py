from pydantic import BaseModel
from typing import List

class Persona(BaseModel):
    position: str
    place: str
    event: str

class Situation(BaseModel):
    name: str
    description: str

class Phase(BaseModel):
    name: str
    description: str
    persona: Persona
    situation: Situation
    task_prompt: str

class Phases(BaseModel):
    phases: List[Phase]