#!/usr/bin/env python3
#################################################################################
import socket


###
class SocketServer:
    """

    """
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._host, self._port))

    def __del__(self):
        self._socket.close()

    def run(self):
        # Wait for client connections
        client_connection, client_address = self._socket.accept()
        while True:
            data = client_connection.recv(2048)
            if not data:
                break
            # Send  response
            response = 'test'
            client_connection.sendall(response.encode())
            client_connection.close()


###
def main():
    pass

###
if __name__ == "__main__":
    main()

