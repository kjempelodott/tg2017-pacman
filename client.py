import socket
import json


RUN = False

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((127.0.0.1, 54321))
    s.send('NAME kjempelodott\n')
    
    data = ''

    while '\n' not in data:
        data += s.recv(4096)
    welcome, data = data.split('\n', 1)
    js = json.loads(welcome) 
    gamemap = Map(**js['map'])
    ai = Proteus(**js['you'])
    ai.set_map(gamemap)
    
    while 1:
        while '\n' not in data:
            data += s.recv(4096)
        *states, data = data.split('\n')
        js = msg = None

        for state in states:
            js = json.loads(state)
            msg = js['messagetype']
            if msg in ['dead', 'endofround']:
                RUN = False
            elif msg == 'startofround':
                for other in js['others']:
                    ai.set_other(**other)
                RUN = True

        # Use last update only
        if RUN and msg == 'stateupdate':
            gamemap.update(js['map']['content'])
            for other in js['others']:
                ai.set_other(**other)

            
