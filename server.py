import socket
import os
import noise
import ssl

sock = ssl.wrap_socket(socket.socket(), 'server.key', 'server.crt', True)
sock.bind( ('localhost', 9090) )
sock.listen(1)

conn, addr = sock.accept()
print('Client connected: ', addr[0])
while True:
    data = conn.recv(1024)
    if not data:
        break
    request = data.decode()
    print(addr[0], ' request - ' + request)
    fname = request[4:len(request)]
    try:
        fname = noise.add(fname, 'pepper')
        file = open(fname, 'rb')
        size = os.stat(fname).st_size
        info = 'File found! Size of ' + str(size/1024) + ' KB'
        conn.send(info.encode())
        conn.send(bytes(str(size), 'utf-8'))
        conn.send(file.read())
        file.close()
       #os.remove(fname)
    except FileNotFoundError:
        conn.send('No such file!'.encode())

conn.close()