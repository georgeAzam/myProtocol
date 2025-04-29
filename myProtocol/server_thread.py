from struct import *
import socket
import binascii
from _thread import *
import struct
from server_toolbox import *

def thread_client(conn, addr):
    #Print info: Connected address, Server IP & Port, Client IP & Port
    print("Server Socket port: ", conn.getsockname())
    print("Client Socket port: ", conn.getpeername())


    while(1):

        msg = conn.recv(4) #collect the first 4 bytes (msg_type  length an id)
        
        server_msg_type, msg_length, server_msg_id = unpack_from("!BBH", msg)
        if server_msg_type not in [1, 2, 3]:
            print(f"Invalid message type {server_msg_type} received! Closing connection.")
            conn.close()  # Close the connection
            # Skip processing and wait for a new connection

        msg_pad_size = (4- msg_length%4)%4  #calculate the padding
        payload_size = msg_length - 4
        
        print('Total message length without pad='+str(msg_length)) #--check
        print("message type " + str(server_msg_type))   #--check
        print("message length "+ str(msg_length))   #--check
        print("message id " + str(server_msg_id))
        full_payload = conn.recv(payload_size + msg_pad_size) #here is the length of the bites of the payload and the padding in buffer
        print("rest message in buffer is " + str(full_payload))
        payload_bytes = full_payload[:payload_size] #extract the actual message from client in bytes
        if(server_msg_type==1):
            format_str = "b"
        elif(server_msg_type==2):
            format_str = "B"
        elif(server_msg_type==3):
            format_str = "H"
        else:
            print("Huston we have a problem")
        format_str = format_str * (len(payload_bytes) // struct.calcsize(format_str)) #calculate the element of format_str bytes in the payload
        print("The format string is: " + str(format_str)) #------debuging message------checks out
        msg_payload = unpack(format_str, payload_bytes)
        print("The payload is: " + str(msg_payload))

        # here we have done with the unpacking of the message
        # we have all the necessary information to do the operations and return the result

        #the server header is:

        #   0       8       16      24      31
        #   +-------+-------+-------+-------+
        #   |  type |status |    ID         |
        #   +-------+-------+-------+-------+       
        #   | lenght|  responce.....padding |   
        #   +-------+-------+-------+-------+

        responce_length=0
            
        match server_msg_type:
            case 1: #--wokrs
                if(check_list_length(10, 2, msg_payload)==True):
                    if(check_muliplication_numbers(msg_payload)==True):
                        result = multiply(msg_payload)
                        status_code=200
                        responce_length = 4
                    else:
                        status_code=1
                else:
                    status_code=0
                        
            case 2: #--works
                if(check_list_length(20, 2, msg_payload)==True):
                    if(check_mean_numbers(msg_payload)==True):
                        result = mean(msg_payload)
                        status_code=200
                        responce_length = 4
                    else:
                        status_code=2
                else:
                    status_code=0
                    
            case 3: #--works
                if(half_sub_list_check(msg_payload)==True):
                    if(check_list_length(20, 4, msg_payload)==True):
                        if(check_substraction_numbers(msg_payload)==True):
                            result_sub = substraction(msg_payload)
                            result = []
                            for num in result_sub:
                                result.append(int(num))
                            status_code=200
                            responce_length = len(result)*4
                            print("The result is: " + str(result))
                            print("The length of the result is: " + str(responce_length))
                        else:
                            status_code=3
                    else:
                        status_code=0
                else:
                    status_code=4
                
            case _:
                print("Invalid message type")
                status_code=100
            
        server_message_length = 5 + responce_length 
        print("The message length is: " + str(server_message_length))
        print("Status code is: " + str(status_code)) #--check                
        if(status_code==200):
            responce= pack("!BBHB", server_msg_type, status_code, server_msg_id, server_message_length)
            print("The header bytes are :" + str(len(bytes(responce)))) #------debuging message------
            if(server_msg_type==1):    #the max value of result in case 1 is (5^10) 9765625 and the min values is ((-5^9)*5) -9765625 so we have to use 4 bytes for signed integer
                responce = responce + pack("!i", result)
            elif(server_msg_type==2): #the result is the average of the numbers so the max value is 200 and the min value is 0, but it is a float
                responce = responce + pack("!f", result)
            elif(server_msg_type==3):  #the max value of the result in case 3 is 60000 and the min value is -60000, so we have to use 4 bytes for signed integer
                format_str = f'!{len(result)}i'
                responce = responce + struct.pack(format_str, *result)


            msg_padding_size=(4-server_message_length%4)%4
            print("Padding size is: " + str(int(msg_padding_size))) #------debuging message------
            if(msg_padding_size>0):
                responce = responce + struct.pack(f"{(msg_padding_size)}x")
                
            print("The result of message in bytes is : " + str(len(bytes(responce)))) #------debuging message------
            print("The message in hex to send to client")#------debuging message------
            print(binascii.hexlify(responce))
            
                
        else:
            responce= pack("!BBHB", server_msg_type, status_code, server_msg_id, server_message_length)
            
        err = conn.sendall(responce)
        print("Messasgqe sent to client")
        print(err)

serverIP, serverPort = get_server_IP_And_port()
close = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    #Bind the socket
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive at port", str(serverPort))
    #Listen for connections
    #If we don't specify in the listen a number e.g. serverSocket.listen(5), it goes to the system default
    serverSocket.listen()
    
    thread_counter=0
    
    while not close:
        conn, addr = serverSocket.accept()
        #Listen and wait for connection
        start_new_thread(thread_client, (conn, addr))
        thread_counter+=1
        print("Thread number: " + str(thread_counter))
        if(thread_counter==10):
            close = True
            print("Closing the server")
            conn.close()
            serverSocket.close()
            print("Server closed")