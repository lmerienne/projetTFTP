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
            while 

        print('[{}:{}] client request: {}'.format(addr[0], addr[1], data))
        
    s.close()
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    # todo
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    targetname = open(filename,'rb')
    for line in targetname :
        s.sendto(line, (addr[0],addr[1]))

        
        





    pass

########################################################################


def get(addr, filename, targetname, blksize, timeout):
    # todo
    pass

# EOF