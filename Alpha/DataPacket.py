import rsa
import cx_Oracle

class DataPacket:
    def __init__(self, encryptedData, hashValue):
        self.encryptedData = encryptedData
        self.hashValue = hashValue

    def checkSignature(self, otherDevice):
        # Openign the public key to check signiture
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XEPDB1')
        conn = cx_Oracle.connect(user='system', password='Floppy@Disk', dsn=dsn_tns)
        cursor = conn.cursor()

        query = "SELECT Public_Key FROM Network_Devices WHERE Device_ID = :device_id"
        cursor.execute(query, device_id=otherDevice)
        result = cursor.fetchone()

        key = self.symmetricDecryption(result)
        # Verifying signiture of sender
        try:
            rsa.verify(self.encryptedData, self.hashValue, key) == "SHA-256"
            return True
        except:
            return False