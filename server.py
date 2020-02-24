import socket
import os
import noise
import ssl

sock = ssl.wrap_socket(socket.socket(), 'localhost.key', 'localhost.crt', True)
sock.bind( ('localhost', 9090) )
sock.listen(1)

conn, addr = sock.accept()
print('Client connected: ', addr[0])
while True:
    data = conn.recv(2048)
    if not data:
        break
    request = data.decode()
    print(addr[0], ' request - ' + request)
    fname = request[len(request)]
    try:
        fname = noise.add(fname, 'salt')
        file = open(fname, 'rb')
        size = os.stat(fname).st_size
        info = 'File found! Size of ' + str(size/1024) + ' KB'
        conn.send(info.encode())
        conn.send(bytes(str(size), 'UTF-8'))
        conn.sendall(file.read())
        file.close()
    except FileNotFoundError:
        conn.send('No such file!'.encode())
    except (ConnectionAbortedError, ConnectionResetError):
        print("fdg")
        conn.close()