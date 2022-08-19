from itertools import count
from cryptography.fernet import Fernet

key = ""  # read from encryption_key.txt
with open("encryption_key.txt", "r") as f:
    key = f.read()
    print("Key Read complete successfully ✅")

key_info_encrypted = "keylog_enc.txt"
system_info_encrypted = "sysinfo_enc.txt"

encrypted_files = [key_info_encrypted, system_info_encrypted]
count = 0

for file in encrypted_files:
    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(
            f"-----------------------{encrypted_files[count]}-----------------------")
        f.write(decrypted)
        f.write("---------------------------------------------------------------------")
    count += 1
