import azure.functions as func
import json
import base64
from database import get_connection, get_display_name, save_display_name


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
    try:
        display_name=get_display_name(user["userId"])
    except Exception:
        return func.HttpResponse(
            "Profile database unavailable.",
            status_code=503
        )
    return func.HttpResponse(
        json.dumps({
            "userId": user["userId"],
            "userDetails": user.get("userDetails"),
            "displayName": display_name
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

@app.route(route="profile", methods=["POST"])
def update_profile(req: func.HttpRequest) -> func.HttpResponse:
    encoded_user=req.headers.get("x-ms-client-principal")

    if not encoded_user:
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        user=json.loads(
            base64.b64decode(encoded_user, validate=True).decode("utf-8")
        )
    except(ValueError, UnicodeError, TypeError):
        return func.HttpResponse("Unauthorized", status_code=401)
    if(
        not isinstance(user,dict)
        or not isinstance(user.get("userRoles"),list)
        or "authenticated" not in user["userRoles"]
        or not isinstance(user.get("userId"),str)
        or not user["userId"]
    ):
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        data=req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON.", status_code=400)

    if not isinstance(data,dict):
        return func.HttpResponse("Invalid request.", status_code=400)
    display_name=data.get("displayName")

    if(
        not isinstance(display_name,str)
        or not 1 <= len(display_name.strip()) <=80
        or any(ord(char) <32 for char in display_name)
    ):
        return func.HttpResponse(
            "Display name must be 1-80 characters.",
            status_code=400
        )
    display_name=display_name.strip()

    try:
        save_display_name(user["userId"], display_name)
    except Exception:
        return func.HttpResponse(
            "Could not save profile.", status_code=503
        )
    return func.HttpResponse(
        json.dumps({"displayName": display_name}),
        mimetype="application/json",
        status_code=200
    )