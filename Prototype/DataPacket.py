import rsa

class DataPacket:
    def __init__(self, encryptedData, hashValue):
        self.encryptedData = encryptedData
        self.hashValue = hashValue

    def checkSignature(self, publicKey):
        # Openign the public key to check signiture
        with open (publicKey, "rb") as f:
            key = rsa.PublicKey.load_pkcs1(f.read())
        # Verifying signiture of sender
        try:
            rsa.verify(self.encryptedData, self.hashValue, key) == "SHA-256"
            return True
        except:
            return False