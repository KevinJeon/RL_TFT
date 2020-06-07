import config_3 as cfg
import numpy as np
def find_name(ind):
    champs = list(cfg.champ_state_info)
    if ind == 100:
        return dict(name='Mech Pilot',cost=0,elem=[])
    return champs[ind-1]
def a_star(hexes,st,en):
    sth = [st[0]+int(round(st[1]/2+0.001)),st[1]]
    enh = [en[0]+int(round(en[1]/2+0.001)),en[1]]
    move = [[-1,0],[1,0],[0,-1],[0,1],[1,1],[-1,-1]]
    f_list = []
    for i in range(6):
        g = np.max([abs(move[i][0]),abs(move[i][1]),abs(move[i][0]-move[i][1])])
        h = np.max([abs(enh[0]-sth[0]-move[i][0]),abs(enh[1]-sth[1]-move[i][1]),
            abs(enh[0]-sth[0]-move[i][0]-enh[1]+sth[1]+move[i][1])])
        f = g + h
        f_list.append(f)
    while True:
        minval = np.min(f_list)
        candidates = np.where(f_list==minval)
        near = np.random.choice(candidates[0],1)[0]
        orig = np.array([int(move[near][0]+sth[0]-round(sth[1]/2+0.001)),sth[1]+move[near][1]])
        if np.sum(f_list) == 6000:
            return [0,0]
        elif (orig[0] < 0) or (orig[0] > 6) or (orig[1] < 0) or (orig[1] > 7):
            f_list[near] = 1000
        elif hexes[orig[0],orig[1],0] != 0:
            f_list[near] = 1000
        else:
            break
    return orig
