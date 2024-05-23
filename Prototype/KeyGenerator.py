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
    
    
    def generateAsymKeys():
        # Generating key-pairs
        pubKey, privKey = rsa.newkeys(1024)

        # Save public key to PEM file
        with open("public1.pem", "wb") as f:
            f.write(pubKey.save_pkcs1("PEM"))    
        print("Public key created successfully!")

        # Save private key to PEM file
        with open("private1.pem", "wb") as f:
            f.write(privKey.save_pkcs1("PEM"))
        print("Private key created successfully!")

    
    def generateDES_Key():
        pem_key = Random.get_random_bytes(24)
        # Save the key to a file
        with open("3DES.pem", "wb") as f:
            f.write(pem_key)
        