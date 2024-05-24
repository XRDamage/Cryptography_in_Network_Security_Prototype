from Device import *

print("\n========================== Input ==========================\n")
# Getting input for the first Device
device1Name = input("\nEnter the name for the first device: ")
device1Level = input("Enter the security level for the first device: ")
device1 = Device(device1Name, device1Level, f"public{device1Level}.pem")

# Getting input for the second device
device2Name = input("\nEnter the name for the second device: ")
device2Level = input("Enter the security level for the second device: ")
device2 = Device(device2Name, device2Level, f"public{device2Level}.pem")

# Getting input for the message to send
message = input("\nEnter a message to send between the devices: ")

# Sending the message from device1 to device2
print("\n==================== Encrypted Message ====================\n")
# Displaying the encrypted data before reciever decrypts the data
device1.sendData(message, device2)
# Diplaying the data that was recieved by device2
print("\n==================== Decrypted Message ====================\n")
device2.viewRecievedData()
print("\n===========================================================\n")
