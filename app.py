from flask import Flask, redirect, url_for, session, request, render_template, jsonify
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key")

# OAuth Configuration
CLIENT_ID = os.environ.get("CLIENT_ID", "your-client-id")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "your-client-secret")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:5000/callback")
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = [
    "User.Read",
    "offline_access",
    "Contacts.Read",
    "Mail.Read",
    "Mail.Send",
    "MailboxSettings.ReadWrite",
    "Notes.Read.All",
    "User.ReadBasic.All"
]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    auth_url = (
        f"{AUTHORITY}/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query&scope={' '.join(SCOPES)}&state=12345"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing authorization code", 400

    token_url = f"{AUTHORITY}/oauth2/v2.0/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
    }

    token_resp = requests.post(token_url, data=token_data)
    if not token_resp.ok:
        return f"Token exchange failed: {token_resp.text}", 500

    token_json = token_resp.json()
    session["access_token"] = token_json.get("access_token")
    session["refresh_token"] = token_json.get("refresh_token")
    session["id_token"] = token_json.get("id_token")

    return redirect(url_for("dashboard"))


@app.route("/refresh")
def refresh_token():
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return "No refresh token found in session", 400

    token_url = f"{AUTHORITY}/oauth2/v2.0/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
    }

    token_resp = requests.post(token_url, data=token_data)
    if not token_resp.ok:
        return f"Refresh failed: {token_resp.text}", 500

    token_json = token_resp.json()
    session["access_token"] = token_json.get("access_token")
    session["refresh_token"] = token_json.get("refresh_token", refresh_token)

    print("🔄 Access token refreshed successfully")
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")
    if not access_token:
        return redirect(url_for("login"))

    headers = {"Authorization": f"Bearer {access_token}"}
    user_resp = requests.get(f"{GRAPH_API_ENDPOINT}/me", headers=headers)

    if user_resp.status_code == 401:
        session.clear()
        return redirect(url_for("login"))

    user_info = user_resp.json()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "dashboard.html",
        user=user_info,
        access_token=access_token,
        refresh_token=refresh_token,
        now=now
    )


# ---------------- Extra Routes for Graph API ----------------

@app.route("/emails")
def emails():
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    resp = requests.get(f"{GRAPH_API_ENDPOINT}/me/messages?$top=10", headers=headers)
    return jsonify(resp.json())


@app.route("/contacts")
def contacts():
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    resp = requests.get(f"{GRAPH_API_ENDPOINT}/me/contacts", headers=headers)
    return jsonify(resp.json())


@app.route("/sendmail")
def send_mail():
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    mail_data = {
        "message": {
            "subject": "Hello from Flask app",
            "body": {
                "contentType": "Text",
                "content": "This is a test email sent via Microsoft Graph API."
            },
            "toRecipients": [
                {"emailAddress": {"address": "someone@example.com"}}
            ]
        }
    }
    resp = requests.post(f"{GRAPH_API_ENDPOINT}/me/sendMail", headers=headers, json=mail_data)
    return jsonify({"status": resp.status_code, "detail": resp.text})


@app.route("/mailsettings")
def mail_settings():
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    settings = {
        "automaticRepliesSetting": {
            "status": "alwaysEnabled",
            "internalReplyMessage": "I am currently out of office",
            "externalReplyMessage": "I am unavailable right now"
        }
    }
    resp = requests.patch(f"{GRAPH_API_ENDPOINT}/me/mailboxSettings", headers=headers, json=settings)
    return jsonify({"status": resp.status_code, "detail": resp.text})


@app.route("/notes")
def notes():
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    resp = requests.get(f"{GRAPH_API_ENDPOINT}/me/onenote/notebooks", headers=headers)
    return jsonify(resp.json())


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
