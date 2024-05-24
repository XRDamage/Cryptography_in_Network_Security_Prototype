from Cryptography import *
from DataPacket import *

class Device:
    def __init__(self, name, securityLevel, encryptionKey):
        self.securityLevel = securityLevel
        self.encryptionKey = encryptionKey
        self.name = name
        self.completeData = None

    def negotiateKeyLevel(self, otherDevice):
        return otherDevice.encryptionKey


    def sendData(self, data, otherDevice):
        # Encrypting and hashing data for transfer
        encData = Cryptography.asymmetricEncryption(data, self.negotiateKeyLevel(otherDevice))
        hashValue = Cryptography.hash(encData, f"private{self.securityLevel}.pem")
        # Sending data
        packet = DataPacket(encData, hashValue)
        otherDevice.receiveData(packet, self)
        
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports 


    def receiveData(self, dataPacket, otherDevice):
        # Decrypting data that was recieveds
        data = Cryptography.asymmetricDecryption(dataPacket.encryptedData, f"private{self.securityLevel}.pem")
        # Validating signature
        if not dataPacket.checkSignature(otherDevice.encryptionKey):
            print("Signiture was not verified!")
        else:
            print(f"Verified and recieved from {otherDevice.name}")
        
        print(data)
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports 


    def splitPackets(self, data):
        print()


    def reconstructPackets(self, data):
        print()