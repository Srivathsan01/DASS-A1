import os,time
import sys
from colorama import Fore,Style,Back

class Coin:
    def __init__(self,x,y):
        self.value = Back.LIGHTYELLOW_EX + Fore.GREEN + '$'
        self.__x = x
        self.__y = y
        self.__picked = 0
    
    def retpos(self):                                               # Returns positions
        return [self.__x,self.__y]
    def retstat(self):
        return self.__picked
    
    def mark(self):
        # print("Collected")
        self.__picked = 1

class Bullet:
    
    def __init__(self , x , y):
        self._posx = x
        self._posy = y
        self.__Speed = 2
    
    def clearbullet(self, Gboard):
        try:
            Gboard.putobject(self._posy,self._posx,' ')
            # print("Clearing for ",self._posy,self._posx)
        except:
            print("Eror clearing")
    def retposx(self):
        return self._posx
    
    def place_bullet(self,Gboard , x , y):
        # print("Initialcoord",x,y)
        Gboard.putobject(y , x , Fore.BLUE + Back.LIGHTBLACK_EX + '►')
    
    def move_bullet(self,Gboard):
        Gboard.putobject(self._posy,self._posx , Fore.BLUE  + Back.LIGHTBLACK_EX + '►')
    
    def update_bullet_pos(self,Gboard):
        self._posx = self._posx + 2
    
    def bulletcollision(self,Gboard,Drag):
        # print("met this guy",Gboard.getvalue(self._posy,self._posx) )
        
        ############ DRAGON COLLISION ###############
        dragar = Gboard.retdragar()
        
        if( [self._posx, self._posy] in dragar):
            # print("Bullet hit")
            # print([self._posx, self._posy])                                       # Checking if bullet position belongs to dragon coordinataes
            # print(dragar.index([self._posx,self._posy]))
            Drag.Deductlife(Gboard)
            return 1                    
        
        ############ MAGNET COLLISION ###################
        
        magarray = Gboard.retmagar()
        if([self._posx,self._posy] in magarray):                                        # Check if coordinates of bullet is part of magnet
            # print("BULLET COLLIDED")
            return 1
            
        ############ COIN COLLISION #####################
        carray = Gboard.coins()
        for c in carray:
            if( [self._posx, self._posy] == c.retpos() and c.retpos()[0]!= Gboard.retcol() - 1):  # Check if coordinates of bullet matches with coin
                self.update_bullet_pos(Gboard)
        
        ############ BEAM COLLISION #####################
        beamarray = Gboard.beamcoords()
        tempbeam = Beam(0,0)
        
        # print(beamarray)
        righton = 0
        if( Gboard.getvalue(self._posy, self._posx) == tempbeam.retval() ):
            righton = 1            
        if( self._posx < Gboard.retcol()-1):
            if(Gboard.getvalue(self._posy,self._posx+1) == tempbeam.retval() and Gboard.getvalue(self._posy,self._posx) != tempbeam.retval()):
                righton = 2
        if(righton == 1):
            # print("Collision has taken place")
            for x in range(-2,4):  #HORIZONTAL
                if([self._posy,self._posx+x] in beamarray):
                    # try:
                    # print("Removing the beam by bullet")
                    Gboard.putobject(self._posy , self._posx+x , ' ')
                    # except:
                        # print("Didnt remove horizontal")
                    Gboard.beamcoords().remove([self._posy,self._posx+x])

            for y in range(-4,4):  #VERTICAL
                if([self._posy+y,self._posx] in beamarray):
                    try:
                        # print("Removing the beam by bullet")
                        Gboard.putobject(self._posy+y , self._posx , ' ')
                    except:
                        print("Didnt remove vertical")
                    Gboard.beamcoords().remove([self._posy+y,self._posx])
            for t in range(-4,4):  #DIAGONAL
                if([self._posy +t ,self._posx+t] in beamarray):
                    try:
                        # print("Removing the beam by bullet")
                        Gboard.putobject(self._posy+t , self._posx + t , ' ')
                    except:
                        print("Didnt remove diagonal")
                    Gboard.beamcoords().remove([self._posy + t,self._posx + t])
            
        elif(righton == 2):
            # print("Collision Imminent")
            for x in range(-1,4):  #HORIZONTAL
                if([self._posy,self._posx+1+x] in beamarray):
                    # try:
                    # print("Removing the beam by bullet")
                    Gboard.putobject(self._posy , self._posx+1+x , ' ')
                    # except:
                        # print("Didnt remove horizontal")
                    Gboard.beamcoords().remove([self._posy,self._posx+1+x])
            for y in range(-4,4):  #VERTICAL
                if([self._posy+y,self._posx+1] in beamarray):
                    try:
                        # print("Removing the beam by bullet")
                        Gboard.putobject(self._posy+y , self._posx+1 , ' ')
                    except:
                        print("Didnt remove vertical")
                    Gboard.beamcoords().remove([self._posy+y,self._posx+1])
            for t in range(-4,4):  #DIAGONAL
                if([self._posy +t ,self._posx+1+t] in beamarray):
                    try:
                        # print("Removing the beam by bullet")
                        Gboard.putobject(self._posy+t , self._posx +1 + t , ' ')
                    except:
                        print("Didnt remove diagonal")
                    Gboard.beamcoords().remove([self._posy + t,self._posx + 1 + t])
        
        if(righton == 1 or righton == 2):
            return 1
        else:
            return 0            
            
class Beam:
    def __init__(self,x,y):
        self.__beamsize = 4
        self.__xco = x
        self.__yco = y
        self.__value = Fore.RED + Back.WHITE + '#'

    def getbeamsize(self):
        return self.__beamsize
    
    def retval(self):
        return self.__value
     
    def fillbeam(self):
        for i in range(self.__beamsize):
            self.__beam.append(Fore.RED + Back.WHITE +  '#')
            
    def retbeampos(self):
        return [self.__xco,self.__yco]
    
    
    
class Magnet:
    def __init__(self,x,y):
        self.__posx = x
        self.__posy = y
        self.__sizex = 4
        self.__sizey = 3
        self.__mag = []
        self.construct_magnet()
        
    def place_magnet(self,px,py,Gboard):
        for x in range(self.__sizey):
            for y in range(self.__sizex):
                Gboard.putobject(py+x ,px+y , self.__mag[x][y])
    
    def construct_magnet(self):
        redpiece =   Fore.RED + '█'
        whitepiece =  Fore.WHITE + '█'
        for x in range(self.__sizey):
            t = []
            for y in range(self.__sizex):
                if x == 0:
                    t.append(redpiece)
                elif(x <= 1):
                    if(y == 0 or y == 3):
                        t.append(redpiece)
                    else:
                        t.append(' ')
                else:
                    if( y == 0 or y == 3):
                        t.append(whitepiece)
                    else:
                        t.append(' ')
            self.__mag.append(t)
        # print(self.__mag)
    
    def attract_character(self , Jedi,Gboard):
        if(Jedi.retx() > self.__posx):
            if( Jedi.retx() - self.__posx <= 8 and Jedi.retx() - self.__posx >=0 ):
                if(Jedi.Collision_left(Jedi.retx()-2,Gboard.retcol()) == False):
                        # print("Attracted left with current pos",Jedi.retx(),self.__posx)
                        Jedi.updx(-2)
                
        else:
            if( self.__posx - Jedi.retx() <= 8 and self.__posx - Jedi.retx()>=0  ):
                if(Jedi.Collision_right(Jedi.retx()+2,Gboard.retcol()) == False):
                    Jedi.updx(2)
                # print("Attracted right with current pos",Jedi.retx(),self.__posx)
            
        
        
# a = Magnet(20,30)
# a.construct_magnet()