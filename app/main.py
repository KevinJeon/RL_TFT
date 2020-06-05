from env import TFT_env
import config_3 as cfg
import numpy as np
from agent.random_agent import RandomAgent
from agent.rulebased_agent import RulebasedAgent
from one_player import Player
import json
import os
def main():
    keys = dict()
    for k,i in cfg.__dict__.items():
        if k[:2] != '__':
            keys[k] = i
    env = TFT_env(**keys)
    # plug-in the player
    rand = RandomAgent
    rule = RulebasedAgent
    agent1 = Player(rule)
    agent2 = Player(rand)
    agent3 = Player(rand)
    agent4 = Player(rand)
    agent5 = Player(rand)
    agent6 = Player(rand)
    agent7 = Player(rand)
    agent8 = Player(rand)
    env.agent1 = agent1
    env.agent2 = agent2
    env.agent3 = agent3
    env.agent4 = agent4
    env.agent5 = agent5
    env.agent6 = agent6
    env.agent7 = agent7
    env.agent8 = agent8
    env.init_game()
    while len(env.players) > 1:
        env.play_round()
    msg = ('Last Surviver is {}\n'+\
        'Winner champ is {}\n'+\
        'Winner synergy is {}\n').format(env.players[0].name,
            env.players[0].total_units.keys(),env.players[0].player_synergy)
    return env.place_table
if __name__ == '__main__':
    with open('result.json','r') as f:
        jd = json.load(f)
        jdk = [int(k) for k in jd.keys()]
        jdk = sorted(jdk,reverse=True)
    n = jdk[0]
    for i in range(100):
        place_table = main()
        sorted_place = sorted(place_table,key=(lambda x:x[1]))
        jd[str(i+n+1)] = sorted_place
        if i % 10 == 0:
            with open('result.json', 'w', encoding='utf-8') as f:
                json.dump(jd, f, indent="\t")
