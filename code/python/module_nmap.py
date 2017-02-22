import subprocess
import socket
import json


def nmapscan(list):
    for server in list:
        try:
            p = subprocess.Popen(
                ['nmap', '-Pn', list[server][2]], stdout=subprocess.PIPE)
            # call(["ssh_scan", "-t", list[server][2]])
            out, err = p.communicate()
            print out
        except:
            print "No IP for:" + server


def sshscan(list):
    for server in list:
        try:
            p = subprocess.Popen(
                ['ssh_scan', '-t', list[server][2]], stdout=subprocess.PIPE)
            # call(["ssh_scan", "-t", list[server][2]])
            out, err = p.communicate()
            jout = json.loads(out)
            print "IP: %s is using: %s" % (jout[0]['ip'], jout[0]['auth_methods'])
        except Exception, e:
            print "Could not check ssh (port 22): %s" % e
