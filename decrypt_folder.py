import os
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(password: str) -> bytes:
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def decrypt_file(filepath, key):
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        encrypted = file.read()

    decrypted = fernet.decrypt(encrypted)

    original_path = filepath.replace(".enc", "")
    with open(original_path, "wb") as file:
        file.write(decrypted)

def decrypt_folder(folder_path, password):
    key = generate_key(password)

    print(f"\nDecrypting files in: {folder_path}\n")

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if not filename.endswith(".enc"):
                continue

            full_path = os.path.join(root, filename)

            print(f"Decrypting: {full_path}")
            decrypt_file(full_path, key)

    print("\n✔ Decryption complete!")

if __name__ == "__main__":
    folder = input("Enter the full path of the folder to decrypt: ").strip()
    
    if not os.path.isdir(folder):
        print("❌ Invalid folder path")
        exit()

    password = input("Enter password used for encryption: ")

    decrypt_folder(folder, password)
