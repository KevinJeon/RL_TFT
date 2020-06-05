import json
import matplotlib.pyplot as plt
import numpy as np
with open('result.json') as f:
    jd=json.load(f)
    fig = plt.figure(figsize=(32,16))
    fig.suptitle('Result of 200 Games',position=(0.5, 1),fontsize=50)
    st = 241
    for d in jd.items():

        '''
        plt.subplot(st)
        plt.title(d[0].capitalize(),fontsize=40)
        dd = np.bincount(d[1])
        y = list(range(1,9))
        plt.bar(y,list(dd[1:]))
        plt.xticks(np.arange(1,9),fontsize=40)
        plt.yticks([0,10,20,30,40,50],fontsize=40)
        plt.xlabel('Place',fontsize=40)
        plt.ylabel('Number of times',fontsize=40)
        '''
        dd = np.bincount(d[1][:200])[1:]
        avg = np.mean(d[1][:200])
        var = np.var(d[1][:200])
        st += 1
        print(dd)
        print(avg,var)
    '''
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('result.tif'.format(),dpi=300)
    '''
