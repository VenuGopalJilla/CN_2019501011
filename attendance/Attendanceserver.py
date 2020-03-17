import socket
import threading

host = '127.0.0.1'
port = 2020

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
server_socket.bind((host, port))
group = { "1001" : "absent", "1002" : "absent", "1003" : "absent", "1004" : "absent", "1005" : "absent", "1006" : "absent",
"1007" : "absent", "1008" : "absent", "1009" : "absent", "1010" : "absent", "1011" : "absent"}
users = {}

def mark_number(client_data, server_socket):
	client_request_data = client_data[0].decode("utf-8")
	if client_request_data != 'q' :
		if client_request_data in group.keys():
			group[client_request_data] = "Present"
			# print(group.keys())
			string = ""
			for st in group.keys():
				if group[st] == "absent":
					# print(st)
					string = string + st + " "
			for stri in users.keys():
				print(stri)
				server_socket.sendto(string.encode("utf-8"), stri)
		else:
			for stri in users.keys():
				print(stri)
				server_socket.sendto("Roll Number Not Found".encode("utf-8"), strin)
	else:
		print("Client closed")

def host_server():
	while True:
		print("entered")
		client_data = server_socket.recvfrom(1024)
		users[client_data[1]] = client_data
		thread1 = threading.Thread(target = mark_number, args = (client_data, server_socket))
		thread1.start()

host_server()
