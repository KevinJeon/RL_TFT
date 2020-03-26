import config_3 as cfg
import numpy as np
# env
'''
to do
0. 변수, 함수 네이밍 재점검 - done
1. full round without fight,item,skill,level - done
    1-1. sell 구현 - done
2. level champs_levelup - done
    2-1. 챔피언 레벨 정보 - done
3. 시너지 단순 네이밍과 등급만 - done
    3-1. 시너지 묶기 함수화 - done
4. 시너지
    4-1. 시너지 설명 및 수치 추가 - done
    4-2. 시너지 함수 필요 - 나중에 구현 후 해야할 것
3. item 할당과 속성만, 융합은 x
    3-1. item 속성 완료
    3-2. item 함수
4. item 융합 포함
5. simple skill(단순 거리, 데미지)
6. skill 복잡 스킬 구현
7. fight
    7-1. 몹 라운드
--to fix--
1. 3성 만들면, 스시에도 빠지는 것 - removal에서 할당 후, 스시 distribution 돌릴 때 같이 빠지는 바얗응로
2. 아이템 개인 할당 방법
3. 초반 금액 상승폭 수정 필요 - done
4. 골드 지급은 라운드 시작 시 지급 - done
'''

class TFT_env(object):
    def __init__(self,elements,champ_state_info,champ_cost_info,champ_level_info,
        champ_distribution,sushi_distribution,synergy_info,agent=None,
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
        # player
        self.need_xp = [2,4,8,14,24,44,76,126,192]
        # units
        self.total_units = dict()
        self.removal = dict() # already level 3 unit
        self.fight_units = [] # fore rearrange
        self.wait_units = []
        # about sushi,reroll
        self.sushi_distribution = sushi_distribution
        self.champ_distribution = champ_distribution
        # agent
        self.agent = agent
        self._init_game()
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

    def _init_game(self):
        # init game
        self.money = 0 # 돈
        self.place = 8 # 등수 --> 최종 reward
        self.life = 100 # 체력
        self.xp = 0 # xp
        self.continuous = 0 # state reward
        self.player_level = 1
        self.five_champs = [True]*5
        self.five_cost = [0]*5
        self.player_synergy = []
        self._sushi()
        msg = ('-----------------------\n'+\
            'Hi, Welcome to League of Legends TFT\n'+\
            'Life : {}\n'+\
            'Player level : {}\n'+\
            'Money : {}\n'+\
            '# of Champ : {}\n'+\
            '-----------------------').format(self.life,self.player_level,
                self.money,len(self.total_units))
        print(msg)
    def _sushi(self):
        self.sushi = []
        stars = np.bincount(np.random.choice(range(5),9,
            p=self.sushi_distribution['r'+str(self.cur_round[0])]))
        for star,n_champs in zip(stars,self.champ_cost_info.items()):
            champs = list(np.random.choice(len(n_champs[1]),star,replace=False))
            self.sushi += [n_champs[1][c] for c in champs]
        my_order = np.random.choice(8,1)[0]
        item = np.random.choice(8,1)[0]
        self._champ_append(self.sushi[my_order]+'_1',item)
        print('sushi finished your champ is {}'.format(self.sushi[my_order]))
    def _champ_queue(self):
        self.five_champs,self.five_cost = [],[]
        stars = np.bincount(np.random.choice(5,size=5,
            p=self.champ_distribution['l'+str(self.player_level)]))
        for star,n_champs in zip(stars,self.champ_cost_info.items()):
            champs = np.random.choice(len(n_champs[1]),size=star)
            self.five_champs += [n_champs[1][c] for c in champs]
        self.five_cost += [self._cost(c+'_1') for c in self.five_champs]
        msg = 'champ queue make!\n{}'.format(self.five_champs)
    def _cost(self,champ):
        cost_info = np.array([1,3,5])
        level = int(champ[-1])
        champ = champ[:-2]
        for (star,champs) in self.champ_cost_info.items():
            if champ in champs:
                return cost_info[level]
            cost_info += 1
    def _money(self):
        '''
        money rule
        1. 1-4?
        2. interset : 10골드 당 1원 max 5
        3. continuous : 2~3  - +1 4~6 - +2 7~ - +3
        '''
        if self.cur_round in ['1-2','1-3','2-1','2-2']:
            self.money += 2
            if self.cur_round[0] == '2':
                self.money += 1
                if self.cur_round[-1] == '2':
                    self.money += 1
        else:
            self.money += 5
        if self.money > 50:
            self.money += 5
        else:
            self.money += self.money // 10
        if abs(self.continuous) >= 7:
            self.money += 3
        elif abs(self.continuous) >= 4:
            self.money += 2
        elif abs(self.continuous) >= 2:
            self.money += 1
    def _update_synergy(self):
        '''
        for total units, not fight units
        '''
        syn_list = []
        used = []
        self.player_synergy = []
        for k,i in self.total_units.items():
            if k[:-2] not in used:
                syn_list += i['synergy']
                used.append(k[:-2])
        syn = np.bincount(syn_list)
        for ((k,i),s) in zip(self.synergy_info.items(),syn):
            rate = 0
            while s > i['rate'][rate]:
                rate += 1
                if rate >= len(i['rate']):
                    break
            if rate >= 1:
                self.player_synergy.append(k+'_'+str(rate))
    def _fight(self):
        # 임시
        n = int(self.cur_round[0])
        return np.random.choice([True,False]),np.random.randint(2*n,8*n)
    def _champ_append(self,champ,item=None):
        if champ in self.total_units.keys():
            self.total_units[champ]['count'] += 1
            if item:
                self.total_units[champ]['items'].append(item)
            if self.total_units[champ]['count'] == 3:
                levup = int(champ[-1]) + 1
                levup_champ = champ[:-1] + str(levup)
                self._champ_append(levup_champ,item)
                del self.total_units[champ]
        else:
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
                    items=[item])
            else:
                self.total_units[champ] = dict(count=1,synergy=synergy,info=info,
                    items=[])
            if level == '3':
                for c in self.champ_cost_info.items():
                    if champ[:-2] in c[1]:
                        if c[0] in self.removal.keys():
                            self.removal[c[0]].append(c[1].index(champ[:-2]))
                        else:
                            self.removal[c[1]] = [c[1].index(champ[:-2])]
    def _player_levelup(self):
        if self.player_level == 9:
            pass
        else:
            while self.xp >= self.need_xp[self.player_level-1]:
                self.player_level += 1
            self.champ_prob = self.champ_distribution['l'+str(self.player_level)]
    def _before_fight(self,act1):
        if act1 <= 4:
            cost = self._cost(self.five_champs[act1]+'_1')
            self.money -= cost
            self._champ_append(self.five_champs[act1]+'_1',None)
            self.five_champs[act1] = False
            self.is_prepared = False
        elif act1 == 5:
            self.is_prepared = True
        elif act1 == 6:
            ind = np.random.choice(len(self.total_units.keys()))
            champ = list(self.total_units.keys())[ind]
            self.money += self._cost(champ)
            self.total_units[champ]['count'] -= 1
            if self.total_units[champ]['count'] == 0:
                if self.total_units[champ]['items']:
                    self.items += self.total_units[champ]['items']
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
    def _rearrange(self):
        # update later
        1 == 1
    def play_round(self,act):
        result = 'sushi'
        if self.cur_round == '1-1':
            pass
        elif (self.cur_round[0] != '1') and (self.cur_round[-1] == '4'):
            self._sushi()
            self._update_synergy()
        else:
            action1 = self.act1_spc.index(act)
            print(act)
            self._before_fight(action1)
            if not self.is_prepared:
                return self.money,self.life,self.xp,self.total_units
            else:
                self._money()
                self.xp += 2
                self._player_levelup()
                self._rearrange()
                self._update_synergy()
                result,life_change = self._fight()
                if result:
                    self.money += 1
                    if self.continuous >=  0:
                        self.continuous += 1
                    else:
                        self.continuous = 1
                else:
                    self.life -= life_change
                    if self.continuous <= 0:
                        self.continuous -= 1
                    else:
                        self.continuous = -1
        msg = ('-----------------------\n'+\
            'ROUND {} finish\n'+\
            'Win : {}\n'+\
            'Life : {}\n'+\
            'Player level : {}\n'+\
            'Money : {}\n'+\
            'Champs : {}\n'+\
            'Continuous : {}\n'+\
            'Synergy : {}\n'+\
            '-----------------------').format(self.cur_round,result,self.life,self.player_level,
                self.money,self.total_units.keys(),self.continuous,self.player_synergy)
        print(msg)
        self._champ_queue()
        self._round()
        return self.money,self.life,self.xp,self.total_units
