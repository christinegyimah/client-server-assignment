import azure.functions as func
import json
import base64
from database import get_connection

app= func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="me", methods=["GET"])
def get_current_user(req: func.HttpRequest) -> func.HttpResponse:
    encoded_user=req.headers.get("x-ms-client-principal")

    if not encoded_user:
        return func.HttpResponse(
            "Unauthorized", status_code=401
        )
    try:
        decoded_user=base64.b64decode(
            encoded_user,validate=True
        ).decode("utf-8")
        user=json.loads(decoded_user)
    except (ValueError,UnicodeError):
        return func.HttpResponse(
            "Invalid authentication data", status_code=401
        )

    if (
        not isinstance(user,dict)
        or not isinstance(user.get("userRoles"), list)
        or "authenticated" not in user["userRoles"]
        or not user.get("userId")
    ):
        return func.HttpResponse(
            "Unauthorized", status_code=401
        )
    return func.HttpResponse(
        json.dumps({
            "userId": user["userId"],
            "userDetails": user.get("userDetails")
        }),
        mimetype="application/json",
        status_code=200
    )

@app.route(route="db-check", methods=["GET"])
def check_database(req: func.HttpRequest) -> func.HttpResponse:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result=cursor.fetchone()

        if result and result[0]==1:
            return func.HttpResponse(
                "Database connection successful!",
                status_code=200
            )
        return func.HttpResponse(
            "Database check failed.",
            status_code=503
        )
    except Exception as error:
        return func.HttpResponse(
            f"Database error type: {type(error).__name__}",
            status_code=503
        )