from states import ServerState
from constants import *
import socket
import ssl
import time
import json

from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
import encryption_utils as enc_utils
import task_gen


class Server:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile="certfile.pem", keyfile="keyfile.pem")
        self.sock = context.wrap_socket(self.sock, server_side=True)

        self.state = ServerState.READY
        print(f"Server listening on {host}:{port}")
    
    # Main function
    def run(self) -> None:
        conn, addr = self.sock.accept()
        self.state = ServerState.CONNECTED
        print(f"Connection from {addr}")

        while True:
            task_data: json = task_gen.generate_json_file()
            self.sendTask(conn, task_data, 1)
            response = self.receiveResponse(conn)
            outcome = self.handleResponse(response)
            self.sendOutcome(conn, outcome)
            if outcome == 1: break
        
        conn.close()
    
    def sendTask(self, conn, task_data, attempt) -> None:
        curr_time = time.time()

        task_msg = json.dumps({
            "attempt": attempt,
            "task_data": task_data,
            "curr_time": curr_time,
            "exp_time": curr_time + EXP_TIME
        })

        try:
            conn.sendall(task_msg.encode())
            self.state = ServerState.WAITING
        except Exception as e:
            print(f"Error when trying to send task:\n{e}")
    
    def receiveResponse(self, conn) -> json:
        try:
            response_data = conn.recv(1024)
            return json.loads(response_data.decode())
        except Exception as e:
            print(f"Error when trying to receive response:\n{e}")
    
    def handleResponse(self, response) -> int:
        self.state = ServerState.CHECKING
        task_id = response["task_id"]
        resp_time = response["resp_time"]
        user_resp = response["user_resp"]

        # Process the response (this is a placeholder, implement logic here)
        print(f"Received response for task {task_id}: {user_resp}")

        self.state = ServerState.CHECKED
        # Returning 1 just as placeholder
        return 1
    
    def sendOutcome(self, conn, outcome) -> None:
        outcome_msg = json.dumps({"outcome": outcome})

        try:
            conn.sendall(outcome_msg.encode())
        except Exception as e:
            print(f"Error when trying to send outcome:\n{e}")


if __name__ == "__main__":
    s = Server('127.0.0.1', 65432)
    s.run()
