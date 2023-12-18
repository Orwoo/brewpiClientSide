import json
import smtplib
import subprocess
from email.message import EmailMessage

import psutil


def is_process_running(process_name):
    """Check if there is any running process that contains the given name."""
    for process in psutil.process_iter(['pid', 'name']):
        if process_name in process.info['name']:
            print("temperature_control.py is running")
            return True
    print("temperature_control.py is not running")
    return False

def start_process(script_name):
    """Start a Python script."""
    subprocess.Popen(["python3", script_name])
    print("temperature_control.py started")

def kill_process_by_name(process_name):
    """Kill a process by its name."""
    for process in psutil.process_iter(['pid', 'name']):
        if process_name in process.info['name']:
            psutil.Process(process.info['pid']).terminate()
            print("temperature_control.py terminated")


def send_email(error):
    with open("src/config.json") as f:
        data = json.load(f)
    msg = EmailMessage()
    msg.set_content(f"The fermPi script has crashed.\nHere is the error msg:\n\n{error}")
    msg['Subject'] = 'fermPi server app crashed'
    msg['From'] = data['mail']['from']
    msg['To'] = data['mail']['to']

    # Establish a connection to your SMTP server
    with smtplib.SMTP(data['mail']['smtp_server'], data['mail']['port']) as server:
        server.starttls()
        server.login(data['mail']['from'], data['mail']['password'])
        server.send_message(msg)