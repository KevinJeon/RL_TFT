import numpy as np

class Item:
    def __init__(self,item_assign):
        self.subitem = np.zeros(13)
        self.subitem[5] = 15
        self.subitem[6] = 0.15
        self.subitem[7] = 25
        self.subitem[8] = 25
        self.subitem[10] = 0.2
        self.subitem[3] = 15
        self.subitem[2] = 200
        self.subitem[9] = 0
        self.subitem[12] = 0.1
        #items
        self.deathblade= False
        self.force_of_nature = 0
    def update(self,champs):
        for i in range(3):
            for c in champs:
                i1 = self.items[c[0],c[1],19+2*i]
                i2 = self.items[c[0],c[1],20+2*i]
            if not 0 in [i1,i2]:
                self._merge_item(c,i1,i2)
    def _merge_item(self,c,i1,i2):
        1 == 1
    def _death_blade(self,c):
        1 == 1
    def _giant_slayer(self,c):
        1 == 1
    def _guardian_angel(self,c):
        1 == 1
    def _blood_thirster(self,c):
        1 == 1
    def _hextech_gunblade(self,c):
        1 == 1
    def _spear_of_shojin(self,c):
        1 == 1
    def _zekes_herald(self,c):
        1 == 1
    def _blade_of_the_ruined_king(self,c):
        1 == 1
    def _infinity_edge(self,c):
        1 == 1
    def _rapid_firecannon(self,c):
        1 == 1
    def _titans_resolve(self,c):
        1 == 1
    def _runnans_hurricane(self,c):
        1 == 1
    def _guinsoos_rageblade(self,c):
        1 == 1
    def _statikk_shiv(self,c):
        1 == 1
    def _zzrot_portal(self,c):
        1 == 1
    def _infiltrators_talons(self,c):
        1 == 1
    def _last_whisper(self,c):
        1 == 1
    def _bramble_vest(self,c):
        1 == 1
    def _sword_breaker(self,c):
        1 == 1
    def _locket_of_the_iron_solari(self,c):
        1 == 1
    def _frozen_heart(self,c):
        1 == 1
    def _red_buff(self,c):
        1 == 1
    def _rebel_medal(self,c):
        1 == 1
    def _shroud_of_stillness(self,c):
        1 == 1
    def _dragons_claw(self,c):
        1 == 1
    def _ionic_spark(self,c):
        1 == 1
    def _chalice_of_favor(self,c):
        1 == 1
    def _zephyr(self,c):
        1 == 1
    def _celestial_orb(self,c):
        1 == 1
    def _quicksilver(self,c):
        1 == 1
    def _rabadons_deathcap(self,c):
        1 == 1
    def _ludens_echo(self,c):
        1 == 1
    def _morellonomicon(self,c):
        1 == 1
    def _demolitionists_charge(self,c):
        1 == 1
    def _jeweled_gauntlet(self,c):
        1 == 1
    def _seraphs_embrace(self,c):
        1 == 1
    def _redemption(self,c):
        1 == 1
    def _star_guardians_charm(self,c):
        1 == 1
    def _hand_of_justice(self,c):
        1 == 1
    def _warmogs_armor(self,c):
        1 == 1
    def _protectors_chestguard(self,c):
        1 == 1
    def _trap_claw(self,c):
        1 == 1
    def _force_of_nature(self,c):
        1 == 1
    def _dark_stars_heart(self,c):
        1 == 1
    def _thiefs_gloves(self,c):
        1 == 1
