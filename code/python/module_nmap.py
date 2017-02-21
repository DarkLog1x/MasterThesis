from subprocess import call
import socket


def nmapscan(list):
    for server in list:
        try:
            call(["nmap", "-Pn", list[server][2]])
        except:
            print "No IP for:" + server


def sshscan(list):
    for server in list:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((list[server][2], 22))
        except:
            print "Could not check ssh (port 22)"
