# dependency
import hashlib
import os
import random
import numpy as np
from PIL import Image
from helper_PLS import handle_PLS

PLS_obj = handle_PLS()


class LSB(object):
    def __init__(self):
        self.img = Image.open("./images/input.png")
        self.PLS = []
        [self.row, self.col] = self.img.size

    def DataListInBit(self, data):
        dataBits = list(format(c, '08b')
                        for c in bytearray(data.encode('latin-1')))
        return dataBits

    def PLSgen(self, row, col, lenEncodedText):
        new = []
        for i in range(row * col):
            new.append(i)
        for i in range(len(new) - 1, 0, -1):
            j = random.randint(0, i + 1)
            new[i], new[j] = new[j], new[i]
        for i in range(lenEncodedText * 3):
            self.PLS.append(new[i])
        pixelLocaterSequence = np.array(self.PLS)
        np.savetxt("./generated-data/pls.txt",
                   pixelLocaterSequence, delimiter="\t")

    def LSB_Encoding(self, encodedText):
        self.PLSgen(self.row, self.col, len(encodedText))
        dataBits = self.DataListInBit(encodedText)
        dr = 0
        for i in range(0, len(encodedText) * 3, 3):
            dc = 0
            for j in range(0, 3):
                rr = self.PLS[i + j] // self.col
                rc = self.PLS[i + j] % self.col
                rgb = self.img.getpixel((rr, rc))
                value = []
                idx = 0
                for k in rgb:
                    if (k % 2 == 0 and dataBits[dr][dc] == '1'):
                        if (k == 0):
                            k += 1
                        else:
                            k -= 1
                    if (k % 2 == 1 and dataBits[dr][dc] == '0'):
                        k -= 1
                    value.append(k)
                    idx += 1
                    dc += 1
                    if (dc >= 8):
                        break
                if (dc >= 8):
                    value.append(rgb[2])
                newrgb = (value[0], value[1], value[2])
                self.img.putpixel((rr, rc), newrgb)
            dr += 1
        self.img.save("./images/output.png")
        plsPassword = input("password for PLS encyption : ")
        key = hashlib.sha256(plsPassword.encode()).digest()
        PLS_obj.encrypt_file(key, './generated-data/pls.txt')

    def LSB_Decoding(self):
        plspassword = input("password for PLS decryption : ")
        key = hashlib.sha256(plspassword.encode()).digest()
        PLS_obj.decrypt_file(
            key, './generated-data/pls.txt.enc', './generated-data/out.txt')
        pls = np.genfromtxt('./generated-data/out.txt', delimiter='\t')
        if os.path.exists("./generated-data/out.txt"):
            os.remove("./generated-data/out.txt")
        if os.path.exists("./generated-data/pls.txt.enc"):
            os.remove("./generated-data/pls.txt.enc")
        decodedTextInBits = []
        stegoImage = Image.open("./images/output.png")
        for i in range(0, len(pls), 3):
            ithChar = ""
            for j in range(0, 3):
                rr = pls[i + j] // self.col
                rc = pls[i + j] % self.col
                rgb = stegoImage.getpixel((rr, rc))
                for k in rgb:
                    if (k & 1):
                        ithChar += '1'
                    else:
                        ithChar += '0'
            ithChar = ithChar[:-1]
            decodedTextInBits.append((ithChar))
        decodedText = ''
        for i in decodedTextInBits:
            decodedText += chr(int(i, 2))
        return decodedText
