# Agent-
# 🧠 AI Task Management Agent

> A stateful AI agent that manages tasks through natural language — powered by LangChain, Groq, and SQLite.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Agent-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red?style=flat-square&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?style=flat-square&logo=sqlite)

---

## 📌 Overview

This is my first stateful AI agent — built as step one of my **Agent Engineering roadmap for 2026**.

Instead of a simple chatbot, this agent connects to a real SQLite database, uses tool-based reasoning, and maintains conversational memory across a session. You can create, update, and query tasks entirely through natural language.

---

## 🚀 Features

- ✅ **Create tasks** via natural language
- ✅ **Update existing tasks** with pre-update existence validation
- ✅ **Query tasks** from the database using SQL tool calls
- ✅ **Conversational memory** — context is preserved across the session
- ✅ **Reasoning before action** — the agent validates data before making changes

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | [LangChain](https://www.langchain.com/) |
| Language Model | [Groq](https://groq.com/) |
| Database | SQLite |
| User Interface | [Streamlit](https://streamlit.io/) |
| Memory & State | LangChain session state + memory |

---

## 📁 Project Structure

```
ai-task-agent/
│
├── app.py                  # Streamlit interface and agent initialization
├── requirements.txt
│
├── agent/
│   ├── tools.py            # SQL tool functions
│   ├── prompts.py          # System prompt logic
│   └── memory.py           # Memory configuration
│
└── database/
    └── tasks.db            # SQLite task database
```

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/your-username/ai-task-agent.git
cd ai-task-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your Groq API key**
```bash
export GROQ_API_KEY=your_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## 🧩 Challenges & What I Learned

### 1️⃣ Database Initialization Issue
The database wasn't being created on startup. The root cause was an incorrect path reference — the directory didn't exist before `sqlite3.connect()` was called.

**Fix:** Added explicit directory creation before initializing the database, which also made the project structure cleaner overall.

### 2️⃣ Agent Update Logic
The agent was attempting `UPDATE` queries without first verifying that the task existed — leading to silent failures.

**Fix:** Refined the system prompt to enforce a strict 3-step flow:
1. Run a `SELECT` query
2. Confirm the task exists
3. Only then execute the `UPDATE`

This made the agent's behavior significantly more reliable and deterministic.

---

## 🎓 Why I Built This

I'm currently studying databases this semester, and I wanted to apply SQL concepts inside a real system rather than writing isolated queries. This project was the first time LLM reasoning, tool calling, and structured database validation came together for me in a meaningful way.

---

## 🔮 Roadmap

- [ ] Deploy to Streamlit Cloud or HuggingFace Spaces
- [ ] Cleaner tool abstractions
- [ ] Structured validation layer
- [ ] Multi-tool agent expansion
- [ ] Task priorities and deadlines

---

## 📄 License

MIT License — feel free to fork and build on this.
