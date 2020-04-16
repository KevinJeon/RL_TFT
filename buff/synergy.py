import numpy as np
import config_3 as cfg

class Synergy:
    def __init__(self,hexes,start_hexes,mysyn,tic,arrs,opparrs,ds_died=False,
        mech_died=[False,'init'],pirate_kill=0,skilled_champs=0,valkyrie_target=False,
        fourth_attack=False,demol_skilled=False,protector_skillcast=False,
        protector_maintain=[],sniper_enemy=[]):
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
        self.opparrs = opparrs
        self.hexes = hexes
        self.start_hexes = start_hexes
        self.tic = tic
        self.mech_died = mech_died
        self.pirate_kill = pirate_kill
        self.skilled_champs = skilled_champs
        self.valkyrie_target = valkyrie_target
        self.fourth_attack = fourth_attack
        self.demol_skilled = demol_skilled
        self.protector_skillcast = protector_skillcast
        self.sniper_enemy = sniper_enemy
        self.functions = [self._celestial,self._chrono,self._cybernatic,self._dark_star,
            self._mech_pilot,self._rebel,self._space_pirate,self._star_guardian,
            self._valkyrie,self._void,self._blademaster,self._blaster,self._brawler,
            self._demolitionist,self._infiltrator,self._mana_reaver,self._mercenary,
            self._mystic,self._protector,self._sniper,self._sorcerer,self._starship,
            self._vanguard]
        self.pirate_kill = pirate_kill
        self.updated_hexes = None
    def apply(self):
        for k,i in self.syns:
            xy = np.where(self.hexes[:,:,14:15]==i['index'])
            champs = [[x,y] for x,y in zip(xy[0],xy[1])]
            self.functions[i['index']](champs,i['effect'])
    def _celestial(self,champs,effect):
        print('_celestial')
        if self.tic == 0:
            for arr in self.arrs:
                self.hexes[arr[0],arr[1],11] = effect
    def _chrono(self,champs,effect):
        print('_chrono')
        if self.tic > 15:
            pass
        elif self.tic % 4 == 3:
            for arr in self.arrs:
                self.hexes[arr[0],arr[1],6] += effect

    def _cybernatic(self,champs,effect):
        print('_cybernatic')
        if self.tic == 0:
            for champ in champs:
                if self.hexes[champ[0],champ[1],16] != 0:
                    self.hexes[champ[0],champ[1],2] += effect[0]
                    self.hexes[champ[0],champ[1],5] += effect[1]
    def _dark_star(self,champs,effect):
        print('_dark_star')
        if self.ds_died:
            for champ in champs:
                self.hexes[champ[0],champ[1],10] += effect
                self.hexes[champ[0],champ[1],5] += effect
    def _mech_pilot(self,champs,effect):
        print('_mech_pilot')
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
        print('_rebel')
        if self.tic == 0:
            for champ in champs:
                copies = np.tile(champ,(len(champs),1))
                diff = abs(copies-champs)
                adj = len(diff[diff<=2])
                self.hexes[champ[0],champ[1],2] += effect[0]*adj
                self.hexes[champ[0],champ[1],5] += effect[1]*adj
    def _space_pirate(self,champs,effect):
        print('_space_pirate')
        items = [1,2,4,5,6,7,8,10,12,13]
        self.pirate_money,self.pirate_item = 0,[]
        for kill in self.fight_kill:
            self.pirate_money += np.random.choice([0,1],1)[0]
            give = np.random.choice([0,1],1,p=[1-effect,effect])[0]
            if give == 1:
                self.pirate_item += np.random.choice(items,1)[0]
    def _star_guardian(self,champs,effect):
        print('_star_guardian')
        for champ in champs:
            self.hexes[champ[0],champ[1],3] += self.skilled_champs * effect
    def _valkyrie(self,champs,effect):
        '''need to order same with champs'''
        print('_valkyrie')
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
        print('_void')
        1 == 1
    def _blademaster(self,champs,effect):
        print('_blademaster')
        for champ in champs:
            hit = np.random.choice([1,2],1,p=[1-effect,effect])[0]
            self.hexes[champ[0],champ[1],5] = hit * self.hexes[champ[0],champ[1],5]
    def _blaster(self,champs,effect):
        print('_blaster')
        if self.fourth_attack:
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
        print('_brawler')
        if self.tic == 0:
            for champ in champs:
                self.hexes[champ[0],champ[1],2] += effect
    def _demolitionist(self,champs,effect):
        print('_demolitionist')
        for skilled in self.demol_skilled:
            self.hexes[skilled[0],skilled[1],16] = 1
    def _infiltrator(self,champs,effect):
        print('_infiltrator')
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
        print('_mana_reaver')
        1 == 1
    def _mercenary(self,champs,effect):
        '''
        later
        '''
        print('_mercenary')
        1 == 1
    def _mystic(self,champs,effect):
        print('_mystic')
        if self.tic == 0:
            for champ in champs:
                self.hexes[champ[0],champ[1],8] += effect
    def _protector(self,champs,effect):
        print('_protector')
        for prot in self.protector_skillcast:
            self.hexes[prot[0],prot[1],2] += self.start_hexes[prot[0],prot[1],2]*effect
            '''disappear shield later'''
    def _sniper(self,champs,effect):
        print('_sniper')
        if self.tic > 0:
            for champ,enemy in zip(champs,self.sniper_enemy):
                x = abs(champ[0]-enemy[0])
                y = abs(champ[1]-enemy[1])
                self.hexes[champ[0],champ[1],5] += (effect * (x+y))*\
                    self.hexes[champ[0],champ[1],5]
    def _sorcerer(self,champs,effect):
        print('_sorcerer')
        if self.tic == 0:
            for champ in champs:
                self.hexes[champ[0],champ[1],10] += effect
    def _starship(self,champs,effect):
        '''move later'''
        print('_starship')
        for champ in champs:
            self.hexes[champ[0],champ[1],3] += 20
    def _vanguard(self,champs,effect):
        print('_vanguard')
        if self.tic == 0:
            for champ in champs:
                self.hexes[champ[0],champ[1],7] += effect
