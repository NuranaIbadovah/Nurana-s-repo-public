#!/usr/bin/python3

import sys
import requests
import os

# Zabbix passes 3 arguments: To, Subject, Message
if len(sys.argv) < 4:
    sys.exit(1)

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "7997271903:AAFDJcmGMicr_M-1FsIQhtIq6lsiZT9****"
# --------------------

chat_id = sys.argv[1]
subject = sys.argv[2]
message_body = sys.argv[3]

# Use HTML for more robust formatting
def escape_html(text):
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text

safe_subject = escape_html(subject)
safe_message = escape_html(message_body)

# Format the message using simple HTML tags
full_message = f"<b>{safe_subject}</b>\n\n{safe_message}"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

payload = {
    'chat_id': chat_id,
    'text': full_message,
    'parse_mode': 'HTML' # Use HTML
}

try:
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    error_details = response.text if 'response' in locals() else 'No response.'
    with open("/tmp/zabbix_telegram_error.log", "a") as log_file:
        log_file.write(f"Error: {e}\nResponse: {error_details}\n")
    sys.exit(1)
