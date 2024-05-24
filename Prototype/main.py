from Device import *
from DataPacket import *
from Cryptography import *
from KeyGenerator import *


device1 = Device("Xavier", 1, "public1.pem")
device2 = Device("Cayden", 2, "public2.pem")

with open("Text.txt", "rb") as f:
    data = f.read()

device1.sendData(data, device2)
device2.viewRecievedData()
