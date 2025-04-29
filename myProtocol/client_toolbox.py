import random

# this is the client's toolbox to use to do the each operation
# by the client section we will check the values to fit in our protocol only by the memory scope


def  multiply () -> list[int]:
    print("\n****Multiply N numbers from -5 to 5****\n")
    print("You want to enter numbers or use random numbers?")
    answer = input("Enter 'y' for entering numbers or 'n' for random numbers: ")
    list_mul= []
    if answer =="y":
        print("Enter  numbers between -5 and 5,to stop enter n")
        while True:
            try:    
                number = (input("Enter a number :")) 
                if number =="n": # check if the user want to stop entering numbers
                    break
                else:
                    number = int(number)# the input now is a string so we have to convert it to an integer

                if -128 <= number <= 127: #check if the number is 1 byte. Use 1 byte for the number because it's an signed integer from -5 to 5. The range of 1 byte suports the number and it's more memory efficient
                    list_mul.append(number)
                else:
                    print("Value out of range!")
            except ValueError:
                print("Invalid input! Please enter a valid number")    
    else: 
         print("We will fill the list with random numbers")
         N = random.randint(2, 10)
         while len(list_mul) < N:
            number = random.randint(-5, 5) # we don't realy have to do a check here because the numbers are valid
            list_mul.append(number)
    print(f"List: {list_mul}")             
    return list_mul           


def mean () -> list[int]:
    print("\n****Calculate the mean of N numbers fron 0 to 200****\n")
    print("You want to enter numbers or use random numbers?")
    list_mean=[]
    answer = input("Enter 'y' for entering numbers or 'n' for random numbers: ")
    if answer =="y":
        print("Enter  numbers between 0 and 200,to stop enter n")
        if answer =="y":
            while True:
                try:
                    number = (input("Enter a number :")) 
                    if number =="n": # check if the user want to stop entering numbers
                        break
                    else:
                        number = int(number)# the input now is a string so we have to convert it to an integer
                    if   0 <= number <=255: # we check the value to be in this range so it's one byte. We don't need more than 1 byte to represend a number from 0 to 200
                      list_mean.append(number)
                    else:
                      print("Va;ue out of range!")
                except ValueError:
                    print("Invalid input! Please enter a valid number")   
    else: 
        print("We will fill the list with random numbers")
        N = random.randint(2, 10)
        while len(list_mean) < N:
            number = random.randint(0, 200)
            list_mean.append(number)  
    print(f"List: {list_mean}")   
    return list_mean         


def substraction() -> list[int]:
    print("\n****Substract 2 sets of N numbers from 0 to 60000****\n")
    print("You want to enter numbers or use random numbers?")
    answer = input("Enter 'y' for entering numbers or 'n' for random numbers: ")
    list_sub1=[]
    list_sub2=[]
    temp_length=0
    if answer == "y":
        print("Enter  numbers between 0 and 60000 for the first set of 10 numbers max,to stop enter n")
        while True:
            try:
                number = (input("Enter a number :")) 
                if number =="n": # check if the user want to stop entering numbers
                    break
                else:
                    number = int(number)# the input now is a string so we have to convert it to an integer

                if 0 <= number <= 65535 : #check if the number is 2 bytes for unsigned number, so we have a range from 0 to 65535
                    if (len(list_sub1)<10): #check if the list for the first set is full
                        list_sub1.append(number)
                    else:
                        print("You have reach the maximum capacity for the first set of numbers")
                else:
                    print("Value out of range!")
            except ValueError:
                print("Invalid input! Please enter a valid number") 
        print("Enter  numbers between 0 and 60000 for the second set,to stop enter n")   
        while True:
            try:
                number = (input("Enter a number :")) 
                if number =="n": # check if the user want to stop entering numbers
                    break
                else:
                    number = int(number)# the input now is a string so we have to convert it to an integer

                if 0 <= number <= 65535:
                    if (len(list_sub2)<10):
                        list_sub2.append(number)
                    else:
                        print("You have complete the 2 sets of numbers needed")
                else:
                    print("Value out of range!")
            except ValueError:
                print("Invalid input! Please enter a valid number") 
    else:
        print("We will fill the lists with random numbers")

        N = random.randint(2, 10) #choose a random number for the list length

        while len(list_sub1) < (N): 
            number = random.randint(0, 60000)
            list_sub1.append(number)   
            print   

        while len(list_sub2) < (N): 
            number = random.randint(0, 60000)
            list_sub2.append(number)   
        print(f"List 1: {list_sub1}")
        print(f"List 2: {list_sub2}")

    for temp in list_sub2:  # do it this way rather to append the whole list because in len it counts and the []
        list_sub1.append(temp)  
    print("The combained list is: " + str(list_sub1))
    return list_sub1  
           









        


