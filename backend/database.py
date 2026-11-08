import os
import mssql_python
from dotenv import load_dotenv

load_dotenv()
SQL_SERVER= os.getenv("SQL_SERVER")
SQL_DATABASE= os.getenv("SQL_DATABASE")
SQL_USER= os.getenv("SQL_USER")
SQL_PASSWORD= os.getenv("SQL_PASSWORD")

def get_connection():
    connection=mssql_python.connect(
        server=SQL_SERVER,
        database=SQL_DATABASE,
        uid=SQL_USER,
        pwd=SQL_PASSWORD,
        encrypt="yes",
        trustservercertificate="no",
        timeout=60
    )
    return connection

def save_study_note(user_id, topic, note):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO StudyNotes (user_id, topic, note)
                VALUES (?,?,?)
                """,
                (user_id,topic,note)
            )
        conn.commit()

def get_study_notes(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, topic, note, created_at
                FROM StudyNotes
                WHERE user_id=?
                ORDER BY created_at DESC, id DESC
                """,
                (user_id,)
            )
            rows=cursor.fetchall()
    return[
        {
            "id": row[0],
            "topic": row[1],
            "note": row[2],
            "created_at": row[3].isoformat()
        }
        for row in rows
    ]