from states import ClientState
import socket
import time
import json


class Client:
    def __init__(self, host, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.state = ClientState.READY
        self.HOST = host
        self.PORT = port
    
    # Main function
    def run(self) -> None:
        self.conn2Server()

        try:
            while True:
                task = self.receiveTask()
                # Here, we show the task to the user so that the user attempts it
                # Just for this to work right now, I am creating a response to send to the server
                response = self.getUserResponse()
                self.sendResponse(response)
                outcome = self.receiveOutcome()
                
                if outcome == 1:
                    self.state = ClientState.APPROVED
                    print("Success")
                    break
        except Exception as e:
            print(f"Client disconnected from server\n{e}")
    
    def conn2Server(self) -> None:
        while True:
            try:
                self.sock.connect((self.HOST, self.PORT))
                self.state = ClientState.CONNECTED
                break
            except Exception as e:
                print("Connection failed. Will try again in 2 seconds.")
                time.sleep(2)
    
    def receiveTask(self) -> str:
        try:
            task_data = self.sock.recv(1024)
            task = json.loads(task_data.decode())
            print(f"Received task: {task}")
            self.state = ClientState.SOLVING
            return task
        except Exception as e:
            print(f"Error when trying to receive task:\n{e}")
    
    # Implement actual function. This is just placeholder.
    def getUserResponse(self) -> json:
        response = json.dumps({
            "task_id": 1234,
            "resp_time": time.time() + 20,
            "user_resp": "The correct answer"
        })
        self.state = ClientState.SOLVED
        return response

    def sendResponse(self, response) -> None:
        try:
            self.sock.sendall(response.encode())
            self.state = ClientState.WAITING
        except Exception as e:
            print(f"Error when trying to send response:\n{e}")
    
    def receiveOutcome(self) -> None:
        try:
            outcome = self.sock.recv(1024)
            outcome = json.loads(outcome.decode())
            print(f"Recieved outcome: {outcome}")
            return outcome
        except Exception as e:
            print(f"Error when trying to receive outcome\n{e}")


if __name__ == "__main__":
    c = Client('127.0.0.1', 65432)
    c.run()
