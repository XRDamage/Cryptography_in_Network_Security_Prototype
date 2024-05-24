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
        try:
            batches = self.splitPackets(data, 100)
            for batch in batches:
                # Encrypting and hashing data for transfer
                encData = Cryptography.asymmetricEncryption(batch, self.negotiateKeyLevel(otherDevice))
                hashValue = Cryptography.hash(encData, f"private{self.securityLevel}.pem")
                # Sending data
                packet = DataPacket(encData, hashValue)
                otherDevice.receiveData(packet, self)
        except Exception as e:
            print(f"Error during encryption or sending: {e}")
        
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports 


    def receiveData(self, dataPacket, otherDevice):
        try:
            if dataPacket.checkSignature(otherDevice.encryptionKey):
                # Decrypting data that was recieveds
                data = Cryptography.asymmetricDecryption(dataPacket.encryptedData, f"private{self.securityLevel}.pem")
                if self.completeData is None:
                    self.completeData = []
                self.completeData.append(data.decode())
            else:
                print("Signiture not validated")
        except Exception as e:
            print(f"Error during data decryption: {e}")
        
        # For the purpose of the project, the sending and recieving 
        # will be done by calling the different class methods.
        # In a network , the sending and recieving will be done
        # over network ports

    def viewRecievedData(self):
        data =  self.reconstructPackets(self.completeData)
        print(data)
        self.completeData = None


    def splitPackets(self, data, batchSize=100):
        # splitting the data into smaller batches
        if isinstance(data, bytes):
            codeData = data
        elif isinstance(data, str):
            codeData = data.encode('utf-8')
        else:
            raise ValueError("Data not string or byte")
        return [codeData[i:i + batchSize] for i in range(0, len(codeData), batchSize)]


    def reconstructPackets(self, batches):
        # Reconstructing the batches into original data
        return ''.join(batches)