import os
import numpy as np
from colorama import Style,Fore,Back
import random
from math import floor
import time
from entities import Coin,Beam
from entities import Magnet
class GameBoard:

    def __init__(self, rows, columns, gamestart,framewidth,windowstart):
        self.__rows = rows
        self.__columns = columns
        self.__framewidth = framewidth
        self.__board = []
        self.__gamestarttime = gamestart
        self.__windowstart = windowstart
        self.__Scrollspeed = 1
        self.__scrollflag = 0
        self.__totalcoins = 50
        self.__coins =[]
        self.__beamcoord = []
        self.__totalbeams = int(self.__columns / 25)
        self.__bullets = 0
        self.__bulletarray = []
        self.__dragonpos = []
        self.__gravity = 0
        self.__gravitytime = 0
        self.__magnetelements = []
        self.__dragonbullets = []
    
    def updscrf(self):
        self.__scrollflag = 1
    
    def retdragbul(self):
        return self.__dragonbullets
        
    def retbular(self):
        return self.__bulletarray
    
    def retmagar(self):
        return self.__magnetelements
    
    def retdragar(self):
        return self.__dragonpos
    
    def retwidth(self):
        return self.__framewidth
    
    def getgravity(self):
        # print("Current gravity",self.__gravity)
        return self.__gravity
    
    def retwinstart(self):
        return self.__windowstart
    
    def retscrf(self):
        return self.__scrollflag
    
    def coins(self):
        return self.__coins
    
    def updatescrollspeed(self,val):
        self.__Scrollspeed = val
    
    def setbular(self,Shot):
        self.__bulletarray.append(Shot)    
    
    def setdragbular(self,Iceball):
        self.__dragonbullets.append(Iceball) 
        
    def removecoin(self,ob):
        self.__coins.remove(ob)
    
    def resetgravity(self):
        # print("Reset Gravity")
        self.__gravity = 0
    def update_gravity(self):
        self.__gravity  = self.__gravity + 1    
        # print("Gravity now ",self.__gravity)
    
    def incbullet(self):
        self.__bullets = self.__bullets + 1
    
    def beamcoords(self):
        return self.__beamcoord
    
    def place_coins(self):
        for coin in range(self.__totalcoins):
            y = random.randint(2,self.retrow() - 3)
            x = random.randint(2,self.retcol() - 3)
            c = Coin(x,y)
            self.__coins.append(c)
            coinchar  = Fore.YELLOW + c.value                               # Method to place coins randomly on the board
            self.putobject(y,x,coinchar) 
            
    def createdragon(self,Drago):
        dx = Drago.retxco()
        dy = Drago.retyco()
        # dsx = Drago.retsx()
        # dsy = Drago.retsy()                                               # Creates Boss Dragon and places it in the chamber
        # print("CREATING DRAGON")
        for i in range(4):
            for j in range(30):
                self.__dragonpos.append([dx+j,dy+i])
        # print(self.__dragonpos)
        Drago.placedragon(dx,dy,self)
        
    
    def updragarray(self,draggy):
        self.__dragonpos.clear()
        # print("PRINTING DRAGPOS" ,self.__dragonpos)
        dx = draggy.retxco()
        dy = draggy.retyco()                                                 #Updates the current position array of the boss dragon
        # dsx = draggy.retsx()
        # dsy = draggy.retsy()
        if(draggy.retlife()<=0):
            self.__dragonpos.clear()
            return
        for x in range(4):
            for y in range(30):
                self.__dragonpos.append([dx+y,dy+x])
        # print("PRINTING DRAGPOS AFTER FILLINg " ,self.__dragonpos)
    
    def play_board(self):

        boardmatrix = []
        charac =  ' '
        for r in range(self.__rows):
            self.newrow = []
            for c in range(self.__columns):
                self.newrow.append(charac)
            boardmatrix.append(self.newrow)
        self.__board = np.array(boardmatrix, dtype=object)
        # self.__board = boardmatrix
    
    def retcol(self):
        return self.__columns
    
    def retrow(self):
        return self.__rows
    
    def getvalue(self,i,j):
        return self.__board[i][j]
    
    def retcol(self):
        return self.__columns
    
    def putobject(self, xcoord, ycoord, charac):
        try:
            self.__board[xcoord][ycoord] = charac
        except:
            print("Error Placing on ",xcoord,ycoord)
        #     print("Value",self)
        
    def scroll(self,Hero,Drag):
        if(self.__scrollflag == 0):
            self.__windowstart = self.__windowstart +self.__Scrollspeed                 # Scrolls the window frame of given width
        if(self.__windowstart == Hero.retx()):
                Hero.Board_update(self,'d',Drag)
                Hero.moveMandolorian(self,'d')
            
    def display_board(self, Hero,Drag):                                                 # Display the entire gameboard
            cl = Hero.coinslives()
            TimeRemain = 120-floor(time.time()-self.__gamestarttime)
            print(Fore.BLUE + Back.BLACK + "Score      " ,10*cl[0],"                 ",Back.LIGHTYELLOW_EX + "                                           ",Fore.GREEN + Back.BLACK +" TIME REMAINING   ",TimeRemain)
            # print(Fore.RED + Back.LIGHTYELLOW_EX + "Mandolorian Lives      ",cl[1],Back.LIGHTCYAN_EX + "                              ",Back.LIGHTRED_EX + Fore.GREEN + "BOSS LIFE","   ",Drag.retlife())
            print(Fore.LIGHTMAGENTA_EX + Back.BLACK + "Mandolorian Lives : ",end ='')
            for lives in range(cl[1]):
                print(Fore.RED + '❤',end='')
            print(Back.BLACK + " ",Back.LIGHTYELLOW_EX+"                                           ",Fore.RED + Back.BLACK+"       BOSS LIFE:  ",Drag.retlife())
                            
            for rowno in range(self.__rows):
                for colno in range(self.__windowstart , self.__windowstart + self.__framewidth):
                    if( colno < self.__columns):
                        if(self.__board[rowno][colno] == ' ' and rowno >= 2 and rowno <= self.__columns-3):
                            print(Back.LIGHTBLACK_EX + self.__board[rowno][colno],end='')
                        else:
                            print(self.__board[rowno][colno], end='')
                        print(Style.RESET_ALL, end='')
                print()

    def create_magnet(self):
        properlyplaced = 1
        while(properlyplaced == 1):
            posx = random.randint(30,self.retcol() - 100)
            posy = random.randint(2,self.retrow() - 8)
            for i in range(3):
                for j in range(3):
                    if(self.getvalue(posy,posx) != ' '):
                        properlyplaced = 0
                        break
                if(properlyplaced == 0):
                    break
        M = Magnet(posx,posy)
        self.__MAGNET = M
        for xiter in range(5):
            for yiter in range(4):
                self.__magnetelements.append([posx + xiter, posy+yiter])
                
        M.place_magnet(posx,posy,self)
        
    def usemagnet(self,Jedi):
        self.__MAGNET.attract_character(Jedi,self)

    def create_beams(self):
        temp = Beam(0,0)
        beamsize = temp.getbeamsize()
        # beam = []
        # for i in range(beamsize):
        #     beam.append(Fore.RED +  '#')

        for beamno in range(self.__totalbeams):
            
            
            
            alignment = random.randint(0,2)
            if alignment == 0:                  #Horizontal
                alreadypresent = 1
                while(alreadypresent == 1):
                    ct=0
                    bx = random.randint(2,self.retcol() - 8)
                    by = random.randint(2,self.retrow() - 8)                                    #Randomly chosing type of beam (Horizontal,Vertical,Slant) and placing them in random position
                    for temp in range(beamsize):
                        if(self.getvalue(by,bx+temp) == ' '):
                            ct=ct+1
                    if(ct == 4):
                        alreadypresent = 0
                    
                for x in range(beamsize):
                    if(bx +x <= self.retcol()):
                        B = Beam(by ,bx+x)
                        self.__beamcoord.append( B.retbeampos() )
                        self.putobject(by,bx+x,B.retval())
                        
            elif alignment == 1:                #Vertical
                alreadypresent = 1
                while(alreadypresent == 1):                                                     # If a beam element is already present find a newer position to place the whole beam
                    ct=0
                    bx = random.randint(2,self.retcol() - 8)
                    by = random.randint(2,self.retrow() - 8)
                    for temp in range(beamsize):
                        if(self.getvalue(by+temp,bx) == ' '):
                            ct=ct+1
                    if(ct == 4):
                        alreadypresent = 0
                for y in range(beamsize):
                    if(by + y <= self.retrow()):
                        B = Beam(by+y,bx)
                        self.__beamcoord.append( B.retbeampos())
                        self.putobject(by + y, bx, B.retval())
           
            elif alignment == 2:                # Right Slant
                alreadypresent = 1
                while(alreadypresent == 1):
                    ct=0
                    bx = random.randint(2,self.retcol() - 8)
                    by = random.randint(2,self.retrow() - 8)
                    for temp in range(beamsize):
                        if(self.getvalue(by+temp,bx+temp) == ' '):
                            ct=ct+1
                    if(ct == 4):
                        alreadypresent = 0
                for y in range(beamsize):
                    if(by + y <= self.retrow() and bx + y <=self.retcol() ):
                        B = Beam(by+y,bx+y)
                        self.__beamcoord.append( B.retbeampos() )
                        self.putobject(by + y, bx + y , B.retval())

