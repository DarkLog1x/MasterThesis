#!/bin/sh

echo "This program is created to take a memory dump and cpu stats."
echo "This program may cause problems if not used correctly, ensure that you are an administrator and understand the risks."
echo "If you are not sure please stop the script with a \"ctr_c\" command."

while true; do
    read -p "Would you like to continue: y/N " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

while true; do
    read -p "Would you like to list the instances in the cluster: y/N " yn
    case $yn in
        [Yy]* ) nova list; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

read -p "Enter the file location to store the output files (defalt is  \"/tmp/\"): " filepath
filepath=${filepath:-/tmp}
echo $filepath

read -p "What is the server ID: " IDName
openstack server show $IDName
echo "Find the Hypervisor ID for the VM from the list above"

sudo virsh -c qemu:///system list
echo "Ensure that the ID is the same in this list and the one above."

read -p "What is the VM Hypervisor ID: " IDHyperName
echo "The memory dump will be in $filepath/memdump"
sudo virsh -c qemu:///system dump $IDHyperName $filepath/memdump

echo "The disk dump will be in $filepath/diskdump"
sudo virsh -c qemu://system snapshot-create $IDHyperName $filepath/diskdump --disk-only

echo "The cpu-stats dump will be in $filepath/cpustats"
sudo virsh -c qemu:///system cpu-stats $IDHyperName 2> $filepath/cpustats

echo "The domain memory stats will be in $filepath/dommemdump"
sudo virsh -c qemu:///system dommemstat $IDHyperName

echo "To connect to the machine:"
sudo virsh -c qemu:///system domdisplay $IDHyperName

echo "Domain screenshot at $filepath/screenshot:"
sudo virsh -c qemu:///system screenshot $IDHyperName $filepath/screenshot

