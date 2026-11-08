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