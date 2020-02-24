import socket
import ssl
import cv2
import os
print('Подключение к серверу ...')
sock = ssl.wrap_socket(socket.socket())
sock.connect( ('localhost', 9090) )
print('Подключен')

while True:
    print('Введите get и название файла из предложенного списка. Или exit для выхода')
    files = os.listdir("image")
    print(files)
    k = input()
    if k[0:4] == 'get ':
        print('Поиск файла...')
        sock.send(k.encode())
        data = sock.recv(2048).decode()
        size = sock.recv(2048).decode('UTF-8')
        if data == 'Файл не найден!':
            print(data)
        else:
            print(data)
            new_name = 'downloaded_'+k[4:len(k)]
            downloaded_file = open(new_name,'wb')
            data2 = bytearray()
            while len(data2) != int(size):
                data2 += sock.recv(int(size))
            downloaded_file.write(data2)

            downloaded_file.close()
            median = cv2.medianBlur(cv2.imread(new_name), 5)
            cv2.imwrite(new_name, median)
            cv2.imshow('Загруженное изображение ', median)
            print('Файл скачен успешно!')
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.waitKey(1)
        print('')
    else:
        if k == 'exit':
            sock.close()
            print('Закрытие соединения...')
            break
        print('Неверный ввод')
print('Выключение...')