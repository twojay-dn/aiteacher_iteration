from typing import List
from models import Phases, Phase

class Checkpoint:
  def __init__(self):
    self.messages = []
    
  def append(self, role: str, message: str):
    self.messages.append((role, message))
    
  def get(self):
    return [{"role": m[0], "content": m[1]} for m in self.messages]

  def get_with_system_message(self, system_message: str):
    return [{"role": "system", "content": system_message}] + self.get()

from typing import Protocol

class PersonaInfo(Protocol):
  position: str
  place: str
  event: str

class SituationInfo(Protocol):
  name: str
  description: str

class PhaseNode:
  def __init__(self,
      name: str = None,
      description: str = None,
      checkpoint: Checkpoint = None
    ):
    self.name = name
    self.description = description
    self.checkpoint = checkpoint
    if self.checkpoint is None:
      self.checkpoint = Checkpoint()
    self.work = None
    self.next_edge = []

  def _current_checkpoint(self):
    return self.checkpoint

  def _current_work(self):
    return self.work
  
  def check_able_to_move(self):
    return len(self.next_edge) > 0

  def move(self):
    assert self.check_able_to_move(), "No next edge"
    self.work = self.next_edge[0]
    self.next_edge = self.next_edge[1:]

class LLMPhaseNode(PhaseNode):
  def __init__(self,
      name: str = None,
      description: str = None,
      checkpoint: Checkpoint = None,
      persona_info : PersonaInfo = None,
      situation : SituationInfo = None,
      prompt : str = None
    ):
    super().__init__(name, description, checkpoint)
    self.persona_info = persona_info
    self.situation = situation
    self.prompt = prompt
    assert self.prompt is not None, "prompt is required"
    
    
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