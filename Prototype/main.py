from Device import *
from DataPacket import *
from Cryptography import *
from KeyGenerator import *

device1 = Device(1, "public1.pem")
device2 = Device(2, "public2.pem")

message = "Hello"
device1.sendData(message, device2)