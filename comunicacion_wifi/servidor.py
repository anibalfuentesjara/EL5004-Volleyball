import socket
import sys

HOST = socket.gethostname() # Obtener nombre del host local
PORT = 88
print("Server en host {} puerto {}".format(HOST,PORT))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket creado")

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print(msg)
    sys.exit()

print('Socket bind complete')
info = "Coord1#Coord2#Velocidad" #Info a enviar
# Start listening on socket
s.listen(10)
print('Socket escuchando')

#Enviar info en cada request del cliente
while(True):
    conn, addr = s.accept()
    conn.send(info.encode())
    print("Datos enviados")
    conn.close()


s.close()
