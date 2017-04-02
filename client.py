import socket
import json
from ghostly import Map, Player, ProteusV
import random

RUN = False

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 54321))
    s.send(b'NAME %i\n' % random.choice(range(1000)))
    
    data = b''

    while b'\n' not in data:
        data += s.recv(4096)
    welcome, data = data.split(b'\n', 1)
    js = json.loads(welcome.decode())
    gamemap = ai = None
    asciimap = js['map']
    
    while 1:
        while b'\n' not in data:
            data += s.recv(4096)
        *states, data = data.split(b'\n')
        js = msg = None

        for state in states:
            js = json.loads(state.decode())
            msg = js['messagetype']
            if msg in ['dead', 'endofround']:
                RUN = False
            elif msg == 'startofround':
                gamemap = Map(**asciimap)
                ai = ProteusV(gamemap)
                RUN = True

        # Use last update only
        if RUN and msg == 'stateupdate':
            gamemap.update(js['gamestate']['map']['content'])
            ai.update(js['gamestate']['you'], js['gamestate']['others'])
            s.send(b'%s\n' % ai.move())
            
