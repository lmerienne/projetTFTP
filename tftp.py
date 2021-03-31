"""
TFTP Module.
"""

import socket
import sys

########################################################################
#                          COMMON ROUTINES                             #
########################################################################

# todo

########################################################################
#                             SERVER SIDE                              #
########################################################################


def runServer(addr, timeout, thread):
    # todo
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((addr[0], addr[1]))
    
    while True:
        data, addr = s.recvfrom(512)
        frame = data         
        frame1 = frame[0:2]                               
        frame2 = frame[2:]                                
        opcode = int.from_bytes(frame1, byteorder='big')  
        args = frame2.split(b'\x00')                      
        filename = args[0].decode('ascii')                
        mode = args[1].decode('ascii') 
        if opcode == 1 :                                        #read request
            file_objet = open(filename,'rb')                    
            for line in file_object :
                s.sendto(line,addr)
        if opcode == 2 :                                       #write request
            file_object = open(filename,'wb')
            for line in file_object :


        print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
        
    s.close()
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    # todo
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    requete = bytearray()
    requete.append(0)
    requete.append(2)
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    s.sendto(requete,addr)
    targetname = open(filename,'rb')
    for line in targetname :
        s.sendto(line, addr)

        
        





    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    # todo
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    requete = bytearray()
    requete.append(0)
    requete.append(1)
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    s.sendto(requete,addr)
    pass

# EOF