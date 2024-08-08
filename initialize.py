from typing import List, TypedDict

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


import os,json
default_json_path = f"{os.getcwd()}/phases.json"

def parse_json_to_graph(json_path : str = None) -> Phases:
  if json_path is None:
    json_path = default_json_path
  with open(json_path, "r", encoding="utf-8") as f:
    phases = json.load(f)
  process_phases(phases)
  return phases

def process_phases(phases: Phases) -> None:
  for phase in phases['phases']:
    process_single_phase(phase)

def process_single_phase(phase: Phase) -> None:
  print(f"단계 이름: {phase['name']}")
  print(f"설명: {phase['description']}")
  print(f"페르소나 위치: {phase['persona']['position']}")
  # 여기에 단일 단계를 처리하는 로직을 추가합니다.