import numpy as np
import copy,os
from utils.draw import draw_chess,make_video,find_name
from fight.items import item_apply
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
        hexes = np.zeros((7,8,20))
        self.opparr = [(6-oa[0],7-oa[1]) for oa in myarr]
        self.hexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
            mynum,self.opparr,myitems,mysyn,myinfo,myskill)
    def _assign_hexes(self,hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
        oppnum,opparr,oppitems,oppsyn,oppinfo,oppskill):
        for mn,ma,mitem,minf,on,oa,oitem,oinf in \
            zip(mynum,myarr,myitems,myinfo,oppnum,opparr,oppitems,oppinfo):
            hexes[ma[0],ma[1],0] = 1
            hexes[oa[0],oa[1],0] = -1
            hexes[ma[0],ma[1],1] = mn
            hexes[oa[0],oa[1],1] = on
            hexes[ma[0],ma[1],2] = minf['health']
            hexes[oa[0],oa[1],2] = oinf['health']
            hexes[ma[0],ma[1],3] = minf['mana'][0]
            hexes[oa[0],oa[1],3] = oinf['mana'][0]
            hexes[ma[0],ma[1],4] = minf['mana'][1]
            hexes[oa[0],oa[1],4] = oinf['mana'][1]
            # index 5 is is_skill
            hexes[ma[0],ma[1],6] = minf['attack_range']
            hexes[oa[0],oa[1],6] = oinf['attack_range']
            hexes[ma[0],ma[1],7] = minf['attack_damage']
            hexes[oa[0],oa[1],7] = oinf['attack_damage']
            hexes[ma[0],ma[1],8] = minf['attack_speed']
            hexes[oa[0],oa[1],8] = oinf['attack_speed']
            hexes[ma[0],ma[1],9] = minf['armor']
            hexes[oa[0],oa[1],9] = oinf['armor']
            hexes[ma[0],ma[1],10] = minf['magical_resistance']
            hexes[oa[0],oa[1],10] = oinf['magical_resistance']
            # index 11 is skill
            # index 12 is sparring
            for c,(m,o) in enumerate(zip(mitem,oitem)):
                hexes[ma[0],ma[1],13+c] = m
                hexes[oa[0],oa[1],13+c] = o
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
        todo : 앞에 상대 있을 시, 못 가게 해야함
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
    def _one_champ_tic(self,hexes,attack_range,arr,you,opp,enemies,tic):
        tiles = np.tile(np.array(arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        if attack_range >= nearest_dist:
            damage = hexes[arr[0],arr[1],7] - hexes[enemies[ind][0],enemies[ind][1],9]
            if damage < 0:
                damage = 0
            hexes[enemies[ind][0],enemies[ind][1],2] -= damage/tic*hexes[arr[0],arr[1],8]
            self._mana(hexes,arr,hit=True)
            self._mana(hexes,enemies[ind],hit=False)
            if hexes[enemies[ind][0],enemies[ind][1],2] == 0:
                hexes[enemies[ind][0],enemies[ind][1],2] = -1.333
            arrind = hexes[arr[0],arr[1],1]
            eneind = hexes[enemies[ind][0],enemies[ind][1],1]
            attack_info = copy.copy([eneind,damage/tic*hexes[arr[0],arr[1],8],arr,arrind])
            return hexes,attack_info
        else:
            targ = enemies[ind]
            eneind = copy.copy(hexes[targ[0],targ[1],1])
            attack_info = [eneind,0]
            moved = self._move(hexes,arr,targ)
            if moved != arr:
                hexes[moved[0],moved[1],:] = hexes[arr[0],arr[1],:]
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
        tot_mana = hexes[arr[0],arr[1],4]
        is_skill = False
        if hit:
            cur_mana += 10
        else:
            cur_mana += 4
        if cur_mana >= tot_mana:
            hexes[arr[0],arr[1],5] = 1
            cur_mana -= tot_mana
        hexes[arr[0],arr[1],3] = cur_mana
        return hexes,is_skill
    def _skill(self,hexes):
        '''
        if skill use, use one tic
        - todo :
        단순 스킬 데미지 적용
        '''
        skill = np.where(hexes[:,:,5]>=1)
        skill_xy = [[x,y] for x,y in zip(skill[0],skill[1])]
        for ski in skill_xy:
            hexes[ski[0],ski[1],5] = 0
        return hexes
    def _fight_tic(self,hexes,n,draw=False):
        '''2 tic = 1 seconds'''
        tic = 2
        hexes = self._skill(hexes)
        attack_infos = []
        for oa,ma in zip(self.opparr,self.myarr):
            oa,ma = list(oa),list(ma)
            mark = hexes[:,:,0]
            oar = hexes[oa[0],oa[1],6]
            mar = hexes[ma[0],ma[1],6]
            oxs,oys=np.where(mark==1)
            oa_enemies = np.array([[x,y] for x,y in zip(oxs,oys)])
            hexes,attack_info = self._one_champ_tic(hexes,oar,oa,-1,1,oa_enemies,tic)
            mark = hexes[:,:,0]
            mxs,mys=np.where(mark==-1)
            ma_enemies = np.array([[x,y] for x,y in zip(mxs,mys)])
            attack_infos.append(attack_info)
            hexes,attack_info = self._one_champ_tic(hexes,mar,ma,1,-1,ma_enemies,tic)
            #    print(find_name(int(attack_info[0])),find_name(int(attack_info[3])))
            attack_infos.append(attack_info)
        self._read_hexes(hexes)
        skill = None
        if draw:
            self.visualize(hexes,n,attack_infos)
        return hexes
    def _die(self):
        health = self.hexes[:,:,2]
        dies = np.where(health<0)
        diesx,diesy = dies
        for x,y in zip(diesx,diesy):
            who = self.hexes[x,y,0]
            if who == -1:
                self.opparr.remove((x,y))
            elif who == 1:
                self.myarr.remove((x,y))
            self.hexes[x,y,:] = 0
    def _end(self):
        '''
        judge the round end & calcul the life change
        '''
        myopp = self.hexes[:,:,0]
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
    def fight(self,video=False):
        notend = True
        n = 0
        self.hexes = item_apply(self.hexes)
        while notend:
            self._fight_tic(self.hexes,n,draw=False)
            self._die()
            notend,win,life_change = self._end()
            n += 1
            if n > 2000:
                self.hexes[:,:,2] = 0
        if video:
            dir = './fig/{}'.format(self.cur_round)
            make_video(dir,dir+'/{}.avi'.format(self.cur_round))
        return win,life_change
    def visualize(self,hexes,n,attack_infos):
        if not os.path.exists('./fig/{}'.format('ROUND_'+self.cur_round)):
            os.mkdir('./fig/{}'.format('ROUND_'+self.cur_round))
        xs,ys = np.meshgrid(np.linspace(1,8,8),np.linspace(1,7,7))
        imgname = './fig/{}/frame_{}.jpg'.format('ROUND_'+self.cur_round,n)
        draw_chess(hexes,imgname,attack_infos)
