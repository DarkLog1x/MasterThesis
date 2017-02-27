import subprocess
import socket
import json
import os
import xml.etree.ElementTree
import database


def sshscan(list, IPChoose):
    for server in list:
        try:
            p = subprocess.Popen(
                ['ssh_scan', '-t', list[server][IPChoose]], stdout=subprocess.PIPE)
            out, err = p.communicate()
            jout = json.loads(out)
            if IPChoose is 1:
                database.PrintList(
                    server, 'ip_internal', "%s : %s " % (jout[0]['ip'], jout[0]['auth_methods']))
                # database.PrintList(
                # server, 'ip_internal_auth', jout[0]['auth_methods'])
            elif IPChoose is 2:
                database.PrintList(
                    server, 'ip_external', "%s : %s" % (jout[0]['ip'], jout[0]['auth_methods']))
                # database.PrintList(
                # server, 'ip_external_auth', jout[0]['auth_methods'])
            # print "IP: %s is using: %s" % (jout[0]['ip'],
            # jout[0]['auth_methods'])
        except Exception, e:
            # print "Could not check ssh (port 22): %s" % e
            pass
