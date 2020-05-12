import numpy as np
class RandomAgent:
    def bef_action(money,player_level,five_champs,five_cost,total_units):
        a = list(range(9))
        if money < 2:
            ind = a.index(7)
            del a[ind]
        if (money < 4) or (player_level == 9):
            ind = a.index(8)
            del a[ind]
        if len(total_units) >= player_level + 9:
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
        if total_units:
            ind = a.index(6)
            del a[ind]
        if money <= 0:
            a = [5]
        act = np.random.choice(a,1)[0]
        return act
    def rearr_action(player_level,syns):
        1 == 1
