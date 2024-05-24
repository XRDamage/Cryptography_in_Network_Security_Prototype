from Cryptography import *
from DataPacket import *

class Device:
    def __init__(self, securityLevel, encryptionKey):
        self.securityLevel = securityLevel
        self.encryptionKey = encryptionKey
        self.completeData = ""

    def negotiateKeyLevel(self, otherDevice):
        return otherDevice.encryptionKey


    def sendData(self, data, otherDevice):
        # Encrypting data for transfer
        encData = Cryptography.asymmetricEncryption(data, self.negotiateKeyLevel(otherDevice))
        
        
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports 
        otherDevice.receiveData(encData)


    def receiveData(self, dataPacket):
        # Decrypting data that was recieveds 
        data = Cryptography.asymmetricDecryption(dataPacket.encryptedData, f"private{self.securityLevel}.pem")
        
        
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports 


    def splitPackets(self, data):
        print()


    def reconstructPackets(self, data):
        print()