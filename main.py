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

def main():
    # multimedia_data = input("Enter text to encrypt ")
    input_file = input(
        "Enter the name of file to encrypt present in ./test_files/ > ")
    file_type = input_file.split(".")[1]
    output_file = "test."+file_type

    # im = Image.open("test_files/"+input_file)
    # width, height = im.size
    # 1. Multimedia data -> Base64 Encoding and plain text
    multimedia_data = converter.fileToBase64("test_files/" + input_file)
    aes_key = 57811460909138771071931939740208549692
    ecc_obj_AESkey = ECC.ECC()
    private_key = 59450895769729158456103083586342075745962357150281762902433455229297926354304
    public_key = ecc_obj_AESkey.gen_pubKey(private_key)
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(public_key, str(aes_key))
    print("C1_aesKey: " , C1_aesKey, "\n\n")
    print("C2_aesKey: " , C2_aesKey, "\n\n")
    aes = AES.AES(aes_key)
    # encrypted_multimedia = aes.encryptBigData(input_text)
    encrypted_multimedia = aes.encryptBigData(multimedia_data)

    print("encrypted multimedia: " , encrypted_multimedia, "\n\n")
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    print("data for ecc: ", data_for_ecc)
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)
    print("C1_multimedia: " , C1_multimedia, "\n\n")
    print("C2_multimedia: " , C2_multimedia, "\n\n")
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
    with open('cipher.json') as f:
        data = json.load(f)
    #input_file = input("Enter the name of file to decrypt> ")
    #data = converter.fileToBase64(input_file)[532:]
    # temp =
    # for i in range(len(data),0,-1):
    #     if data[i]=='=':

    # print(json.loads(data))
    # C1_aesKey = data["C1_aesKey"]
    # C2_aesKey = data["C2_aesKey"]
    # private_key = data["private_key"]
    # file_type = data["file_type"]
    # # This is on the receiver side
    # # Decrypt with ECC to get the AES key
    # ecc_AESkey = ECC.ECC()
    # decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)
    # print("decrypted AES key: ", decryptedAESkey, "\n\n")
    # C1_multimedia = data["C1_multimedia"]
    # C2_multimedia = data["C2_multimedia"]
    # print("C1_multimedia: " , C1_multimedia, "\n\n")
    # print("C2_multimedia: " , C2_multimedia, "\n\n")
    # ecc_obj = ECC.ECC()
    # encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
    # clean_data_list = converter.makeListFromString(encrypted_multimedia)
    # aes_obj = AES.AES(int(decryptedAESkey))
    # decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    # print("Decrypted Multimedia: ", decrypted_multimedia, "\n\n")

    print(data)
    C1_aesKey = data["C1_aesKey"]
    C2_aesKey = data["C2_aesKey"]
    private_key = data["private_key"]
    file_type = data["file_type"]
    # This is on the receiver side
    # Decrypt with ECC to get the AES key
    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)

    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    # 1. Decrypt the data with ECC
    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)
    # 2. Decrypt with AES
    # aes_multimedia_data = AES.AES(int(hex(int(decryptedAESkey)),0))
    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    # 3. Decode from Base64 to the corresponding fileToBase64
    output_file = "test."+file_type
    converter.base64ToFile(decrypted_multimedia, output_file)
    delete = int(input("Delete File? 1/0:"))
    if(delete):
        import os
        os.remove(output_file)

if __name__ == "__main__":
    main()
