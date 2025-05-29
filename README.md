# tinySCPI
A Python library that enables the use of SCPI commands on the tinySA Ultra.

See the [Commands](https://github.com/tinySCPI-S25-24/tinySCPI_Ultra/blob/main/docs/Commands.md) documentation for each command and a description.

# Table of Contents

1. [**Getting Started**](#getting-started)
2. [**Dependencies**](#dependencies)
3. [**Contact Us**](#contact)
4. [**Safety**](#safety)
5. [**Output**](#output) 

## Getting Started <a name="getting-started"></a>
1. Clone the repository.
2. In the 'Web Server Client' file, run 'WebApp.py'. (Dependencies may need to be installed before running)
3. Using the IP address and port number provided in the terminal, enter the URL into a Web Browser. (e.g,  http://IP:PORT)
4. Enter the key 'password' into the login.
5. Ensure the tinySA Ultra is connected to the PC that is running the server.
6. Now you're ready to execute any of the commands located in the [Command Tree](https://github.com/tinySCPI-S25-24/tinySCPI_Ultra/blob/main/docs/Commands.md)!
7. SCPI commands can also be run directly in the terminal using the file tinySCPI.py and the functions in [Class Documentation](https://github.com/tinySCPI-S25-24/tinySCPI_Ultra/blob/main/docs/Class_Documentation.md). NOTE: The Python file must be run through a terminal and not an IDE. For example:
   ```
   C:\Users\'your_identifier'> python3 .\source\repos\tinySCPI_Ultra\tinyscpi\tinySCPI.py user_input "*HLP"
   ```
   This file destination may look different from the one you have.
   
## Dependency: <a name="dependencies"></a>
tinySCPI requires python >= 3.6, pyserial, pytest, and pytest-cov, flask, flask_login

```pip install pyserial```
```pip install pytest```
```pip install pytest-cov```
```pip install flask```
```pip install flask_login```

## Contact Us: <a name="contact"></a>
Email: kidus1127@vt.edu

## Safety: <a name="safety"></a>
Like with all RF devices, there involves some risk in operation. For more information, please refer to [Safety](https://github.com/noldono/tinySCPI/blob/main/SAFETY.md).

## Output: <a name="output"></a>
On older firmware, output mode control over serial may not be stable and can return the "FATAL ERROR" message on screen. [Updating to a newer firmware](https://github.com/noldono/tinySCPI/blob/main/docs/tinySA_Firmware_Update_Manual.pdf) seems to resolve this issue.
