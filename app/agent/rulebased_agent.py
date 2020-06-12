import numpy as np
import config_3 as cfg
import operator
class RulebasedAgent(object):

    def _synergy(total_units):
        synergy = dict()
        for unit,items in total_units.items():
            for syn in items['synergy']:
                if str(syn) not in synergy.keys():
                    synergy[str(syn)] = 1
                else:
                    synergy[str(syn)] += 1
        return synergy
    def bef_action(money,player_level,five_champs,five_cost,total_units,unit_number,
        life=None):
        synergy = RulebasedAgent._synergy(total_units)
        sorted_syns = sorted(synergy.items(),key=operator.itemgetter(0))
        if len(sorted_syns) > 3:
            sorted_syns = sorted_syns[:3]
        RulebasedAgent.top_syns = [int(syn[0]) for syn in sorted_syns]
        a = list(range(9))
        # base rule
        if money < 2:
            ind = a.index(7)
            del a[ind]
        if (money < 4) or (player_level == 9):
            ind = a.index(8)
            del a[ind]
        if unit_number >= player_level + 9:
            ind = a.index(0)
            del a[ind]
            ind = a.index(1)
            del a[ind]
            ind = a.index(2)
            del a[ind]
            ind = a.index(3)
            del a[ind]
            ind = a.index(4)
            del a[ind]
        else:
            for i in range(5):
                if (five_champs[i] == False) or (money < five_cost[i]):
                    ind = a.index(i)
                    del a[ind]
                else:
                    syns = cfg.champ_state_info[five_champs[i]]['elem']
                    print(syns)
                    for s in syns:
                        if s in RulebasedAgent.top_syns:
                            print(five_champs)
                            ind = a.index(i)
                            return i
        #if life < 20:
        #    np.random.choice([7,8],1,p=[0.7,0.3])[0]
        if total_units:
            ind = a.index(6)
            del a[ind]
        if money <= 0:
            a = [5]
        if money <= 30:
            a = [5]
        else:
            return np.random.choice([7,8],1,p=[0.7,0.3])[0]
        return a[0]
    def rearr_action(avail_units,syns):
        battle_indices = []
        check = list(range(len(syns)))
        for i,syn in enumerate(syns):
            is_pass = False
            for s in syn:
                if is_pass:
                    pass
                elif (s in RulebasedAgent.top_syns) or (s in RulebasedAgent.top_syns):
                    battle_indices.append(i)
                    check.remove(i)
                    is_pass = True
        tofill = avail_units - len(battle_indices)
        if tofill > 0:
            rand_fill = list(np.random.choice(check,tofill))
            battle_indices += rand_fill
        else:
            1 == 1
        return battle_indices
