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

### Security Rules ###

Security rules are a set of instructions that can be placed on to VMs that will limit that pariculer VMs abbiltiy to access external environments. They act very similer to a firewall with allowing or blocking diffrent types of connections to the individual VMs. To set up proper rules the following steps should be taken:

1. Log into OpenStack and select the "Access & Security" tab on the left hand side. 

2. You will now see a list of security groups that you are part of. Selcet the group that you would like to edit by clicking the "Manage Rules" button on the right hand side. 
   ![Manage Rules]()
   
3. The new screen should look something like this:
   ![Rules}()
   
   Lets break down what the diffrent components are:
   * The "Direction" field describes if inbound or outbound trafic is affected by the rule
   * "Ether Type" describes wiether the rule talks about IPv4 or IPv6 traffic
   * "IP Protocal" describes what type of traffic is permited or blocked (i.e. http, pop3, etc.)
   * "Port Range" what ports that rule applies to for that machine
   * "Remote IP Prefix" describes what IP address the trafic should come from

### Security Groups ###
