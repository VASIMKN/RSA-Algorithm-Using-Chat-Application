import socket
import rsa
from base64 import b64encode, b64decode

public, private = rsa.newkeys()

server = socket.socket()
server.bind(('localhost',5050))
server.listen(10)

conn, address = server.accept()
choice = int(conn.recv(1024))
conn.send(public.exportKey())
conn.send(private.exportKey())
if choice == 1:
    print 'Encryption & Decryption' 
    while True:
        msg = conn.recv(1024)
        print 'Encrypted Text :',msg
        print '--> ',rsa.decrypt(b64decode(msg), private) 
        msge = raw_input('Enter message:')
        if msge == 'Quit':
            conn.send(msge)
            conn.close()
            break
        else:
            encrypted = b64encode(rsa.encrypt(msge, public))
            conn.send(encrypted)
elif choice == 2:
    print 'Digital Signature' 
    msg = conn.recv(1024)
    sign = conn.recv(1024)
    verify = rsa.verify(msg, b64decode(sign), public)
    print  'Is the Sender Verified ?', verify
    conn.close()
    
elif choice == 3:
    print  'Encryption Decryption With Digital Signature'
    msg = conn.recv(1024)
    sign = conn.recv(1024)
    verify = rsa.verify(msg, b64decode(sign), public)
    print  'Is the Sender Verified ?', verify
    if verify:
        while True:
            msg = raw_input('Enter message:')
            encrypted = b64encode(rsa.encrypt(msg, public))
            conn.send(encrypted)
            msge = conn.recv(1024)
            if msge == 'Quit':
                conn.close()
                break 
            else:
                print  rsa.decrypt(b64decode(msge), private)
    else:
        print  'User Is not verified'
        client.close()

else:
    conn.close()
