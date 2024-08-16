import streamlit as st
from PIL import Image
from openai import OpenAI
from phases import PhaseNode, parse_json_to_graph

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def init_state(parsed_json : dict = None, render_component = None):
  st.session_state.setdefault("file_uploader", FileUploader(type=["txt", "md","json"], accept_multiple_files=True, name="텍스트 파일 업로드"))
  st.session_state.setdefault("uploaded_image", None)
  st.session_state.setdefault("uploaded_image_names", [])
  st.session_state.setdefault("chat_history", [])
  st.session_state.setdefault("phase", None)
  st.session_state.setdefault("phases", [])
  st.session_state.setdefault("current_phase", None)
  if parsed_json is not None:
    st.session_state["phases"] = parse_json_to_graph(parsed_json)
    if len(st.session_state["phases"]) > 0:
      st.session_state["current_phase"] = st.session_state["phases"][0]
    else:
      st.error("프롬프트 파일이 없습니다.")
      return

def chat_history_render():
  for role, message in st.session_state["chat_history"]:
    st.chat_message(role).write(message)

from llm import talk

def chat_input():
  if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state["chat_history"].append(("user", prompt))
    system_prompt = st.session_state["current_phase"].prompt
    if system_prompt is None:
      st.error("시스템 프롬프트가 없습니다.")
      return
    res = talk(prompt, system_prompt)
    st.session_state["chat_history"].append(("assistant", res))

def current_node_info_render():
  if st.session_state["current_phase"] is None:
    st.write("현재 단계가 설정되지 않았습니다.")
    return
  st.write(f"현재 단계: {st.session_state['current_phase'].name}")
  st.write(f"현재 단계 설명: {st.session_state['current_phase'].description}")

def image_board_render():
  uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
  if uploaded_file is not None:
    image = Image.open(uploaded_file, mode="r")
    st.session_state["uploaded_image"] = image
    if uploaded_file.name not in st.session_state["uploaded_image_names"]:
      st.session_state["uploaded_image_names"].append(uploaded_file.name)

    st.write("업로드된 이미지 목록:")
    
    # 이미지 목록을 가로로 길쭉한 패널로 표시
    for idx, image_name in enumerate(st.session_state["uploaded_image_names"]):
      with st.container():
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
          st.write(image_name)
        with col2:
          if st.button("삭제", key=f"delete_{idx}"):
            st.session_state["uploaded_image_names"].remove(image_name)
            st.rerun()


def chat_mode():
  column1, column2 = st.columns([0.7, 0.3])
  with column1:
    chathistory_container = st.container(height=500)
    chatinput_container = st.container(height=150)
  with column2:
    current_node_info_container = st.container(height=150)
    image_board_container = st.container(height=500)
  
  if st.session_state["current_phase"] is None:
    st.error("현재 단계가 설정되지 않았습니다.")
    return
  else:
    with chatinput_container:
      chat_input()
    with chathistory_container:
      chat_history_render()
    with current_node_info_container:
      current_node_info_render()
    with image_board_container:
      image_board_render()

def init_mode():
  column1, column2 = st.columns([0.7, 0.3])
  with column1:
    input_json = st.text_area("초기화 입력", height=500)
    if st.button("초기화"):
      if input_json is None or input_json == "":
        st.error("초기화 입력이 비어있습니다.")
      else:
        init_state(input_json)
        st.rerun()
  with column2:
    st.session_state["file_uploader"].upload()

def render():
  tab1, tab2 = st.tabs(["초기화", "챗봇"])
  init_state()
  
  with tab1:
    init_mode()
  with tab2:
    chat_mode()

def read_uploaded_files(file_name, list):
  for file in list:
    if file.name == file_name:
      return file.read().decode("utf-8")
  return None

from typing import List

class FileUploader:
  def __init__(self, type : List[str], accept_multiple_files : bool=True, name : str="텍스트 파일 업로드"):
    self.uploaded_files = []
    self.uploader = st.file_uploader
    self.type = type
    self.accept_multiple_files = accept_multiple_files
    self.name = name

  def upload(self):
    self.uploaded_files = self.uploader(self.name, type=self.type, accept_multiple_files=self.accept_multiple_files)
    for file in self.uploaded_files:
      if file not in self.uploaded_files:
        self.uploaded_files.append(file)

  def get_uploaded_files(self):
    return self.uploaded_files

  def search_file(self, file_name):
    for file in self.uploaded_files:
      if file.name == file_name:
        return file
    return None

  def read_file(self, file_name):
    file = self.search_file(file_name)
    if file is not None:
      return file.read().decode("utf-8")
    return None

