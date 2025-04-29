This is a custom protocol working on TCP. The server acts as a computational engine that supports three operations:

# Multiplication of N signed integers

N must be between 2 and 10
Each integer must be between -5 and 5
Server returns the product

# Average of N integers

N must be between 2 and 20
Each integer must be between 0 and 200
Server returns the average

# Subtraction of two sets of N integers

N must be between 2 and 10
Integers must be between 0 and 60000
Server subtracts each element of the second set from the first and returns the result set


# Protocol Requirements:
The client sends:

The operation type (A, B, or C)
The required number(s)


The server replies:

Either the correct result
Or an error message indicating the type of error (e.g., invalid input range)

The are two files (one for client and one for the server) that works as a toolbox.
They have functions to help with the main code for client and server, so we can keep it clean and easy to read.

We also got two servers code. One (server.py) is for one client and the second (server_thread.py) is for multiclient and uses threads to serve each client separtly

There is also the RFC pdf to expalin the headers, the formats of the payloads and the status code
