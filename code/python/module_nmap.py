import subprocess
import socket
import json
import os
import xml.etree.ElementTree


def nmapscan(list):
    tmpOut = []
    for server in list:
        try:
            tmpOut.append(list[server][2])
        except:
            # print "No IP for:" + server
            pass
    tmp = '\n'.join(map(str, tmpOut))
    with open("tmp_nmap.txt", "a") as file:
        file.write(tmp)
    file.close()
    p = subprocess.Popen(
        ['sudo', 'nmap', '-PnsS', '-T5', '-oX', 'output.xml', '-iL', 'tmp_nmap.txt'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    e = xml.etree.ElementTree.parse('output.xml').getroot()
    for host in e.findall('host'):
        print host.find('address').get('addr')
        for port in host.find('ports').findall('port'):
            print "--" + port.get('portid') + ": " + port.find('state').get('state')

    os.remove("tmp_nmap.txt")
    os.remove("output.xml")
