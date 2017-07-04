import socket      #import socket module   
import thread      #import thread for threading
from Crypto.Cipher import AES #import for encryption 
import os

key =raw_input("enter a 16 digit or a multiple of 16 digit long encryption key !eg password12345678\n") #key for encrypting data
while len(key)%16 != 0:
    print "please enter a key of valid length"
    key = raw_input("enter a 16 digit or a multiple of 16 digit long encryption key !eg password12345678\n")
obj = AES.new(key, AES.MODE_CBC, 'This is an IV456') #set encryption mode and !need to change third parameter to something random 16digit and send it with data



s = socket.socket()         # Create a socket object
host = '' # set host name so that it listens on all interfaces
port = input("enter port number between 2000-10000\n")        # Reserve a port for y service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
print 'listening for connection'



file_name = ''



while True:
    c, addr = s.accept() #when client makes a connection
    while True:
        file_t = c.recv(1) #recive byte by byte !this section was coz tcp packet can contain atleast 1 byte without loss !i aint really good at documenting stuff :p
        if  file_t=='$':    #can make this better $ is passed at end of the file name to mark the end of  file name !causes problem when file_name consits itslef of $
            break
        file_name += file_t
    file_name = str(file_name) #dont know if necessary but no harm
    print 'Got connection from', addr 
    print file_name," is being received"
    f = open(file_name+'enc','wb')   #open a file for temporarily writing encrypted data stuff 
        # Establish connection with client.
    print "receiving"
    l = c.recv(65008)               #this will not receive 65008 bytes always but can recive a maximum of 65008 bytes and minimum of 1 byte refer c.recv(1) due to data loss while transmission
    while (l): #close loof when eof is reached
        f.write(l)
        l = c.recv(65008)
    f.close()
    print "Done Receiving"
    break


print 'started decrypting \n crunching numbers'
file_encrypt = open(file_name+'enc',"rb")
file_decrypt = open(file_name,"wb")
enc_data = file_encrypt.read(52428832) #memmory hog when reading large files !! need to optimize !made as a proof of concept
while enc_data:
    print '.',
    decrypt_data = obj.decrypt(enc_data) #this thing needs the whole encrypted thing ,so the file was read as a whole or we need to send chunks of encrypted data one by one and start decrypting it
    length=decrypt_data[-2:] #the last 2 bytes contain the length of " " given to make the file a multiple of 16bytes or 128 bits for 128 bit encryption
    try:    
        decrypt_data =decrypt_data[:-int(length)] #remove the added ' ' or removing the padding
    except:
        decrypt_data = decrypt_data[:-1]
    decrypt_data = decrypt_data[16:] #remove first 16 char as it gets corrupted !!a fix would be nice
    file_decrypt.write(decrypt_data)
    enc_data = file_encrypt.read(52428832)

file_decrypt.close()
os.remove(file_name+'enc')
#os.system("rm "+file_name+'enc') #deletes the temporary encrypted file !need to remove linux specific code 
print '\nfile decrypted and saved as ',file_name