from env import TFT_env
import config_3 as cfg
import numpy as np
from agent.random_agent import RandomAgent
from agent.rulebased_agent import RulebasedAgent
from one_player import Player
from utils.draw import make_video
import json
import os
import copy
def main(env):
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
        env.play_round(gui=False)
    return env.final_place
if __name__ == '__main__':
    if os.path.exists('result.json'):
        with open('result.json','r') as f:
            print('hi')
            jd = json.load(f)
    else:
        jd = dict()
    keys = dict()
    cfgs = cfg.__dict__.items()
    for k,i in cfgs:
        if k[:2] != '__':
            keys[k] = i
    for i in range(300):
        keys_copy = copy.deepcopy(keys)
        msg = ('-----------------------\n'+\
            '{} th game start!\n'+\
            '-----------------------').format(i)
        print(msg)
        print(keys_copy['champ_state_info'])
        env = TFT_env(**keys_copy)
        final_place = main(env)
    #    for agent in final_place.keys():
    #        if agent not in jd.keys():
    #            jd[agent] = [final_place[agent]]
    #        else:
    #            jd[agent].append(final_place[agent])
    #        with open('result.json', 'w', encoding='utf-8') as f:
    #            json.dump(jd, f, indent="\t")
