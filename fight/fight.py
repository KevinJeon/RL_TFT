import numpy as np
import config_3 as cfg
import cv2
class Fight:

    def __init__(self,myunits,mynum,myarr,myitems,mysyn,myinfo):
        myskill = None
        self.myunits = myunits
        self.mynum = mynum
        self.myarr = myarr
        self.myitems = myitems
        self.mysyn = mysyn
        self.myinfo = myinfo
        hexes = np.zeros((7,8,16))
        self.opparr = []
        self.hexes = self._assign_hexes(hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
            mynum,myarr,myitems,mysyn,myinfo,myskill)
    def _assign_hexes(self,hexes,mynum,myarr,myitems,mysyn,myinfo,myskill,
        oppnum,opparr,oppitems,oppsyn,oppinfo,oppskill):
        for mn,ma,mitem,minf,on,oa,oitem,oinf in \
            zip(mynum,myarr,myitems,myinfo,oppnum,opparr,oppitems,oppinfo):
            oa = (6-oa[0],7-oa[1])
            self.opparr.append(oa)
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
            hexes[ma[0],ma[1],6] = minf['dps']
            hexes[oa[0],oa[1],6] = oinf['dps']
            hexes[ma[0],ma[1],7] = minf['armor']
            hexes[oa[0],oa[1],7] = oinf['armor']
            hexes[ma[0],ma[1],8] = minf['magical_resistance']
            hexes[oa[0],oa[1],8] = oinf['magical_resistance']
            for c,(m,o) in enumerate(zip(mitem,oitem)):
                hexes[ma[0],ma[1],10+c] = m
                hexes[oa[0],oa[1],10+c] = o
        return hexes
    def _move(self,hexes,arr,targ):
        '''1 move에 적 방향으로 찾아가야함 '''
        1 == 1
    def _is_attack_and_move(self,hexes,attack_range,arr,you,opp,enemies):
        tiles = np.tile(np.array(arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        if attack_range < nearest_dist:
            hexes[enemies[ind][0],enemies[ind][0],2] -= \
                (hexes[arr[0],arr[1],6]-hexes[enemies[ind][0],enemies[ind][0],7])/2
            if hexes[enemies[ind][0],enemies[ind][0],2] == 0:
                hexes[enemies[ind][0],enemies[ind][0],2] = -1
            return hexes,True
        else:
            targ = enemies[ind]
            self._move(hexes,arr,targ)
            return hexes,False

    def _fight_tic(self,hexes,first=True):
        '''2 tic = 1 seconds'''
        mark = hexes[:,:,0]
        oxs,oys=np.where(mark==1)
        mxs,mys=np.where(mark==-1)
        oa_enemies = np.array([[x,y] for x,y in zip(oxs,oys)])
        ma_enemies = np.array([[x,y] for x,y in zip(mxs,mys)])
        for oa,ma in zip(self.opparr,self.myarr):
            oa,ma = list(oa),list(ma)
            oar = hexes[oa[0],oa[1],5]
            mar = hexes[ma[0],ma[1],5]
            hexes,is_attack = self._is_attack_and_move(hexes,oar,oa,-1,1,oa_enemies)
            hexes,is_attack = self._is_attack_and_move(hexes,mar,ma,1,-1,ma_enemies)
        print(hexes[:,:,0])
        skill = None
        hexes = np.zeros((7,8,16))
        hexes = self._assign_hexes(hexes,self.mynum,self.myarr,self.myitems,
            self.mysyn,self.myinfo,skill,self.mynum,self.myarr,self.myitems,
                self.mysyn,self.myinfo,skill)
        #print(hexes[:,:,0][::-1])
        return hexes
    def _die(self):
        health = self.hexes[:,:,2]
        print('die!')
        print(np.where(health<0))
    def _end(self):
        myopp = self.hexes[:,:,0]
        if len(myopp[myopp==1]) == 0:
            return False,False
        elif len(myopp[myopp==0]) == 0:
            return False,True
        else:
            return True,None
    def fight(self):
        notend = True
        while notend:
            self._fight_tic(self.hexes)
            self._die()
            notend,win = self._end()
            notend = False
        return win
