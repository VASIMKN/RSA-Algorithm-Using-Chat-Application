import socket
import rsa
from base64 import b64encode, b64decode

client = socket.socket()
client.connect(('localhost',5050))


choice = input('Choose any one.\n1.Encrption & Decryption.\n2.Digital Signature.\n3.Both.\n4.Quit\n')
client.send(str(choice))
public = rsa.importKey(client.recv(1024))
private = rsa.importKey(client.recv(1024))
if int(choice) == 1:
    print  'Encyption & Decryption'
    while True:
        msg = raw_input('Enter message:')
        encrypted = b64encode(rsa.encrypt(msg, public))
        client.send(encrypted)
        msgec = client.recv(1024)
        if msgec == 'Quit' :
            client.close()
            break 
        else:
            print 'Encrypted Text :',msgec
            print '--> ',rsa.decrypt(b64decode(msgec), private)
 
elif int(choice) == 2:
    print  'Digital Signature'
    msg = raw_input('Enter Message:')
    client.send(msg)
    signature = b64encode(rsa.sign(msg, private))
    client.send(signature)

elif int(choice) == 3:
    print 'Encryption Decryption With Digital Signature' 
    msg = raw_input('Enter Message:')
    client.send(msg)
    signature = b64encode(rsa.sign(msg, private))
    client.send(signature)
    while True:
        msg = client.recv(1024)
        print rsa.decrypt(b64decode(msg), private) 
        msge = raw_input('Enter message:')
        if msge == 'Quit':
            client.send(msge)
            client.close()
            break
        else:
            encrypted = b64encode(rsa.encrypt(msge, public))
            client.send(encrypted)
            

