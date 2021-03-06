import numpy as np

class ExtensionAudio:
    @staticmethod
    def getLengthHeader(name):
        data = {'wav':44}
        try:
            return data[name]
        except KeyError as e:
            raise "NonExtension"


int2bytes = lambda array: np.array(array, dtype='<u1').tobytes()
arrayBytes = lambda block, secret: [byte|1 if int(bit) == 1 else byte&254  for element in secret for byte, bit in zip(block, '{0:08b}'.format(ord(element))) ]

lenbinary4lenSecret = 32

def encrypt(inFile, outFile, secret):
    try:
        lenHeader = ExtensionAudio.getLengthHeader(inFile.split('.')[-1])
    except:
        return "Can not detect extension of file input"
    
    file = open(inFile,'rb').read()
    _lenSecret, _lenFile = len(secret) * 8, len(file) - lenHeader - lenbinary4lenSecret//8

    if _lenSecret > _lenFile:
        return "The size of file input is not enough to contain secret"

    out = open(outFile,'wb')
    out.write(file[:lenHeader])

    block4len = file[lenHeader:lenHeader + lenbinary4lenSecret]
    lenSecret = "{0:032b}".format(len(secret))
    
    arrBytes = [byte|1 if int(bit) == 1 else byte&254 for byte,bit in zip(block4len, lenSecret)]

    out.write(int2bytes(arrBytes))

    block4secret = file[lenHeader + lenbinary4lenSecret:lenHeader + len(secret) * 8 + lenbinary4lenSecret]

    out.write(int2bytes(arrayBytes(block4secret, secret)))
    out.write(file[lenHeader + len(secret) * 8 + lenbinary4lenSecret:])
    out.close()
    return "Success"

def decrypt(inFile):
    try:
        lenHeader = ExtensionAudio.getLengthHeader(inFile.split('.')[-1])
    except:
        return "Non Extension"

    file = open(inFile,'rb').read()[lenHeader:]

    block4len = file[:lenbinary4lenSecret]

    lenSecret = int(''.join(['%s'%(byte&1) for byte in block4len]), 2)

    block4secret = file[lenbinary4lenSecret:lenbinary4lenSecret + lenSecret * 8]

    return ''.join([chr(int(''.join(['%s'%(byte&1) for byte in block4secret[step * 8 : (step + 1) * 8]]),2)) for step in range(0,len(block4secret)//8)])   
