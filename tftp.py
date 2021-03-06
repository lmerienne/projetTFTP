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
            numero = 1
            print(socket_reception.getsockname())
            print("action PUT")
            print("adresse du client: ", addr_client[0])
            print("port du client : ", addr_client[1])
            ack = bytearray()
            ack.append(0)
            ack.append(4)
            ack.append(0)
            ack.append(numero-1)
            socket_reception.sendto(ack,addr_client)  
            del ack[:]                                    
            print("avant data")
            data , addr_client = socket_reception.recvfrom(1024)
            print("data = ",data)
            frame = data         
            frame1 = frame[0:2]                               
            frame2 = frame[2:]                                
            opcode = int.from_bytes(frame1, byteorder='big')
            if opcode == 5 :
                frame = data
                frame2 = frame[4:]
                print("ERROR")
                socket_reception.close()
            else :
                targetname = open(filename, 'wb')                           #ICI MODIFIÉ POUR LE VPL
                print("paquet envoyé par le client :", data)
                frame = data
                frame2 = frame[4:]
                numero += 1
                print("taille bloc de data :", len(frame2))
                while len(frame2) == 512 :
                    print("paquet à ecrire sur le fichier serveur :",frame2)
                    targetname.write(frame2)
                    ack.append(0)
                    ack.append(4)
                    ack.append(0)
                    ack.append(numero-1)
                    socket_reception.sendto(ack,addr_client)
                    del ack[:]
                    print("accuse de recpetion du paquet pour le client\n")
                    numero += 1
                    data,addr_client = socket_reception.recvfrom(1024)
                    frame = data
                    frame2 = frame [4:]
                print("dernier paquet à ecrire sur le fichier serveur :",frame2)
                targetname.write(frame2)
                ack.append(0)
                ack.append(4)
                ack.append(0)
                ack.append(numero-1)
                socket_reception.sendto(ack,addr_client)
                print("dernier accuse de recpetion de paquet pour le client\n")
                targetname.close()
                socket_reception.close()
                
                

                
            
    
        
        
        if opcode == 1 :
            socket_envoie = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            numero_bloc_data = 1                                       # QUAND LE SERVEUR RECOIT UNE REQUETE DE TYPE READ
            print("action READ\n")
            print("adresse du client: ", addr_client[0],"\n")
            print("port du client : ", addr_client[1])
            try:
                file_object = open(filename,'r+b')
            except Exception as e :
                requete = bytearray()
                requete.append(0)
                requete.append(5)               #OPCODE
                requete.append(0)
                requete.append(1)
                requete += bytearray(str(e).encode('utf-8'))
                requete.append(0)
                socket_envoie.sendto(requete,addr_client)
                print("ERROR :",bytearray(str(e).encode('utf-8')))
                socket_envoie.close()
                
            else :
                requete = bytearray()
                requete.append(0)
                requete.append(3)
                requete.append(0)
                requete.append(numero_bloc_data)                
                for line in file_object :
                    for i in line :  
                        if len(requete) - 4 == 512 :
                            print("requete = ",requete )
                            print("taille de la requete :",len(requete)) 
                            socket_envoie.sendto(requete,addr_client)
                            numero_bloc_data += 1
                            del requete[:]
                            requete.append(0)
                            requete.append(3)
                            requete.append(0)
                            requete.append(numero_bloc_data)
                        requete += bytearray(chr(i).encode('utf-8'))
                socket_envoie.sendto(requete,addr_client)
        
        
            
               
    s.close()
    pass

########################################################################
#                             CLIENT SIDE                              #
########################################################################


def put(addr, filename, targetname, blksize, timeout):
    # todo
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try :
        s.settimeout(int(timeout))
    except :
        s.settimeout(2)
    requete = bytearray()
    requete.append(0)
    requete.append(2)               #OPCODE
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    host = 'localhost'
    s.sendto(requete,(host,addr[1]))
    port_client = s.getsockname()
    print("[myclient:",port_client[1]," -> myserver :",addr[1],"] WRQ =",requete)
    #print("[myclient:",host," -> myserver:",addr[1],"] WRQ ",requete)
    numero_bloc_data = 1
    numero_bloc_ack = 0
    accuse_recep ,addr_serveur = s.recvfrom(512)
    if is_ack(accuse_recep): 
        print("[myserveur:",addr_serveur[1]," -> myclient:",port_client[1],"] ACK",numero_bloc_ack," =",accuse_recep, sep="")
        numero_bloc_ack += 1
        try :
            file_to_put = open(filename,'r+b')
        except Exception as e  :
            requete = bytearray()
            requete.append(0)
            requete.append(5)               #OPCODE
            requete.append(0)
            requete.append(1)
            requete += bytearray(str(e).encode('utf-8'))
            requete.append(0)
            host = 'localhost'
            s.sendto(requete,addr_serveur)
            print("ERROR :",bytearray(str(e).encode('utf-8')))
            sys.exit(1)
    

    del requete[:]
    requete.append(0)
    requete.append(3)
    requete.append(0)
    requete.append(numero_bloc_data)
    for line in file_to_put :
        for i in line :
            if len(requete) - 4 == 512 :
                if is_ack(accuse_recep) :
                    s.sendto(requete,addr_serveur)
                    print("[myclient:",port_client[1]," -> myserver :",addr_serveur[1],"] DAT",numero_bloc_data, "=",requete, sep="")
                    numero_bloc_data += 1
                    accuse_recep ,addr_serveur = s.recvfrom(512)
                    print("[myserveur:",addr_serveur[1]," -> myclient:",port_client[1],"] ACK",numero_bloc_ack," =",accuse_recep, sep="")
                    numero_bloc_ack += 1
                    del requete[:]
                    requete.append(0)
                    requete.append(3)
                    requete.append(0)
                    requete.append(numero_bloc_data)
            requete += bytearray(chr(i).encode('utf-8'))
    s.sendto(requete,addr_serveur)
    print("[myclient:",port_client[1]," -> myserver :",addr_serveur[1],"] DAT",numero_bloc_data, "=",requete, sep="")
    numero_bloc_data += 1
    accuse_recep ,addr_serveur = s.recvfrom(512)
    print("[myserveur:",addr_serveur[1]," -> myclient:",port_client[1],"] ACK",numero_bloc_ack," =",accuse_recep, sep="")
    numero_bloc_ack += 1
    s.close()
    pass



    

        
        


def get(addr, filename, targetname, blksize, timeout):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    requete =bytearray()
    requete.append(0)
    requete.append(1)                       #OPCODE
    filename = filename.encode('utf-8')
    requete += filename
    requete.append(0)
    mode = bytearray(bytes('octet', 'utf-8'))
    requete += mode
    requete.append(0)
    s.sendto(requete,('localhost',addr[1]))
    port_client = s.getsockname()
    print("[myclient:",port_client[1]," -> myserver :",addr[1],"] RRQ =",requete)
    data_retour,addr3 =s.recvfrom(1024)
    print("[myserver:",addr3[1]," -> myclient : ",port_client[1],"] DAT",1," =",data_retour, sep ="")
    frame = data_retour
    frame1 = data_retour[0:2]
    frame2 = frame[4:]
    print("taille des datas :",len(frame2))
    opcode = opcode = int.from_bytes(frame1, byteorder='big')
    if opcode == 5 :
        print("ERROR :",frame2)
        sys.exit(1)
    targetname = open(targetname,'w+b')
    args = frame2.split(b'\x00')
    numero = 1
    ack = bytearray()
    while len(frame2) == 512 :
        targetname.write(frame2)
        ack.append(0)
        ack.append(4)
        ack.append(0)
        ack.append(numero)
        s.sendto(ack,addr3)
        port_client = s.getsockname()
        print("[myclient:",port_client[1]," -> myserver:",addr3[1],"] ACK",numero," =",ack, sep ="")
        del ack[:]
        data_retour, addr3 =s.recvfrom(1024)
        print("[myserver:",addr3[1]," -> myclient : ",port_client[1],"] DAT",(numero+1)," =",data_retour, sep="")
        numero += 1
        frame = data_retour
        frame2 = frame[4:]
    if len(frame2) < 512 :
            ack.append(0)
            ack.append(4)
            ack.append(0)
            ack.append(numero)
            targetname.write(frame2)
            s.sendto(ack,addr3)
            print("[myclient:",port_client[1]," -> myserver:",addr3[1],"] ACK",numero,"= ",ack, sep ="")

        
    
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
    s.sendto(ack,addr_client)
    

def is_ack(data) :
    frame = data
    frame1 = frame[0:2]
    if int.from_bytes(frame1, byteorder='big') == 4 :
        return True 
    else :
        return False
