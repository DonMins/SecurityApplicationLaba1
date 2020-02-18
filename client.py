import socket
import ssl
import cv2

print('Подключение к серверу ...')
sock = ssl.wrap_socket(socket.socket())
sock.connect( ('localhost', 9090) )
print('Подключен')

while True:
    print('Type "get" and image name to download image file...')
    k = input()
    if k[0:4] == 'get ':
        print('Searching for file...')
        sock.send(k.encode())
        data = sock.recv(2048).decode()
        size = sock.recv(2048).decode('utf-8')
        if data == 'No such file!':
            print(data)
        else:
            print(data)
            new_name = 'downloaded_'+k[4:len(k)]
            downloaded_file = open(new_name,'wb')
            # data = sock.recv(4096000)
            data = sock.recv(int(size))
            downloaded_file.write(data)
            downloaded_file.close()
            median = cv2.medianBlur(cv2.imread(new_name), 1)
            cv2.imwrite(new_name, median)
            cv2.imshow('Downloaded image', median)
            print('File downloaded successfully!')
            cv2.waitKey(0)
        print('')
    else:
        if k == 'exit':
            sock.close()
            print('Closing connection...')
            break
        print('Invalid input')
print('Shutting down...')