#!/bin/python3
import socket
# trier les imports >< limiter la pollution
import sys
import os
from threading import Thread, Lock
from queue import Queue

socket.setdefaulttimeout(0.10)
threads = 100
queue = Queue()
print_lock = Lock()


def sload():
    global s
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        print("Socket Not loaded.")

def ping(ip):
    r = os.system("ping -c 1 -W 0.150 "+ip+" > /dev/null")
    if r == 0:
        portscan(ip)
    else:
        print("Host is down.")
        sys.exit()

def portscan(ip):
    ports = []
    os.system("clear")
    print("1. Specific port\n")
    print("2. Range of ports\n")
    print("3. All ports\n")
    select=input("Select a choice : ")
    if (select == "1"):
        p = int(input("\nEnter port: "))
        try:
            sload()
            print(ip,p)
            s.connect((ip, p))
            print("[",p,"] Open.")
            #identifier les services
        except:
            print("[",p,"] Closed.")
    elif (select == "2"):
        p = int(input("Start range: "))
        p2 = int(input("End range: "))
        for x in range(p, p2+1):
            try:
                sload()
                s.connect((ip, x))
                with print_lock:
                    print("[O]",x)
                    ports.append(x)
                s.close()
            except (socket.timeout, ConnectionRefusedError):
                pass
    print("Ports open :", ports,"\n")

ch = True
while ch:
    print("1. Scan port\n")
    print("2. Scan network\n")
    select=input("Select a choice : ")
    if (select == "1"):
        ip = input("[.] Enter an IP: ")
        ping(ip)
