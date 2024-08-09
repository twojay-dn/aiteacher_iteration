from typing import List, TypedDict
from phases import PhaseNode

class Persona(TypedDict):
    position: str
    place: str
    event: str

class Situation(TypedDict):
    name: str
    description: str

class Phase(TypedDict):
    name: str
    description: str
    persona: Persona
    situation: Situation
    task_prompt: str

class Phases(TypedDict):
    phases: List[Phase]

import os
from utils import read_json
default_json_path = f"{os.getcwd()}/phases.json"

def parse_json_to_graph(json_path : str = None) -> Phases:
  if json_path is None:
    json_path = default_json_path
  return process_phases(read_json(json_path))

def process_phases(phases: Phases) -> None:
  parsed_phases : List[PhaseNode] = []
  for phase in phases['phases']:
    parsed_phases.append(process_single_phase(phase))
  return parsed_phases

def process_single_phase(phase: Phase) -> None:
  print(f"단계 이름: {phase['name']}")
  print(f"설명: {phase['description']}")
  print(f"페르소나 위치: {phase['persona']['position']}")