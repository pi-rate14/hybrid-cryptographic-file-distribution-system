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
    input_text = input("Enter text to encrypt ")
    aes_key = 57811460909138771071931939740208549692
    ecc_obj_AESkey = ECC.ECC()
    private_key = 59450895769729158456103083586342075745962357150281762902433455229297926354304
    public_key = ecc_obj_AESkey.gen_pubKey(private_key)
    (C1_aesKey, C2_aesKey) = ecc_obj_AESkey.encryption(public_key, str(aes_key))
    print("C1_aesKey: " , C1_aesKey)
    print("C2_aesKey: " , C2_aesKey)
    aes = AES.AES(aes_key)
    encrypted_multimedia = aes.encryptBigData(input_text)
    print("encrypted multimedia: " , encrypted_multimedia)
    data_for_ecc = converter.makeSingleString(encrypted_multimedia)
    print("data for ecc: ", data_for_ecc)
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)
    print("C1_multimedia: " , C1_multimedia)
    print("C2_multimedia: " , C2_multimedia)
    ecc = ECC.ECC()
    (C1_multimedia, C2_multimedia) = ecc.encryption(public_key, data_for_ecc)

    cipher = {
        "file_type": "text",
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
    # input_file = input("Enter the name of file to decrypt> ")
    # data = converter.fileToBase64(input_file)[532:]
    # temp =
    # for i in range(len(data),0,-1):
    #     if data[i]=='=':

    # print(json.loads(data))
    C1_aesKey = data["C1_aesKey"]
    C2_aesKey = data["C2_aesKey"]
    private_key = data["private_key"]
    file_type = data["file_type"]
    # This is on the receiver side
    # Decrypt with ECC to get the AES key
    ecc_AESkey = ECC.ECC()
    decryptedAESkey = ecc_AESkey.decryption(C1_aesKey, C2_aesKey, private_key)
    print("decrypted AES key: ", decryptedAESkey)
    C1_multimedia = data["C1_multimedia"]
    C2_multimedia = data["C2_multimedia"]
    print("C1_multimedia: " , C1_multimedia)
    print("C2_multimedia: " , C2_multimedia)
    ecc_obj = ECC.ECC()
    encrypted_multimedia = ecc_obj.decryption(C1_multimedia, C2_multimedia, private_key)
    clean_data_list = converter.makeListFromString(encrypted_multimedia)
    aes_obj = AES.AES(int(decryptedAESkey))
    decrypted_multimedia = aes_obj.decryptBigData(clean_data_list)
    print("Decrypted Multimedia: ", decrypted_multimedia)


if __name__ == "__main__":
    main()
