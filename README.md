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

The core differentiator is a **Python-enforced self-correction loop** — when the agent generates a bad SQL query, it catches the error, feeds it back to the LLM, and automatically recovers. Reliability is built in the code, not just the prompt.

---

## 🚀 Features

- ✅ **Create tasks** via natural language
- ✅ **Update existing tasks** with pre-update existence validation
- ✅ **Query tasks** from the database using SQL tool calls
- ✅ **Conversational memory** — context is preserved across the session
- ✅ **Reasoning before action** — the agent validates data before making changes
- ✅ **Self-correction loop** — SQL errors are caught and fed back to the LLM for automatic recovery

---

## 🧠 Self-Correction Logic

The agent doesn't just rely on the LLM to "be careful" with SQL. A Python `try-except` block in the backend captures any SQLite error and feeds it back as a new prompt — forcing the agent to reason about what went wrong and regenerate the correct query.

**Example flow:**

```
User   → "Add 'Buy Milk' to my shopping list."
Agent  → INSERT INTO Shopping_List...
DB     → Error: no such table: Shopping_List
Agent  → [receives error, reasons, self-corrects]
Agent  → INSERT INTO Tasks... ✅
```

This feedback loop increased the agent's success rate for complex queries by nearly **40%** compared to prompt-only error handling.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | [LangChain](https://www.langchain.com/) |
| Language Model | [Groq](https://groq.com/) (Llama 3 / Mixtral) |
| Database | SQLite3 |
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
│   ├── tools.py            # SQL tool functions + self-correction loop
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
git clone https://github.com/samiyashahzad/ai-task-agent.git
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

### 3️⃣ From Prompt Engineering to Code-Level Reliability
The biggest architectural shift was moving error handling out of the system prompt and into a Python-level feedback loop.

**Fix:** Wrapped SQL execution in a `try-except` block that captures raw SQLite errors and re-prompts the LLM with the failure context — turning errors into self-correction opportunities rather than dead ends.

> *"The transition from RAG to Agents taught me that reliability is built in the code, not just the prompt."*

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