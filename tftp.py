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
        
        if opcode == 2 :                                                                # LORSQUE LE SERVEUR RECOIT UNE REQUÈTE DE TYPE WRITE 
            socket_reception = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(socket_reception.getsockname())
            print("action PUT")
            print("adresse du client: ", addr_client[0])
            print("port du client : ", addr_client[1])
            send_ack(addr_client, socket_reception)                                       
            targetname = open("targetname.txt", 'wb')
            data , addr_client = socket_reception.recvfrom(512)
            print("data envoyé pour le put :", data)
            frame = data
            frame2 = frame[2:]
            print("frame2 =",frame2)
            args = frame2.split(b'\x00')
            print("args =", args)
            while len(frame2) <= 512 :
                if len(frame2) < 512 :
                    for i in range (len(args)) :
                        targetname.write(args[i])
                        print("requete data de taille inferieure à 512 octets !")
                    break
                for i in range (len(args)) :
                    targetname.write(args[i])
                data, addr3 =s.recvfrom(512)
                
            
    
        
        
        if opcode == 1 :
            numero_bloc_data = 1
            s.sendto(data,addr_client)                                         # QUAND LE SERVEUR RECOIT UNE REQUETE DE TYPE READ
            print("action READ\n")
            print("adresse du client: ", addr_client[0],"\n")
            print("port du client : ", addr_client[1])
            try:
                file_object = open(filename,'r+b')
            except Exception as e :
                print("ERROR:", e)
            socket_envoie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            socket_envoie.sendto(bytearray(str(addr_client[1]).encode('ascii')),addr_client)
            requete = bytearray()
            requete.append(0)
            requete.append(3)
            requete.append(numero_bloc_data)                
            for line in file_object :
                for i in line :   
                    if len(requete) >= 512 :
                        socket_envoie.sendto(requete,addr_client)
                        numero_bloc_data += 1
                        del requete[:]
                        requete.append(0)
                        requete.append(3)
                        requete.append(numero_bloc_data)
                    requete += bytearray(chr(i).encode('ascii'))
            socket_envoie.sendto(requete,addr_client)
            
            
               
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
    print("[myclient:",host," -> myserver:",addr[1],"] WRQ ",requete)
    accuse_recep , addr = s.recvfrom(512)
    print("accuse_recep :",accuse_recep)
    if is_ack(accuse_recep) :
        print("dans le ack")
        file_to_put = open(filename,'r+b')
        for line in file_to_put :
                print("ce qui doit etre put :",line)
                s.sendto(line,addr)
    s.close()
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
    #try :
    targetname = open(targetname,'w+b')
    data_retour,addr3 =s.recvfrom(512)
    print("data retourné par le serveur :", data_retour)
    frame = data_retour
    frame2 = frame[3:]
    args = frame2.split(b'\x00')
    numero = 0
    while len(data_retour) == 512 :
        print("taille du bloc = ",len(data_retour))
        targetname.write(frame2)
        data_retour, addr3 =s.recvfrom(512)
        send_ack(addr3,s,numero)
        numero += 1
        print("ack envoyé au serveur numero ",numero)
        frame = data_retour
        frame2 = frame[3:]
        print("data de retour :",data_retour)
    if len(data_retour) < 512 :
            print("taille du bloc = ",len(data_retour))
            targetname.write(frame2)
            send_ack(addr3,s,numero)
            print("ack envoyé au serveur numero",3)
            print("requete data de taille inferieure à 512 octets !")
        
    
    #except :
     #   print("error\n")
    #print("[myclient:",int(port)," -> myserver :",addr[1],"] RRQ =",data)
    #print("[myserver:",int(addr2[1])," -> myclient : ",int(port),"] DAT1 =",data_retour)
    #print("[myclient:",int(port)," -> myserver:",addr2[1],"] ACK1 =",ack)


    s.close()
    pass

# EOF

def send_ack(addr_client, s,numero) :
    ack = bytearray()
    ack.append(0)
    ack.append(4)
    ack.append(0)
    ack.append(numero)
    print('ack = ',ack)
    s.sendto(ack,addr_client)
    

def is_ack(data) :
    frame = data
    frame1 = frame[0:2]
    if int.from_bytes(frame1, byteorder='big') == 4 :
        return True 
    else :
        return False

