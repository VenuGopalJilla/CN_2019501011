import socket

host = 'localhost'
port = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
server_socket.bind((host, port))
# server_socket.listen(1)

# while True:
	# connection, client_address = server_socket.accept()
	# print(f"Connection from {client_address} has been established!")
while True:
	client_data = server_socket.recvfrom(1024)
	client_request_data = client_data[0].decode("utf-8")
	if client_request_data != 'q' :
		res = client_request_data.upper()
		print(res)
		server_socket.sendto(res.encode(), client_data[1])
	else:
		print("Client closed")
		break
