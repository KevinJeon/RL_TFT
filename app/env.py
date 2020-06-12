
import config_3 as cfg
import numpy as np
from fight.fight import Fight
from buff.items import Item
import time
# env
'''
1. mixed item
2. visualize more
'''

class TFT_env:
    def __init__(self,elements,champ_state_info,champ_cost_info,champ_level_info,
        champ_distribution,sushi_distribution,synergy_info,agent1=None,agent2=None,
        agent3=None,agent4=None,agent5=None,agent6=None,agent7=None,agent8=None,
        **kwargs):
        '''
        action space :
        act1 = player's act before fight
        act2 = player's act about arrange units
        act3 = about item
        state :
        units, arrange, xp, money, life
        '''
        # base
        self.items = ['items']
        self.act1_spc = ['pick1','pick2','pick3','pick4','pick5','save','sell','reroll','xp']
        self.act2_spc = [i for i in range(28)]
        self.act3_spc = ['item']
        self.champ_state_info = champ_state_info
        self.champ_cost_info = champ_cost_info
        self.champ_level_info = champ_level_info
        self.cur_round = '1-1'
        self.synergy_info = synergy_info
        self.items = [2,3,5,6,7,8,9,10,12]
        self.elements = elements
        self.limit = dict(c1=29,c2=22,c3=16,c4=12,c5=10)
        # player
        self.need_xp = [2,4,8,14,24,44,76,126,192]
        # about sushi,reroll
        self.sushi_distribution = sushi_distribution
        self.champ_distribution = champ_distribution
        # agent
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent3 = agent3
        self.agent4 = agent4
        self.agent5 = agent5
        self.agent6 = agent6
        self.agent7 = agent7
        self.agent8 = agent8
        self.place = 8
        self.place_table = [['agent{}'.format(i+1),100] for i in range(8)]
        self.final_place = dict(agent1=1,agent2=1,agent3=1,agent4=1,agent5=1,
            agent6=1,agent7=1,agent8=1,)
    def init_game(self):
        self.players = [self.agent1,self.agent2,self.agent3,self.agent4,self.agent5,
            self.agent6,self.agent7,self.agent8]
        self.jd = dict(state=[],action=[])
        for n,player in enumerate(self.players):
            player.name = 'agent{}'.format(n+1)
            player.champ_distribution = self.champ_distribution
            player.champ_state_info = self.champ_state_info
            player.champ_level_info = self.champ_level_info
            player.champ_cost_info = self.champ_cost_info
            player.synergy_info = self.synergy_info
            player.act1_spc = self.act1_spc
            player.act2_spc = self.act2_spc
            player.act3_spc = self.act3_spc
            player.cur_round = self.cur_round
            player.need_xp = self.need_xp
            player.init_player()
        self._sushi()
    def _round(self):
        big_round = int(self.cur_round[0])
        sub_round = int(self.cur_round[-1])
        if big_round == 1:
            if sub_round == 4:
                big_round += 1
                sub_round = 1
            else:
                sub_round += 1
        else:
            if sub_round == 7:
                big_round += 1
                sub_round = 1
            else:
                sub_round += 1
        self.cur_round = '{}-{}'.format(big_round,sub_round)

    def _sushi(self):
        self.sushi = []
        tofill = 9
        while len(self.sushi) != 9:
            stars = np.bincount(np.random.choice(range(5),tofill,
                p=self.sushi_distribution['r'+str(self.cur_round[0])]))
            for star,n_champs in zip(stars,self.champ_cost_info.items()):
                if len(n_champs[1]) < star:
                     star = len(n_champs)
                cnts = [self.champ_state_info[champ]['count'] for champ in n_champs[1]]
                if sum(cnts) == 0:
                    continue
                prob = [c/sum(cnts) for c in cnts]
                print('sushi cnts',cnts)
                champs = list(np.random.choice(len(n_champs[1]),star,replace=False,p=prob))
                self.sushi += [n_champs[1][c] for c in champs ]
                tofill -= star
        orders = np.arange(8)
        np.random.shuffle(orders)
        item = list(np.random.choice(self.items,8,replace=False))
        for i,(order,player) in enumerate(zip(orders,self.players)):
            self.champ_state_info[self.sushi[order]]['count'] -= 1
            print('sushi!',self.champ_state_info[self.sushi[order]]['count'])
            player.champ_append(self.sushi[order]+'_1',[item[i]])
            print('sushi finished {} champ is {}'.format(player.name,self.sushi[order]))
    def _prepare(self):
        total_champ_queues = []
        for player in self.players:
            player.champ_state_info = self.champ_state_info
            print(player.name)
            player.cur_round = self.cur_round
            champ_queues,action_sequence,arrange,num = player.prepare_round()
            self.jd['action'].append(dict(buysell=np.array(action_sequence).tolist(),
                arrange=np.array(arrange).tolist(),chosen=np.array(num).tolist()))
            print(player.wait_num)
            self.jd['state'].append(dict(xp=player.xp,money=int(player.money),
                wait=player.wait_num,fight=player.fight_num,synergy=player.fight_synergy,
                life=player.life,continuous=player.continuous))
            for champ,count in champ_queues:
                if champ == None:
                    continue
                self.champ_state_info[champ]['count'] += count
    def _match(self):
        match_queue = np.arange(len(self.players))
        np.random.shuffle(match_queue)
        match_queue = list(match_queue)
        is_ai = False
        if len(match_queue) % 2 == 1:
            ai = np.random.choice(match_queue[:-1],1)[0]
            match_queue.append(ai)
            is_ai = False
        match_queue = np.reshape(np.array(match_queue),(-1,2))
        return match_queue,is_ai
    def _continuous(self,agent,win):
        if win:
            if agent.continuous >= 0:
                agent.continuous += 1
            else:
                agent.continuous = 1
        else:
            if agent.continuous <= 0:
                agent.continuous -= 1
            else:
                agent.continuous = -1
    def _game_over(self):
        for player in self.players:
            if player.life <= 0:
                self.players.remove(player)
                self.final_place[player.name] = self.place
                self.place -= 1
                units = player.total_units
                for unit,info in units.items():
                    self.champ_state_info[unit[:-2]]['count'] += \
                        info['count']*(int(unit[-1])-1)
    def play_round(self,gui=True):
        result = 'sushi'
        print(self.cur_round)
        if self.cur_round == '1-1':
            1 == 1
        elif (self.cur_round[0] != '1') and (self.cur_round[-1] == '4'):
            self._sushi()
        else:
            self._prepare()
            match_order,is_ai = self._match()
            for i,m in enumerate(match_order):
                a1 = self.players[m[0]]
                a2 = self.players[m[1]]
                fight = Fight(a1,a2,self.cur_round)
                fight.my_queue = a1.five_champs
                fight.my_cost = a1.five_cost
                fight.my_money = a1.money
                fight.opp_money = a2.money
                fight.place_table = self.place_table
                if str(match_order[i]) == str(match_order[-1]):
                    fight.is_ai = is_ai
                result,life_change = fight.fight(gui=gui)
                if gui:
                    fight.gui.root.destroy()
                time.sleep(1)
                print('finish fight!')
                if result:
                    a2.life -= life_change
                    a1.money += 1
                    self._continuous(a1,True)
                    self._continuous(a2,False)
                    a1.result(result)
                    a2.result(False)
                    self.place_table[int(a2.name[-1])-1] = [a2.name,a2.life]
                elif result == 0:
                    a2.life -= life_change
                    a1.life -= life_change
                    self._continuous(a1,False)
                    self._continuous(a2,False)
                    self.place_table[int(a1.name[-1])-1] = [a1.name,a1.life]
                    self.place_table[int(a2.name[-1])-1] = [a2.name,a2.life]
                else:
                    a1.life -= life_change
                    a2.money += 1
                    self._continuous(a2,True)
                    self._continuous(a1,False)
                    a1.result(True)
                    a2.result(result)
                    self.place_table[int(a1.name[-1])-1] = [a1.name,a1.life]
        self._game_over()
        tem = [(k,i['count']) for k,i in self.champ_state_info.items()]
        #print(tem)
        names = [player.name for player in self.players]
        print('survived players : {}'.format(names))
        self._round()
