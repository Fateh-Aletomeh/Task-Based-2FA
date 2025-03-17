import json
import base64
import os
from encryption_utils import encrypt_data, decrypt_data  # Import your AES encryption functions

# Define a fixed AES key (for testing, replace with a securely stored key in production)
AES_KEY = os.urandom(32)  # In production, use a securely managed key

# Static task with pre-defined circle positions and colors
STATIC_TASK = {
    "taskId": "task-1234",
    "circles": [
        {"id": "circle-0", "x": 100, "y": 150, "color": "red"},
        {"id": "circle-1", "x": 200, "y": 250, "color": "green"},
        {"id": "circle-2", "x": 300, "y": 350, "color": "blue"},
        {"id": "circle-3", "x": 400, "y": 450, "color": "yellow"},
        {"id": "circle-4", "x": 500, "y": 550, "color": "orange"},
        {"id": "circle-5", "x": 600, "y": 100, "color": "purple"},
        {"id": "circle-6", "x": 700, "y": 200, "color": "pink"},
        {"id": "circle-7", "x": 150, "y": 300, "color": "brown"},
        {"id": "circle-8", "x": 250, "y": 400, "color": "cyan"},
        {"id": "circle-9", "x": 350, "y": 500, "color": "magenta"}
    ],
    "creationDate": "2025-03-01T12:00:00",
    "task": "Click on the blue and green circles",
    "expirationDate": "2025-03-01T12:05:00",
    "expectedResponse": ["circle-1", "circle-2"]  # User must select these circles
}

# Encrypt the task
encrypted_task = encrypt_data(STATIC_TASK, AES_KEY)

# Base64 encode the encrypted data for display (this is how it would be transmitted over TCP)
b64_encrypted_task = base64.b64encode(encrypted_task).decode('utf-8')

# Decrypt the task
decrypted_task = decrypt_data(encrypted_task, AES_KEY)

# Display the results
print("\n🔹 **Original Task Data:**")
print(json.dumps(STATIC_TASK, indent=4))

print("\n🔹 **Encrypted Task Data (Base64 Encoded):**")
print(b64_encrypted_task)

print("\n🔹 **Decrypted Task Data:**")
print(json.dumps(decrypted_task, indent=4))
