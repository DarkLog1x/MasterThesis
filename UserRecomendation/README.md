User recommendations to secure virtual machines in OpenStack
============================================================

Understanding the user interface
--------------------------------

Securing access to the Virtual Machine
--------------------------------------

One of the easiest ways for an advisory to get access to a virtual machine in the cloud is through poorly configured login credentials. there are bots on the web that will try to brute force login username and passwords on exposed ssh interfaces. It is therefore important for all machines to use strong login methods. One of these methods is to use a public private key pair instead of a password. Bellow are the instrustions on how to set up an ssh keypair. 

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
    * You now will have a public and private key pair in the location that you specified. You can then submit your public key (`.pub`) when you try and `ssh` into a machine. 
        ```
        $ ssh -i #Path to your private key# username@machine
        ```

2. You must upload your public key into OpenStack control panel:
    * Login to the OpenStack administration panel and select "Access & Security" in the left hand column. 
    * Next select the "key Pair" located to bellow the "Access & Security" title.
        ![Key Pair field](/UserRecomendation/pic/2017-02-13-211146_956x359_scrot.png)
    * Once on the page proceed to click on the "Import Key Pair" button located at the top right of the screen.
    * A pop-up should appear that looks similar to the following:
        ![Key Import](/UserRecomendation/pic/2017-02-13-211418_811x636_scrot.png)
    * Go back to your terminal and find your public key (`.pub`). Copy the contents and paste them into the field marked "Public Key". Then add a name to your key and click the "Import Key Pair" button at the bottom of the pop-up.

### Creating a new machine ###

1. Access the main control panel for OpenStack:
   ![Control Panel](/UserRecomendation/pic/2017-02-13-110643_954x888_scrot.png)

2. Select the "Instance" tab on the left hand side of the screen.

3. Now select the "Launch Instance" button on the upper right hand side of the screen. 

4. A pop-up should apper that look similar to the following:
   ![Instance Panel]()
   
5. Fill out the necacasry setting. 
   * Ensure that the "Security Group" tab has the correct group assigned to the VM.
   * Ensure that the correct public key is selected in the "Key Pair" tab

### Security Roles ###

### Security Groups ###
