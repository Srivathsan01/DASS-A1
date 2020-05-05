import sys
import os,time
from colorama import Fore,Back,Style


class Bullet:
    
    def __init__(self , x , y):
        self.__posx = x
        self.__posy = y
        self.__Speed = 2
    
    def clear(self, Gboard):
        try:
            Gboard.putobject(self.__posy,self.__posx,' ')
            # print("Clearing for ",self.__posy,self.__posx)
        except:
            print("Eror clearing")
    
    def place_bullet(self,Gboard , x , y):
        # print("Initialcoord",x,y)
        Gboard.putobject(y , x , Fore.BLUE + '►')
    
    # def coincollision(self,Gboard):
        
        
    # def beamcollision(self,Gboard):
        
        
    def move_bullet(self,Gboard):
        
        Gboard.putobject(self.__posx,self.__posy , Fore.BLUE + '►')
    
    def update_bullet_pos(self,Gboard):
        self.__posx = self.__posx  + 1