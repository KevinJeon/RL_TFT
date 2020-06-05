import config_3 as cfg
import numpy as np
def find_name(ind):
    champs = list(cfg.champ_state_info)
    if ind == 100:
        return dict(name='Mech Pilot',cost=0,elem=[])
    return champs[ind-1]

def a_star(hexes,st,en):
    if st[1] % 2 == 0:
        move = [[-1,1],[-1,-1],[0,1],[0,-1]]
    elif st[1] % 2 == 1:
        move = [[0,1],[1,1],[1,-1],[-1,-1]]
    move += [[-1,0],[1,0]]
    f_list = []
    for i in range(6):
        g = np.max([abs(move[i][0]),abs(move[i][1]),abs(move[i][0]-move[i][1])])
        h = np.max([abs(en[0]-st[0]-move[i][0]),abs(en[1]-st[1]-move[i][1]),
            abs(en[0]-st[0]-move[i][0]-en[1]+st[1]+move[i][1])])
        f = g + h
        f_list.append(f)
    while True:
        near = np.argmin(f_list)
        if ((st[0] + move[near][0]) < 0) or ((st[0] + move[near][0]) > 6) or \
            ((st[1] + move[near][1]) < 0) or (((st[1] + move[near][1]) > 7)):
            f_list[near] = 1000
        elif hexes[st[0] + move[near][0],st[1] + move[near][1],0] != 0:
            f_list[near] = 1000
        elif np.sum(f_list) == 6000:
            print('no where to move!')
            return [0,0]
        else:
            break
    print('move to',move[near])
    return move[near]
