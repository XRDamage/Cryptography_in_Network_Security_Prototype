from cryptography.fernet import Fernet
import base64
import rsa
from Crypto import Random

class KeyGenerator: 
    def generateSecretKey():
        # Generate Secret Key
        genKey = Fernet.generate_key()
        
        # Encoding key as base64
        pem_key = b"-----BEGIN FERNET KEY-----\n"
        pem_key += base64.encodebytes(genKey)
        pem_key += b"-----END FERNET KEY-----\n"

        # Save the key to PEM file
        with open("secretKey.pem", "wb") as f:
            f.write(pem_key)

        print("Secret key created successfully!")
    
    
    def generateAsymKeys(level):
        if int(level) == 1:
            size = 2048
        elif int(level) == 2:
            size =  3072
        elif int(level) == 3:
            size = 4096
        else:
            return None
        # Generating key-pairs
        pubKey, privKey = rsa.newkeys(size)

        # Save private key to PEM file
        with open("private.pem", "wb") as f:
            f.write(privKey.save_pkcs1("PEM"))
        print("Private key created successfully!")

        # Returning key to save in database
        return pubKey.save_pkcs1("PEM")

    
    def generateDES_Key():
        pem_key = Random.get_random_bytes(24)
        # Save the key to a file
        with open("3DES.pem", "wb") as f:
            f.write(pem_key)
        