import requests
import json
import time
import uuid
import os
import random
from datetime import datetime

# 🎨 Display logo
def print_logo():
    print("\033[1;36m")  # Cyan color
    print('██     ██ ██ ███    ██ ███████ ███    ██ ██ ██████  ')
    print('██     ██ ██ ████   ██ ██      ████   ██ ██ ██   ██ ')
    print('██  █  ██ ██ ██ ██  ██ ███████ ██ ██  ██ ██ ██████  ')
    print('██ ███ ██ ██ ██  ██ ██      ██ ██  ██ ██ ██ ██      ')
    print(' ███ ███  ██ ██   ████ ███████ ██   ████ ██ ██      ')
    print('                                                   ')
    print("Join our Telegram channel: https://t.me/winsnip")
    print("\033[0m")  # Reset color

# 🔹 Read user ID and session token from account.txt
def get_credentials():
    if not os.path.exists("account.txt"):
        print("❌ Error: File 'account.txt' not found!")
        exit()

    with open("account.txt", "r") as file:
        data = file.read().strip().split("|")
        if len(data) != 2:
            print("❌ Error: Invalid 'account.txt' format! (Use format: user_id|session_token)")
            exit()
        return data[0], data[1]  # user_id, session_token

# 🔹 Read messages list from pesan.txt (each line = 1 message)
def get_messages():
    if not os.path.exists("pesan.txt"):
        print("❌ Error: File 'pesan.txt' not found!")
        exit()

    with open("pesan.txt", "r", encoding="utf-8") as file:
        messages = [line.strip() for line in file.readlines() if line.strip()]
    
    if not messages:
        print("❌ Error: File 'pesan.txt' is empty!")
        exit()
    
    return messages

# 🔹 Send request to API
def send_request(message, user_id, session_token):
    url = "https://api1-pp.klokapp.ai/v1/chat"

    headers = {
        "Content-Type": "application/json",
        "x-session-token": session_token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }

    payload = {
        "id": str(uuid.uuid4()),  # New UUID for each request
        "language": "english",
        "user": user_id,  # User ID included in payload
        "messages": [{"role": "user", "content": message}],
        "model": "llama-3.3-70b-instruct",
        "sources": []
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"🔍 Debug: Status Code = {response.status_code}")

        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"✅ Response: {json.dumps(json_response, indent=2)}\n")
            except json.JSONDecodeError:
                print(f"⚠️ Response: {response.text}\n")
        else:
            print(f"⚠️ Error Response {response.status_code}: {response.text}\n")

    except Exception as e:
        print(f"❌ Request failed: {e}\n")

# 🔹 Run auto-chat daily
def run_auto_chat():
    print_logo()  # Display logo
    user_id, session_token = get_credentials()
    messages = get_messages()

    while True:  # Continuous loop to run daily
        print("\n📅 New day started! Sending 10 messages...\n")

        # Select 10 random messages each day
        selected_messages = random.sample(messages, min(10, len(messages)))

        for i, message in enumerate(selected_messages, start=1):
            print(f"📩 Sending message {i}/10: {message}")
            send_request(message, user_id, session_token)

            if i < len(selected_messages):
                print("⏳ Waiting 1 minute before sending next message...\n")
                time.sleep(60)  # Wait 1 minute between messages

        print("⏳ Waiting 24 hours before sending messages again...\n")
        time.sleep(86400)  # Wait 24 hours before next day

# 🔹 Run script
if __name__ == "__main__":
    run_auto_chat()
