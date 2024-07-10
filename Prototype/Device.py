from Cryptography import *
from DataPacket import *
from KeyGenerator import *
import cx_Oracle

class Device:
    def __init__(self, name, securityLevel, encryptionKey):
        self.securityLevel = securityLevel
        self.encryptionKey = encryptionKey
        self.name = name
        self.completeData = None

    def negotiateKeyLevel(otherDevice):
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XEPDB1')
        conn = cx_Oracle.connect(user='system', password='Floppy@Disk', dsn=dsn_tns)
        cursor = conn.cursor()
        cursor.execute("SELECT Public_Key FROM Network_Devices WHERE DeviceID = :device_id", [otherDevice])
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def addDeviceDB(device_name, key_level):
        if (device_name != "") or (key_level != ""):
            key = KeyGenerator.generateAsymKeys(key_level)

            enc_key = Cryptography.symmetricEncryption(key)

            if key != None:
                dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XEPDB1')
                conn = cx_Oracle.connect(user='system', password='Floppy@Disk', dsn=dsn_tns)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Network_Devices (DeviceID, Public_Key) VALUES (:device, :key)", [device_name, enc_key])
                conn.commit()
                conn.close()

            
        else:
            print("0")


    def sendData(self, data, otherDevice):
        try:
            batches = self.splitPackets(data, 100)
            for batch in batches:
                # Encrypting and hashing data for transfer
                encData = Cryptography.asymmetricEncryption(batch, self.negotiateKeyLevel(otherDevice))
                print(encData)
                hashValue = Cryptography.hash(encData, f"private{self.securityLevel}.pem")
                # Sending data
                packet = DataPacket(encData, hashValue)
                otherDevice.receiveData(packet, self)
        except Exception as e:
            print(f"Error during encryption or sending: {e}")



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