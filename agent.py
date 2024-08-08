# from langgraph.graph import StateGraph
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langchain_openai import ChatOpenAI

# class Agent:
#   def __init__(self, initial_data: dict, llm : ChatOpenAI = None):
#     self.initial_data = initial_data
#     self.graph_builder = StateGraph()
#     self.saver = SqliteSaver.from_conn_string(":memory:")
#     self.llm = llm
#     self.compiled = None
    
#   def _run(self):
#     self.compiled = self.graph_builder.compile(checkpointer=self.saver)

#   @property
#   def graph(self):
#     if self.compiled is None:
#       self._run()
#     return self.compiled
  
#   @property
#   def graph_builder(self):
#     return self._graph_builder
  
#   @graph_builder.setter
#   def graph_builder(self, graph_builder: StateGraph):
#     self._graph_builder = graph_builder
    
#   @graph.setter
#   def graph(self, graph: StateGraph):
#     self._graph = graph
    
    

# from typing import Annotated
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages
# from langgraph.checkpoint.sqlite import SqliteSaver
# import json
# import streamlit as st

# memory = SqliteSaver.from_conn_string(":memory:")

# # Messages have the type "list". The `add_messages` function
# # in the annotation defines how this state key should be updated
# # (in this case, it appends messages to the list, rather than overwriting them)
# class State(TypedDict):
#   messages: Annotated[list, add_messages]

# graph_builder = StateGraph(State)
# apikey=st.secrets.OPENAI_API_KEY
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(
#   model="gpt-4o-mini",
#   api_key=apikey,
#   temperature=0.5,
# )

# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}

# graph_builder.add_node("chatbot", chatbot)
# graph_builder.add_edge(START, "chatbot")
# graph_builder.add_edge("chatbot", END)
# config = {"configurable": {"thread_id": "1"}}
# graph = graph_builder.compile(checkpointer=memory)

# def cli_chat_interface(history_verbose: bool = False, graph = graph, config = config):
#   while True:
#     user_input = input("User: ")
#     if user_input.lower() in ["quit", "exit", "q"]:
#       print("Goodbye!")
#       break
#     events = graph.stream({"messages": ("user", user_input)}, config=config, stream_mode="values")
#     for event in events:
#       if history_verbose:
#         print(event["messages"])
#       event["messages"][-1].pretty_print()

# cli_chat_interface(history_verbose=True, graph=graph, config=config)


# 이 프로젝트에서는 랭그래프 안씀