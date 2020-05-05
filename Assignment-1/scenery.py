import os
import time
from colorama import Back, Fore, Style
import gameboard


class Scenery:
    def __init__(self):
        self.__ground = 'W'
    def create_sky(self,scene):
        for col in range(scene.retcol()):
            cloud = Fore.BLUE + '⬤'
            for column in range(scene.retcol()):
                scene.putobject(0,col,cloud)                        # Top 2 rows is made up of the sky
                scene.putobject(1,col,cloud)
                
    def create_ground(self, scene):
        gob = Fore.GREEN + self.__ground
        gobject = Back.LIGHTWHITE_EX + gob
        for col in range(scene.retcol()):                               # Bottom two rows is Grassland
            scene.putobject(scene.retrow() -2, col, gobject)
            scene.putobject(scene.retrow() -1, col, gobject)
