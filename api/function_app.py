import azure.functions as func
import json
import base64

app= func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="me", methods=["GET"])
def get_current_user(req: func.HTTPRequest) -> func.HttpResponse:
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