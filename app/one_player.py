
import config_3 as cfg
import numpy as np
from fight.fight import Fight
from buff.items import Item
from env import TFT_env
from agent.random_agent import *
from agent.rulebased_agent import *
class Player:
    def __init__(self,agent,name=None):
        '''
        action space :
        act1 = player's act before fight
        act2 = player's act about arrange units
        act3 = about item
        state :
        units, arrange, xp, money, life
        '''

        # units
        self.total_units = dict()
        self.removal = dict(c1=[],c2=[],c3=[],c4=[],c5=[]) # already level 3 unit
        self.fight_group = []
        self.fight_units = [] # fore rearrange
        self.fight_synergy = []
        self.fight_items = []
        self.wait_units = []
        self.agent = agent
        self.unit_number = 0
    def init_player(self):
        # init game
        self.money = 0 # 돈
        self.place = 8 # 등수 --> 최종 reward
        self.life = 100 # 체력
        self.xp = 0 # xp
        self.continuous = 0 # state reward
        self.player_level = 1
        self.five_champs = [True]*5
        self.five_cost = [0]*5
        self.player_synergy = dict()
    def _champ_queue(self):
        self.five_champs,self.five_cost = [],[]
        tofill = 5
        while True:
            stars = np.bincount(np.random.choice(5,size=tofill,
                p=self.champ_distribution['l'+str(self.player_level)]))
            for rem,star,n_champs in zip(self.removal.items(),stars,self.champ_cost_info.items()):
                n_champs = n_champs[1]
                for r in rem[1]:
                    if r in n_champs:
                        n_champs.remove(r)
                cnts = [self.champ_state_info[champ]['count'] for champ in n_champs]
                candidates = list(range(len(n_champs)))
                if sum(cnts) == 0:
                    continue
                prob = [c/sum(cnts) for c in cnts]
                #print('n_champs : {}, removal {}, star {}'.format(n_champs,self.removal,star))
                champs = np.random.choice(candidates,size=star,p=prob)
                self.five_champs += [n_champs[c] for c in champs]
            for c in self.five_champs:
                if self.champ_state_info[c]['count'] < self.five_champs.count(c):
                    erase = self.five_champs.count(c) - self.champ_state_info[c]['count']
                    for e in range(erase):
                        print('erase!')
                        print(len(self.five_champs))
                        print(self.five_champs)
                        self.five_champs.remove(c)
            tofill = 5 - len(self.five_champs)
            if tofill == 0:
                break
        self.five_cost += [self._cost(c+'_1') for c in self.five_champs]
    def _cost(self,champ):
        cost_info = np.array([1,3,5])
        level = int(champ[-1])
        champ = champ[:-2]
        for (star,champs) in self.champ_cost_info.items():
            if champ in champs:
                return cost_info[level-1]
            cost_info += 1
    def _money(self):
        '''
        money rule
        1. '1-2','1-3' : 2
        2. '1-4','2-1 : 3
        3. '2-2' : 4
        4. interset : 10골드 당 1원 max 5
        5. continuous : 2 - +1 3 - +2 4 ~ - +3
        '''
        if self.cur_round in ['1-2','1-3','1-4','2-1','2-2']:
            self.money += 2
            if (self.cur_round[0] == '2') or (self.cur_round[-1] == '4'):
                self.money += 1
                if self.cur_round[-1] == '2':
                    self.money += 1
        else:
            self.money += 5
        if self.money > 50:
            self.money += 5
        else:
            self.money += self.money // 10
        if abs(self.continuous) >= 4:
            self.money += 3
        elif abs(self.continuous) >= 3:
            self.money += 2
        elif abs(self.continuous) >= 2:
            self.money += 1
    def _update_synergy(self):
        '''
        for fight units
        '''
        syn_list = []
        used = []
        self.player_synergy = dict()
        for syns,unit in zip(self.fight_synergy,self.fight_units):
            if unit[:-4] not in used:
                syn_list += syns
                used.append(unit[:-4])
        syn = np.bincount(syn_list)
        for n,((k,i),s) in enumerate(zip(self.synergy_info.items(),syn)):
            rate = 0
            while s >= i['rate'][rate]:
                rate += 1
                if rate >= len(i['rate']):
                    break
            if rate >= 1:
                champs = []
                for m,info in enumerate(self.fight_infos):
                    if n in info['synergy'] :
                        champs.append(m)
                self.player_synergy[k] = dict(champ=champs,
                    effect=i['effect'][rate-1],index=n)
    def champ_append(self,champ,item=None):
        self.unit_number += 1
        if champ in self.total_units.keys():
            self.total_units[champ]['count'] += 1
            if item:
                self.total_units[champ]['item'] += item
                self.total_units[champ]['owner'].append(1)
            if self.total_units[champ]['count'] == 3:
                self.unit_number -= 2
                levup = int(champ[-1]) + 1
                levup_champ = champ[:-1] + str(levup)
                self.champ_append(levup_champ,self.total_units[champ]['item'])
                del self.total_units[champ]
        else:
            num = self.champ_state_info[champ[:-2]]['num']
            synergy = self.champ_state_info[champ[:-2]]['elem']
            infos = self.champ_level_info[champ[:-2]].items()
            info = dict()
            level = champ[-1]
            for k,i in infos:
                if (k == 'health') or (k=='attack_damage') or (k=='dps'):
                    info[k] = i*1.8**(int(level)-1)
                else:
                    info[k] = i
            if item:
                self.total_units[champ] = dict(count=1,synergy=synergy,info=info,
                    item=item,owner=[0],num=num)
            else:
                self.total_units[champ] = dict(count=1,synergy=synergy,info=info,
                    item=[],owner=[],num=num)

            if level == '3':
                for c in self.champ_cost_info.items():
                    if champ[:-2] in c[1]:
                        if c[0] in self.removal.keys():
                            self.removal[c[0]].append(champ[:-2])
                        else:
                            self.removal[c[1]] = [champ[:-2]]
    def _player_levelup(self):
        if self.player_level == 9:
            pass
        else:
            while self.xp >= self.need_xp[self.player_level-1]:
                self.player_level += 1
            self.champ_prob = self.champ_distribution['l'+str(self.player_level)]
    def _before_fight(self,act1):
        champ_queue = [None,None]
        if act1 <= 4:
            cost = self._cost(self.five_champs[act1]+'_1')
            self.money -= cost
            self.champ_append(self.five_champs[act1]+'_1',None)
            champ_queue = [self.five_champs[act1],-1]
            print('buy!',champ_queue)
            self.five_champs[act1] = False
            self.is_prepared = False
        elif act1 == 5:
            self.is_prepared = True
        elif act1 == 6:
            ind = np.random.choice(len(self.total_units.keys()))
            champ = list(self.total_units.keys())[ind]
            self.money += self._cost(champ)
            self.unit_number -= 1
            self.total_units[champ]['count'] -= 1
            champ_queue = [champ[:-2],3**(int(champ[-1])-1)]
            print('sell!',[champ[:-2],3**(int(champ[-1])-1)])
            if self.total_units[champ]['count'] == 0:
                if self.total_units[champ]['item']:
                    self.wait_items += self.total_units[champ]['item']
                del self.total_units[champ]
            self.is_prepared = False
        elif act1 == 7:
            self.money -= 2
            self._champ_queue()
            self.is_prepared = False
        elif act1 == 8:
            self.xp += 4
            self._player_levelup()
            self.money -= 4
            self.is_prepared = False
        self._update_synergy()
        return champ_queue
    def _rearrange(self,action=None):
        # random pick & random arrange
        units,syns = [],[]
        self.fight_num,self.fight_infos = [],[]
        self.fight_items,self.fight_units = [],[]
        for k,i in self.total_units.items():
            for n in range(i['count']):
                info = i['info']
                info['synergy'] = i['synergy']
                units += [k+'_'+str(n)]
                syns += [i['synergy']]
                self.fight_num += [i['num']]
                self.fight_infos += [info]
        if len(units) <= self.player_level:
            self.fight_units = units
            avail_units = len(units)
        else:
            avail_units = self.player_level
            if action==RandomAgent.rearr_action:
                chosen = np.random.choice(len(units),self.player_level,replace=False)
            else:
                chosen = action(avail_units,syns)
            self.fight_units = [units[c] for c in chosen]
            self.fight_synergy = [syns[c] for c in chosen]
            self.fight_infos = [self.fight_infos[c] for c in chosen]
            self.fight_num = [self.fight_num[c] for c in chosen]
        for unit in self.fight_units:
            items = self.total_units[unit[:-2]]['item']
            owners = self.total_units[unit[:-2]]['owner']
            unit_item = []
            for owner,item in zip(owners,items):
                if owner == int(unit[-1]):
                    unit_item += [item]
            self.fight_items.append(unit_item)
        yy = np.arange(4)
        xx = np.arange(7)
        hex_x = np.random.choice(xx,avail_units)
        hex_y = np.random.choice(yy,avail_units)
        self.fight_arrange = list(set([(x,y) for x,y in zip(hex_x,hex_y)]))
        tofill = avail_units - len(self.fight_arrange)
        while tofill != 0:
            hex_x = np.random.choice(xx,1)[0]
            hex_y = np.random.choice(yy,1)[0]
            if tuple([hex_x,hex_y]) not in list(self.fight_arrange):
                self.fight_arrange.append((hex_x,hex_y))
                tofill -= 1
    def _assign_item(self):
        items = Item(self.fight_items,self.fight_infos)
    def prepare_round(self):
        self._money()
        self._champ_queue()
        self.xp += 2
        self._player_levelup()
        self.is_prepared = False
        champ_queues = []
        while self.is_prepared != True:
            act = self.agent.bef_action(self.money,self.player_level,self.five_champs,
                self.five_cost,self.total_units)
            #print(act)
            #print(self.act1_spc[act])
            champ_queue = self._before_fight(act)
            champ_queues.append(champ_queue)
            if act == 5:
                self.is_prepared = True
                self._rearrange(action=self.agent.rearr_action)
                self._assign_item()
                self._update_synergy()
        return champ_queues
    def result(self,result):
        msg = ('-----------------------\n'+\
            '{}\n'+\
            'ROUND {} finish\n'+\
            'Win : {}\n'+\
            'Life : {}\n'+\
            'Player level : {}\n'+\
            'Money : {}\n'+\
            'Champs : {}\n'+\
            'Continuous : {}\n'+\
            'Synergy : {}\n'+\
            'Items : {}\n'+\
            '-----------------------').format(self.name,self.cur_round,result,self.life,self.player_level,
                self.money,self.fight_units,self.continuous,self.player_synergy,self.fight_items)
        #print(msg)
