# Keylogger

This is a basic python keylogger that can read system information and keystrokes and mail them to us using the smtp service.

**Libraries Used:**

- email
- smtplib
- socket
- platform
- pynput
- time
- os
- cryptography
- getpass
- requests

**Functions in main**

- sendmail() : To send the mail with attchment
- get_computer_info() : To get the basic info of the computer. For eg: Kernel Version, Processor Info etc.
- on_press_key(), on_release_key() : Keylogger functions

**Additional Files**

- decrypt_file.py : This file will be used to decrypted the encrypted files recieved in the mail
- generate_key.py : This file will generate the key that will be used for encryption and decryption

**Generating Executable**

```
> pip install auto-py-to-exe
> auto-py-to-exe
```

- Browse the file
- Start conversion

Executable stored in output folder :)
