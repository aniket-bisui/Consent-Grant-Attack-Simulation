# 🛑 Consent Grant Attack Simulation

A realistic attacker-themed lab that demonstrates how malicious applications can exploit OAuth 2.0 consent flows in Microsoft Entra ID (Azure AD) to gain unauthorized delegated access to Microsoft Graph APIs.

> ⚠️ **Educational use only** — this simulation is designed for red team demos, portfolio projects, and hands-on learning. Do not deploy on production tenants.

----

## 🎯 Objectives

This lab simulates a full attacker workflow:
- 🧠 Abuse of OAuth consent grant flow
- 🔐 Capture of delegated access tokens
- 📊 Display of granted scopes and user profile
- 💀 Glowing red UI to reflect adversary realism

----

## 🧪 Features

- Simulates an **illicit consent grant attack**
- Displays **access tokens**, **refresh tokens**, and **granted scopes**
- Uses **Microsoft Graph API** to fetch sensitive data
- Glowing red **footer disclaimer** and **header branding** for attacker vibe
- Modular Flask architecture with Jinja2 templates
- Designed for **red team interviews** and **security demos**

----

## 🚀 Setup Instructions

###  Clone the Repo

```bash
git clone https://github.com/your-username/consent-grant-simulation.git
cd consent-grant-simulation

----

###  Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

----

###  Configure Microsoft Entra ID App

Go to Azure Portal
Register a new app
Set redirect URI: http://localhost:5000/login/callback
Add delegated permissions:
    User.Read
    offline_access
    Contacts.Read
    Mail.Read
    Mail.Send
    MailboxSettings.ReadWrite
    Notes.Read.All
    User.ReadBasic.All
Create a .env file:
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
TENANT_ID=your-tenant-id
REDIRECT_URI=http://localhost:5000/login/callback

----

###  Run the App
flask run

----

## 📸 Screenshots

### 🧠 Landing Page
![Landing Page](screenshots\landing-page.png)

### 🎯 Dashboard
![Dashboard](screenshots\dashboard.png)

----

##🧠 Attack Flow
[User] → [Phishing Consent Page] → [OAuth Grant] → [Token Capture] → [Dashboard Display]

----


##📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

----


##🙋‍♂️ Author
AniketBisui — Offensive security enthusiast, red team simulation architect, and relentless learner.