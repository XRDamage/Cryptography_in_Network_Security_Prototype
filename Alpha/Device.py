from Cryptography import *
from DataPacket import *
from KeyGenerator import *
import cx_Oracle
import os
import socket

class Device:
    def __init__(self):
        self.completeData = b""
        self.rec_file = ""

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


    def sendFile(self, file_dir, otherDevice, recieverIP):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((recieverIP, 9999))

        file = open(file_dir, "rb")
        filename = os.path.basename(file_dir)
        client.send(filename.encode())

        data = file.read()

        batches = self.splitPackets(data)

        for batch in batches:
            client.send(Cryptography.asymmetricEncryption(Cryptography, batch, otherDevice))
            client.send(b"<BATCH>")

        client.send(b"<END>")
        file.close()
        client.close()



    def receiveData(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("localhost", 9999))
        server.listen()

        client, adrr = server.accept()

        if self.rec_file == "":
            self.rec_file = client.recv(1024).decode()

        file_bytes = b""
        done = False
        complete = False

        while not done:
            data = client.recv(1024)
            if file_bytes[-12:] != b"<BATCH><END>":
                if file_bytes[-7:] == b"<BATCH>":
                    done = True
                else:
                    file_bytes += data

            else:
                done = True
                complete = True

        self.completeData += Cryptography.asymmetricDecryption(file_bytes)

        if complete:
            file = open(self.rec_file, "wb")
            file.write(self.completeData)
            file.close()        

        client.close()




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