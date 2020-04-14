import numpy as np
import config_3 as cfg

class Synergy:
    def __init__(self,hexes,mysyn,tic,arrs,ds_died=False,mech_died=[False,'init']):
        '''
        hexes : chess board
        mysyn : synergies
            - index : synergy index
            - champ : champ (x,y)
            - effect : effect
        tic : time
        ds_died : dead dark star, judge when _die
        mech_died : [True,xy of mech]
        '''
        self.ds_died = ds_died
        self.syns = list(mysyn.items())
        self.arrs = arrs
        self.hexes = hexes
        self.tic = tic
        self.mech_died = mech_died
        self.functions = [self._celestial,self._chrono,self._cybernatic,self._dark_star,
            self._mech_pilot,self._rebel,self._space_pirate,self._star_guardian,
            self._valkyrie,self._void,self._blademaster,self._blaster,self._brawler,
            self._demolitionist,self._infiltrator,self._mana_reaver,self._mercenary,
            self._mystic,self._protector,self._sniper,self._sorcerer,self._starship,
            self._vanguard]
        self.updated_hexes = None
        self._call()
    def _call(self):
        for k,i in self.syns:
            champs = np.where(self.hexes[:,:,14:15]==i['index'])
            self.functions[i['index']](champs,i['effect'])
    def _celestial(self,champs,effect):
        if self.tic > 0:
            pass
        for arr in self.arrs:
            self.hexes[arr[0],arr[1],11] = effect
    def _chrono(self,champs,effect):
        if self.tic > 15:
            pass
        elif self.tic % 4 == 3:
            for arr in self.arrs:
                self.hexes[arr[0],arr[1],6] += effect

    def _cybernatic(self,champs,effect):
        if self.tic > 0:
            pass
        for champ in champs:
            if self.hexes[champ[0],champ[1],16] != 0:
                self.hexes[champ[0],champ[1],2] += effect[0]
                self.hexes[champ[0],champ[1],5] += effect[1]
    def _dark_star(self,champs,effect):
        if self.ds_died:
            for champ in champs:
                self.hexes[champ[0],champ[1],10] += effect
                self.hexes[champ[0],champ[1],5] += effect
    def _mech_pilot(self,champs,effect):
        if self.mech_died[0]:
            xy = self.mech_died[1]
            n = 0
            tofill = [self.mech1,self.mech2,self.mech3]
            while n != 3:
                xlist = list(range(self.mech_died[1][0]-2,self.mech_died[1][0]+2))
                ylist = list(range(self.mech_died[1][1]-2,self.mech_died[1][1]+2))
                x = np.random.choice(xlist,1)[0]
                y = np.randon.choice(ylist,1)[0]
                if self.hexes[x,y,0] == 0:
                    self.hexes[x,y,:] = tofill[n]
                    n += 1
        elif self.mech_died[1] == 'init':
            selected = np.random.choice(champs,3)
            xy = np.random.choice(selected,1)[0]
            items = []
            it = 0
            self.mech1 = self.hexes[selected[0][0],selected[0][1],:]
            self.mech2 = self.hexes[selected[1][0],selected[1][1],:]
            self.mech3 = self.hexes[selected[2][0],selected[2][1],:]
            for sel in selected:
                if sel == xy:
                    continue
                else:
                    self.hexes[xy[0],xy[1],1] = 100
                    self.hexes[xy[0],xy[1],2:14] += self.hexes[sel[0],sel[1],2:14]
                for i in range(3):
                    item = self.hexes[sel[0],sel[1],16+2*i:18+2*i]
                    if sum(item) == 0:
                        continue
                    is_chosen = np.random.choice([0,1],1)
                    if it > 3:
                        continue
                    if is_chosen != 0:
                        self.hexes[xy[0],xy[1],16+2*it:18+2*it] = item
                        it += 1
    def _rebel(self,champs,effect):
        1 == 1
    def _space_pirate(self,champs,effect):
        1 == 1
    def _star_guardian(self,champs,effect):
        1 == 1
    def _valkyrie(self,champs,effect):
        1 == 1
    def _void(self,champs,effect):
        1 == 1
    def _blademaster(self,champs,effect):
        1 == 1
    def _blaster(self,champs,effect):
        1 == 1
    def _brawler(self,champs,effect):
        1 == 1
    def _demolitionist(self,champs,effect):
        1 == 1
    def _infiltrator(self,champs,effect):
        1 == 1
    def _mana_reaver(self,champs,effect):
        1 == 1
    def _mercenary(self,champs,effect):
        1 == 1
    def _mystic(self,champs,effect):
        1 == 1
    def _protector(self,champs,effect):
        1 == 1
    def _sniper(self,champs,effect):
        1 == 1
    def _sorcerer(self,champs,effect):
        1 == 1
    def _starship(self,champs,effect):
        1 == 1
    def _vanguard(self,champs,effect):
        1 == 1
