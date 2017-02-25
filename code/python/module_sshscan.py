import subprocess
import socket
import json
import os
import xml.etree.ElementTree


def sshscan(list, IPChoose):
    for server in list:
        try:
            p = subprocess.Popen(
                ['ssh_scan', '-t', list[server][IPChoose]], stdout=subprocess.PIPE)
            out, err = p.communicate()
            jout = json.loads(out)
            print "IP: %s is using: %s" % (jout[0]['ip'], jout[0]['auth_methods'])
        except Exception, e:
            # print "Could not check ssh (port 22): %s" % e
            pass
