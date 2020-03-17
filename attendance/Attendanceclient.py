import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
destination_server = ('localhost', 2020)

while True:
	# msg1 = client_socket.recvfrom(1024)
	# print(msg1)
	msg_to_be_sent = input("Enter roll number:")
	client_socket.sendto(str.encode(msg_to_be_sent, "utf-8"), destination_server)
	if msg_to_be_sent == "q" :
		break
	msg_received = client_socket.recvfrom(1024)
	msg = msg_received[0].decode("utf-8")
	print(msg)
	
	
	

