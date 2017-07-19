#coding:utf-8

import socket

def port_check(ip,port):
    try:
        socket.setdefaulttimeout(2)
        s=socket.socket
        s.connect(ip,port)
        banner=s.recv(2048)
        return banner
    except:
        return

if __name__=='__main__':
    port_check("10.1.223.21",11521)