from Cryptography import *

enc = Cryptography.symmetricEncryption("Hello Wolrd")
print(enc)
print(Cryptography.symmetricDecryption(enc))