import ast
import time

from crypto import Random
from crypto.PublicKey import RSA
from crypto.Cipher import PKCS1_OAEP

start_time = time.time()
random_generator = Random.new().read

# Generates public and private key
key = RSA.generate(1024, random_generator)

# Exporting public key to global
public_key = key.publickey()

encryptor = PKCS1_OAEP.new(public_key)
pause1 = time.time()

# Choosing file to read

message_file = input('Input filename for reading: ')

with open(message_file, 'r') as message:
    data1 = message.read()
    data1 = str(data1)
    data1 = bytes(data1, 'utf-8')

# Encryption data from read file
continue1 = time.time()
encrypted = encryptor.encrypt(data1)
pause2 = time.time()

# Writing encrypted data to separate file
with open('encryption.txt', 'w') as encryption:
    encryption.write(str(encrypted))

# Choosing file to read and decrypt encrypted data
encrypted_file = input('Input filename for decoding: ')

with open(encrypted_file, 'r') as code:
    data2 = code.read()

# Decrypting data
continue2 = time.time()
decryptor = PKCS1_OAEP.new(key)
decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
end_time = time.time()

# Writing decrypted text to result file
with open('result.txt', 'w') as result:
    result.write(decrypted.decode('utf-8'))

time = ((end_time - continue2) + (pause2 - continue1) + (pause1 - start_time))
print("Time of the program: " + str(time))
