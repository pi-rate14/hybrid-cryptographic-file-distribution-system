import socket
from threading import Thread
import sys
import random
import json
import re
import base64
from AES_module import AES
from ECC_module import ECC
from Convert import converter
from PIL import Image
import ast



TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))

    def run(self):
        filename='cipher.json'
        f = open(filename,'rb')
        while True:
            l = f.read(BUFFER_SIZE)
            while (l):
                self.sock.send(l)
                #print('Sent ',repr(l))
                l = f.read(BUFFER_SIZE)
            if not l:
                f.close()
                self.sock.close()
                break

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    # multimedia_data = input("Enter text to encrypt ")
    input_file = input(
        "Enter the name of file to encrypt present in ./test_files/ > ")
    file_type = input_file.split(".")[1]
    output_file = "test."+file_type
    print("Uploading file...Please Wait...")
    # im = Image.open("test_files/"+input_file)
    # width, height = im.size
    # 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64("test_files/" + input_file)
    aes_key = 57811460909138771071931939740208549692
    ecc_obj_AESkey = ECC.ECC()
    private_key = 59450895769729158456103083586342075745962357150281762902433455229297926354304
    public_key = ecc_obj_AESkey.gen_pubKey(private_key)
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(public_key, str(aes_key))
    # print("C1_aesKey: " , C1_aesKey, "\n\n")
    # print("C2_aesKey: " , C2_aesKey, "\n\n")
    aes = AES.AES(aes_key)
    # encrypted_multimedia = aes.encryptBigData(input_text)
    encrypted_multimedia = aes.encryptBigData(multimedia_data)

    # print("encrypted multimedia: " , encrypted_multimedia, "\n\n")
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    # print("data for ecc: ", data_for_ecc)
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)
    # print("C1_multimedia: " , C1_multimedia, "\n\n")
    # print("C2_multimedia: " , C2_multimedia, "\n\n")
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)

    cipher = {
        "file_type": file_type,
        "C1_aesKey": C1_aesKey,
        "C2_aesKey": C2_aesKey,
        "C1_multimedia": C1_multimedia,
        "C2_multimedia": C2_multimedia,
        "private_key": private_key
    }
    with open('cipher.json', 'w') as fp:
        json.dump(cipher, fp)
    converter.encodeStringinImage(json.dumps(cipher), "success.jpg", "JPEG")
    print ("File uploaded. Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()