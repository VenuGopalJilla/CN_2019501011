import socket


client_socket = socket.socket()
client_socket.connect(('localhost', 8000))

while True:
	msg_to_be_sent = input("Enter text to be sent :")
	client_socket.sendall(str.encode(msg_to_be_sent, "utf-8"))
	msg_received = client_socket.recv(1024).decode("utf-8")
	print(msg_received)
	if msg_to_be_sent == "q" :
		break
	
	

