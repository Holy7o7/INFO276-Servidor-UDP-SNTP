import socket, time
from ntplib import NTPStats

#parametros para iniciar la conexion con el server
HOST, PORT = "localhost", 3000
data = 'hola mundo'
stats = NTPStats()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
i = 0

while(i < 10):
    sock.sendto(data.encode(), (HOST, PORT))
    received = sock.recv(1024)
    stats.from_data(received)

    print("enviado: ", data)
    print("Received: ", received)   
    print('Tiempo recibido por el usuario:', time.ctime(stats.tx_time))
    time.sleep(5)
    i = i + 1