import subprocess
import socket
import json
import os
import xml.etree.ElementTree
import database


##
# This modual will do all the work in running ssh_scan and extracting the needed data.
# A list of IP addressed is feed into the function
# Will call database.PrintList to add the found data into the list
##

def sshscan(list, IPChoose):
    for server in list:
        try:
            p = subprocess.Popen(
                ['ssh_scan', '-t', list[server][IPChoose]], stdout=subprocess.PIPE)
            out, err = p.communicate()
            jout = json.loads(out)
            if IPChoose is 1:
                database.MongoDBUpdate(
                    server, "IP", ('ip_internal', '%s' % (jout[0]['ip'])))
                if len(jout[0]['auth_methods']) is 1:
                    database.MongoDBUpdate(
                        server, "IP", ('ip_internal_auth', '%s' % (jout[0]['auth_methods'][0])))
                else:
                    database.MongoDBUpdate(
                        server, "IP", ('ip_internal_auth', '%s' % (jout[0]['auth_methods'][0] + " " + jout[0]['auth_methods'][1])))
            elif IPChoose is 2:
                database.MongoDBUpdate(
                    server, "IP", ('ip_external', '%s' % (jout[0]['ip'])))
                if len(jout[0]['auth_methods']) is 1:
                    database.MongoDBUpdate(
                        server, "IP", ('ip_external_auth', '%s' % (jout[0]['auth_methods'][0])))
                else:
                    database.MongoDBUpdate(
                        server, "IP", ('ip_external_auth', '%s' % (jout[0]['auth_methods'][0] + " " + jout[0]['auth_methods'][1])))

        except Exception, e:
            # print "Could not check ssh (port 22): %s" % e
            pass
