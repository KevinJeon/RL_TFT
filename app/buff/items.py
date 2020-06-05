import numpy as np

class Item:
    def __init__(self,item_assign,stats):
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
        self.stat_infos = {2:'health',3:'mana',5:'attack_damage',6:'attack_speed',
            7:'armor',8:'magical_resistance',9:'no',10:'skill',12:'dodge'}
        #items
        self.deathblade= False
        self.force_of_nature = 0
        self._make_table()
        self.stats = self._update(item_assign,stats)
    def _update(self,assigned_items,stats):
        for items,stat in zip(assigned_items,stats):
            sub = 0
            for item in items:
                sub += 1
                if item == 9:
                    continue
                elif item == 12:
                    stat['critical'] += self.subitem[item]
                    stat['dodge'] += self.subitem[item]
                elif item == 3:
                    stat['mana'][0] += self.subitem[item]
                else:
                    stat[self.stat_infos[item]] += self.subitem[item]
                if sub == 2:
                    sub = 0
                    stat = self._merge_item(stat, i1, i2)
        return stats
    def _make_table(self):
        items = [2,3,5,6,7,8,9,10,12]
        health = [0,0,self._warmogs_armor,self._redemption,0,self._zekes_herald,
            self._zzrot_portal,self._red_buff,self._zephyr,self._protectors_chestguard,
            self._morellonomicon,0,self._trap_claw]
        mana = [0,0,self._redemption,self._seraphs_embrace,0,self._spear_of_shojin,
            self._statikk_shiv,self._frozen_heart,self._chalice_of_favor,self._star_guardians_charm,
            self._ludens_echo,0,self._hand_of_justice]
        attack_damage = [0,0,self._zekes_herald,self._spear_of_shojin,0,self._death_blade,
            self._giant_slayer,self._guardian_angel,self._blood_thirster,self._blade_of_the_ruined_king,
            self._hextech_gunblade,0,self._infinity_edge]
        attack_speed = [0,0,self._zzrot_portal,self._statikk_shiv,0,self._giant_slayer,
            self._rapid_firecannon,self._titans_resolve,self._runnans_hurricane,
            self._infiltrators_talons,self._guinsoos_rageblade,0,self._last_whisper]
        armor = [0,0,self._red_buff,self._frozen_heart,0,self._guardian_angel,self._titans_resolve,
            self._bramble_vest,self._sword_breaker,self._rebel_medal,self._locket_of_the_iron_solari,
            0,self._shroud_of_stillness]
        magical_resistance = [0,0,self._zephyr,self._chalice_of_favor,0,self._blood_thirster,
            self._runnans_hurricane,self._sword_breaker,self._dragons_claw,self._celestial_orb,
            self._ionic_spark,0,self._quicksilver]
        spatula = [0,0,self._protectors_chestguard,self._star_guardians_charm,0,
            self._blade_of_the_ruined_king,self._infiltrators_talons,self._rebel_medal,
            self._celestial_orb,self._force_of_nature,self._demolitionists_charge,
            0,self._dark_stars_heart]
        skill = [0,0,self._morellonomicon,self._ludens_echo,0,self._hextech_gunblade,
            self._guinsoos_rageblade,self._locket_of_the_iron_solari,self._ionic_spark,
            self._demolitionists_charge,self._rabadons_deathcap,0,self._jeweled_gauntlet]
        dodge_cri = [0,0,self._trap_claw,self._hand_of_justice,0,self._infinity_edge,
            self._last_whisper,self._shroud_of_stillness,self._quicksilver,self._dark_stars_heart,
            self._jeweled_gauntlet,0,self._thiefs_gloves]
        tables = [0,0,health,mana,0,attack_damage,attack_speed,armor,magical_resistance,
            spatula,skill,0,dodge_cri]
        self.item_table = list(np.zeros((13,13)))
        for i in items:
            for j in items:
                self.item_table[i] = list(self.item_table[i])
                self.item_table[i][j] = tables[i][j]
    def _merge_item(self,stat,i1,i2):
        mixed_item = self.item_table[i1][i2]
        stat['item'] = mixed_item
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
