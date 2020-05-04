import numpy as np
import config_3 as cfg

class Synergy:
    def __init__(self,hexes,start_hexes,mysyn,tic,arrs,opparrs,ds_died=False,
        mech_died=[False,'init'],pirate_kill=0,star_skilled=0,valkyrie_target=[],
        demol_skilled=False,protector_skillcast=[],protector_maintain=[]):
        '''
        hexes : chess board
        mysyn : synergies
            - index : synergy index
            - champ : champ (x,y)
            - effect : effect
        tic : time
        ds_died : dead dark star, judge when _die - done
        mech_died : [True,xy of mech] -
        pirate_kill : int
        star_skilled : int
        valkyrie_target : enemy - [x,y]
        demol_skilled : stunned
        protector_skillcast : shield make
        '''
        self.syns = list(mysyn.items())
        self.arrs = arrs
        self.opparrs = opparrs
        self.hexes = hexes
        self.start_hexes = start_hexes
        self.tic = tic
        self.ds_died = ds_died
        self.mech_died = mech_died
        self.pirate_kill = pirate_kill
        self.pirate_money,self.pirate_item = 0,[]
        self.star_skilled = star_skilled
        self.valkyrie_target = valkyrie_target
        self.demol_skilled = demol_skilled # later
        self.protector_skillcast = protector_skillcast
        self.is_pirate,self.is_sniper,self.is_void = False,False,False
        self.is_starguard,self.is_protector,self.is_valkyrie = False,False,False
        self.is_infil = False
        self.functions = [self._celestial,self._chrono,self._cybernatic,self._dark_star,
            self._mech_pilot,self._rebel,self._space_pirate,self._star_guardian,
            self._valkyrie,self._void,self._blademaster,self._blaster,self._brawler,
            self._demolitionist,self._infiltrator,self._mana_reaver,self._mercenary,
            self._mystic,self._protector,self._sniper,self._sorcerer,self._starship,
            self._vanguard]
        self.updated_hexes = None
    def apply(self):
        for k,i in self.syns:
            xy = np.where(self.hexes[:,:,14:15]==i['index'])
            champs = [[x,y] for x,y in zip(xy[0],xy[1])]
            self.functions[i['index']](champs,i['effect'])
    def _celestial(self,champs,effect):
        if self.tic == 0:
            #print('_celestial')
            for arr in self.arrs:
                self.hexes[arr[0],arr[1],11] = effect
    def _chrono(self,champs,effect):
        if self.tic > 15:
            #print('_chrono')
            pass
        elif self.tic % 4 == 3:
            #print('_chrono')
            for arr in self.arrs:
                self.hexes[arr[0],arr[1],6] += effect

    def _cybernatic(self,champs,effect):
        if self.tic == 0:
            #print('_cybernatic')
            for champ in champs:
                if self.hexes[champ[0],champ[1],16] != 0:
                    self.hexes[champ[0],champ[1],2] += effect[0]
                    self.hexes[champ[0],champ[1],5] += effect[1]
    def _dark_star(self,champs,effect):
        if self.ds_died:
            #print('_dark_star')
            for champ in champs:
                self.hexes[champ[0],champ[1],10] += self.ds_died*effect
                self.hexes[champ[0],champ[1],5] += self.ds_died*effect
    def _mech_pilot(self,champs,effect):
        if self.mech_died[0]:
            #print('_mech_pilot')
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
            #print('_mech_pilot')
            print(champs)
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
                    item = self.hexes[sel[0],sel[1],17+2*i:19+2*i]
                    if sum(item) == 0:
                        continue
                    is_chosen = np.random.choice([0,1],1)
                    if it > 3:
                        continue
                    if is_chosen != 0:
                        self.hexes[xy[0],xy[1],17+2*it:19+2*it] = item
                        it += 1
    def _rebel(self,champs,effect):
        if self.tic == 0:
            #print('_rebel')
            for champ in champs:
                copies = np.tile(champ,(len(champs),1))
                diff = abs(copies-champs)
                adj = len(diff[diff<=2])
                self.hexes[champ[0],champ[1],2] += effect[0]*adj
                self.hexes[champ[0],champ[1],5] += effect[1]*adj
    def _space_pirate(self,champs,effect):
        #print('_space_pirate')
        self.is_pirate = True
        items = [1,2,4,5,6,7,8,10,12,13]
        for kill in range(self.pirate_kill):
            self.pirate_money += np.random.choice([0,1],1)[0]
            give = np.random.choice([0,1],1,p=[1-effect[0],effect[0]])[0]
            if give == 1:
                self.pirate_item += np.random.choice(items,1)[0]
    def _star_guardian(self,champs,effect):
        #print('_star_guardian')
        self.is_starguard = True
        for champ in champs:
            self.hexes[champ[0],champ[1],3] += self.star_skilled * effect
    def _valkyrie(self,champs,effect):
        '''need to order same with champs'''
        #print('_valkyrie')
        for i,champ in enumerate(champs):
            enemy = self.valkyrie_target[i]
            if self.hexes[enemy[0],enemy[1],2] < self.start_hexes[enemy[0],enemy[1],2]/2:
                self.hexes[champ[0],champ[1],13] = 1
            else:
                self.hexes[champ[0],champ[1],13] = self.start_hexes[enemy[0],enemy[1],13]
    def _void(self,champs,effect):
        '''
        apply at fight.py
        '''
        #print('_void')
        self.is_void = True
        1 == 1
    def _blademaster(self,champs,effect):
        #print('_blademaster')
        for champ in champs:
            hit = np.random.choice([1,2],1,p=[1-effect,effect])[0]
            self.hexes[champ[0],champ[1],5] = hit * self.hexes[champ[0],champ[1],5]
    def _blaster(self,champs,effect):
        if self.tic % 4 == 1:
            #print('_blaster')
            for champ in champs:
                if len(self.opparr) <= effect:
                    effect = len(self.opparr)
                additonals = np.random.choice(self.opparr,effect,replace=False)
                for add in additonals:
                    damage = self.hexes[champ[0],champ[1],5] - self.hexes[add[0],add[1],7]
                    if damage < 0:
                        damage = 0
                    self.hexes[add[0],add[1],2] -= damage/2*self.hexes[champ[0],champ[1],6]
    def _brawler(self,champs,effect):
        #print('_brawler')
        if self.tic == 0:
            for champ in champs:
                self.hexes[champ[0],champ[1],2] += effect
    def _demolitionist(self,champs,effect):
        #print('_demolitionist')
        for skilled in self.demol_skilled:
            self.hexes[skilled[0],skilled[1],18] = 2 # stunned for 2 tics
    def _infiltrator(self,champs,effect):
        #print('_infiltrator')
        self.is_infil = True
        if self.tic == 0:
            '''
            move later
            '''
            for champ in champs:
                self.hexes[champ[0],champ[1],6] += effect
    def _mana_reaver(self,champs,effect):
        '''
        later
        '''
        #print('_mana_reaver')
        1 == 1
    def _mercenary(self,champs,effect):
        '''
        later
        '''
        #print('_mercenary')
        1 == 1
    def _mystic(self,champs,effect):
        if self.tic == 0:
            #print('_mystic')
            for champ in champs:
                self.hexes[champ[0],champ[1],8] += effect
    def _protector(self,champs,effect):
        #print('_protector')
        self.is_protector = True
        for prot in self.protector_skillcast:
            self.hexes[prot[0],prot[1],2] += self.start_hexes[prot[0],prot[1],2]*effect
            '''disappear shield later'''
    def _sniper(self,champs,effect):
        self.is_sniper = True
    def _sorcerer(self,champs,effect):
        if self.tic == 0:
            #print('_sorcerer')
            for champ in champs:
                self.hexes[champ[0],champ[1],10] += effect
    def _starship(self,champs,effect):
        '''move later'''
        #print('_starship')

        for champ in champs:
            self.hexes[champ[0],champ[1],3] += 20
    def _vanguard(self,champs,effect):
        if self.tic == 0:
            #print('_vanguard')
            for champ in champs:
                self.hexes[champ[0],champ[1],7] += effect
