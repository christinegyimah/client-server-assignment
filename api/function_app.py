import azure.functions as func
import json
import base64
from database import get_connection, get_display_name, save_display_name, get_study_notes, save_study_note


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

@app.route(route="notes", methods=["GET", "POST"])
def retrieve_notes(req: func.HttpRequest) -> func.HttpResponse:
    encoded_user=req.headers.get("x-ms-client-principal")

    if not encoded_user:
        return func.HttpResponse("Unauthorized", status_code=401)
    try:
        user=json.loads(base64.b64decode(encoded_user, validate=True).decode("utf-8"))
    except (ValueError, UnicodeError, TypeError):
        return func.HttpResponse("Unauthorized", status_code=401)

    if (
        not isinstance(user,dict)
        or not isinstance(user.get("userRoles"),list)
        or "authenticated" not in user["userRoles"]
        or not isinstance(user.get("userId"),str)
        or not user["userId"]
    ):
        return func.HttpResponse("Unauthorized", status_code=401)

    if req.method == "POST":
        try:
            data=req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON.", status_code=400)
        if not isinstance(data,dict):
            return func.HttpResponse("Invalid request.", status_code=400)

        topic=data.get("topic")
        note=data.get("note")

        if not isinstance(topic,str) or not isinstance(note,str):
            return func.HttpResponse("Topic and note must be text.", status_code=400)
        topic=topic.strip()
        note=note.strip()

        if not 1<=len(topic) <=100 or not 1<= len(note) <=1000:
            return func.HttpResponse("Topic must be 1-100 characters and note 1-1000 characters.", status_code=400)
        if(any(ord(c)<32 or ord(c)==127 for c in topic) or any((ord(c)<32 and c not in "\n\r]t") or ord(c)==127 for c in note)):
            return func.HttpResponse("Input contains invalid characters.", status_code=400)
        try:
            save_study_note(user["userId"], topic, note)
        except Exception:
            return func.HttpResponse("Could not save study note.", status_code=503)
        return func.HttpResponse(
            json.dumps({"message": "Study note saved successfully!"}),
            mimetype="application/json",
            status_code=201
        )
    try:
        notes=get_study_notes(user["userId"])
    except Exception as error:
        return func.HttpResponse(
            "Could not retrieve study notes.",
            status_code=503
        )
    return func.HttpResponse(
        json.dumps({"notes": notes}),
        mimetype="application/json",
        status_code=200
    )
