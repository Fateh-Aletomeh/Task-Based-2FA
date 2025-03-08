#!/usr/bin/env python3
import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encrypt_data(data, key):
    """
    Encrypts a JSON-serializable dictionary using AES in CBC mode.

    Steps:
      1. Convert the dictionary to a JSON string and encode it to bytes.
      2. Generate a random 16-byte Initialization Vector (IV).
      3. Pad the data to meet AES's block size (16 bytes) using PKCS7.
      4. Encrypt the padded data.
      5. Return the IV concatenated with the ciphertext.

    Parameters:
      - data (dict): The JSON-serializable data to encrypt.
      - key (bytes): A 256-bit (32-byte) AES key.

    Returns:
      - bytes: The IV concatenated with the ciphertext.
    """
    # Convert the dictionary to JSON bytes
    data_bytes = json.dumps(data).encode('utf-8')
    
    # Generate a random IV (16 bytes for AES)
    iv = os.urandom(16)
    
    # Pad data using PKCS7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data_bytes) + padder.finalize()
    
    # Create AES cipher in CBC mode and encrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return the IV followed by the ciphertext
    return iv + ciphertext

def decrypt_data(encrypted_data, key):
    """
    Decrypts data that was encrypted using the encrypt_data function.

    Steps:
      1. Extract the IV (first 16 bytes) from the encrypted data.
      2. Decrypt the remaining ciphertext.
      3. Remove the padding.
      4. Convert the bytes back into a JSON object (dictionary).

    Parameters:
      - encrypted_data (bytes): The IV concatenated with the ciphertext.
      - key (bytes): The same 256-bit AES key used for encryption.

    Returns:
      - dict: The decrypted data as a dictionary.
    """
    # Extract the IV and ciphertext
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    
    # Create AES cipher for decryption
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove the PKCS7 padding
    unpadder = padding.PKCS7(128).unpadder()
    data_bytes = unpadder.update(padded_data) + unpadder.finalize()
    
    # Convert bytes back to a dictionary
    return json.loads(data_bytes.decode('utf-8'))
