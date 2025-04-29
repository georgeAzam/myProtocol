import ipaddress
import binascii
import socket
from struct import *
import struct
from client_toolbox import *
def menu() -> None:
    while True:
        print("\n\n____Welcome to MyProtocol___\n")
        print("You want to use specific IP and port or use the default values?\n")
        choose = input("Enter 'y' to put your IP and port or 'n' to use the default values: ")
        
        if choose =="y":
            serverIP = input("Enter the IP: ")
            # simple value check for the IP input
            while True:
                if ipCheck(serverIP)==False:
                    print("Please enter a valid IP")
                    serverIP = input("Enter the IP: ")
                else:
                    break    
            serverPort = int(input("Enter the port: "))
            print("Your desire IP is "+serverIP+" and your port is "+str(serverPort))
        else:
            serverIP = "127.0.0.1"
            serverPort = 12345
            print("You choose the default IP "+serverIP+" and the default port "+str(serverPort))

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverIP, serverPort))
        
         

        # Operatios submenu
        print("\n****Operation Options****\n")
        print("1. Multiply N numbers from -5 to 5 (N must be between 2 and 10)")
        print("2. Calculate the mean of N numbers fron 0 to 200 (N muste be between 2 and 20)")
        print("3. Substract 2 sets of N numbers from 0 to 60000 (N must be between 2 and 10)")
        print("4. Exit")
        print("*************************\n")
        try:
            choice = int((input("Choose an operation: ")))
            if choice not in [1, 2, 3, 4]:
                raise ValueError("Invalid choice")
        except ValueError as e:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue
        

        match choice:
            case 1:
                print("Multiply operation selected.")
                payload=multiply()
            case 2:
                print("Mean operation selected.")
                payload=mean()
            case 3:
                print("Subtraction operation selected.")
                payload=substraction()
            case 4:
                print("Exiting...")
                exit()
            case _:
                print("Invalid choice")
                continue
            
        print("The payload is : "+ str(payload))  #-------debuging message---------
        

        # Here starts the magic of packing


        msg_type=choice  #it is the protocol type for server to know witch operant to do
        msg_id=unique_id()  #the unique id so the server and the client knows that the both communicate for the same packet
        print("The message ID is :")#------debuging message------
        print(msg_id)
        if(choice==3):
            msg_len=4+(2*len(payload)) #the length of the message if the operant is substraction in bytes
        else:
            msg_len=4+len(payload) #the length of the message if the operant is mulitplication or average

        print("The message length is :")#------debuging message------
        print(msg_len)

        
        
        msg_padding_size=(4-msg_len%4)%4
        print("padding size")#------debuging message------
        print(msg_padding_size)

        message = pack("!B", msg_type)  #use the B format because it's 1 byte of data
        message = message + pack("!B", msg_len)   #the B format is for unsigned char but in represents a int for 0 to 255
        message = message + pack("!H", msg_id)
            
        if(choice==1):
            format_str="b"
        elif(choice==2):
            format_str="B"
        elif(choice==3):
            format_str="H"
                
            
            
        message = message + pack((str(len(payload)))+format_str, *payload)
        print("The payload in bytes is:")#------debuging message------
            
            

        if(msg_padding_size>0):
            message = message + struct.pack(f"{msg_padding_size}x")

        print("message in hex to send to server")#------print the message in hexademical
        print(binascii.hexlify(message))
        if(choice in[1,2,3]):
            clientSocket.sendall(message)
        else:
            clientSocket.close()
    
        print("Server response: \n")
         
              
        server_responce = clientSocket.recv(5)
        if not server_responce:
            continue
        #Here we got the critical information about the server response
        #like the message type witch determinates the operation to do
        #the status code witch determinates if we have a payload or an error
        #the message id to compare if it is the same with the message we sent so we didn't get any other responce
        #and the lenght for calculating prosses
        responce_server_msg_type, responce_server_status_code, responce_server_msg_id, responce_server_length = unpack("!BBHB", server_responce)
        print("The server response is:")#------debuging message------
        print("The message type is: " + str(responce_server_msg_type))#------debuging message------
        print("The status code is: " + str(responce_server_status_code))#------debuging message------
        print("The message ID is: " + str(responce_server_msg_id))#------debuging message------
        print("The message length is: " + str(responce_server_length))#------debuging message------
        server_padding_size=(4-responce_server_length%4)%4  # The padding with the header
        print("The padding size is: " + str(server_padding_size))#------debuging message------
        payload_size = responce_server_length -5 #The payload size is the length of the message minus the padding minus the header
        print("The payload size is: " + str(payload_size))#------debuging message------

        if(payload_size > 0):
            server_payload = clientSocket.recv(payload_size+server_padding_size)# receives everything to clean the buffer
            print("The server payload with padding is: " + str(server_payload))
            server_payload_bytes = server_payload[:payload_size]
            print("The server payload bytes is: " + str(server_payload_bytes))#------debuging message------
            
        if(responce_server_msg_id==msg_id):
            print("You're in the right place")#------debuging message------
        #Here we check if we have a payload and if it is the right payload for the question we send 
            if(responce_server_status_code==200 ):
            #In this code block we determine the type of the payload (format) and we unpack it
                if(responce_server_msg_type==1):
                    format_str = "!i"  
                    format_str = format_str*(len(server_payload_bytes)//struct.calcsize(format_str)) #the format string for the payload
                    server_message = unpack(format_str, server_payload_bytes)
                elif(responce_server_msg_type==2):
                    format_str = "!f"
                    format_str = format_str*(len(server_payload_bytes)//struct.calcsize(format_str)) #the format string for the payload
                    server_message = unpack(format_str, server_payload_bytes)
                elif(responce_server_msg_type==3):
                    format_str = "i"
                    format_str = "!"+format_str*(len(server_payload_bytes)//struct.calcsize(format_str)) #the format string for the payload
                    print("The format string is: " + str(format_str))#------debuging message------
                    server_message = unpack(format_str, server_payload_bytes)
                    print("The server message is: " + str(server_message))
                    server_message = list(server_message)
                    print("The server message is: " + str(server_message))
                    server_message = [int(i) for i in server_message]
                    print("The server message is: " + str(server_message))
                else:
                    print("Invalid message type")
                    
                
            
                for i in server_message:
                    print(i)
                print("The server message is: " + str(server_message))#------debuging message------
                # We can compare if the message is the same with the message we sent from the server    
                print("Received response:", binascii.hexlify(server_responce + server_payload))
                print("Sent message:", binascii.hexlify(message))

                #if we don't have payload (status=200) means that we have an error and print what error is
                #For easyer approach we sedn only one error even it is more than one
                #with priority on the list lenght, then the range of the numbers
            else:
                if(responce_server_status_code==0):
                    print("The numbers are not in the range")
                elif(responce_server_status_code==1):
                    print("The list is too short for multiplication")
                elif(responce_server_status_code==2):
                    print("The list is too short for mean")
                elif(responce_server_status_code==3):
                    print("The list is too short for substraction")
                elif(responce_server_status_code==4):

                    print("The two lists are not the same length")
                else:
                    print("Invalid message type")
                    exit()
        else:
            print("Opps! Wrong delivery")
        
        # fix the response codes print and get rid of some debuging messages
        


def ipCheck (ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
used_id= set()

def unique_id() ->int:
    if len(used_id) >= 256:
        raise ValueError("No unique IDs available")
    
    while True:
        uid = random.randint(0, 255)
        if uid not in used_id:
            used_id.add(uid)
            return uid


#   0       8       16      24      31
#   +-------+-------+-------+-------+
#   | type  |length |    ID         |
#   +-------+-------+-------+-------+       
#   |    payload......padding       |   
#   +-------+-------+-------+-------+
   






if __name__ == "__main__":
    menu()
    


