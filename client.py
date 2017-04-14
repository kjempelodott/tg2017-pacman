#!/usr/bin/env python3

import sys
import socket
import json
from ghostly import Map, Player, ProteusV

RUN = False
HOST = PORT = None

try:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
except:
    print('Usage: ./client.py host port')
    exit()

if __name__ == '__main__':

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(b'NAME kjempelodott\n')
    
    data = b''
    gamemap = ai = None
    
    while 1:
        while b'\n' not in data:
            data += s.recv(4096)
        *states, data = data.split(b'\n')
        js = msg = None

        for state in states:
            js = json.loads(state.decode())
            msg = js['messagetype']
            if msg == 'dead':
                RUN = False
                ai.die()
            elif msg == 'endofround':
                RUN = False
            elif msg == 'startofround':
                RUN = True
                gamemap = None

        # Use last update only
        if RUN and msg == 'stateupdate':
            if not gamemap:
                gamemap = Map(**js['gamestate']['map'])
                if ai:
                    ai.reset(gamemap)
            else:
                gamemap.update(js['gamestate']['map']['content'])
            if not ai:
                ai = ProteusV(gamemap)

            ai.update(js['gamestate']['you'], js['gamestate']['others'])
            s.send(b'%s\n' % ai.move())
            
