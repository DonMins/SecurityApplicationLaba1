import socket
import os
import ssl

sock = ssl.wrap_socket(socket.socket(), 'localhost.key', 'localhost.crt', True)
sock.bind( ('localhost', 9090) )
sock.listen(1)

conn, addr = sock.accept()
print('Клиент подключен: ', addr[0])
while True:
    try:
        data = conn.recv(2048)
        if not data:
            break
        request = data.decode()
        print(addr[0], ' request - ' + request)
        fname = request[4:len(request)]


        file = open("image\\" + fname, 'rb')
        size = os.stat("image\\" + fname).st_size
        info = 'Файл найден! Размер ' + str(size/1024) + ' KB'

        sock = ssl.wrap_socket(socket.socket())
        sock.connect(('localhost', 9091))
        print('Подключен')
        conn.send(info.encode())
        sock.send(bytes(str(size), 'UTF-8'))
        sock.sendall(file.read())

        # fname = noise.add("image\\" + fname)

        # file = open(fname, 'rb')
        # size = os.stat(fname).st_size
        # info = 'Файл найден! Размер ' + str(size/1024) + ' KB'
        conn.send(info.encode())
        conn.send(bytes(str(size), 'UTF-8'))
        conn.sendall(file.read())
        file.close()
    except FileNotFoundError:
        conn.send('Файл не найден!'.encode())
    except (ConnectionAbortedError, ConnectionResetError, OSError):
        print("Соединение разорвано")
        conn.close()
        break