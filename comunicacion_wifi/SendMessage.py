"""
Codigo para enviar mensajes al arduino via comunicacion wifi.
Se ingresa un mensaje como input a la consola y se envia este mensaje al arduino.
"""

import socket

s = socket.socket()
s.connect(('192.168.43.99',80))

while True:
    msg = input()
    s.sendall(msg.encode())
    
s.close()