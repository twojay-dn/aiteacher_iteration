import streamlit as st
from PIL import Image
from openai import OpenAI
from graph import PhaseNode
from initialize import parse_json_to_graph

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def init_state():
  phases = parse_json_to_graph()
  print(phases)
  st.session_state["phase"] = PhaseNode("main", "main")
  if "uploaded_image" not in st.session_state:
      st.session_state["uploaded_image"] = None
  st.session_state.setdefault("uploaded_image_names", [])
  st.session_state.setdefault("chat_history", [])

def chat_history_render():
  for role, message in st.session_state["chat_history"]:
    st.chat_message(role).write(message)

def chat_input():

    if prompt := st.chat_input("메시지를 입력하세요"):
        st.session_state["chat_history"].append(("user", prompt))
        messages = [{"role": m[0], "content": m[1]} for m in st.session_state["chat_history"]]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ai_message = response.choices[0].message.content
        st.session_state["chat_history"].append(("assistant", ai_message))

def current_node_info_render():
  if st.session_state["phase"] is None:
    st.write("현재 단계가 설정되지 않았습니다.")
    return
  st.write(f"현재 단계: {st.session_state['phase'].name}")
  st.write(f"현재 단계 설명: {st.session_state['phase'].description}")

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

def render():
  init_state()

  

  column1, column2 = st.columns([0.7, 0.3])
  with column1:
    chathistory_container = st.container(height=500)
    chatinput_container = st.container(height=150)
  with column2:
    current_node_info_container = st.container(height=150)
    image_board_container = st.container(height=500)
  
  with chatinput_container:
      chat_input()
  with chathistory_container:
      chat_history_render()
  with current_node_info_container:
      current_node_info_render()
  with image_board_container:
      image_board_render()