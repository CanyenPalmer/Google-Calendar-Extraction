# Google Calendar Export Script

This script pulls all **past and future** events from your Google Calendar and saves them to a `calendar_events.csv` file.

## 📦 Features

- ✅ Works with your Google account
- ✅ Exports all events (past + future)
- ✅ Saves details like summary, start/end time, location, etc.
- ✅ Automatically handles authentication with `token.json`

## 🚀 Setup

### 1. Enable Google Calendar API

- Go to: https://console.cloud.google.com/
- Create a project
- Enable **Google Calendar API**
- Create **OAuth Client ID** (application type: Desktop App)
- Download `credentials.json` and place it in this folder

### 2. Install Dependencies

```bash
pip install -r requirements.txt

