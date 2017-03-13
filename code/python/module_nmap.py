import subprocess
import socket
import json
import os
import xml.etree.ElementTree
import database


##
# This modual will do all the work in running NMAP and extracting the needed data.
# A list of IP addressed is feed into the function
# Will call database.PrintList to add the found data into the list
##

def nmapscan(list):
    tmpOut = []
    tmpserverList = []
    for server in list:
        try:
            tmpOut.append(list[server][2])
            tmpserverList.append(server)
        except:
            # print "No IP for:" + server
            pass
    tmp = '\n'.join(map(str, tmpOut))
    with open("tmp_nmap.txt", "a") as file:
        file.write(tmp)
    file.close()
    p = subprocess.Popen(['sudo', 'nmap', '-A', '-T5', '-oX',
                          'output.xml', '-iL', 'tmp_nmap.txt'], stdout=subprocess.PIPE)
    # ['sudo', 'nmap', '-A', '-p', '1-65535', '-T5', '-oX', 'output.xml', '-iL', 'tmp_nmap.txt'], stdout=subprocess.PIPE)

    out, err = p.communicate()
    e = xml.etree.ElementTree.parse('output.xml').getroot()
    # extract all hosts from file
    for host in e.findall('host'):
        # print host.find('address').get('addr')
        tmpIndex = tmpOut.index(host.find('address').get('addr'))
        # try to get the port out if no ports avaliable for the host fail
        # siglently
        try:
            for port in host.find('ports').findall('port'):
                database.MongoDBConnection(tmpserverList[tmpIndex], "ports", (port.get(
                    'portid'), port.find('state').get('state')))
                database.PrintList(tmpserverList[tmpIndex], "port: %s" % (
                    port.get('portid')), "%s" % (port.find('state').get('state')))
                if port.find('service').get("version") is not None and port.find('service').get('product') is not None:
                    database.PrintList(tmpserverList[tmpIndex], "service: %s on port %s is version:" % (port.find(
                        'service').get('product'), port.get('portid')), "%s" % (port.find('service').get('version')))
            # print "--" + port.get('portid') + ": " +
            # port.find('state').get('state')
            osName = host.find('os').findall('osmatch')
            database.PrintList(
                tmpserverList[tmpIndex], "OS", "%s" % (osName[0].get('name')))
        except:
            pass
    os.remove("tmp_nmap.txt")
    os.remove("output.xml")
