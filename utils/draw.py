import cv2,glob,os
import numpy as np
import config_3 as cfg
def make_video(dir,videoname):
    frames = []
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(videoname,cv2.VideoWriter_fourcc(*'DIVX'),3,(1920,1920))
    for fn in os.listdir(dir):
        img = cv2.imread(os.path.join(dir,fn))
        print(fn)
        out.write(img)
    out.release()
    cap.release()
    cv2.destroyAllWindows()
def draw_chess(hexes,maxhexes,imgname,attack_infos):
    '''
    center
    - odd : (310+200n,240),(310+200n,640)
    - even : (410+200n,440),(410+200n,840)
    '''
    img = make_chess()
    find_units = np.where(hexes[:,:,0]!=0)
    item_name = [None,'Spatula','Giant Belt','Tear of the Goddeness',0,
        'Needless Large Rod',0,'BF sword','Recurve bow','Chain vest',
        'Negatron Clock',0,'Sparring Gloves']
    pairs = [[x,y] for x,y in zip(find_units[0],find_units[1])]
    for p in pairs:
        side = hexes[p[0],p[1],0]
        if p[1] % 2 == 0:
            const = 210
        else:
            const = 310
        st = (200*p[0]+const,140+200*p[1])
        en = (200*p[0]+const+200,340+200*p[1])
        if side == 1:
            clr = (255,0,0)
        else:
            clr = (0,0,255)
        img = cv2.rectangle(img,st,en,clr,2)
        ind = int(hexes[p[0],p[1],1])
        name = find_name(ind)
        hp = hexes[p[0],p[1],2]
        if hp > 500:
            hp_clr = (0,255,0)
        elif hp > 300:
            hp_clr = (10,200,200)
        else:
            hp_clr = (0,0,255)
        cur_mana = hexes[p[0],p[1],3]
        tot_mana = maxhexes[p[0],p[1],3]
        is_skill = hexes[p[0],p[1],9]
        item_ind = hexes[p[0],p[1],18:]
        items = set([item_name[int(ind)] for ind in item_ind])
        if is_skill == 1:
            skill = 'already'
        else:
            skill = 'not yet'
        img = cv2.putText(img,name,(st[0],st[1]+190),cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,0,0),1)
        img = cv2.putText(img,'health : {}'.format(hp),(st[0],st[1]+170),
            cv2.FONT_HERSHEY_SIMPLEX,0.5,hp_clr,2)
        img = cv2.putText(img,'mana : {}/{}'.format(cur_mana,tot_mana),
            (st[0],st[1]+150),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
        img = cv2.putText(img,'skill : {}'.format(skill),(st[0],st[1]+130),
            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
        img = cv2.putText(img,'item : {}'.format(items),(st[0],st[1]+110),
            cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    for info in attack_infos:
        eneind,damage,arr,arrind = info
        if arr[1] % 2 == 0:
            const = 210
        else:
            const = 310
        st = (200*arr[0]+const,140+200*arr[1])
        damaging = find_name(int(arrind))
        damaged = find_name(int(eneind))
        if damage == 0:
            damage ='move to'
        img = cv2.putText(img,'{} {} {}'.format(damaging,damage,damaged),
            (st[0],st[1]+90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
    cv2.imwrite(imgname,img)
def make_chess():
    img = np.full((1920,1920,3),255).astype('float')
    for i in range(7):
        img = cv2.rectangle(img,(200*i+210,140),(200*i+410,340),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+210,540),(200*i+410,740),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+310,340),(200*i+510,540),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+310,740),(200*i+510,940),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+210,940),(200*i+410,1140),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+210,1340),(200*i+410,1540),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+310,1140),(200*i+510,1340),(0,0,0),2)
        img = cv2.rectangle(img,(200*i+310,1540),(200*i+510,1740),(0,0,0),2)
    return img
def find_name(ind):
    champs = list(cfg.champ_state_info)
    if ind == 100:
        return dict(name='Mech Pilot',cost=0,elem=[])
    return champs[ind-1]
#if __name__ =='__main__':
#    make_video('./fig/ROUND_5-1','./fig/ex.avi')
