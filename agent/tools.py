import os
import sqlite3
from langchain.tools import tool                           # ← make sure this
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

def create_sql_executor_tool(db_path: str) -> tool:
    """Return a LangChain Tool that executes raw SQL against the given database.

    The wrapped function catches sqlite3 errors and returns them verbatim so the
    LLM can diagnose syntax or table-name problems.
    """
    def execute_sql_query(query: str):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            else:
                conn.commit()
                return "Success: The operation was completed."
        except sqlite3.Error as e:
            return f"Error: {str(e)}. Please check your table names or syntax and try again."
        finally:
            conn.close()

    # `tool` takes either a callable or a name+callable; the previous
    # implementation passed `name`/`func` keywords which aren’t supported in
    # the current LangChain version and caused a TypeError.
    return tool(
        "execute_sql_query",
        execute_sql_query,
        description="Executes a SQL query on the tasks.db and returns results or an error message."
    )