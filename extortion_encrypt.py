import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_file(file_path, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB8(b'1234567890123456'), backend=backend)
    encryptor = cipher.encryptor()

    with open(file_path, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as f:
        f.write(ciphertext)

def main():
    directory = input("Enter the path to the directory you want to encrypt: ").strip()

    if not os.path.isdir(directory):
        print("The provided path is not a directory or does not exist.")
        return

    key = secrets.token_bytes(32)  # AES-256 key
    key_file_path = os.path.join(directory, 'aes_key.key')

    # Save the key to a file
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

    # Encrypt all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and not filename.endswith('.enc') and filename != 'aes_key.key':
            encrypt_file(file_path, key)
            os.remove(file_path)  # Optionally remove the original file after encryption

    print(f"Encryption complete. Key saved to {key_file_path}")

if __name__ == '__main__':
    main()
