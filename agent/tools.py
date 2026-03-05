import os
import sqlite3
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq


def init_database(db_path: str):
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    return db


def create_toolkit(db):
    model = ChatGroq(model="openai/gpt-oss-20b") 
    return SQLDatabaseToolkit(db=db, llm=model)


def create_sql_executor_tool(db_path: str):
    
    @tool(description="Executes a SQL query on tasks.db. Returns results for SELECT or a success/error message for other operations.")
    def execute_sql_query(query: str) -> str:
        """Executes raw SQL against the task database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return str(rows) if rows else "No results found."
            else:
                conn.commit()
                print(f"[SQL SUCCESS] {query}")  # visible in terminal
                return "Success: operation completed."
        except sqlite3.Error as e:
            print(f"[SELF-CORRECTION TRIGGERED] Error: {e}")  # visible in terminal
            print(f"[FAILED QUERY] {query}")
            return (
                f"Error: {str(e)}. "
                f"The query was: `{query}`. "
                f"Please check table names, column names, and syntax, then try again."
            )
        finally:
            conn.close()

    return execute_sql_query