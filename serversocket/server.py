#import socket module
from socket import *
import sys # In order to terminate the program


#Initialise socket with address family and sock_stream for TCP connection
serverSocket = socket(AF_INET, SOCK_STREAM)

print("Please type in the port you would like to use (Between 1-65535): ")
serverPort = int(input())

#Bind IP address of device and server port to the socket
serverSocket.bind(('', serverPort))

#Allow for only a single incoming connection
serverSocket.listen(1)

while True:
	print ('Ready to serve...')
	#Accepting a connection and initialising a pair to hold the returning values. (a new socket object to send and recieve data, the destinations IP and port)
	connectionSocket, addr = serverSocket.accept()
	print ("Destination address is: " + str(addr))

	try:

		message = connectionSocket.recv(1024)
		print ('Message is: ', message.decode("UTF-8"))

		#Split the message recieved into parts and
		filename = message.split()[1]

		#Read from the second character since the split will contain a '/' in front of "HelloWorld" ('/HelloWorld.html')...
		#...then open the file and save the contents to a variable
		f1 = (filename[1:].decode("UTF-8"))
		f = open(f1)
		outputdata = f.read()

		#Send one HTTP header line into socket
		connectionSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n",'UTF-8'))
		#Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send(bytes("\n\r", "UTF-8"))
		connectionSocket.close()

	except IOError:
		#Send response message for file not found
		f = open("/404/NRzNLz.html", 'r')
		error_notfound = ("HTTP/1.1 404 Not Found\r\n\r\n" + f.read())
		f.close()
		connectionSocket.sendall(bytes(error_notfound, 'UTF-8'))
		#connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", 'UTF-8'))
		#connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", 'UTF-8'))
#Close client socket
serverSocket.close()
sys.exit()
