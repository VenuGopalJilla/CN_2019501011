import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
destination_server = ('localhost', 8000)
# client_socket.connect(('localhost', 8000))

while True:
	msg_to_be_sent = input("Enter text to be sent :")
	client_socket.sendto(str.encode(msg_to_be_sent, "utf-8"), destination_server)
	if msg_to_be_sent == "q" :
		break
	msg_received = client_socket.recvfrom(1024)
	msg = msg_received[0].decode("utf-8")
	print(msg)
	
	
	

