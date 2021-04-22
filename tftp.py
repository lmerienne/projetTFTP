"""
TFTP Module.
"""

import socket
import sys
import os
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
        if args[2].decode('ascii') != '':
            blksize = args[2].decode('ascii')
        else :
            blksize = 512
        copie = "blksize"
        print("copie =",copie)
        print("blksize =",blksize)
        if blksize == copie :
            print("entree dans if")
            taille_bloc = args[3].decode('utf-8')
            taille_bloc = int(taille_bloc)
            print("taille bloc =", taille_bloc)
        else :
            taille_bloc = 512
            print("taille bloc =",taille_bloc)

        
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
                while len(frame2) == taille_bloc :
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
                fichier_entier_taille = os.path.getsize(filename)
                print("taille fichier =", fichier_entier_taille)
                print("entree dans else")
                requete = bytearray()
                requete.append(0)
                requete.append(3)
                requete.append(0)
                requete.append(numero_bloc_data)                
                """for line in file_object :
                    for i in line :  
                        if (len(requete) - 4) == taille_bloc :
                            print("requete = ",requete)
                            print("taille de la requete :",len(requete)) 
                            socket_envoie.sendto(requete,addr_client)
                            numero_bloc_data += 1
                            del requete[:]
                            requete.append(0)
                            requete.append(3)
                            requete.append(0)
                            requete.append(numero_bloc_data)
                            
                        requete += bytearray(chr(i).encode('utf-8'))
                        print("taille requete =",len(requete) - 4)
                        print("taille bloc blksize =", taille_bloc)
                socket_envoie.sendto(requete,addr_client)"""
                
                emplacement = taille_bloc
                nombre_octets_restants = fichier_entier_taille
                if fichier_entier_taille >= taille_bloc :
                    partie_fichier = file_object.read(taille_bloc)
                    print("partie_fichier =",partie_fichier)
                    requete += bytearray(partie_fichier)
                    print("requete premier ajout :",requete)
                    socket_envoie.sendto(requete,addr_client)
                    numero_bloc_data += 1
                    del requete[:]
                    requete.append(0)
                    requete.append(3)
                    requete.append(0)
                    requete.append(numero_bloc_data)
                    nombre_octets_restants -= taille_bloc
                    file_object.seek(emplacement)
                    
                else :
                    fichier_entier = file_object.read()
                    requete += bytearray(fichier_entier)
                    print("requete quand inferieur a taille blksize",requete)
                    socket_envoie.sendto(requete, addr_client)
                accuse_recep, addr_client = socket_envoie.recvfrom(512)
                while nombre_octets_restants >= taille_bloc :
                    print("nombre octets restants =", nombre_octets_restants)
                    if is_ack(accuse_recep) :
                        partie_fichier = file_object.read(taille_bloc)
                        emplacement += taille_bloc
                        print("data à put :", partie_fichier)
                        requete += bytearray(partie_fichier)
                        print("requete a envoyé :",requete)
                        socket_envoie.sendto(requete,addr_client)
                        numero_bloc_data += 1
                        del requete[:]
                        requete.append(0)
                        requete.append(3)
                        requete.append(0)
                        requete.append(numero_bloc_data)
                        nombre_octets_restants -= taille_bloc
                        file_object.seek(emplacement)
                        accuse_recep, addr_client = socket_envoie.recvfrom(512)
                if is_ack(accuse_recep) :
                    partie_fichier = file_object.read(taille_bloc)
                    emplacement += taille_bloc
                    print("data à put :", partie_fichier)
                    requete += bytearray(partie_fichier)
                    print("requete a envoyé :",requete)
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
    print("blksize =",blksize)
    if blksize != 512 :
        taille_bloc = bytearray(bytes('blksize','utf-8'))
        requete += taille_bloc
        requete.append(0)
        requete += bytearray(bytes(str(blksize),'utf-8'))
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
            file_object = open(filename,'r+b')
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
    """for line in file_to_put :
        for i in line :
            if (len(requete) - 4) == blksize :
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
    numero_bloc_ack += 1"""

    fichier_entier_taille = os.path.getsize(filename)
    print("taille fichier =", fichier_entier_taille)
    requete = bytearray()
    requete.append(0)
    requete.append(3)
    requete.append(0)
    requete.append(numero_bloc_data)                
    emplacement = blksize
    nombre_octets_restants = fichier_entier_taille
    if fichier_entier_taille >= blksize:
        partie_fichier = file_object.read(blksize)
        requete += bytearray(partie_fichier)
        print("requete premier ajout :",requete)
        s.sendto(requete,addr_serveur)
        numero_bloc_data += 1
        del requete[:]
        requete.append(0)
        requete.append(3)
        requete.append(0)
        requete.append(numero_bloc_data)
        nombre_octets_restants -= blksize
        file_object.seek(emplacement)
        
    else :
        fichier_entier = file_object.read()
        requete += bytearray(fichier_entier)
        print("requete quand inferieur a taille blksize",requete)
        s.sendto(requete, addr_serveur)
    accuse_recep, addr_serveur = s.recvfrom(512)
    while nombre_octets_restants >= blksize :
        print("nombre octets restants =", nombre_octets_restants)
        if is_ack(accuse_recep) :
            partie_fichier = file_object.read(blksize)
            emplacement += blksize
            print("data à put :", partie_fichier)
            requete += bytearray(partie_fichier)
            print("reqauete =",requete)
            s.sendto(requete,addr_serveur)
            numero_bloc_data += 1
            del requete[:]
            requete.append(0)
            requete.append(3)
            requete.append(0)
            requete.append(numero_bloc_data)
            nombre_octets_restants -= blksize
            file_object.seek(emplacement)
            accuse_recep, addr_serveur = s.recvfrom(512)
    if is_ack(accuse_recep) :
        partie_fichier = file_object.read()
        emplacement += blksize
        print("data à put :", partie_fichier)
        requete += bytearray(partie_fichier)
        print("requete a envoyé :",requete)
        s.sendto(requete,addr_serveur)

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
    if blksize != 512 :
        taille_bloc = bytearray(bytes('blksize','utf-8'))
        requete += taille_bloc
        requete.append(0)
        requete += bytearray(bytes(str(blksize),'utf-8'))
        requete.append(0)
    print("blksize =", blksize)
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
    while len(frame2) == blksize :
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
    if len(frame2) < blksize :
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





