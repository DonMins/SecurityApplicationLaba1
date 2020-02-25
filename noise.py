import numpy as np
import cv2
import ssl
import socket

def add(image_name):
    image_name.rfind('.')
    im = cv2.imread(image_name)
    amount = 0.03
    out = np.copy(im)
    num_salt = np.ceil(amount * im.size )
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in im.shape]
    out[coords] = 255

    temp_name = image_name[0:image_name.rfind('.')] + '_temp' + image_name[image_name.rfind('.'):len(image_name)]
    cv2.imwrite(image_name[0:image_name.rfind('.')]+'_temp'+image_name[image_name.rfind('.'):len(image_name)],out)
    return temp_name

sock = ssl.wrap_socket(socket.socket(), 'localhost.key', 'localhost.crt', True)
sock.bind( ('localhost', 9091) )
sock.listen(1)
conn, addr = sock.accept()
print('Сервер подключен: ', addr[0])
while True:
    try:
        data = conn.recv(2048).decode()
        size = conn.recv(2048).decode('UTF-8')

        data2 = bytearray()
        downloaded_file = open("new_name.jpg", 'wb')

        while len(data2) != int(size):
            data2 += sock.recv(int(size))

        downloaded_file.write(data2)


    except FileNotFoundError:
        conn.send('Файл не найден!'.encode())
    except (ConnectionAbortedError, ConnectionResetError, OSError):
        print("Соединение разорвано")
        conn.close()
        break


