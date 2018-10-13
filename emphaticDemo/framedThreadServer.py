#! /usr/bin/env python3
import sys, os, socket, params, time
import threading
from threading import Thread
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

lock = threading.Lock() # Mutex object

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0        # one instance / class
    def __init__(self, sock, debug):
        global lock
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
        global lock
        while True:
            msg = self.fsock.receivemsg()
            if not msg:
                if True: print(self.fsock, "server thread done")
                lock.release() # Release lock
                return    
            requestNum = ServerThread.requestCount
            time.sleep(0.001)
            ServerThread.requestCount = requestNum + 1
            isAFileName = msg.decode()
            msg = ("%s! (%d)" % (msg, requestNum)).encode()
            self.fsock.sendmsg(msg)
            spl = isAFileName.split("$")
            if spl[0] == "NOF":
             if not os.path.isfile("serverFiles/"+spl[1]):
              self.fsock.sendmsg(b"good to go")
              fileName = spl[1]
              with open("serverFiles/"+fileName,"wb") as file:
               print("Allocating file "+fileName)
               while True:
               	data = self.fsock.receivemsg()
               	if not data:
               	 break
               	file.write(data)
               	self.fsock.sendmsg(data)
             else:
               self.fsock.sendmsg(b"FIS$")


while True:
    lock.acquire() # Lock activated 
    sock, addr = lsock.accept()
    ServerThread(sock, debug)
