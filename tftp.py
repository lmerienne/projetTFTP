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
    print("le serveur est à l'écoute sur le port",addr[1],"..")
    
    while True:
        data, addr_client = s.recvfrom(512)
        print("data reçu par le serveur :",data)
        frame = data         
        frame1 = frame[0:2]                               
        frame2 = frame[2:]                                
        opcode = int.from_bytes(frame1, byteorder='big')  
        args = frame2.split(b'\x00')                      
        filename = args[0].decode('ascii')                
        mode = args[1].decode('ascii') 
        if opcode == 1 :                                        #read request
            print("action READ\n")
            try:
                file_object = open(filename,'rb')
            except Exception as e :
                print("ERROR:", e)
            requete = bytearray()
            requete.append(0)
            requete.append(3)                    
            for line in file_object :
                requete += line
            s.sendto(requete,addr_client)
        if opcode == 2 :
            print("action GET\n")
            send_ack(addr_client, s)                                       #write request
            file_to_put = open(filename,'rb')
            targetname = open("targetname.txt", 'wb')
            for line in file_to_put :
                print("ce qui doit etre put :",line)
                targetname.write(line)

                
                
            
    s.close()
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    # todo
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    requete = bytearray()
    requete.append(0)
    requete.append(2)
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    s.sendto(requete,('localhost',6969))
    print("[myclient:",addr[1]," -> myserver:6969] WRQ")
    accuse_recep , addr = s.recvfrom(512)
    #if is_ack(accuse_recep) :
    pass



    

        
        


def get(addr, filename, targetname, blksize, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    requete =bytearray()
    requete.append(0)
    requete.append(1)
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    print("requete émise :",requete)
    s.sendto(requete,('localhost',6969))
    data, addr = s.recvfrom(512)
    print(data)

    s.close()
    pass

# EOF

def send_ack(addr_client, s) :
    ack = bytearray()
    ack.append(0)
    ack.append(4)
    s.sendto(ack,addr_client)

def is_ack(data) :
    frame = data
    frame1 = frame[0:2]
    if int.from_bytes(frame1, byteorder='big') == 4 :
        return True 
    else :
        return False