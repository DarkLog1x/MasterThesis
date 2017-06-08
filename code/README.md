# Installation Instructions

## Prerequisites

**API Keys**

* Obtain a Slack API key from `Slack API [text link](https://api.slack.com/custom-integrations/legacy-tokens)`
* Create a bot in Slack `Slack Bot [text link](https://api.slack.com/bot-users)`

**Local Computer**

* Have access to a Unix box {This setup assumes one is using a flavor of Linux}
* Have ansible installed [text link](https://www.ansible.com/)
* Have git installed on machine

**Virtual Machine**

* Create a ssh key pair and enable it for the virtual machine
* Start a virtual machine in the cluster
-- Tested on Ubuntu 16.04 LTS
-- vCPU 1, memory 512mb, drive space 20G, Network connection

## Steps

1. Start the virtual machine up and ensure that it has network access. This machine should be started in the same cluster as the other machines.
2. On the local computer run `git clone [text link](https://github.com/DarkLog1x/MasterThesis)`.
3. Once cloned, move into the code directory `cd code`.
4. In this directory create a new folder called ssh_keys `mkdir ssh_keys`. This folder will hold all the ssh and api keys for this project, ensure that these are kept safe.
5. Enter into the ssh_keys directory `cd ssh_keys`. Move the key for the virtual machine into the directory.
6. Download the OpenStack rc file into the `ssh_keys` directory.
7. Create a file called 'keys' in the ssh_keys directory `touch keys`.
8. Edit the file and insert your slack api key, the slack bot api key, your OpenStack user password, and the name of the bot. {Order matters and each item should be on its own line}
9. Now go back and enter into the ansible directory `../ansible`.
10. Edit the hosts file to fit your ansible needs, it will look like this:
```
[all]
host1 ansible_ssh_host=[IP ADDRESS OF VM] ansible_ssh_private_key_file=[POINT THIS TO YOUR PRIVATE SSH KEY FROM EARLIER] ansible_user=[USER NAME ON VM] ansible_python_interpreter=/usr/bin/python3

```
11. Now move to the python directory `cd ../python`
12. Here we first need to edit the config file. This is up to you how the system works, therefor look inside the file and see some example work.
13. Next we need to edit the environmentVariables.py file. These fields are taken from your .rc file that you downloaded from OpenStack.
15. Now go back to the ansible directory `cd ../andible` and run the start.sh script `./start.sh`. Everything should run smoothly if not file a but report!
