import socket

host = 'localhost'
port = 8000

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

while True:
	connection, client_address = server_socket.accept()
	print(f"Connection from {client_address} has been established!")
	try:
		while True:
			client_request_data = connection.recv(1024).decode("utf-8")
			if client_request_data != 'q' :
				res = client_request_data.upper()
				print(res)
				connection.sendall(res.encode())
			else:
				print("Client closed")
				break
	finally:
		connection.close()
