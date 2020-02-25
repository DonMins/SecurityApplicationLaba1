import socket
import os
import ssl

sock = ssl.wrap_socket(socket.socket(), 'localhost.key', 'localhost.crt', True)
sock.bind(('localhost', 9093))
sock.listen(1)

sock2 = ssl.wrap_socket(socket.socket())
sock2.connect(('localhost', 9092))

conn, addr = sock.accept()
print('Клиент подключен: ', addr[0])

while True:
    try:
        data = conn.recv(2048)

        request = data.decode()
        print(addr[0], ' request - ' + request)
        fname = request[4:len(request)]

        file = open("image\\" + fname, 'rb')
        size = os.stat("image\\" + fname).st_size
        info = 'Файл найден! Размер ' + str(size / 1024) + ' KB'

        sock2.send(fname.encode())
        sock2.send(bytes(str(size), 'UTF-8'))
        sock2.sendall(file.read())

        size = sock2.recv(2048).decode('UTF-8')
        data2 = bytearray()

        while len(data2) != int(size):
            data2 += sock2.recv(int(size))

        conn.send(info.encode())
        conn.send(bytes(str(size), 'UTF-8'))
        conn.sendall(data2)
        file.close()

    except FileNotFoundError:
        conn.send('Файл не найден!'.encode())
    except (ConnectionAbortedError, ConnectionResetError, OSError):
        print("Клиент отсоединился")
        sock2.close()
        break
