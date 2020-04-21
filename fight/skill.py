import numpy as np

class Skill:
    def __init__(self,hexes,arr):
        self.hexes = hexes
        self.arr = arr
        self.level = level
        self.skills = [self._zoe,self._ziggs,self._xayah,self._twistedfate,self._poppy,
            self._malphite,self._leona,self._khazix,self._jarvan_iv,self._graves,
            self._fiora,self._caitlyn,self._yasuo,self._xin_zhao,self._sona,self._shen,
            self._rakan,self._mordekaiser,self._lucian,self._kaisa,self._darius,
            self._blitzcrank,self._annie,self._ahri,self._vi,self._syndra,self._shaco,
            self._rumble,self._neeko,self._master_yi,self._lux,self._kassadin,
            self._karma,self._jayce,self._ezreal,self._ashe,self._wukong,self._velkoz,
            self._soraka,self._kayle,self._jinx,self._jhin,self._irelia,self._fizz,
            self._chogath,self._thresh,self._miss_fortune,self._lulu,self._ganplank,
            self._ekko,self._aurelion_sol]
        self.myskill = []
        self.oppskill = []
        ##champs
        #duration
        self.xayah = False
        self.shen = False
        self.annie = False
    def _find_target(self,enemies,khazix=False):
        tiles = np.tile(np.array(self.arr),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        nearest_dist = np.min(dist)
        ind = np.argmin(dist)
        tx,ty = enemies[ind]
        return tx,ty
    def cast(self,enemy):
        ind = self.hexes[self.arr[0],self.arr[1],1]
        level = self.hexes[self.arr[0],self.arr[1],17]
        xy = np.where(self.hexes[:,:,0]==enemy)
        enemies = [[x,y] for x,y in zip(xy[0],xy[1])]
        self.hexes = self.skills[ind](level,enemies)
        self.hexes[self.arr[0],self.arr[1],9] = 0
        self.myopp = self.hexes[self.arr[0],self.arr[1],0]
        return self.hexes
    def _zoe(self,level,enemies,damage=[200,275,400],stun=[4,5,8]):
        target = np.argmax(self.hexes[:,:,2])
        tx,ty = target%8,target//8
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
        self.hexes[tx,ty,18] = stum[level]
    def _ziggs(self,level,enemies,damage=[250,325,550]):
        tx,ty = self._find_target(enemies)
        self.hexes[tx,ty,2] -= (damage[level] - self.hexes[tx,ty,8])/2
    def _xayah(self,level,enemies,speed=[1,1.25,1.5],duration=[8,8,8]):
        self.hexes[self.arr[0],self.arr[1],6] += speed[level]
        self.xayah = duration[level]
    def _twistedfate(self,level,enemies,damage=[200,300,500]):
        '''continuous is later tic for 6 tic'''
    def _poppy(self,level,enemies,damage=[100,175,250],shield=[200,350,500]):
        '''continuous is later for 4 tic'''
    def _malphite(self,level,enemies,shield=[0.4,0.45,0.5]):
        self.hexes[self.arr[0],self.arr[1],2] += \
            self.hexes[self.arr[0],self.arr[1],2]*shield[level]
    def _leona(self,level,enemies,shield=[40,80,120]):
        '''continuous is later for 8 tic'''
    def _khazix(self,level,enemies,damage=[175,250,400],bonus=[600,800,1350]):
        tx,ty = self._find_target(enemies)
        tiles = np.tile(np.array([tx,ty]),(len(enemies),1))
        dist = np.max(abs(tiles-enemies),axis=1)
        self.hexes[tx,ty,2] -= (damage[level]-self.hexes[tx,ty,8])/2
        if dist > 1:
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
        selected = np.random.choice(us,healed[level],replace=False)
        for sel in selected:
            self.hexes[sel[0],sel[1],2] += heal[level]
            self.hexes[sel[0],sel[1].18] = 0
    def _shen(self,level,enemies,resist=[15,30,45],duration=[5,6,7]):
        self.shen = duration
        xy = np.where(self.hexes[:,:,0]==self.myopp)
        us = [[x,y] for x,y in zip(xy[0],xy[1])]
        tiles = np.tile(np.array(self.arr),(len(us),1))
        dist = np.max(abs(tiles-enemies),axis=1)
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
        xy = np.where(dist<=2)
        targets = [[x,y] for x,y zip(xy[0],xy[1])]
        for t in targets:
            self.hexes[t[0],t[1],2] -= (50*hit[level] - self.hexes[t[0],t[1],8])/2
    def _darius(self,level,enemies,damage=[400,500,750]):
        '''later~~~~'''
    def _blitzcrank(self,level,enemies,damage=[250,400,900]):
        '''continuous is later for 2 tic'''
    def _annie(self,level,enemies,damage=[150,200,300],shield=[270,360,540]):
        self.annie = 8
        '''shield later'''
        tx,ty = self._find_target(enemies)
        '''내일 생각하자'''
    def _ahri(self,level):
        1 == 1
    def _vi(self,level):
        1 == 1
    def _syndra(self,level):
        1 == 1
    def _shaco(self,level):
        1 == 1
    def _rumble(self,level):
        1 == 1
    def _neeko(self,level):
        1 == 1
    def _master_yi(self,level):
        1 == 1
    def _lux(self,level):
        1 == 1
    def _kassadin(self,level):
        1 == 1
    def _karma(self,level):
        1 == 1
    def _jayce(self,level):
        1 == 1
    def _ezreal(self,level):
        1 == 1
    def _ashe(self,level):
        1 == 1
    def _wukong(self,level):
        1 == 1
    def _velkoz(self,level):
        1 == 1
    def _soraka(self,level):
        1 == 1
    def _kayle(self,level):
        1 == 1
    def _jinx(self,level):
        1 == 1
    def _jhin(self,level):
        1 == 1
    def _irelia(self,level):
        1 == 1
    def _fizz(self,level):
        1 == 1
    def _chogath(self,level):
        1 == 1
    def _thresh(self,level):
        1 == 1
    def _miss_fortune(self,level):
        1 == 1
    def _lulu(self,level):
        1 == 1
    def _gangplank(self,level):
        1 == 1
    def _ekko(self,level):
        1 == 1
    def _aurelion_sol(self,level):
        1 == 1
