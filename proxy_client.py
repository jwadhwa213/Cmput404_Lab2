import socket, sys

def create_tcp_socket():
    print('Creating socket')
    try:
    	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
    	host_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {host_ip}')
    return host_ip
def send_data(socket_obj, payload):
    print("Sending payload")
    try:
        socket_obj.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    try:
        host = 'localhost'
        port = 8001
        payload = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
        buffer_size = 4096

	 	# create the socket
        s =create_tcp_socket()

	 	# get the remote ip of host
        remote_ip = get_remote_ip(host)

	 	# open a connection to the server
        s.connect((remote_ip, port))
        print (f'Socket Connected to {host} on ip {remote_ip}')

	 	# send the data
        send_data(s , payload)
	 	#shutdown client side
        s.shutdown(socket.SHUT_WR)

	 	#continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        #close the connection
        s.close()

if __name__ == "__main__":
    main()
