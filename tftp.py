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
        s.sendto(data,addr_client)
        if opcode == 1 :                                        #read request
            print("action READ\n")
            print("adresse du client: ", addr_client[0],"\n")
            print("port du client : ", addr_client[1])
            try:
                file_object = open(filename,'rb')
            except Exception as e :
                print("ERROR:", e)
            socket_connecté = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_connecté.sendto(bytearray(str(addr_client[1]).encode('ascii')),addr_client)
            requete = bytearray()
            requete.append(0)
            requete.append(3)                    
            for line in file_object :
                requete += line
            socket_connecté.sendto(requete,addr_client)
            
        if opcode == 2 :
            print("action GET")
            print("adresse du client: ", addr_client[0])
            print("port du client : ", addr_client[1])
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
    host = 'localhost'
    s.sendto(requete,(host,6969))
    print("[myclient:",host," -> myserver:6969] WRQ")
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
    s.sendto(requete,('localhost',addr[1]))
    data,addr1 = s.recvfrom(512)
    port, addr2 = s.recvfrom(512)
    try :
        data_retour,addr3 =s.recvfrom(512)
    except :
        print("error\n")
    ack = bytearray()
    ack.append(0)
    ack.append(4)
    s.sendto(ack,addr3)
    print("[myclient:",int(port)," -> myserver :",addr[1],"] RRQ =",data)
    print("[myserver:",int(addr2[1])," -> myclient : ",int(port),"] DAT1 =",data_retour)
    print("[myclient:",int(port)," -> myserver:",addr2[1],"] ACK1 =",ack)


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

