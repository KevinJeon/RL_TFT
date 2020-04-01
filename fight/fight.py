import numpy as np

def fight(mychamp,myarr,myitem,mysyn):
    '''
    simple version of fight
    - to do
    apply skill
    apply synergy effect
    apply item effect
    '''
    hexes = list(np.zeros(28))
    for a,c in zip(myarr,mychamp):
        hexes[a] = c
    print(hexes)
    tic_fight(mychamp,myarr,myitem,mysyn)
    return np.random.choice([True,False]),np.random.randint(2,8)
def tic_fight(mychamp,myarr,myitem,mysyn):
    '''
    change for one second
    '''
    print('1 tic')
