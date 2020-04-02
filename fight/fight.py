import numpy as np
import config_3 as cfg
class Fight:
    def __init__(self,myunits,mynum,myarr,myitems,mysyn,myinfo):
        myskill = None
        self.myunits = myunits
        self.mynum = mynum
        self.myarr = myarr
        self.myitems = myitems
        self.mysyn = mysyn
        self.myinfo = myinfo
        hexes = np.zeros((56,15))
        self.myhexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill)
        self.opphexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill)
        self.myarr = myarr
    def _assign_hexes(self,hexes,num,arr,items,syn,info,skill):
        for n,a,item,inf in zip(num,arr,items,info):
            hexes[a,0] = n
            hexes[a,1] = inf['health']
            hexes[a,2] = inf['mana'][0]
            hexes[a,3] = inf['mana'][1]
            hexes[a,4] = inf['attack_range']
            hexes[a,5] = inf['attack_damage']
            hexes[a,6] = inf['armor']
            hexes[a,7] = inf['magical_resistance']
            for c,it in enumerate(item):
                hexes[a,9+c] = it
        return hexes
    def _move(self,hexes):
        move_range = [-1,0,1]
        for i,arr in enumerate(self.myarr):
            while True:
                move = np.random.choice(move_range,2)
                move[1] = move[1]*7
                move = sum(move)
                if ((arr+move < 27) and (arr+move > -54)) and (arr+move not in self.myarr):
                    self.myarr[i] = move + arr
                    break
    #def _avail_attack(self):
    #    self.myhexes
    def _fight_tic(self,hexes):
        print(np.reshape(hexes[:,0],(8,7)))
        self._move(hexes)
        skill = None
        hexes = np.zeros((56,15))
        hexes = self._assign_hexes(hexes,self.mynum,self.myarr,self.myitems,
            self.mysyn,self.myinfo,skill)
        print(np.reshape(hexes[:,0],(8,7)))
        return hexes
    def fight(self):
        self._fight_tic(self.myhexes)
