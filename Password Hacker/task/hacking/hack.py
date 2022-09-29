"""
Project: Password Hacker
Stage 2/5: Simple brute force


Description
The admin noticed someone sneaking around the site with admin rights and came up with a password. Now to log in as an admin, you need to enter the password first. Maybe the admin has set a relatively easy and short password so that it is easy to remember? Let's try to brute force all possible passwords to enter the site!

So far the program is very simplistic: it’s time to improve it so that it can generate different variants of the password and then try each one. The admin of the server doesn’t hide the information that passwords vary in length and may include letters from a to z and numbers from 0 to 9. You should start with a,b,c,....,z,0,1,..aa,ab,ac,ad and continue until your password is correct. The itertools.product() function can help you here. It’s very important to try all the variants of every length because otherwise your program risks never finding the password!

If the password is correct, you will receive the Connection success! message. Otherwise, you will see the Wrong password! message. The server cannot receive more than a million attempts, so if your program works indefinitely, you will see the unfortunate message Too many attempts.

Objectives
In this stage, you should write a program that:

Parses the command line and gets two arguments that are IP address and port.
Tries different passwords until it finds the correct one.
Prints the password it found.
Note that you can connect to the server only once and then send messages many times. Don't connect to the server before sending every message.

Also, note that here and throughout the project, the password is different every time you check your code.

Example
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

> python hack.py localhost 9090
pass
"""


import socket
import sys


host_name, port, message = sys.argv[1:]
with socket.socket() as client_socket:
    client_socket.connect((host_name, int(port)))
    client_socket.send(message.encode())
    response = client_socket.recv(1024).decode()
    print(response)
