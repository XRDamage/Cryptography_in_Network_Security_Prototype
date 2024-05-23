from Device import *
from DataPacket import *
from Cryptography import *
from KeyGenerator import *

message = "Xavier Ramage"
encData = Cryptography.asymmetricEncryption(message, "public4.pem")
hashValue = Cryptography.hash(encData, "private4.pem")
packet = DataPacekt(encData, hashValue)
decData = Cryptography.asymmetricDecryption(encData, "private4.pem")

print()
print(encData)
print()
print(packet.checkSignature(hashValue, "public4.pem"))
print()
print(decData)
print()