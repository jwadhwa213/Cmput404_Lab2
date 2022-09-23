import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip
 
def handle_echo(remote_server, client_addr, client_conn) :
	client_data_recvd = client_conn.recv(BUFFER_SIZE)
	print(f"Received data from client {client_data_recvd}")
	print(f"Sending data to google : {client_data_recvd}")

	remote_server.sendall(client_data_recvd)
	remote_server.shutdown(socket.SHUT_WR)

	server_resp = remote_server.recv(BUFFER_SIZE)
	print(f'Server Response: {server_resp}')
	print(f'Sending Server Response {server_resp} to the Client')
	client_conn.send(server_resp)

def main():
	host = 'www.google.com'
	port = 80
	# payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
    # buffer_size = 4096

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_server:

		proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#bind socket to address
		proxy_server.bind((HOST, PORT))
		proxy_server.listen(1)
		while True:
			client_conn, client_addr = proxy_server.accept()
			print("Connected by", client_addr)
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_server:
				remote_ip = socket.gethostbyname(host)
				remote_server.connect((remote_ip, port))
				# multiprocessing
				p = Process(target = handle_echo, args = (remote_server, client_addr, client_conn))
				p.daemon = True
				p.start()
				print("Started process ", p)
			client_conn.close()


if __name__ == '__main__':
	main()