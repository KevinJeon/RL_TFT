import numpy as np

def item_apply(hexes,player_level):
    '''
    0 : None
    1 : Spatula
    2 : Giant Belt
    3 : Tear of the Goddeness
    7 : BF sword
    8 : recurve bow
    9 : chain vest
    10 : Negatron Clock
    11 : Needless Large Rod
    12 : Sparring Gloves
    input argument
    - hexes
    - arr(place)
    - to do
    아이템 조합해서 구현
    '''
    plus = [0,0,200,20,0,0,0,15,0.15,25,25,0.2,0.1]
    for i in range(3):
        item1 = hexes[:,:,13+2*i]
        item2 = hexes[:,:,14+2*i]
        if np.sum(item) == 0:
            continue
        have_item1 = np.where(item1!=0)
        have_item2 = np.where(item2!=0)
        item_xy1 = [[x,y] for x,y in zip(have_item[0],have_item[1])]
        item_xy2 = [[x,y] for x,y in zip(have_item[0],have_item[1])]
        updated_xy = []
        updated_ind = []
        for xy in item_xy1:
            x,y = xy
            ind = int(item[x,y])
            if ind == 0:
                continue
            updated_xy += xy
            updated_ind += [ind]
            hexes[x,y,ind] = hexes[x,y,ind] + plus[ind]
        for xy in item_xy2:
            x,y = xy
            ind = int(item[x,y])
            if ind == 0:
                continue
            hexes[x,y,ind] = hexes[x,y,ind] + plus[ind]
            if xy in updated_xy:
                mer_ind = updated_xy.index(xy)
                merge = Merge(hexes,[ind,updated_ind[mer_ind]])
                result,name,change = merge.apply()
                if result == 'player_level':
                    player_level += 1
                    return hexes,player_level
                elif result == 'synergy':

                else:
                    return hexes,player_level
class Merge:
    def __init__(self,items,kill_contrib=False):
        self.items = items
        self.hexes = hexes
        self.kill_contrib = kill_contrib
        self.spatula = [self._force_of_nature,self._protectors_chestguard,
            self._starguardians_charm,self._bladeofruinedking,self._infiltrators_talons,
            self._rebel_medal,self._celestial_orb,self._demolitionists_charge,
            self._darkstars_heart]
        self.giantbelt = [self._warmogs_armor,self._redemption,self._zekes_herald,
            self._zzrots_portal,self._red_buff,self._zephyr,self._morellonomicon,
            self._trap_claw]
        self.tear_of_the_goddness = [self._seraphs_embrace,self._spear_of_shojin,
            self._statikk_shiv,self._frozen_heart,self._chalice_of_favor,
            self._ludens_echo,self._hand_of_justice]
        self.bf_sword = [self._deathblade,self._giant_slayer,self._guardian_angel,
            self._bloodthirster,self._hextech_gunblade,self._infinity_edge]
        self.recurve_bow = [self._rapid_firecannon,self._titans_resolve,
            self._runaans_hurricane,self._guinsoos_regeblade,self._last_whisper]
        self.chain_vest = [self._bramble_vest,self._sword_breaker,
            self._locket_of_the_iron_solari,self._shroud_of_stillness]
        self.negatron_clock = [self._dragon_claw,self._ionic_spark,self._quicksilver]
        self.needless_large_rod = [self._rabadons_deathcap,self._jeweled_gauntlet]
        self.sparring_gloves = [self._thiefs_gloves]
        self.under_item = [self.spatula,self.giantbelt,self.tear_of_the_goddness,
            self.bf_sword,self.reucurve_bow,self.chain_vest,self.negatron_clock,
            self.needless_large_rod,self.sparring_gloves]
        self.subitems = [1,2,3,7,8,9,10,11,12]
        self._item_table()
    def _item_table(self):
        self.item_table = list(np.zeros((13,13)))
        for s1,sub1 in enumerate(self.subitems):
            for s2,sub2 in self.subitems[s1:]:
                self.item_table[sub1][sub2] = self.under_item[s1][s2]
                self.item_table[sub2][sub1] = self.under_item[s1][s2]
    def _force_of_nature(self):
        return 'player_level','force of nature',1
    def _protectors_chestguard(self):
        return 'synergy',"protector's chestguard",'Protector'
    def _starguardians_charm(self):
        return 'synergy',"starguardian's charm",'Star_Guardian'
    def _bladeofruinedking(self):
        return 'synergy','blade of ruined king','Blademaster'
    def _infiltrators_talons(self):
        return 'synergy',"infiltrator's talons",'Infiltrator'
    def _rebel_medal(self):
        return 'synergy','rebel medal','Rebel'
    def _celestial_orb(self):
        return 'synergy','celestial orb','Celstial'
    def _demolitionists_charge(self):
        return 'synergy',"demolitionist's charge",'Demolitionist'
    def _darkstars_heart(self):
        return 'synergy',"darkstar's heart",'Dark_Star'
