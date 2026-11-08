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