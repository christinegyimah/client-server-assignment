import os
import mssql_python

def get_connection():
    connection= mssql_python.connect(
        server=os.environ["SQL_SERVER"],
        database=os.environ["SQL_DATABASE"],
        uid=os.environ["SQL_USER"],
        pwd=os.environ["SQL_PASSWORD"],
        encrypt="yes",
        trustservercertificate="no",
        timeout=60
    )
    return connection

def get_display_name(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT display_name
                FROM dbo.UserProfiles
                WHERE user_id=?
                """,
                (user_id,)
            )
            row=cursor.fetchone()
    return row[0] if row else None

def save_display_name(user_id, display_name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE dbo.UserProfiles
                SET display_name=?,
                    updated_at=SYSUTCDATETIME()
                WHERE user_id=?
                """,
                (display_name,user_id)
            )
            if cursor.rowcount==0:
                cursor.execute(
                    """
                    INSERT INTO dbo.UserProfiles (user_id, display_name)
                    VALUES (?,?)
                    """,
                    (user_id, display_name)
                )
        conn.commit()

def save_study_note(user_id, topic, note):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO dbo.StudyNotes (user_id, topic, note)
                VALUES (?,?,?)
                """,
                (user_id, topic, note)
            )
        conn.commit()

def get_study_notes(user_id):
    with get_connection() as conn:
        with conn.sursor() as cursor:
            cursor.execute(
                """
                SELECT id, topic, note, created_at
                FROM dbo.StudyNotes
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
        for rows in rows
    ]