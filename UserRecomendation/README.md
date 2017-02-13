User recommendations to secure virtual machines in OpenStack
============================================================

Understanding the user interface
--------------------------------

Securing access to the Virtual Machine
--------------------------------------

1. Ensure that one has created an ssh key pair.
    * In a terminal run the following command:
        ```
        $ ssh-keygen -t rsa -b 4096
        # The `ssh-keygen` command will create the key
        # The `-t` option will set the cryptosystem to rsa
        # The `-b` will set the key length to 4096 bits 
        Generating public/private rsa key pair.
        Enter file in which to save the key (/home/groot/.ssh/id_rsa): #Your path goes here
        Enter passphrase (empty for no passphrase): #Enter a password
        Enter same passphrase again: #Reenter your password
        ...
        ``` 
    * You now will have an public and private key pair in the location that you specifed. You can then submit your publick key (`.pub`) when you try and `ssh` into a machine. 
        ```
        $ ssh -i #Path to your private key# username@machine
        ```

2. You must upload your public key into OpenStack control panel:
    * Login to the OpenStack administration panel and select 

### Creating a new machine ###

1. Access the main control panel for OpenStack:
    ![Control Panel](/UserRecomendation/pic/2017-02-13-110643_954x888_scrot.png)

2. Select the 

### Security Roles ###

### Security Groups ###
