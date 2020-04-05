import numpy as np
import config_3 as cfg
import cv2
import copy
class Fight:
    '''
    죽거나 이동 시, 삭제 함수 별도 필요
    '''
    def __init__(self,myunits,mynum,myarr,myitems,mysyn,myinfo):
        myskill = None
        self.myunits = myunits
        self.mynum = mynum
        self.myarr = myarr
        self.myitems = myitems
        self.mysyn = mysyn
        self.myinfo = myinfo
        hexes = np.zeros((7,8,17))
        self.opparr = [(6-oa[0],7-oa[1]) for oa in myarr]
        self.hexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
            mynum,self.opparr,myitems,mysyn,myinfo,myskill)
    def _assign_hexes(self,hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
        oppnum,opparr,oppitems,oppsyn,oppinfo,oppskill):
        for mn,ma,mitem,minf,on,oa,oitem,oinf in \
            zip(mynum,myarr,myitems,myinfo,oppnum,opparr,oppitems,oppinfo):
            #oa = (6-oa[0],7-oa[1])
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
            hexes[ma[0],ma[1],5] = minf['attack_range']
            hexes[oa[0],oa[1],5] = oinf['attack_range']
            hexes[ma[0],ma[1],6] = minf['attack_damage']
            hexes[oa[0],oa[1],6] = oinf['attack_damage']
            hexes[ma[0],ma[1],7] = minf['attack_speed']
            hexes[oa[0],oa[1],7] = oinf['attack_speed']
            hexes[ma[0],ma[1],8] = minf['armor']
            hexes[oa[0],oa[1],8] = oinf['armor']
            hexes[ma[0],ma[1],9] = minf['magical_resistance']
            hexes[oa[0],oa[1],9] = oinf['magical_resistance']
            # index 10 is skill
            for c,(m,o) in enumerate(zip(mitem,oitem)):
                hexes[ma[0],ma[1],11+c] = m
                hexes[oa[0],oa[1],11+c] = o
        return hexes
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
    def _is_attack_and_move(self,hexes,attack_range,arr,you,opp,enemies,tic):
        tiles = np.tile(np.array(arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        if attack_range < nearest_dist:
            damage = hexes[arr[0],arr[1],6] - hexes[enemies[ind][0],enemies[ind][1],8]
            hexes[enemies[ind][0],enemies[ind][1],2] -= damage/tic*hexes[arr[0],arr[1],7]
            #print('hit {}'.format(damage/2*hexes[arr[0],arr[1],7]))
            if hexes[enemies[ind][0],enemies[ind][1],2] == 0:
                hexes[enemies[ind][0],enemies[ind][1],2] = -1.333
            return hexes,True
        else:
            print('bef',arr)
            targ = enemies[ind]
            moved = self._move(hexes,arr,targ)
            if you == -1:
                self.opparr.remove(tuple(arr))
                self.opparr.append(tuple(moved))
            elif you == 1:
                self.myarr.remove(tuple(arr))
                self.myarr.append(tuple(moved))
            hexes[moved[0],moved[1],:] = hexes[arr[0],arr[1],:]
            hexes[arr[0],arr[1],:]  = 0

            return hexes,False

    def _fight_tic(self,hexes,first=True):
        '''2 tic = 1 seconds'''
        tic = 2
        mark = hexes[:,:,0]
        oxs,oys=np.where(mark==1)
        mxs,mys=np.where(mark==-1)
        oa_enemies = np.array([[x,y] for x,y in zip(oxs,oys)])
        ma_enemies = np.array([[x,y] for x,y in zip(mxs,mys)])
        for oa,ma in zip(self.opparr,self.myarr):
            oa,ma = list(oa),list(ma)
            oar = hexes[oa[0],oa[1],5]
            mar = hexes[ma[0],ma[1],5]
            hexes,is_attack = self._is_attack_and_move(hexes,oar,oa,-1,1,oa_enemies,tic)
            hexes,is_attack = self._is_attack_and_move(hexes,mar,ma,1,-1,ma_enemies,tic)
        #print(hexes[:,:,0])
        #print(hexes[:,:,2])
        print(self.opparr,self.myarr)
        skill = None
        hexes = np.zeros((7,8,17))
        hexes = self._assign_hexes(hexes,self.mynum,self.myarr,self.myitems,
            self.mysyn,self.myinfo,skill,self.mynum,self.myarr,self.myitems,
                self.mysyn,self.myinfo,skill)
        #print(hexes[:,:,0][::-1])
        return hexes
    def _die(self):
        health = self.hexes[:,:,2]
        dies = np.where(health<0)
        diesx,diesy = dies
        for x,y in zip(diesx,diesy):
            who = self.hexes[x,y,0]
            print('who dead',who,x,y)
            if who == -1:
                print('bam')
                self.opparr.remove((x,y))
            elif who == 1:
                print('bam')
                self.myarr.remove((x,y))
            self.hexes[x,y,:] = 0

        #print('die!')
        #print(np.where(health<0))
    def _end(self):
        myopp = self.hexes[:,:,0]
        print('myopp : ',myopp)
        print(self.myarr,self.opparr)
        if self.myarr == []:
            return False,False,2
        elif self.opparr == []:
            return False,True,2
        else:
            return True,None,2
    def fight(self):
        notend = True
        while notend:
            self._fight_tic(self.hexes)
            self._die()
            notend,win,life_change = self._end()
            #notend = False
        return win,life_change
