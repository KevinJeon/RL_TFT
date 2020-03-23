from env import TFT_env
import config_3 as cfg
import numpy as np
def main():
    keys = dict()
    for k,i in cfg.__dict__.items():
        if k[:2] != '__':
            keys[k] = i
    env = TFT_env(**keys)
    # rule-based random policy for before_fight
    while env.life > 0:
        a = list(range(9))
        if env.money < 2:
            ind = a.index(7)
            del a[ind]
        if (env.money < 4) or (env.player_level == 9):
            ind = a.index(8)
            del a[ind]
        for i in range(5):
            if (env.five_champs[i] == False) or (env.money < env.five_cost[i]):
                ind = a.index(i)
                del a[ind]
        if env.total_units:
            ind = a.index(6)
            del a[ind]
        if env.money <= 0:
            a = [5]
        act = np.random.choice(a,1)[0]
        env.play_round(env.act1_spc[act])
        if env.life <= 0:
            print('lose!!!!!!!')
            break
        if env.cur_round[0] == '6':
            print('win!!!!!!!!')
            break
    for u,i in env.total_units.items():
        print(u,i)
if __name__ == '__main__':
    main()
