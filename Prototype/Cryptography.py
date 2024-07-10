import rsa
from cryptography.fernet import Fernet
import base64
from Crypto.Cipher import DES3
from Crypto import Random


class Cryptography:  
    def symmetricEncryption(data):
        # Reading Key from file
        with open("secretKey.pem", "rb") as f:
            pemKey = f.read()
        
        # Decoding the Base64 key
        pemKeyLines = pemKey.split(b"\n")
        b64Key = b"".join(pemKeyLines[1:-2])
        key = base64.b64decode(b64Key)

        # Initialising Fernet object
        fernet = Fernet(key)

        # Encrypting data and returning encrypted data
        return fernet.encrypt(data)

    
    def symmetricDecryption(data):
        # Reading Key from file
        with open("secretKey.pem", "rb") as f:
            pemKey = f.read()
        
        # Decoding the Base64 key
        pemKeyLines = pemKey.split(b"\n")
        b64Key = b"".join(pemKeyLines[1:-2])
        key = base64.b64decode(b64Key)

        # Initialising Fernet object
        fernet = Fernet(key)

        # Decrypting data and returning decrypted data
        code = fernet.decrypt(data)
        return code

    
    def asymmetricEncryption(data, publicKey):
        # Opening the public Key file
        with open(publicKey) as f:
            rkey = rsa.PublicKey.load_pkcs1(f.read())
        # Encrypting the data using public key
        encData = rsa.encrypt(data, rkey)

        # Encryptiong using 3DES
        with open("3DES.pem", "rb") as f:
            key = f.read()

        # Padding Data
        iv = Random.new().read(DES3.block_size)
        cipher = DES3.new(key, DES3.MODE_OFB, iv)
        output = cipher.encrypt(encData)

        iv_encData = iv + output

        return iv_encData
    

    def asymmetricDecryption(data, privateKey):
        # Decrypting using 3DES
        with open("3DES.pem", "rb") as f:
            key = f.read()

        # Removing the padding
        iv = data[:DES3.block_size]
        encData = data[DES3.block_size:]

        cipher = DES3.new(key, DES3.MODE_OFB, iv)
        decData = cipher.decrypt(encData)

        # Opening the private Key file
        with open(privateKey) as f:
            rkey = rsa.PrivateKey.load_pkcs1(f.read())
        # Decryptign the data using private key
        plainData = rsa.decrypt(decData, rkey)
        return plainData

    
    def hash(data, privateKey):
        # Loading the private key to sign encrypted data
        with open(privateKey, "rb") as f:
            key = rsa.PrivateKey.load_pkcs1(f.read())
        # Creating signature
        signature = rsa.sign(data, key, "SHA-256")
        return signature