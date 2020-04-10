import numpy as np

def item_apply(hexes):
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
    for i in range(6):
        item = hexes[:,:,13+i]
        if np.sum(item) == 0:
            continue
        have_item = np.where(item!=0)
        item_xy = [[x,y] for x,y in zip(have_item[0],have_item[1])]
        for xy in item_xy:
            x,y = xy
            ind = int(item[x,y])
            if ind == 0:
                continue
            hexes[x,y,ind] = hexes[x,y,ind] + plus[ind]
    return hexes
def item_merge(hexes):
    
