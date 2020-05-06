import tkinter as tk
from PIL import ImageTk as itk
from PIL import Image
class GUI:
    #pallete
    black = '#000000'
    red = '#ff0000'
    blue = '#0000ff'
    white = '#ffffff'
    cost1 = '#d9ded7'
    cost2 = '#3ed119'
    cost3 = '#0974b3'
    cost4 = '#4d0391'
    cost5 = '#ffcb3b'
    queue = '#35353d'
    queue_border = '#5e4604'
    wait = '#918f89'
    gold = '#e0d44f'
    nogold = '#3b3b3b'
    battlefield = '#69bf47'
    def __init__(self,x,y,cost=None,name=None,is_exist=None,infos=None,
        my_money=0,opp_money=0):
        # canvas
        self.x = x
        self.y = y
        self.w = 11*x
        self.h = 10*x+y
        # queue
        self.q_w = 10*x
        self.q_h = y
        # waitfield
        self.w_w = 9*x
        self.w_h = x
        # gold
        self.g = 0.7*x
        #battlefield
        self.b_w = 8*x
        self.b_h = 8*x
        self.root = tk.Tk()
        self.root.title('TFT GYM')
        self.root.geometry('{}x{}+{}+{}'.format(self.w,self.h,0,0))
        self.root.resizable(False,False)
        self.arr = []
        self.game = tk.Canvas(self.root,width=self.w,height=self.h,bd=0)
        # wait
        self.game.create_rectangle(self.x+1,self.h-self.q_h,self.x+self.w_w,
            self.h-self.q_h-self.w_h,fill=GUI.wait,outline=GUI.black)
        self.game.create_rectangle(self.x,0,self.x+self.w_w,self.w_h,fill=GUI.wait,
            outline=GUI.black)
        # item
        self.game.create_rectangle(0,self.h-self.q_h,self.x,self.h-self.q_h-1.5*self.x,
            fill=GUI.wait,outline=GUI.black)
        self.game.create_rectangle(self.w,0,self.w-self.x,1.5*self.x,fill=GUI.wait,
            outline=GUI.black)
        # queue
        self.game.create_rectangle(0,self.h,self.q_w,self.h-self.q_h,fill=GUI.queue,
            outline=GUI.queue_border,width=2)
        self._make_queue(self.game,is_exist,cost,name=name)
        # _gold
        self._gold(self.game,my_money,opp_money)
        # field
        self.game.create_rectangle(self.x*1.5,self.x,self.x*1.5+self.b_w,
            self.x+self.b_h,fill=GUI.battlefield,outline=GUI.black,width=1)
        self._make_board(self.game,self.x*1.75)
        self.init_make_champs(self.game,infos)
        self.game.pack()
    def _gold(self,game,data1,data2):
        dist = 0.3*self.g
        clr1,clr2 = GUI.gold,GUI.gold
        money1 = data1 // 10
        money2 = data2 // 10
        for i in range(5):
            if i+1 > money1:
                clr1 = GUI.nogold
            if i+1 > money2:
                clr2 = GUI.nogold
            st = (self.g+dist)*(i+1)
            en = self.g+(self.g+dist)*(i+1)
            game.create_oval(2,self.h-self.q_h-self.w_h-st,self.g+2,
                self.h-self.q_h-self.w_h-en,fill=clr1,outline=GUI.white)
            game.create_oval(self.w-2,self.w_h+st,self.w-2-self.g,
                self.w_h+en,fill=clr2,outline=GUI.white)
    def _make_board(self,game,st):
        self.center = dict()
        for i in range(8):
            h = self.w_h+self.x*i
            if i % 2 == 0:
                st1 = st
            else:
                st1 = st+self.x*0.5
            for j in range(7):
                game.create_rectangle(st1+self.x*j,h,st1+self.x*(j+1),h+self.x,
                    fill=GUI.battlefield,outline=GUI.black,width=2)
                x,y = (st1+self.x*j+st1+self.x*(j+1))/2,h+self.x/2
                self.center['[{}, {}]'.format(j,i)] = [y,x]
    def _make_queue(self,game,data,cost,name):
        w = self.x * 2
        h = self.y
        i_w = 50
        i_h = 50
        clrs = [GUI.cost1,GUI.cost2,GUI.cost3,GUI.cost4,GUI.cost5]
        imgs = []
        for n in name:
            print(n)
            if n == None:
                img = None
            else:
                img = tk.PhotoImage(file='./utils/icon/{}.gif'.format(n))
            imgs.append(img)
        game.ph1 = imgs[0]
        game.ph2 = imgs[1]
        game.ph3 = imgs[2]
        game.ph4 = imgs[3]
        game.ph5 = imgs[4]
        imgs = [game.ph1,game.ph2,game.ph3,game.ph4,game.ph5]
        print(imgs)
        self.photos = self._ready_champs(game)
        for i in range(5):
            if  data[i]==False:
                continue
            game.create_rectangle(w*i,self.h,w*(i+1),self.h-h,fill=clrs[cost[i]-1])
            game.create_text(w*i+w/3,self.h-h/4,text=name[i],fill='white')
            game.create_oval(w*i,self.h-3*h/4,w*i+10,self.h-3*h/4-10,fill=GUI.gold)
            game.create_text(w*i+15,self.h-3*h/4-10,text=str(cost[i]),fill='white')
            game.create_image(w*(i+1)-i_w/2,self.h-h+i_h/2,image=imgs[i])
    def init_make_champs(self,game,infos):
        for n,(k,info) in enumerate(infos.items()):
            k = str(list(k))
            xy = self.center[k]
            name = info[0]
            myopp = info[1]
            if myopp == 1:
                clr = GUI.blue
            else:
                clr = GUI.red
            img = tk.PhotoImage(file='./utils/icon/{}.gif'.format(name))
            print('./utils/icon/{}.gif'.format(name))
            self.photos[n] = img
            image_info = game.create_image(xy[1],xy[0],image=self.photos[n])
            self.arr.append([info[2],k,info[0],self.photos[n],image_info])
    def update_champs(self,game,infos):
        hexes = [i[1] for i in self.arr]
        who = [i[0] for i in self.arr]
        for k,info in infos.items():
            k = str(list(k))
            ind = who.index(info[2])
            if hexes[ind] != k:
                print('hi!')
                xy = self.center[k]
                kk =eval(k)
                hex = eval(hexes[ind])
                change = self.center[k]
                orig = self.center[hexes[ind]]
                dx,dy = change[1]-orig[1],change[0]-orig[0]
                print(dx,dy)
                #dx,dy = kk[0]-hex[0],kk[1]-hex[1]
                print(dx,dy)
                game.move(self.arr[ind][4],dx,dy)
                self.arr[ind][1] = k

    def _ready_champs(self,game):
        game.ch1 = None
        game.ch2 = None
        game.ch3 = None
        game.ch4 = None
        game.ch5 = None
        game.ch6 = None
        game.ch7 = None
        game.ch8 = None
        game.ch9 = None
        game.ch10 = None
        game.ch11 = None
        game.ch12 = None
        game.ch13 = None
        game.ch14 = None
        game.ch15 = None
        game.ch16 = None
        game.ch17 = None
        game.ch18 = None
        game.ch19 = None
        game.ch20 = None
        game.ch21 = None
        game.ch22 = None
        game.ch23 = None
        game.ch24 = None
        game.ch25 = None
        photos = [game.ch1,game.ch2,game.ch3,game.ch4,game.ch5,game.ch6,game.ch7,
            game.ch8,game.ch9,game.ch10,game.ch11,game.ch12,game.ch13,game.ch14,
            game.ch15,game.ch16,game.ch17,game.ch18,game.ch19,game.ch20,game.ch21,
            game.ch22,game.ch23,game.ch24,game.ch25]
        return photos
if __name__ == '__main__':
    GUI(60,70)
