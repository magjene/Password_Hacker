"""
Project: Password Hacker
Stage 4/5: Catching exception


Description
The server is becoming smarter along with your hacking program. Now the admin has implemented a security system by login and password. In order to access the site with admin privileges, you need to know the admin's login and password. Fortunately, we have a dictionary of different logins and a very interesting vulnerability. You need to improve your program once again to hack the new system.

Also, now the admin has made a complex password that is guaranteed to be absent in the databases since it's randomly generated from several characters.

The server now uses JSON to send messages.

First of all, you should adjust your program so that it can send the combination of login and password in JSON format to the server. Your request should now look like this:

{
    "login": "admin",
    "password": "12345678"
}
In case of the wrong login, the response you receive looks like this:

{
    "result": "Wrong login!"
}
If you got the login right but failed to find the password, you get this:

{
    "result": "Wrong password!"
}
If some exception happens, you'll see this result:

{
    "result": "Exception happened during login"
}
When you finally succeed in finding both the login and the password, you'll see the following:

{
    "result": "Connection success!"
}
Use the dictionary of typical admin logins. Since you don’t know the login, you should try different variants from the dictionary the same way you did at the previous stage with the passwords.

Use an empty password while searching for the correct login. It matters because you will know that the login is correct the moment you get the ‘wrong password’ result instead of ‘wrong login’.
As for passwords, they’ve become yet harder, so a simple dictionary is no longer enough. Fortunately, a vulnerability has been found: the ‘exception’ message pops up when the symbols you tried for the password match the beginning of the correct one.

Objectives
Your algorithm is the following:

Try all logins with an empty password.
When you find the login, try out every possible password of length 1.
When an exception occurs, you know that you found the first letter of the password.
Use the found login and the found letter to find the second letter of the password.
Repeat until you receive the ‘success’ message.
Finally, your program should print the combination of login and password in JSON format. The examples show two ways of what the output can look like.

Examples
The greater-than symbol followed by a space (> ) represents the user input. Note that it's not part of the input.

Example 1:

> python hack.py localhost 9090
{
    "login" : "superuser",
    "password" : "aDgT9tq1PU0"
}
Example 2:

> python hack.py localhost 9090
{"login": "new_user", "password": "Sg967s"}
"""


import itertools
import socket
import sys


with open(r'.\hacking\logins.txt', 'r') as login_file:
    login_list = login_file.read().split()

host_name, port = sys.argv[1:]
with socket.socket() as client_socket:
    client_socket.connect((host_name, int(port)))
    for password in password_list:
        password_iter = itertools.product(*list(zip(password.lower(), password.upper())))
        for passwords in password_iter:
            client_socket.send(''.join(passwords).encode())
            response = client_socket.recv(1024).decode()
            if response == 'Connection success!':
                print(''.join(passwords))
                exit()
    else:
        print('Wrong password!')
