from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langgraph.prebuilt import create_react_agent  # ✅ correct import

from agent.tools import init_database, create_toolkit, create_sql_executor_tool
from agent.prompts import system_prompt
from agent.memory import get_checkpointer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database", "tasks.db")

db = init_database(db_path)
toolkit = create_toolkit(db)
tools = toolkit.get_tools()
tools.append(create_sql_executor_tool(db_path))

@st.cache_resource
def get_agent():
    return create_react_agent(  # ✅ correct function
        model=toolkit.llm,
        tools=tools,
        prompt=system_prompt,
        checkpointer=get_checkpointer(),
    )

agent = get_agent()

st.title("SQL Agent - Task Management Assistant")
st.subheader("Ask me anything about your tasks!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Ask me anything about your tasks! Create, read, update, or delete using natural language.")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if prompt.lower() in ["exit", "quit"]:
        st.write("Goodbye!")
        st.stop()

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response = agent.invoke(
                {"messages": [{"role": "user", "content": prompt}]},
                {"configurable": {"thread_id": "sql_agent_thread1"}}
            )
            reply = response["messages"][-1].content
            st.markdown(reply)  # ✅ no double bubble

    st.session_state.messages.append({"role": "assistant", "content": reply})