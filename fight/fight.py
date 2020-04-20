import numpy as np
import copy,os
from utils.draw import draw_chess,make_video,find_name
from buff.synergy import Synergy
class Fight:
    '''
    '''
    def __init__(self,myunits,mynum,myarr,myitems,mysyn,myinfo,cur_round):
        myskill = None
        self.cur_round = cur_round
        self.myunits = myunits
        self.mynum = mynum
        self.myarr = myarr
        self.myitems = myitems
        self.mysyn = mysyn
        self.myinfo = myinfo
        self.player_synergy = mysyn
        hexes = np.zeros((7,8,26))
        self.opparr = [(6-oa[0],7-oa[1]) for oa in myarr]
        self.start_hexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
            mynum,self.opparr,myitems,mysyn,myinfo,myskill)
        self.cur_hexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
            mynum,self.opparr,myitems,mysyn,myinfo,myskill)
        self.mysyns = dict()
        self.oppsyns = dict()
    def _assign_hexes(self,hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
        oppnum,opparr,oppitems,oppsyn,oppinfo,oppskill,max=True):
        '''
        '''
        if max:
            mana = 1
        else:
            mana = 0
        for mu,mn,ma,mitem,minf,ou,on,oa,oitem,oinf in \
            zip(self.myunits,mynum,myarr,myitems,myinfo,self.myunits,oppnum,
                opparr,oppitems,oppinfo):
            hexes[ma[0],ma[1],0] = 1
            hexes[oa[0],oa[1],0] = -1
            hexes[ma[0],ma[1],1] = mn
            hexes[oa[0],oa[1],1] = on
            hexes[ma[0],ma[1],2] = minf['health']
            hexes[oa[0],oa[1],2] = oinf['health']
            hexes[ma[0],ma[1],3] = minf['mana'][mana]
            hexes[oa[0],oa[1],3] = oinf['mana'][mana]
            hexes[ma[0],ma[1],4] = minf['attack_range']
            hexes[oa[0],oa[1],4] = oinf['attack_range']
            hexes[ma[0],ma[1],5] = minf['attack_damage']
            hexes[oa[0],oa[1],5] = oinf['attack_damage']
            hexes[ma[0],ma[1],6] = minf['attack_speed']
            hexes[oa[0],oa[1],6] = oinf['attack_speed']
            hexes[ma[0],ma[1],7] = minf['armor']
            hexes[oa[0],oa[1],7] = oinf['armor']
            hexes[ma[0],ma[1],8] = minf['magical_resistance']
            hexes[oa[0],oa[1],8] = oinf['magical_resistance']
            # index 9 is is_skill
            # index 10 is sklll damage - config
            # index 11 is health recovery by damage
            # index 12 is sparring prob
            hexes[oa[0],oa[1],13] = 0.2 # index 13 is critical probability
            hexes[ma[0],ma[1],14] = minf['synergy'][0]
            hexes[oa[0],oa[1],14] = oinf['synergy'][0]
            hexes[ma[0],ma[1],15] = minf['synergy'][1]
            hexes[oa[0],oa[1],15] = oinf['synergy'][1]
            if len(minf['synergy']) == 3:
                hexes[ma[0],ma[1],16] = minf['synergy'][2]
            else:
                hexes[ma[0],ma[1],16] = -1
            if len(oinf['synergy']) == 3:
                hexes[oa[0],oa[1],16] = oinf['synergy'][2]
            else:
                hexes[oa[0],oa[1],16] = -1
            hexes[ma[0],ma[1],17] = int(mu[-1])
            hexes[oa[0],oa[1],17] = int(ou[-1])
            # index 18 is level
            for c,(m,o) in enumerate(zip(mitem,oitem)):
                hexes[ma[0],ma[1],19+c] = m
                hexes[oa[0],oa[1],19+c] = o
            # synergy fields
        return hexes
    def _read_hexes(self,hexes):
        status = hexes[:,:,0]
        oppxy = np.where(status==-1)
        myxy = np.where(status==1)
        self.opparr = [(x,y) for x,y in zip(oppxy[0],oppxy[1])]
        self.myarr = [(x,y) for x,y in zip(myxy[0],myxy[1])]
    def _move(self,hexes,arr1,targ):
        '''
        1 tic에 1 move 가져감.
        todo : 지능적 움직임
        '''
        moved = copy.copy(arr1)
        diff = targ - arr1
        absdiff = abs(diff)
        ind = np.argmax(absdiff)
        if diff[ind] < 0:
            moved[ind] -= 1
            if hexes[moved[0],moved[1],0] != 0:

                moved[ind] += 1
        elif diff[ind] == 0:
            print('error!',targ,arr1)
        else:
            moved[ind] += 1
            if hexes[moved[0],moved[1],0] != 0:
                moved[ind] -= 1
        return moved
    def _one_champ_tic(self,hexes,attack_range,arr,you,opp,enemies,tic,
        void=False,sniper=False,pirate=False,starguard=False,protector=False):
        tiles = np.tile(np.array(arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        if hexes[arr[0],arr[1],9] == 1:
            Skill(hexes,arr).cast()
            if starguard:
                if you == 1:
                    self.mysyns['star_skilled'] += 1
                elif you == -1:
                    self.oppsyns['star_skilled'] += 1
            if protector:
                if you == 1:
                    self.mysyns['protector_skillcast'].append([arr[0],arr[1]])
                elif you == -1:
                    self.oppsyns['protector_skillcast'].append([arm[0],arr[1]])
        elif attack_range >= nearest_dist:
            damage = hexes[arr[0],arr[1],5] - hexes[enemies[ind][0],enemies[ind][1],7]
            if void:
                damage = hexes[arr[0],arr[1],5]
            if sniper:
                diff = abs(tiles[ind]-enemies[ind])
                damage += hexes[arr[0],arr[1],5]*(sum(diff)-1)
            if damage < 0:
                damage = 0
            hexes[enemies[ind][0],enemies[ind][1],2] -= damage/tic*hexes[arr[0],arr[1],6]
            self._mana(hexes,arr,hit=True)
            self._mana(hexes,enemies[ind],hit=False)
            if hexes[enemies[ind][0],enemies[ind][1],2] == 0:
                hexes[enemies[ind][0],enemies[ind][1],2] = -1.333
            if hexes[enemies[ind][0],enemies[ind][1],2] < 0:
                if pirate:
                    if you == 1:
                        self.mysyns['pirate_kill'] += 1
                    elif you == -1:
                        self.oppsyns['pirate_kill'] += 1
            arrind = hexes[arr[0],arr[1],1]
            eneind = hexes[enemies[ind][0],enemies[ind][1],1]
            attack_info = copy.copy([eneind,damage/tic*hexes[arr[0],arr[1],6],arr,arrind])
            return hexes,attack_info
        else:
            targ = enemies[ind]
            eneind = copy.copy(hexes[targ[0],targ[1],1])
            attack_info = [eneind,0]
            moved = self._move(hexes,arr,targ)
            if moved != arr:
                hexes[moved[0],moved[1],:] = hexes[arr[0],arr[1],:]
                self.start_hexes[moved[0],moved[1],:] = self.start_hexes[arr[0],arr[1],:]
                hexes[arr[0],arr[1],:]  = 0
            arrind = hexes[moved[0],moved[1],1]
            attack_info += [moved,arrind]
            attack_info = copy.copy(attack_info)
            return hexes,attack_info
    def _mana(self,hexes,arr,hit=True):
        '''
        hit : 10 mana
        damaged by opp : 4
        if skill, next tic skill activate
        '''
        cur_mana = hexes[arr[0],arr[1],3]
        tot_mana = self.start_hexes[arr[0],arr[1],3]
        is_skill = False
        if hit:
            cur_mana += 10
        else:
            cur_mana += 4
        if cur_mana >= tot_mana:
            hexes[arr[0],arr[1],9] = 1
            cur_mana = 0
        hexes[arr[0],arr[1],3] = cur_mana
        return hexes,is_skill
    def _is_who(self,hexes,arr,synergy):
        if (hexes[arr[0],arr[1],14]==synergy) or (hexes[arr[0],arr[1],15]==synergy):
            is_who = True
        else:
            is_who = False
        return is_who
    def _syn_tic(self,hexes,syns,arr):
        torf = [False]*5
        if syns.is_sniper:
            torf[0] = self._is_who(hexes,arr,19)
        elif syns.is_pirate:
            torf[1] = self._is_who(hexes,arr,6)
        elif syns.is_void:
            torf[2] = self._is_who(hexes,arr,9)
        elif syns.is_starguard:
            torf[3] = self._is_who(hexes,arr,)
        elif syns.is_protector:
            torf[4] = self._is_who(hexes,arr,)
        return torf
    def _fight_tic(self,hexes,n,draw=False,*kwargs):
        '''2 tic = 1 seconds'''
        tic = 2
        attack_infos = []
        self.mysyns['pirate_kill'] = 0
        self.mysyns['star_skilled'] = 0
        self.mysyns['valkyrie_target'] = []
        self.mysyns['protector_skillcast'] = []
        self.oppsyns['pirate_kill'] = 0
        self.oppsyns['star_skilled'] = 0
        self.oppsyns['valkyrie_target'] = []
        self.oppsyns['protector_skillcast'] = []
        for oa,ma in zip(self.opparr,self.myarr):
            oa,ma = list(oa),list(ma)
            mark = hexes[:,:,0]
            mar = hexes[ma[0],ma[1],4]
            oar = hexes[oa[0],oa[1],4]
            oxs,oys = np.where(mark==1)
            oa_enemies = np.array([[x,y] for x,y in zip(oxs,oys)])
            osni,opir,ovoi = self._syn_tic(hexes,self.oppsyn_infos,oa)
            msni,mpir,mvoi = self._syn_tic(hexes,self.mysyn_infos,ma)
            hexes,attack_info = self._one_champ_tic(hexes,oar,oa,-1,1,oa_enemies,
                tic,sniper=osni,pirate=opir,void=ovoi)
            mark = hexes[:,:,0]
            mxs,mys=np.where(mark==-1)
            ma_enemies = np.array([[x,y] for x,y in zip(mxs,mys)])
            attack_infos.append(attack_info)
            hexes,attack_info = self._one_champ_tic(hexes,mar,ma,1,-1,ma_enemies,
                tic,sniper=msni,pirate=mpir,void=mvoi)
            attack_infos.append(attack_info)
        self._read_hexes(hexes)
        skill = None
        if draw:
            self.visualize(hexes,n,attack_infos)
        return hexes
    def _die(self):
        health = self.cur_hexes[:,:,2]
        dies = np.where(health<0)
        diesx,diesy = dies
        self.mysyns['ds_died'] = 0
        self.oppsyns['ds_died'] = 0
        self.oppsyns['mech_died'] = [False,False]
        self.mysyns['mech_died'] = [False,False]
        for x,y in zip(diesx,diesy):
            who = self.cur_hexes[x,y,0]
            if who == -1:
                if (self.cur_hexes[x,y,14] == 3) or (self.cur_hexes[x,y,15] == 3):
                    self.oppsyns['ds_died'] += 1
                if self.cur_hexes[x,y,1] == 100:
                    self.oppsyns['mech_died'] = [True,[x,y]]
                self.opparr.remove((x,y))
            elif who == 1:
                if (self.cur_hexes[x,y,14] == 3) or (self.cur_hexes[x,y,15] == 3):
                    self.mysyns['ds_died'] += 1
                if self.cur_hexes[x,y,1] == 100:
                    self.mysyns['mech_died'] = [True,[x,y]]
                self.myarr.remove((x,y))
            self.cur_hexes[x,y,:] = 0
    def _end(self):
        '''
        judge the round end & calcul the life change
        '''
        myopp = self.cur_hexes[:,:,0]
        round_damage = [0,3,4,5,10,15,20]
        if self.myarr == []:
            count = len(self.opparr)
            round = round_damage[int(self.cur_round[0])]
            return False,False,count+round
        elif self.opparr == []:
            count = len(self.myarr)
            round = round_damage[int(self.cur_round[0])]
            return False,True,count+round
        else:
            return True,None,0
    def _synergy(self,infos,syns,n):
        infos.tic = n
        infos.ds_died = syns['ds_died']
        infos.mech_died = syns['mech_died']
        infos.pirate_kill = syns['pirate_kill']
        infos.star_skilled = syns['star_skilled']
        infos.valkyrie_target = syns['valkyrie_target']
        infos.protector_skillcast = syns['protector_skillcast']
        infos.tic = n
        infos.hexes = self.cur_hexes
        infos.apply()
        self.cur_hexes = infos.hexes
    def fight(self,video=False):
        notend = True
        n = 0
        self.mysyn_infos = Synergy(self.cur_hexes,self.start_hexes,self.mysyn,n,self.myarr,
            self.opparr)
        self.mysyn_infos.apply()
        self.cur_hexes = self.mysyn_infos.hexes
        self.oppsyn_infos = Synergy(self.cur_hexes,self.start_hexes,self.mysyn,n,self.opparr,
            self.myarr)
        self.oppsyn_infos.apply()
        self.cur_hexes = self.oppsyn_infos.hexes
        self.start_hexes = copy.copy(self.oppsyn_infos.hexes)
        self.money = 0
        self.item = []
        while notend:
            if n != 0:
                self._synergy(self.mysyn_infos,self.mysyns,n)
                self._synergy(self.oppsyn_infos,self.oppsyns,n)
            self._fight_tic(self.cur_hexes,n,draw=True)
            self._die()
            notend,win,life_change = self._end()
            n += 1
            if n > 2000:
                self.cur_hexes[:,:,2] = 0
        print('my pirate money {}'.format(self.mysyn_infos.pirate_money))
        print('my pirate money {}'.format(self.mysyn_infos.pirate_item))
        print('enemy pirate money {}'.format(self.oppsyn_infos.pirate_money))
        print('enemy pirate money {}'.format(self.oppsyn_infos.pirate_item))
        if video:
            dir = './fig/{}'.format(self.cur_round)
            make_video(dir,dir+'/{}.avi'.format(self.cur_round))
        return win,life_change
    def visualize(self,hexes,n,attack_infos):
        if not os.path.exists('./fig/{}'.format('ROUND_'+self.cur_round)):
            os.mkdir('./fig/{}'.format('ROUND_'+self.cur_round))
        xs,ys = np.meshgrid(np.linspace(1,8,8),np.linspace(1,7,7))
        fn = (4 - len(str(n)))*'0' + str(n)
        imgname = './fig/{}/frame_{}.jpg'.format('ROUND_'+self.cur_round,fn)
        draw_chess(hexes,self.start_hexes,imgname,attack_infos)
