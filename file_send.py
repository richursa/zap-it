import socket #import sockets for sending data
import time
import os	#need this thing for geting the file size without going thorugh it byte by byte
from Crypto.Cipher import AES  #thing for encryption
import thread #need this for threadng encrypting data in background while main thread continues to operate
file_name = raw_input("please enter the name of the file to be ecrypted and send\n")
while 1:
	try:
		a=open(file_name,"r") #checks if a file of the given name is there
		a.close()
		break
	except IOError:
		print "file not found"
		file_name = raw_input("please enter the name of the file to be ecrypted and send\n")
print "file size is " , os.path.getsize(file_name)," bytes" #this thing prints the size of file #efficent 



key =raw_input("enter a 16 digit or a multiple of 16 digit long encryption key !eg password12345678\n")
while len(key)%16 != 0:
   	print "please enter a key of valid length"
   	key = raw_input("enter a 16 digit or a multiple of 16 digit long encryption key !eg password12345678\n")
print "file is being encrypted in background"


obj = AES.new(key, AES.MODE_CBC, 'This is an IV456')
file_var = open(file_name,"r")
r = file_var.read(52428800)
length =len(r)%16 #get length of file in bytes
for i in range (length,15): #if the file length is not multiple of 16 we need to make it 16 bytes by padding it with spaces which will be removed at other end#the last bytes need to be the length of padding that is why the looop is only run upto 15
	r = r + ' '
if (16-length)>9: #need to pass the no of space added with the file so checking if we need to remove the last two digits if added spaces was more than 9
	r = r[:-1]
r = "1234567812345678" + r + str(16-length) #first 16 bytes gets corrupted on other end !dont know why !
#file_var_enc.write(obj.encrypt(r))
r = obj.encrypt(r) #starts encrypting the file in background while the user continues entering relevant info 
host = raw_input("enter target ip\n") # ip of the target
port = input("enter a port number 2000-10000 \n")  # Reserve a port for your service.
s = socket.socket()         # Create a socket object
s.connect((host, port)) #connect with the host 
s.send(file_name+'$')	#the file name is added with a terminator $ temporary to mark end of file name while receiving
vnc_flag =1
s_flag = 1
def sen():
	global vnc_flag
	global s 
	global o
	s.sendall(r)
	print len(r)
	vnc_flag = 1
while r:


	if s_flag ==1:
		s_flag = 0
		print "please wait while file is being encrypted\n generating randoms \n crunching numbers"
		print "sending file"
	else:
		#file_var = open(file_name,"rb") #open the file
		#file_var_enc = open(file_name+'enc',"wb") #create a temporary file for writing encrypted data !unoptimised wont be necessary if encrypted data can be send efficently
		#r =file_var.read() #memmory hog !need to keep it this way as due to lack of expirience in data transmission over sockets and encryption
		length =len(r)%16 #get length of file in bytes
		for i in range (length,15): #if the file length is not multiple of 16 we need to make it 16 bytes by padding it with spaces which will be removed at other end#the last bytes need to be the length of padding that is why the looop is only run upto 15
			r = r + ' '
		if (16-length)>9: #need to pass the no of space added with the file so checking if we need to remove the last two digits if added spaces was more than 9
			r = r[:-1]
		if 16-length != 1:
			string =str(16-length)
		else:
			string = 'k'
		r = "1234567812345678" + r + string #first 16 bytes gets corrupted on other end !dont know why !
		#file_var_enc.write(obj.encrypt(r))
		r = obj.encrypt(r)
		

	print ".",
	#f = open(file_name+'enc','rb')
	#print 'Sending...'
	#l = f.read(65008) #max size of tcp packets is 65535 !
	#while vnc_flag != 1:
#		time.sleep(0.000001)
	vnc_flag = 0
	s.sendall(r)
	#thread.start_new_thread(sen, ())
	#print s.recv(1024)
	r = file_var.read(52428800)
print "\nfile sent sucessfully"
s.close()         