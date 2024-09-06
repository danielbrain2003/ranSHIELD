import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_file(encrypted_file_path, key, iv):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=backend)
    decryptor = cipher.decryptor()

    with open(encrypted_file_path, 'rb') as f:
        ciphertext = f.read()
    
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_file_path = encrypted_file_path.rsplit('.enc', 1)[0]
    with open(decrypted_file_path, 'wb') as f:
        f.write(plaintext)

def main():
    directory = input("Enter the path to the directory containing encrypted files: ").strip()

    if not os.path.isdir(directory):
        print("The provided path is not a directory or does not exist.")
        return

    key_file_path = os.path.join(directory, 'aes_key.key')

    if not os.path.isfile(key_file_path):
        print("Key file not found.")
        return

    # Load the key from the file
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    iv = b'1234567890123456'  # The same IV used for encryption

    # Decrypt all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith('.enc'):
            decrypt_file(file_path, key, iv)
            os.remove(file_path)  # Optionally remove the encrypted file after decryption

    # Remove the key file
    os.remove(key_file_path)
    print("Decryption complete. Key file deleted.")

if __name__ == '__main__':
    main()
