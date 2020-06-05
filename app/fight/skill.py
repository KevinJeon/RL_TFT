import numpy as np
import copy
class Skill:
    def __init__(self,hexes,maxhexes,arr=None,tic=0):
        '''마나 0인 챔프들 여기서 때려야함'''
        self.hexes = hexes
        self.maxhexes = maxhexes
        self.arr = arr
        self.tic = tic
        self.skills = [None,self._zoe,self._ziggs,self._xayah,self._twistedfate,self._poppy,
            self._malphite,self._leona,self._khazix,self._jarvan_iv,self._graves,
            self._fiora,self._caitlyn,self._yasuo,self._xin_zhao,self._sona,self._shen,
            self._rakan,self._mordekaiser,self._lucian,self._kaisa,self._darius,
            self._blitzcrank,self._annie,self._ahri,self._vi,self._syndra,self._shaco,
            self._rumble,self._neeko,self._master_yi,self._lux,self._kassadin,
            self._karma,self._jayce,self._ezreal,self._ashe,self._wukong,self._velkoz,
            self._soraka,self._kayle,self._jinx,self._jhin,self._irelia,self._fizz,
            self._chogath,self._thresh,self._miss_fortune,self._lulu,self._gangplank,
            self._ekko,self._aurelion_sol,self._mech_garren]
        self.myskill = []
        self.oppskill = []
        ##champs
        #duration
        self.xayah = False
        self.shen = False
        self.annie = False
        self.gangplank = False
        #effect
        self.demol = False
        self.master_yi = False
        self.kayle = True
        self.jinx = False
        self.jinx_speed = True
        self.irel_kill = False
        self.ekko = False
        self.fly = 0
        self.syndra = 0
    def _find_target(self,enemies,min=True):
        tiles = np.tile(np.array(self.arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        if min:
            ind = np.argmin(dist)
        if max:
            ind = np.argmax(dist)
        tx,ty = enemies[ind]
        return int(tx),int(ty)
    def _boundary(self,x,y,d1,d2):
        x1 = x+d1
        x2 = x+d2
        y1 = y+d1
        y2 = y+d2
        if (x+d1<0):
            x1 = 0
        elif (x+d2>6):
            x2 = 6
        if (y+d1<0):
            y1 = 0
        elif (y+d2>7):
            y2 = 7
        return int(x1),int(x2),int(y1),int(y2)
    def cast(self,enemy):
        ind = self.hexes[self.arr[0],self.arr[1],1]
        level = self.hexes[self.arr[0],self.arr[1],17]
        xy = np.where(self.hexes[:,:,0]==enemy)
        enemies = [[x,y] for x,y in zip(xy[0],xy[1])]
        self.myopp = self.hexes[self.arr[0],self.arr[1],0]
        if ind == 100:
            torf = self.skills[-1](int(level-1),enemies)
        else:
            torf = self.skills[int(ind)](int(level),enemies)
        self.hexes[self.arr[0],self.arr[1],9] = 0
        return self.hexes,torf
    def stop(self):
        #print(self.hexes[:,:,26])
        #print(self.hexes[:,:,0])
        #print(self.hexes[:,:,-1])
        ind = self.hexes[self.arr[0],self.arr[1],1]
        level = self.hexes[self.arr[0],self.arr[1],17]
        self.myopp = self.hexes[self.arr[0],self.arr[1],0]
        self.skills[int(ind)](int(level),None,stop=True)
        return self.hexes
    def _zoe(self,level,enemies,damage=[200,275,400],stun=[4,5,8],stop=False):
        target = np.argmax(self.hexes[:,:,2])
        tx,ty = int(target//8),int(target%8)
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[tx,ty,18] = stun[level]
    def _ziggs(self,level,enemies,damage=[250,325,550],stop=False):

        tx,ty = self._find_target(enemies)
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            if self.demol:
                self.hexes[tx,ty,18] += 2
    def _xayah(self,level,enemies,speed=[1,1.25,1.5],duration=[8,8,8],stop=False):
        if stop:
            self.hexes[self.arr[0],self.arr[1],6] -= speed[level]
        else:
            self.hexes[self.arr[0],self.arr[1],6] += speed[level]
            self.hexes[self.arr[0],self.arr[1],26] = duration[level]+1
    def _twistedfate(self,level,enemies,damage=[200,300,500],stop=False):
        '''continuous is later tic for 6 tic'''
    def _poppy(self,level,enemies,damage=[100,175,250],shield=[200,350,500],stop=False):
        tx,ty = self._find_target(enemies)
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[self.arr[0],self.arr[1],25] += shield[level]/2
    def _malphite(self,level,enemies,shield=[0.4,0.45,0.5],stop=False):
        '''0mana'''
        if self.tic == 0:
            self.hexes[self.arr[0],self.arr[1],2] += \
                self.hexes[self.arr[0],self.arr[1],2]*shield[level]
        else:
            return True
    def _leona(self,level,enemies,shield=[40,80,120],stop=False):
        if stop:
            self.hexes[self.arr[0],self.arr[1],7] -= shield[level]/2
            self.hexes[self.arr[0],self.arr[1],8] -= shield[level]/2
        else:
            self.hexes[self.arr[0],self.arr[1],7] += shield[level]/2
            self.hexes[self.arr[0],self.arr[1],8] += shield[level]/2
            self.hexes[self.arr[0],self.arr[1],26] = 10

    def _khazix(self,level,enemies,damage=[175,250,400],bonus=[600,800,1350],stop=False):
        tx,ty = self._find_target(enemies)
        tiles = np.tile(np.array([tx,ty]),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            nearest_dist = np.min(dist)
            if nearest_dist > 1:
                self.hexes[tx,ty,2] -= (bonus[level]-self.hexes[tx,ty,8])/2
    def _jarvan_iv(self,level,enemies,speed=[0.5,0.75,1],stop=False):
        if stop:

            for buffed in self.jarvan:
                x,y = np.where(self.hexes[:,:,-1]==int(buffed))
                if len(x) == 0:
                    continue
                self.hexes[int(x[0]),int(y[0]),6] -= speed[level]
        else:
            self.jarvan = []
            us = self.hexes[self.arr[0],self.arr[1],0]
            x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-1,2)
            xy = np.where(self.hexes[x1:x2,y1:y2,0]==us)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                self.hexes[x1+tx,y1+ty,6] += speed[level]
                self.jarvan.append(self.hexes[x1+tx,y1+ty,-1])
            self.hexes[self.arr[0],self.arr[1],26] = 8
    def _graves(self,level,enemies,damage=[150,200,400],stun=[6,8,10],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        speed = [self.hexes[x,y,6] for x,y in enemies]
        ind = np.argmax(speed)
        x1,y1,x2,y2 = self._boundary(enemies[ind][0],enemies[ind][1],-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[x1+tx,y1+ty,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
    def _fiora(self,level,enemies,damage=[200,300,450],stun=[3,3,6],stop=False):
        if stop:
            if (damage[level] - self.hexes[self.fiora[0],self.fiora[1],8])/2 < 0:
                1 == 1
            else:
                self.hexes[self.fiora[0],self.fiora[1],2] -= \
                    (damage[level] - self.hexes[self.fiora[0],self.fiora[1],8])/2
            self.hexes[self.fiora[0],self.fiora[1],18] = stun[level]
            self.hexes[self.arr[0],self.arr[1],7] -= 10000
            self.hexes[self.arr[0],self.arr[1],8] -= 10000
        else:
            self.hexes[self.arr[0],self.arr[1],26] = 4
            self.hexes[self.arr[0],self.arr[1],7] += 10000
            self.hexes[self.arr[0],self.arr[1],8] += 10000
            self.fiora = self._find_target(enemies)
    def _caitlyn(self,level,enemies,damage=[750,1500,3000],stop=False):
        if stop:
            if (damage[level] - self.hexes[self.caitlyn[0],self.caitlyn[1],8])/2 < 0 :
                1 == 1
            else:
                self.hexes[self.caitlyn[0],self.caitlyn[1],2] -= (damage[level] -\
                    self.hexes[self.caitlyn[0],self.caitlyn[1],8])/2
        else:
            tiles = np.tile(np.array(self.arr),(len(enemies),1))
            dist = np.max(abs(tiles-enemies),axis=1)
            nearest_dist = np.min(dist)
            ind = np.argmax(dist)
            self.caitlyn = enemies[ind]
            self.hexes[self.arr[0],self.arr[1],26] = 9
    def _yasuo(self,level,enemies,hit=[8,10,12],stop=False):
        tx,ty = self._find_target(enemies)
        self.hexes[tx,ty,2] -= (hit[level]*self.hexes[self.arr[0],self.arr[1],6]*\
            self.hexes[self.arr[0],self.arr[1],5] - self.hexes[tx,ty,7])/2
        '''move 구현해야함'''
    def _xin_zhao(self,level,enemies,damage=[200,275,375],stop=False):
        if stop:
            tx,ty = self._find_target(self.xin_zhao)
            if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2# stop한다고 공격을 쉬지는 않기에 공격은 안넣음
            self.hexes[tx,ty,18] = 3
        else:
            self.xin_zhao = enemies
            self.hexes[self.arr[0],self.arr[1],26] = 3
    def _sona(self,level,enemies,healed=[2,3,4],heal=[100,150,200],stop=False):
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        if len(us) < healed[level]:
            toheal = len(us)
        else:
            toheal = healed[level]
        inds = np.random.choice(len(us),toheal,replace=False)
        selected = [us[i] for i in inds]
        for sel in selected:
            self.hexes[sel[0],sel[1],2] += heal[level]
            self.hexes[sel[0],sel[1],18] = 0
            if self.hexes[sel[0],sel[1],2] > self.maxhexes[sel[0],sel[1],2]:
                self.hexes[sel[0],sel[1],2] = self.maxhexes[sel[0],sel[1],2]
    def _shen(self,level,enemies,resist=[15,30,45],duration=[5,6,10],stop=False):
        if stop:
            self.shen_duration -= 1
            if self.shen_duration == 0:
                for buffed in self.shen:
                    x,y = np.where(self.hexes[:,:,-1]==buffed)
                    self.hexes[x,y,7] -= 10000
                    self.hexes[x,y,8] -= resist[level]
                self.shen = []
                x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-1,2)
                self.hexes[self.arr[0],self.arr[1],26] = 2
                xy = np.where(self.hexes[x1:x2,y1:y2,0]==self.myopp)
                targets = [[x,y] for x,y in zip(xy[0],xy[1])]
                for tx,ty in targets:
                    self.hexes[tx+x1,ty+y1,7] += 10000
                    self.hexes[tx+x1,ty+y1,8] += resist[level]
                    self.shen.append(self.hexes[tx+x1,ty+y1,-1])
                self.hexes[self.arr[0],self.arr[1],26] = 2
            else:
                for buffed in self.shen:
                    x,y = np.where(self.hexes[:,:,-1]==buffed)
                    self.hexes[x,y,7] -= 10000
                    self.hexes[x,y,8] -= resist[level]
                self.shen = []
        else:
            self.shen = []
            self.shen_duration = duration[level]
            x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-1,2)
            self.hexes[self.arr[0],self.arr[1],26] = 2
            xy = np.where(self.hexes[x1:x2,y1:y2,0]==self.myopp)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                self.hexes[tx+x1,ty+y1,7] += 10000
                self.hexes[tx+x1,ty+y1,8] += resist[level]
                self.shen.append(self.hexes[tx+x1,ty+y1,-1])
    def _rakan(self,level,enemies,damage=[175,250,400],stun=[3,3,3],stop=False):
        att_range = self.hexes[self.arr[0],self.arr[1],4]
        x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-att_range,att_range+1)
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x+x1,y+y1] for x,y in zip(xy[0],xy[1])]
        if targets == []:
            pass
        else:
            tx,ty = self._find_target(targets)
            x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
            xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                    1 == 1
                else:
                    self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
                self.hexes[tx+x1,ty+y1,18] = stun[level]
    def _mordekaiser(self,level,enemies,shield=[350,500,800],damage=[50,75,125],stop=False):
        if stop:
            if self.hexes[self.arr[0],self.arr[1],25] < 0:
                1 == 1
            else:
                enemy = self.hexes[self.moredekaiser[0][0],self.moredekaiser[0][1],0]
                self.hexes[self.arr[0],self.arr[1],26] = 2
                x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-1,2)
                xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
                targets = [[x,y] for x,y in zip(xy[0],xy[1])]
                for tx,ty in targets:
                    if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                        1 == 1
                    else:
                        self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
        else:
            enemy = self.hexes[enemies[0][0],enemies[0][1],0]
            self.hexes[self.arr[0],self.arr[1],25] += shield[level]/2
            self.hexes[self.arr[0],self.arr[1],26] = 2
            x1,y1,x2,y2 = self._boundary(self.arr[0],self.arr[1],-1,2)
            xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                    1 == 1
                else:
                    self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.moredekaiser = enemies
    def _lucian(self,level,enemies,damage=[150,200,325],stop=False):
        tx,ty = self._find_target(enemies)
        atk = self.hexes[self.arr[0],self.arr[1],5]*self.hexes[self.arr[0],self.arr[1],6]
        if (atk - self.hexes[tx,ty,7])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (atk - self.hexes[tx,ty,7])/2
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        '''move 구현해야함'''
    def _kaisa(self,level,enemies,hit=[4,6,9],stop=False):
        tiles = np.tile(np.array(self.arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        inds = list(np.where(dist<=2)[0])
        if len(inds) == 0:
            targets = []
        else:
            targets = [enemies[int(i)] for i in inds]
        for t in targets:
            if (50*hit[level] - self.hexes[t[0],t[1],8])/2 < 0 :
                1 == 1
            else:
                self.hexes[t[0],t[1],2] -= (50*hit[level] - self.hexes[t[0],t[1],8])/2
    def _darius(self,level,enemies,damage=[400,500,750],stop=False):
        while True:
            tx,ty = self._find_target(enemies)
            if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
                1 == 1
            else:
                if 0.5 * self.maxhexes[tx,ty,2] > self.hexes[tx,ty,2]:
                    self.hexes[tx,ty,2] -= (damage[level]-self.hexes[tx,ty,8])/2
                self.hexes[tx,ty,2] -= (damage[level]-self.hexes[tx,ty,8])/2
            if self.hexes[tx,ty,2] > 0:
                break
            enemies.remove([tx,ty])
            if len(enemies) == 0:
                break
        '''move 구현해야함'''
    def _blitzcrank(self,level,enemies,damage=[250,400,900],stop=False):
        tx,ty = self._find_target(enemies,min=False)
        if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[tx,ty,18] = 2
        '''move 구현해야함'''
    def _annie(self,level,enemies,damage=[150,200,300],shield=[270,360,540],stop=False):
        if stop:
            self.hexes[self.arr[0],self.arr[1],25] = 0
        else:
            self.hexes[self.arr[0],self.arr[1],25] += shield[level]/2
            self.hexes[self.arr[0],self.arr[1],26] = 9
        '''damage 나중에 원뿔?'''
    def _ahri(self,level,enemies,damage=[175,250,375],stop=False):
        '''damage 나중에 각도?'''
    def _vi(self,level,enemies,damage=[400,600,1200],knock=[150,200,500],
            stun=[4,5,6],stop=False):
        tx,ty = self._find_target(enemies,min=False)
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
        '''경로에 knock damage 해야함 '''
    def _syndra(self,level,enemies,damage=[80,120,200],stop=False):
        self.syndra += 3
        target = np.argmax(self.hexes[:,:,2])
        tx,ty = target//8,target%8
        if (damage[level]*self.syndra - self.hexes[tx,ty,8])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage[level]*self.syndra - self.hexes[tx,ty,8])/2
    def _shaco(self,level,enemies,percent=[2,2.25,2.5],stop=False):
        tx,ty = self._find_target(enemies)
        dd = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        for d in dd:
            dx,dy = tx+d[0],ty+d[1]
            if (dx<0) or (dx>6) or (dy<0) or (dy>7):
                dd.remove(d)
        i = np.random.choice(len(dd),1)[0]
        x,y = dd[i][0],dd[i][1]
        damage = self.hexes[self.arr[0],self.arr[1],5]*self.hexes[self.arr[0],self.arr[1],6]
        self.hexes[self.arr[0],self.arr[1],:] = 0
        if (damage*percent[level]-self.hexes[tx,ty,7])/2 < 0 :
            1 == 1
        else:
            self.hexes[tx,ty,2] -= (damage*percent[level]-self.hexes[tx,ty,7])/2
        '''move 나중에'''
    def _rumble(self,level,enemies,damage=[250,400,800],stop=False):
        '''
        damage 나중에 원뿔?
        if self.demol:
            self.hexes[tx,ty,18] += 2
        '''
    def _neeko(self,level,enemies,damage=[200,275,550],stun=[3,5,7],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        xy = np.where(self.hexes[self.arr[0]-2:self.arr[0]+3,
            self.arr[1]-2:self.arr[1]+3,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx,ty,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
    def _master_yi(self,level,enemies,bonus=[75,100,200],heal=[0.08,0.1,0.15],stop=False):
        self.mater_yi = [bonus[level],heal[level]]
    def _lux(self,level,enemies,damage=[200,300,600],stun=[3,4,5],stop=False):
        '''damage 나중에 원뿔?'''
    def _kassadin(self,level,enemies,damage=[250,400,800],stun=[5,6,7],stop=False):
        tx,ty = self._find_target(enemies)
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        '''damage 나중에 원뿔?'''
    def _karma(self,level,enemies,shield=[250,400,800],speed=[0.35,0.5,1],stop=False):
        if stop:
            x,y = np.where(self.hexes[:,:,-1]==self.karma)
            self.hexes[x,y,25] -= shield[level]/2
            self.hexes[x,y,6] -= speed[level]
        else:
            xy = np.where(self.hexes[:,:,0]==self.myopp)
            us = [[x,y] for x,y in zip(xy[0],xy[1])]
            tiles = np.tile(np.array(self.arr),(len(us),1))
            dist = list(np.max(abs(tiles-us),axis=1))
            if len(dist) != 1:
                dist.remove(0)
            ind = np.argmin(dist)
            self.hexes[us[ind][0],us[ind][1],25] += shield[level]/2
            self.hexes[us[ind][0],us[ind][1],6] += speed[level]
            self.karma = self.hexes[us[ind][0],us[ind][1],-1]
            self.hexes[self.arr[0],self.arr[1],26] = 9
    def _jayce(self,level,enemies,damage=[450,600,1200],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        tx,ty = self._find_target(enemies)
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
    def _ezreal(self,level,enemies,damage=[200,300,600],stop=False):
        '''mana reaver characteristics changes to 50% decrease cur_mana'''
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        t = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[t]
        x1,y1,x2,y2 = self._boundary(tx,ty,-2,3)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.hexes[tx+x1,ty+y1,3] = 0.5*self.hexes[tx+x1,ty+y1,3]
    def _ashe(self,level,enemies,damage=[250,350,700],stun=[4,4,4],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        i = np.random.choice(len(enemies),1)[0]
        tx,ty= enemies[i]
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.hexes[tx+x1,ty+y1,18] = stun[level]
    def _wukong(self,level,enemies,damage=[350,500,4000],stun=[4,4,10],stop=False):
        '''move 구현해야함'''
    def _velkoz(self,level,enemies,damage=[425,550,2000],stop=False):
        '''damage 나중에 원뿔?'''
    def _soraka(self,level,enemies,heal=[375,550,20000],stop=False):
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        for u in us:
            self.hexes[u[0],u[1],2] += heal[level]
            if self.hexes[u[0],u[1],2] > self.maxhexes[u[0],u[1],2]:
                self.hexes[u[0],u[1],2] = self.maxhexes[u[0],u[1],2]
    def _kayle(self,level,enemies,damage=[125,200,750],stop=False):
        if self.kayle:
            self.hexes[self.arr[0],self.arr[1],5] += damage[level]
            self.kayle = False
    def _jinx(self,level,enemies,speed=[0.6,0.75,1],damage=[100,175,750],stop=False):
        '''0mana'''
        if self.jinx >= 2:
            enemy = self.hexes[enemies[0][0],enemies[0][1],0]
            tx,ty = self._find_target(enemies)
            atk = self.hexes[self.arr[0],self.arr[1],5]*self.hexes[self.arr[0],self.arr[1],6]
            self.hexes[tx,ty,2] -= (atk - self.hexes[tx,ty,7])/2
            x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
            xy = np.where(self,hexes[x1:x2,y1:y2,0]==enemy)
            target = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                    1 == 1
                else:
                    self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
        elif (self.jinx >= 1) and (self.jinx_speed):
            self.hexes[self.arr[0],self.arr[1],6] += speed[level]
            self.jinx_speed = False
    def _jhin(self,level,enemies,percent=[2.44,3.44,44.44],stop=False):
        '''0mana'''
        if self.tic % 4 == 0:
            tx,ty = self._find_target(enemies)
            if (self.hexes[self.arr[0],self.arr[1],5]*percent[level]-self.hexes[tx,ty,7])/2 < 0:
                1==1
            else:
                self.hexes[tx,ty,2] -= (self.hexes[self.arr[0],self.arr[1],5]*\
                    percent[level]-self.hexes[tx,ty,7])/2
        else:
            return True
    def _irelia(self,level,enemies,percent=[1.75,2.5,5],stop=False):
        while True:
            tx,ty = self._find_target(enemies)
            if (self.hexes[self.arr[0],self.arr[1],5]*percent[level]-self.hexes[tx,ty,7])/2 < 0:
                1 == 1
            else:
                self.hexes[tx,ty,2] -= (self.hexes[self.arr[0],self.arr[1],5]*percent[level] \
                    - self.hexes[tx,ty,7])/2
            if self.hexes[tx,ty,2] > 0:
                break
            enemies.remove([tx,ty])
            if len(enemies) == 0:
                break
    def _fizz(self,level,enemies,damage=[350,500,2000],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        ind = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[ind]
        x1,y1,x2,y2 = self._boundary(tx,ty,-3,4)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.hexes[tx+x1,ty+y1,18] = 3
    def _chogath(self,level,enemies,damage=[150,250,2000],stun=[4,4,8],stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        ind = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[ind]
        x1,y1,x2,y2 = self._boundary(tx,ty,-3,4)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.hexes[tx+x1,ty+y1,18] = stun[level]
    def _thresh(self,level,enemies,mana=[25,50,200],units=[1,1,9],stop=False):
        if self.myopp == 1:
            wait_units = self.mywait
        else:
            wait_units = self.oppwait
        #units = np.random.choice(len(wait_units),units[level])
        '''wait_unit 빈 곳 배치 해야함'''
    def _miss_fortune(self,level,enemies,damage=[0.6,0.8,9.99],stop=False):
        '''damage 나중에 원뿔?'''
    def _lulu(self,level,enemies,num=[2,4,12],bonus=[0.05,0.1,0.25],stun=[6,6,16],
        stop=False):
        if stop:
            for tx,ty,_ in self.lulu:
                self.hexes[tx,ty,7] += bonus[level]*self.hexes[tx,ty,7]
                self.hexes[tx,ty,8] += bonus[level]*self.hexes[tx,ty,8]
        else:
            tiles = np.tile(np.array(self.arr),(len(enemies),1))
            dist = np.max(abs(tiles-enemies),axis=1)
            enemies = [[e[0],e[1],d] for e,d in zip(enemies,dist)]
            enemies = sorted(enemies,key = lambda enemy: enemy[2])
            if num[level] > len(enemies):
                nums = len(enemies)
            else:
                nums = num[level]
            targets = enemies[:nums]
            self.hexes[self.arr[0],self.arr[1],26] = stun[level] + 1
            for tx,ty,_ in targets:
                self.hexes[tx,ty,7] -= bonus[level]*self.hexes[tx,ty,7]
                self.hexes[tx,ty,8] -= bonus[level]*self.hexes[tx,ty,8]
            self.lulu = targets
    def _gangplank(self,level,enemies,damage=[450,600,9001],stop=False):
        if stop:
            x1,y1,x2,y2 = self.gangpalnk
            xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                if (damage[level] - self.hexes[tx+x1,ty+y1,8])/2 < 0 :
                    1 == 1
                else:
                    self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
                    if self.demol:
                        self.hexes[tx,ty,18] += 2
        else:
            tx,ty = self._find_target(enemies)
            self.gangplank = [self._boundary(tx,ty,-3,4)]
    def _ekko(self,level,enemies,damage=[225,400,2000],stop=False):
        self.ekko = True
        for x,y in enemies:
            ad = self.hexes[self.arr[0],self.arr[1],5] - self.hexes[x,y,7]
            ap = damage[level] - self.hexes[x,y,8]
            if ad < 0:
                ad = 0
            if ap < 0:
                ap = 0
            self.hexes[x,y,2] -= (ad+ap)/2
    def _aurelion_sol(self,level,enemies,damage=[100,150,750],stop=False):
        self.fly += 3
        inds = np.random.choice(len(enemies),self.fly)
        for ind in inds:
            x,y = enemies[ind]
            if (damage[level] - self.hexes[x,y,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[x,y,2] -= (damage[level] - self.hexes[x,y,8])/2
    def _mech_garren(self,level,enemies,damage=[750,1250,1700],stun=2,stop=False):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        tx,ty = self._find_target(enemies)
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            if (damage[level] - self.hexes[int(tx)+x1,int(ty)+y1,8])/2 < 0 :
                1 == 1
            else:
                self.hexes[tx+x1,ty+y1,2] -= (damage[level] - self.hexes[tx+x1,ty+y1,8])/2
            self.hexes[tx+x1,ty+y1,18] = stun
