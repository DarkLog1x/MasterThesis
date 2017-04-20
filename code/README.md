# Installation Instructions

## Prerequisites

**Local Computer**

* Have access to a Unix box {This setup assumes one is using a flavor of Linux}
* Have ansible installed [text link](https://www.ansible.com/)
* Have git installed on machine

**Virtual Machine**

* Start a virtual machine in the cluster
-- Tested on Ubuntu 16.04 LTS
-- vCPU 1, memory 512mb, drive space 20G, Network connection

## Steps

1. Start the virtual machine up and ensure that it has network access. This machine should be started in the same cluster as the other machines.
2. On the local computer run `git clone [text link](https://github.com/DarkLog1x/MasterThesis)` (!!!IMPORTANT!!! Currently Working Branch is **dev** one must `git cheackout dev` untill master is updated)
3. Once cloned, move into the code directory `cd code`
4. In this directory create a new folder called ssh_keys `mkdir ssh_keys`. This folder will hold all the ssh and api keys for this project, ensure that these are kept safe.
