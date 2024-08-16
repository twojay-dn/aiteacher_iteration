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
    self._prompt = prompt
    
  def __str__(self):
    return f"{self.name} - {self.description}"
  
  def _current_checkpoint(self):
    return self.checkpoint
  
  def _current_work(self):
    return self.work
  
  @property
  def prompt(self):
    return self._prompt
  
  @prompt.setter
  def prompt(self, value: str):
    self._prompt = value

import os
from utils import read_json
import json
default_json_path = f"{os.getcwd()}/phases.json"

def parse_json_to_graph(json_data : dict = None) -> Phases:
  if json_data is None:
    return None
  data = json.loads(json_data)
  return process_phases(data)

def process_phases(phases: Phases) -> None:
  parsed_phases : List[PhaseNode] = []
  for phase in phases['phases']:
    if result := process_single_phase(phase):
      parsed_phases.append(result)
    else:
      return []
  return parsed_phases

import streamlit as st

def process_single_phase(phase: Phase) -> None:
  prompt = st.session_state["file_uploader"].read_file(phase['task_prompt'])
  if prompt is None:
    return
  phase_node = LLMPhaseNode(
    name = phase['name'],
    description = phase['description'],
    persona_info = phase['persona'],
    situation = phase['situation'],
  )
  prompt = load_prompt(phase_node, prompt)
  phase_node.prompt = prompt
  return phase_node

@st.cache_data
def base_prompt():
  path = f"{os.getcwd()}/resources/prompts/node_prompt_base.md"
  with open(path, "r") as file:
    return file.read()

def load_prompt(parsed_phase : PhaseNode, prompt_text : str):
  base = base_prompt()
  prompt = base.replace("<_persona_position>", parsed_phase.name)
  prompt = prompt.replace("<_persona_place>", "교실")
  prompt = prompt.replace("<_persona_event>", "수업")
  task_prompt = prompt_text
  task_prompt = task_prompt.replace("<_class_title>", parsed_phase.description)
  task_prompt = task_prompt.replace("<_class_summary>", parsed_phase.description)
  prompt = prompt.replace("<_task>", task_prompt)
  return prompt