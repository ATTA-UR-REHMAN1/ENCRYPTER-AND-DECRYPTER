import os
import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(password: str) -> bytes:
    """Convert password to a Fernet key using SHA-256."""
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def encrypt_file(filepath, key):
    """Encrypt a single file."""
    fernet = Fernet(key)

    with open(filepath, "rb") as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    with open(filepath + ".enc", "wb") as file:
        file.write(encrypted)

def encrypt_folder(folder_path, password):
    key = generate_key(password)

    print(f"\nEncrypting files in: {folder_path}\n")

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            full_path = os.path.join(root, filename)

            if full_path.endswith(".enc"):
                continue

            print(f"Encrypting: {full_path}")
            encrypt_file(full_path, key)

    print("\n✔ Encryption complete!")
    print("Use the decrypt script to restore your files.")

if __name__ == "__main__":
    folder = input("Enter the full path of the folder you want to encrypt: ").strip()
    
    if not os.path.isdir(folder):
        print("❌ Invalid folder path")
        exit()

    password = input("Enter password to encrypt files: ")

    encrypt_folder(folder, password)
