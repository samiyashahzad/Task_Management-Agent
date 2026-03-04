from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from langchain.agents import create_agent

from agent.tools import init_database, create_toolkit, create_sql_executor_tool
from agent.prompts import system_prompt
from agent.memory import get_checkpointer

# path configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "tasks.db")

# initialize database, toolkit and agent components

db = init_database(db_path)
toolkit = create_toolkit(db)
tools = toolkit.get_tools()
# add custom raw-sql executor tool so the agent can run arbitrary
# queries and return errors directly to the LLM
tools.append(create_sql_executor_tool(db_path))

@st.cache_resource  # Cache the agent to avoid reinitialization on every interaction

def get_agent():
    agent = create_agent(
        model=toolkit.llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=get_checkpointer(),
    )
    return agent

agent = get_agent()

# streamlit UI
st.title("SQL Agent - Task Management Assistant")
st.subheader("Ask me anything about your tasks!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("ask me anything about your tasks! You can create, read, update, or delete tasks using natural language.")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        with st.spinner("processing ..."):
            if prompt.lower() in ["exit", "quit"]:
                st.write("Goodbye!")
                st.stop()
            response = agent.invoke({"messages": [{"role": "user", "content": prompt}]}, {"configurable": {"thread_id": "sql_agent_thread1"}})
            st.chat_message("assistant").markdown(response["messages"][-1].content)
            st.session_state.messages.append({"role": "assistant", "content": response["messages"][-1].content})
