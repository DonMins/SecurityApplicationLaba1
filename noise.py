import numpy as np
import cv2
import ssl
import socket
import os
from PIL import Image


def add(im):
    amount = 0.003
    out = np.copy(im)
    num_salt = np.ceil(amount * im.size)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in im.shape]
    out[coords] = 0

    return out


sock = ssl.wrap_socket(socket.socket(), 'localhost.key', 'localhost.crt', True)
sock.bind(('localhost', 9092))
sock.listen(1)
conn, addr = sock.accept()
print('Сервер подключен: ', addr[0])

while True:
    try:
        fname = conn.recv(2048).decode()
        size = conn.recv(2048).decode('UTF-8')

        if len(fname) == 0 and len(size) == 0:
            raise ConnectionAbortedError('Сервер 1 отсоединился')

        data2 = bytearray()
        temp_name = fname[0:fname.rfind('.')] + '_temp' + fname[fname.rfind('.'):len(fname)]

        downloaded_file = open(temp_name, 'wb')

        while len(data2) != int(size):
            data2 += conn.recv(int(size))

        downloaded_file.write(data2)
        out = add(cv2.imread(temp_name))
        cv2.imwrite(temp_name, out)

        file = open(temp_name, 'rb')
        size = os.stat(temp_name).st_size

        conn.send(bytes(str(size), 'UTF-8'))
        conn.sendall(file.read())
        file.close()

    except (ConnectionAbortedError, ConnectionResetError, OSError):
        print("Сервер 1 отсоединился")
        conn.close()
        break
