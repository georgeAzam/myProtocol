from typing import Tuple


def get_server_IP_And_port() -> Tuple[str, int]:
    #Ask the user if he/she wants to enter IP and port or use the default
    choose = input("Do you want to enter the IP and port? (y/n): ")
    if choose =="y":
        serverIP = input("Enter the IP: ")
        serverPort = int(input("Enter the port: "))
    else:
        serverIP = ""
        serverPort = 12345
    return serverIP, serverPort   

def check_muliplication_numbers(list : list[int]) -> bool:  #check the multiplication numbers range
    for number in list:
        if number < -5 or number > 5:
            print("Number out of range")
            return False
    return True

def check_mean_numbers(list : list[int]) -> bool:   #check the average numbers range
    for number in list:
        if number < 0 or number > 200:
            print("Number out of range")
            return False
    return True

def check_substraction_numbers(list : list[int]) -> bool:   #check the multiplications numbers range
    flag=True
    for numbers in list:
        if(numbers<0 or numbers>60000):
            print("The numbers are out of range")
            flag= False
            if(flag==False):
                return False
    return flag
        
            

def check_list_length(max : int, min :int,  list :list[int]) -> bool:    #check the list length
    if (len(list) > max or len(list) < min):
        print("List out of boundries")
        return False
    return True

def half_sub_list_check(list) ->bool:   #check if the sets for the substraction are even
    if(len(list) % 2==0):
        print("The sets of numbers are even")
        return True
    else:
        print("The sets of numbers are uneven")
        return False
    

def multiply(list :list[int]) -> int:
    print("\n__$__Multiplication__$__\n")
    mul=1 #neutral element of multiplication is 1
    for number in list:
        mul *= number
    print(f"The result of multiplication is  {mul}")
    return mul

def mean(list :list[int]) -> int:
    print("\n__$__Mean__$__\n")
    sum=0
    for number in list:
        sum += number
    mean = sum/len(list) 
    print(f"The result of average is + {mean}")   
    return mean

def substraction(list) -> list[int]:
    print("\n__$__Substraction__$__\n")
    result = []
    sets_length= len(list)//2
    for i in range(sets_length):
        result.append(list[i] - list[i+sets_length])
    
    print(f"The result of substraction is  {result}")
    return result 
    
