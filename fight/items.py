import numpy as np

def item_apply(hexes,arr):
    '''
    0 : None
    1 : Spatula
    2 : Giant Belt
    3 : Tear of the Goddeness
    5 : Needless Large Rod
    7 : BF sword
    8 : recurve bow
    9 : chain vest
    10 : Negatron Clock
    12 : Sparring Gloves
    input argument
    - hexes
    - arr(place)
    '''
    plus = [0,0,200,20,0,0.2,0,15,0.15,25,25,0,0.1]
    items = hexes[arr[0],arr[1],13:]
    if sum(items) == 0:
        return hexes
    for item in items:
        item = int(item)
        hexes[arr[0],arr[1],item] = hexes[arr[0],arr[1],item] + plus[item]
    return hexes
