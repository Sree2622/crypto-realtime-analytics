import socket
ade=socket.gethostbyname('kafka')
host = '172.18.0.4'
port = 9092
timeout = 3  # seconds
print(socket.gethostname())  
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(timeout)
print(f'IP{ade}')
try:
    sock.connect((host, port))
    print(f"Connection to {host}:{port} succeeded!")
except (socket.timeout, ConnectionRefusedError):
    print(f"Connection to {host}:{port} failed.")
finally:
    sock.close()
