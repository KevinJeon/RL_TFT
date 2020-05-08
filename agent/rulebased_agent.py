import numpy as np
class RulebasedAgent:

    def bef_action(money,player_level,five_champs,five_cost,total_units):
        favorite_syn = ['khazix_1','kaisa_1','rumble_1','annie_1','fizz_1','shaco_1',
            'ekko_1']
        a = list(range(9))
        # base rule
        if money < 2:
            ind = a.index(7)
            del a[ind]
        if (money < 4) or (player_level == 9):
            ind = a.index(8)
            del a[ind]
        for i in range(5):
            if (five_champs[i] == False) or (money < five_cost[i]):
                ind = a.index(i)
                del a[ind]
        if total_units:
            ind = a.index(6)
            del a[ind]
        if money <= 0:
            a = [5]
        if money <= 50:
            a = [5]
        else:
            for i in range(5):
                if five_champs[i] in favorite_syn:
                    print(five_champs)
                    ind = a.index(i)
                    return i
            return np.random.choice([7,8],1,p=[0.7,0.3])[0]

        return a[0]
    def rearr_action(avail_units,syns):
        battle_indices = []
        for i,syn in enumerate(syns):
            if (4 in syn) or (14 in syn):
                battle_indices.append(i)
                del syns[i]
        tofill = avail_units - len(battle_indices)
        rand_fill = list(np.random.choice(len(syns),tofill))
        battle_indices += rand_fill
        return battle_indices
