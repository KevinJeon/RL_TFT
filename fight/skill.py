import numpy as np
import copy
class Skill:
    def __init__(self,hexes,maxhexes,arr,tic):
        self.hexes = hexes
        self.maxhexes = maxhexes
        self.arr = arr
        self.tic = tic
        self.skills = [self._zoe,self._ziggs,self._xayah,self._twistedfate,self._poppy,
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
        self.master_yi = False
        self.kayle = False
        self.jinx = False
        self.jinx_bomb = False
        self.irel_kill = False
        self.ekko = False
        self.fly = 0
    def _find_target(self,enemies,khazix=False):
        tiles = np.tile(np.array(self.arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        tx,ty = enemies[ind]
        return tx,ty
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
        return x1,x2,y1,y2
    def cast(self,enemy):
        ind = self.hexes[self.arr[0],self.arr[1],1]
        level = self.hexes[self.arr[0],self.arr[1],17]
        xy = np.where(self.hexes[:,:,0]==enemy)
        enemies = [[x,y] for x,y in zip(xy[0],xy[1])]
        self.myopp = self.hexes[self.arr[0],self.arr[1],0]
        if ind == 100:
            self.skills[-1](enemies)
        else:
            self.skills[int(ind)](int(level),enemies)
        if self.irel_kill:
            pass
        else:
            self.hexes[self.arr[0],self.arr[1],9] = 0
        return self.hexes
    def _zoe(self,level,enemies,damage=[200,275,400],stun=[4,5,8]):
        target = np.argmax(self.hexes[:,:,2])
        tx,ty = target//8,target%8
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[tx,ty,18] = stun[level]
    def _ziggs(self,level,enemies,damage=[250,325,550]):
        tx,ty = self._find_target(enemies)
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
    def _xayah(self,level,enemies,speed=[1,1.25,1.5],duration=[8,8,8]):
        self.hexes[self.arr[0],self.arr[1],6] += speed[level]
        self.xayah = duration[level]
    def _twistedfate(self,level,enemies,damage=[200,300,500]):
        '''continuous is later tic for 6 tic'''
    def _poppy(self,level,enemies,damage=[100,175,250],shield=[200,350,500]):
        tx,ty = self._find_target(enemies)
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[self.arr[0],self.arr[0],2] += shield[level]
    def _malphite(self,level,enemies,shield=[0.4,0.45,0.5]):
        if self.tic == 1:
            self.hexes[self.arr[0],self.arr[1],2] += \
                self.hexes[self.arr[0],self.arr[1],2]*shield[level]
    def _leona(self,level,enemies,shield=[40,80,120]):
        self.hexes[self.arr[0],self.arr[0],7] += 40
        self.hexes[self.arr[0],self.arr[0],8] += 40
        self.hexes[self.arr[0],self.arr[0],26] = 8

    def _khazix(self,level,enemies,damage=[175,250,400],bonus=[600,800,1350]):
        tx,ty = self._find_target(enemies)
        tiles = np.tile(np.array([tx,ty]),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        self.hexes[tx,ty,2] -= (damage[level]-self.hexes[tx,ty,8])/2
        nearest_dist = np.min(dist)
        if nearest_dist > 1:
            self.hexes[tx,ty,2] -= (bonus[level]-self.hexes[tx,ty,8])/2
    def _jarvan_iv(self,level,enemies,speed=[0.5,0.75,1]):
        '''continuous is later for 6 tic'''
    def _graves(self,level,enemies,damage=[150,200,400]):
        '''continuous is later for 8 tic'''
    def _fiora(self,level,enemies,damage=[200,300,450]):
        '''continuous is later for 3,3 tic'''
    def _caitlyn(self,level,enemies,damage=[750,1500,3000]):
        '''continuous is later for 8 tic'''
    def _yasuo(self,level,enemies,hit=[8,10,12]):
        '''continuous is later for 2 tic'''
    def _xin_zhao(self,level,enemies,damage=[200,275,375]):
        '''continuous is later for 3 tic'''
    def _sona(self,level,enemies,healed=[2,3,4],heal=[100,150,200]):
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
    def _shen(self,level,enemies,resist=[15,30,45],duration=[5,6,7]):
        self.shen = duration
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        tiles = np.tile(np.array(self.arr),(len(us),1))
        dist = np.max(abs(tiles-us),axis=1)
        '''later~~~~~~~~~~~~~~~~'''
    def _rakan(self,level,enemies,damage=[175,250,400],duration=[3,3,3]):
        '''continuous is later for 3 tic'''
    def _mordekaiser(self,level,enemies,shield=[350,500,800],damage=[50,75,125]):
        '''need to make shield '''
    def _lucian(self,level,enemies,damage=[150,200,325]):
        tx,ty = self._find_target(enemies)
        d = [np.sign(tx-self.arr[0]),np.sign(ty-self.arr[1])]
        dir = np.random.choice([0,1],2,replace=False)
        moved = copy.copy(self.arr)
        shp = np.shape(self.hexes)
        if (moved[dir[0]] + d[dir[0]] < 0) or (moved[dir[0]] + d[dir[0]] > shp[dir[0]]):
            if (moved[dir[1]] + d[dir[1]] < 0) or (moved[dir[1]] + d[dir[1]] > shp[dir[1]]):
                1 == 1
            else:
                moved[dir[1]] = moved[dir[1]] + d[dir[1]]
        else:
            moved[dir[0]] = moved[dir[0]] + d[dir[0]]
        '''solve to existed someone when moved'''
    def _kaisa(self,level,enemies,hit=[4,6,9]):
        tiles = np.tile(np.array(self.arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        inds = list(np.where(dist<=2)[0])
        if len(inds) == 0:
            targets = []
        else:
            print(inds)
            print(len(inds))
            targets = [enemies[int(i)] for i in inds]
        for t in targets:
            self.hexes[t[0],t[1],2] -= (50*hit[level] - self.hexes[t[0],t[1],8])/2
    def _darius(self,level,enemies,damage=[400,500,750]):
        '''later~~~~'''
    def _blitzcrank(self,level,enemies,damage=[250,400,900]):
        '''continuous is later for 2 tic'''
    def _annie(self,level,enemies,damage=[150,200,300],shield=[270,360,540]):
        self.annie = 8
        '''shield & damage later'''
        tx,ty = self._find_target(enemies)
        dx,dy = np.sign(self.arr[0] - tx), np.sign(self.arr[1] - ty)
    def _ahri(self,level,enemies,damage=[175,250,375]):
        '''continuous is later for 4 tic'''
    def _vi(self,level,enemies,damage=[400,600,1200],knock=[150,200,500],
            duration=[4,5,6]):
        '''continuous is later for 4 tic'''
    def _syndra(self,level,enemies,damage=[80,120,200]):
        target = np.argmax(self.hexes[:,:,2])
        tx,ty = target//8,target%8
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
    def _shaco(self,level,enemies,percent=[2,2.25,2.5]):
        tx,ty = self._find_target(enemies)
        dd = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        avail = []
        for d in dd:
            dx,dy = tx+d[0],ty+d[1]
            if (dx<0) or (dx>6) or (dy<0) or (dy>7):
                continue
            avail.append(d)
        i = np.random.choice(len(avail),1)[0]
        x,y = dd[i][0],dd[i][1]
        damage = self.hexes[self.arr[0],self.arr[1],5]*self.hexes[self.arr[0],self.arr[1],6]
        self.hexes[tx+x,ty+y,:] = self.hexes[self.arr[0],self.arr[1],:]
        self.hexes[self.arr[0],self.arr[1],:] = 0
        self.hexes[tx,ty,2] -= (damage*percent[level]-self.hexes[tx,ty,7])/2
    def _rumble(self,level,enemies,damage=[250,400,800]):
        '''continuous is later for 6 tic,10 tic'''
    def _neeko(self,level,enemies,damage=[200,275,550],stun=[3,5,7]):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        xy = np.where(self.hexes[self.arr[0]-2:self.arr[0]+3,
            self.arr[1]-2:self.arr[1]+3,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
    def _master_yi(self,level,enemies,bonus=[75,100,200],heal=[0.08,0.1,0.15]):
        self.mater_yi = [bonus[level],heal[level]]
    def _lux(self,level,enemies,damage=[200,300,600],stun=[3,4,5]):
        '''continuous is later for 4 tic'''
    def _kassadin(self,level,enemies,damage=[250,400,800],stun=[5,6,7]):
        '''range?'''
    def _karma(self,level,enemies,shield=[250,400,800],speed=[0.35,0.5,1]):
        '''continuous is later for 4 tic'''
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        us,uy = self._find_target(us)
        '''later'''
    def _jayce(self,level,enemies,damage=[450,600,1200]):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        tx,ty = self._find_target(enemies)
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
    def _ezreal(self,level,enemies,damage=[200,300,600]):
        '''mana reaver characteristics changes to 50% decrease cur_mana'''
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        t = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[t]
        x1,y1,x2,y2 = self._boundary(tx,ty,-2,3)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for t in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,3] = 0.5*self.hexes[tx,ty,3]
    def _ashe(self,level,enemies,damage=[250,350,700],stun=[4,4,4]):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        i = np.random.choice(len(enemies),1)[0]
        tx,ty= enemies[i]
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
    def _wukong(self,level,enemies,damage=[350,500,4000],stun=[4,4,10]):
        '''continuous is later for 6 tic'''
    def _velkoz(self,level,enemies,damage=[425,550,2000]):
        '''continuous is later for 4 tic'''
    def _soraka(self,level,enemies,heal=[375,550,20000]):
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        for u in us:
            self.hexes[u[0],u[1],2] += heal[level]
            if self.hexes[u[0],u[1],2] > self.maxhexes[u[0],u[1],2]:
                self.hexes[u[0],u[1],2] = self.maxhexes[u[0],u[1],2]
    def _kayle(self,level,enemies,damage=[125,200,750]):
        '''continuous is later for 4 tic'''
        self.kayle = damage[level]
    def _jinx(self,level,enemies,speed=[0.6,0.75,1],damage=[100,175,750]):
        if self.jinx > 2:
            self.jinx_bomb = [True,damage[level]]
        elif self.jinx > 1:
            self.hexes[self.arr[0],self.arr[1],6] += speed[level]
    def _jhin(self,level,enemies,percent=[2.44,3.44,44.44]):
        if self.tic % 4 == 0:
            tx,ty = self._find_target(enemies)
            self.hexes[tx,ty,2] -= (self.hexes[self.arr[0],self.arr[1],5]*\
                percent[level]-self.hexes[tx,ty,7])/2
    def _irelia(self,level,enemies,percent=[1.75,2.5,5]):
        '''target is random'''
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        tx,ty = np.random.choice(enemies,1)[0]
        stop=False
        self.hexes[tx,ty,2] -= (self.hexes[arr[0],arr[1],5]*percent[level] \
            - self.hexes[tx,ty,7])/2
        if self.hexes[tx,ty,2] <= 0:
            self.irel_kill = True
        else:
            self.irel_kill = False
    def _fizz(self,level,enemies,damage=[350,500,2000]):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        ind = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[ind]
        x1,y1,x2,y2 = self._boundary(tx,ty,-3,4)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for t in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = 3
    def _chogath(self,level,enemies,damage=[150,250,2000],stun=[4,4,8]):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        ind = np.random.choice(len(enemies),1)[0]
        tx,ty = enemies[ind]
        x1,y1,x2,y2 = self._boundary(tx,ty,-3,4)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun[level]
    def _thresh(self,level,enemies,mana=[25,50,200],units=[1,1,9]):
        '''later '''
    def _miss_fortune(self,level,enemies,damage=[0.6,0.8,9.99]):
        '''continuous is later for 5 tic'''
    def _lulu(self,level,enemies,num=[2,4,12],bonus=[0.05,0.1,0.25],stun=[6,6,16]):
        '''later'''
    def _gangplank(self,level,enemies,damage=[450,600,9001]):
        if self.gangplank == 0:
            xy = np.where(self.hexes[self.grange[0]-3:self.grange[0]+4,\
                self.grange[1]-3:self.grange[1]+4,0]==enemy)
            targets = [[x,y] for x,y in zip(xy[0],xy[1])]
            for tx,ty in targets:
                self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
            self.gangpalnk = False
        elif self.gangplank:
            tx,ty = self._find_target(enemies)
            self.grange = [tx,ty]
            if type(self.gangplank) == int:
                self.gangplank -= 1
    def _ekko(self,level,enemies,damage=[225,400,2000]):
        self.ekko = True
        for x,y in enemies:
            ad = self.hexes[self.arr[0],self.arr[1],5] - self.hexes[x,y,7]
            ap = damage[level] - self.hexes[x,y,8]
            self.hexes[x,y,2] -= (ad-ap)/2
    def _aurelion_sol(self,level,enemies,damage=[100,150,750]):
        self.fly += 3
        xy = np.random.choice(enemies,self.fly)
        for x,y in xy:
            self.hexes[x,y,2] -= (damage[level] - self.hexes[x,y,8])/2
    def _mech_garren(self,enemies,damage=750,stun=2):
        enemy = self.hexes[enemies[0][0],enemies[0][1],0]
        tx,ty = self._find_target(enemies)
        x1,y1,x2,y2 = self._boundary(tx,ty,-1,2)
        xy = np.where(self.hexes[x1:x2,y1:y2,0]==enemy)
        targets = [[x,y] for x,y in zip(xy[0],xy[1])]
        for tx,ty in targets:
            self.hexes[tx,ty,2] -= (damage - self.hexes[tx,ty,8])/2
            self.hexes[tx,ty,18] = stun
