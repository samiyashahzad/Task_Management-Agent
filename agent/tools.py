import os
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq


def init_database(db_path: str):
    # ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    db.run("""
    CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL 
            CHECK(status IN ('pending', 'in_progress', 'completed')) 
            DEFAULT 'pending',
        Created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    return db


def create_toolkit(db):
    model = ChatGroq(model="openai/gpt-oss-20b")
    return SQLDatabaseToolkit(db=db, llm=model)
