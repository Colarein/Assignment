import socket
import struct

MCAST_GRP = '239.255.255.250'
MCAST_PORT = 5007

def headerValue(response, header):
    source = response.splitlines()
    for line in source:
        if line.startswith(header):
            return line[line.find(":")+1:]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,  socket.SO_REUSEPORT, 1)

sock.bind((MCAST_GRP, MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


while True:
    data, address = sock.recvfrom(4096)
    data = str(data.decode('UTF-8'))
    print('Received ' + str(len(data)) + ' bytes from ' + str(address))
    if headerValue(data,"ST") == 'urn:sense_pi':
        print('responding...')
        sent = sock.sendto(str("I'm Here!").encode(), address)
