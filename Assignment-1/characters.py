import os
import time
import sys
import numpy
import pyfiglet
from math import floor
from colorama import Fore, Back, Style
from termcolor import cprint
from entities import Bullet, Coin, Beam
# from enemy import Dragon,DragonBullet


class StarWars:                             #Class from which every character is derived
    def __init__(self, name, Type):
        self.__name = name
        self.__Type = Type

    def Collision_left(self, value, framew):
        # print("Checking for ",value, framew)
        if(value >= framew):                        #Checks for collision towards left
            return True
        else:
            return False

    def ground_collision(self, yvalue, Gboard):
        if(yvalue > Gboard.retrow()-5):                #Method for checking collision with ground
            # print("Gone BITCH")
            return True
        else:
            return False

    def Collision_right(self, value, rbound):
        if(value <= rbound-1):                         #Method for checking collision with the end
            return False
        else:
            return True

    def sky_collision(self, yvalue):
        if(yvalue < 2):                                 #Checking collision with sky
            return True
        else:
            return False


class Mandalorian(StarWars):

    def __init__(self, height, breadth, xco, yco, name, Type):
        super().__init__(name, Type)
        self.__Score = 0
        self.__coins = 0
        self.__body = [["[", "(", "/"], ["]", ")", "\\"], ["*", "/", " "]]
        self.__height = height
        self.__breadth = breadth
        self.__xco = xco
        self.__yco = yco
        self.__speed = 3
        self.__Lives = 10
        self.__startshield = 0
        self.__rechargeshield = 0                               #Constructor for Mandalorian
        self.__shieldused = 0
        self.__usedonce = 0

    def retlives(self):
        return self.__Lives

    def deductlife(self):
        # print("Deducted life")
        if(self.__shieldused == 0):
            self.__Lives = self.__Lives - 1

    def retheight(self):
        return self.__height

    def retx(self):
        return self.__xco

    def rety(self):
        return self.__yco

    def coinslives(self):                                                   #Returns coins lives
        return [self.__coins, self.retlives()]

    def retscore(self):
        cl = self.coinslives()
        return 10*cl[0]

    def updx(self, val):                                                    #Updates x coordinate of Mando
        self.__xco = self.__xco + val

    def updy(self, val):                                                    #Updates x coordinate of Mando
        self.__yco = self.__yco + val

    def use_sheild(self):
        if(self.__usedonce == 0):
            self.__shieldused = 1
            self.__usedonce = self.__usedonce + 8
        # else:
        #     if(floor(time.time())  - floor(self.__startshield) >= 10):
        #      self.__shieldused = 1

    def checkshield(self):
        curtime = floor(time.time())
        if(curtime - self.__startshield >= 6):
            self.__shieldused = 0

    def collectcoin(self, Gboard):
        carray = Gboard.coins()
        for x in range(self.retheight()):
            for y in range(self.retheight()):
                for c in carray:
                    if([self.__xco+x, self.__yco + y] == c.retpos() and c.retstat() == 0):
                        #     Gboard.coincoords().remove([self.__yco+y,self.__xco+x])
                        self.__coins = self.__coins + 1
                        c.mark()
                        Gboard.removecoin(c)

    def clear(self, Gboard):
        for x in range(3):
            for y in range(3):                                                      #Clears the space occupied by Mando on the board
                Gboard.putobject(self.__yco+y, self.__xco+x, " ")
        # print("Board cleared")
        # for x in range(3):
        #     for y in range(3):
        #         r = Gboard.getvalue(self.__xco+x,self.__yco+y)
        #         if(r==' '):
        #             print("Empty space")

    def placeHero(self, xcoordinate, ycoordinate, Gboard):
        for x in range(3):
            for y in range(3):
                # print( str(ycoordinate+y) + " " + str(xcoordinate + x))           # Used to place Mando initially on the gameboard
                if(self.__shieldused == 0):
                    Gboard.putobject(ycoordinate+y, xcoordinate+x,
                                     Fore.BLACK + Back.LIGHTBLACK_EX + self.__body[x][y])
                elif(self.__shieldused == 1):
                    Gboard.putobject(
                        ycoordinate+y, xcoordinate+x, Back.LIGHTWHITE_EX + Fore.BLACK + self.__body[x][y])

    def moveMandolorian(self, Gboard, direction):
            # print("Initial coordinates")
            # print(self.__xco , self.__yco)
        self.placeHero(self.__xco, self.__yco, Gboard)

    def Shoot_bullet(self, Gboard):
        Shot = Bullet(self.__xco + 4, self.__yco + 1)
        Gboard.setbular(Shot)
        # print(Gboard.retbular())
        Shot.place_bullet(Gboard, self.__xco + 4, self.__yco + 1)

    def check_lives(self):
        if(self.__Lives <= 0):
            os.system('clear')
            for x in range(7):
                print()
            tempstr = "GAME OVER"
            cprint(pyfiglet.figlet_format(tempstr),
                   'red', 'on_yellow', attrs=['bold'])
            str2 = "YOUR SCORE IS  "
            str1 = str2
            cprint(pyfiglet.figlet_format(str1),
                   'cyan', 'on_green', attrs=['bold'])
            cprint(pyfiglet.figlet_format(str(self.retscore())),
                   'white', 'on_red', attrs=['bold'])
            for x in range(7):
                print()
            sys.exit(0)

    def Speed_Boost(self, Gboard):
        Gboard.updatescrollspeed(2)
        self.__speed = self.__speed + 2

    def Board_update(self, Gboard, direction, Drag):

        self.clear(Gboard)
        Gboard.usemagnet(self)
        self.magnet_collision(Gboard)                       #Checking all collisions of Mando
        self.collectcoin(Gboard)
        self.beam_collision(Gboard)
        
        if(Drag.retlife() >= 1):
            Drag.positionupdate(self.__yco, Gboard)
        if(Drag.retlife() <= 0):
            Gboard.updragarray(Drag)                        #If dragon is dead no more bullets
            for dbul in Gboard.retdragbul():
                dbul.clearbullet(Gboard)
            Gboard.retdragbul().clear()
        
        self.checkshield()                                                                 #This Board_update updates coordinataes of all the entities ,Mando and the dragon.Correspondingly
        # Bullet.update_bullet_pos(Gboard)                                                 # changes are made and next movement is done
        # Bullet.move_bullet(Gboard)
        for bno in Gboard.retbular():
            bno.clearbullet(Gboard)
            bno.update_bullet_pos(Gboard)
            if(bno.retposx() < Gboard.retcol()):
                # print("Current x",bno.retposx())
                beamhit = bno.bulletcollision(Gboard, Drag)
                if(beamhit == 1):
                    Gboard.retbular().remove(bno)
                else:                                                                   #Updaing positions of all bullets and checkind collisions of bullets
                    bno.move_bullet(Gboard)
            else:
                bno.clearbullet(Gboard)
                Gboard.retbular().remove(bno)

        if(Gboard.retscrf() == 1 and Drag.retlife() >=1):
            if(Drag.retfirstshot == 0):
                IceBall = DragonBullet(Drag.retxco()-2, Drag.retyco())
                Gboard.setdragbular(IceBall)
                IceBall.place_bullet(Gboard, Drag.retxco() - 2, Drag.retyco())
                Drag.incfir()                                                            #Updating positions of all dragon snow balls and checking timer to shoot another snow ball
                Drag.incshottime(time.time())

            else:
                if(floor(time.time() - Drag.retshottime()) >= 2):
                    IceBall = DragonBullet(Drag.retxco()-2, Drag.retyco())
                    Gboard.setdragbular(IceBall)
                    IceBall.place_bullet(
                        Gboard, Drag.retxco() - 2, Drag.retyco())
                    Drag.incshottime(time.time())

            for dbul in Gboard.retdragbul():
                dbul.clearbullet(Gboard)
                dbul.update_bullet_pos(Gboard)
                if(dbul.retposx() >= Gboard.retwinstart()):
                    manhit = dbul.bulletcollision(Gboard, self)
                    if(manhit == 1):
                        self.__Lives = self.__Lives - 2
                        Gboard.retdragbul().remove(dbul)
                    else:
                        dbul.move_bullet(Gboard)
                else:
                    dbul.clearbullet(Gboard)
                    Gboard.retdragbul().remove(dbul)

        if direction is None:
            # print("Direction NONE")
            if(self.ground_collision(self.__yco+Gboard.getgravity() , Gboard) == True):
                self.clear(Gboard)
                self.__yco = Gboard.retrow() - 5
                self.moveMandolorian(Gboard,' ')                                                    #If no key is pressed , Gravity simply works
                Gboard.resetgravity()
            else:
                self.__yco = self.__yco + Gboard.getgravity()
                # print("Calling update since direction none")
                Gboard.update_gravity()
                
        if(direction is not None):
            if(direction != 'w'):                                                               
                Gboard.update_gravity()                                                             #Gravity effect
                if(self.ground_collision(self.__yco + Gboard.getgravity(), Gboard) == False):
                    self.__yco = self.__yco + Gboard.getgravity()                    
                else:
                    self.clear(Gboard)
                    self.__yco = Gboard.retrow() - 5
                    Gboard.resetgravity()
                    
            
            if(direction == 'd'):
                if(self.Collision_right(self.__xco+self.__speed + 2, Gboard.retcol()) == False):            #Move right
                    self.__xco = self.__xco+self.__speed

            if(direction == 'a'):
                if(self.Collision_left(self.__xco-5, Gboard.retwinstart()) == True):                        #Move Left
                    self.__xco = self.__xco-3

            if(direction == ' '):
                if(self.__usedonce == 0):
                    self.__startshield = floor(time.time())                                                 #Activate Shield
                    self.use_sheild()
                else:
                    if(floor(time.time() - self.__startshield) >= 10):
                        self.__startshield = floor(time.time())
                        self.__shieldused = 1

            if(direction == 'b'):
                # Gboard.__bullets = Gboard.__bullets + 1                                               #Shoot bullet
                Gboard.incbullet()
                self.Shoot_bullet(Gboard)
            if(direction == 'p'):                                                                       # Use Speed booster
                self.Speed_Boost(Gboard)

            if(direction == 'w'):                                                               
                if(self.sky_collision(self.__yco-2) == False):                                          # Use jetpack to thrust upwards
                    self.__yco = self.__yco-2
                Gboard.resetgravity()

        self.magnet_collision(Gboard)

    def beam_collision(self, Gboard):
        beamarray = Gboard.beamcoords()
        # print(beamarray)
        for x in range(self.retheight()):
            for y in range(self.retheight()):
                if([self.__yco+y, self.__xco + x] in beamarray):                                         #Function to check collision of mando with beam
                    self.deductlife()
                    Gboard.beamcoords().remove([self.__yco+y, self.__xco+x])
                    # print("Within match",beamarray)
                    for iter in range(4):  # Vertical beam removal
                        if([self.__yco+y+iter, self.__xco + x] in beamarray):                       # Once Mando hits a part of Lazer Beam , entire vertical beam is being removed
                            try:
                                Gboard.putobject(
                                    self.__yco+y+iter, self.__xco+x, ' ')
                            except:
                                print("didnt remove vertical")
                            Gboard.beamcoords().remove(
                                [self.__yco+y+iter, self.__xco+x])
                        if([self.__yco+y-iter, self.__xco + x] in beamarray):
                            try:
                                Gboard.putobject(
                                    self.__yco+y-iter, self.__xco+x, ' ')
                            except:
                                print("didnt remove vertical")
                            Gboard.beamcoords().remove(
                                [self.__yco+y-iter, self.__xco+x])

                    for iter in range(4):  # Horizontal beam removal
                        if([self.__yco+y, self.__xco + x + iter] in beamarray):
                            try:
                                Gboard.putobject(
                                    self.__yco+y, self.__xco+x + iter, ' ')
                            except:
                                print("didnt remove horizontal")
                            Gboard.beamcoords().remove(
                                [self.__yco+y, self.__xco+x + iter])
                        if([self.__yco+y, self.__xco + x - iter] in beamarray):
                            try:
                                Gboard.putobject(
                                    self.__yco+y, self.__xco+x - iter, ' ')
                            except:
                                print("didnt remove horizontal")
                            Gboard.beamcoords().remove(
                                [self.__yco+y, self.__xco+x - iter])

                    for iter in range(4):  # Diagonal beam removal
                        if([self.__yco+y+iter, self.__xco + x+iter] in beamarray):
                            try:
                                Gboard.putobject(
                                    self.__yco + y + iter, self.__xco+x+iter, ' ')
                            except:
                                print("didnt remove diagonal1")
                            Gboard.beamcoords().remove(
                                [self.__yco + y + iter, self.__xco + x + iter])

                        if([self.__yco+y-iter, self.__xco + x-iter] in beamarray):
                            try:
                                Gboard.putobject(
                                    self.__yco + y - iter, self.__xco+x-iter, ' ')
                            except:
                                print("didnt remove diagonal2")

                            Gboard.beamcoords().remove(
                                [self.__yco + y - iter, self.__xco + x - iter])

    def magnet_collision(self, Gboard):
        magarray = Gboard.retmagar()
        for xc in range(self.retheight()):              
            for yc in range(self.retheight()):                                                  #Method to check magnet collision.If Mando hits magnet life is reduced
                if([self.retx() + xc, self.rety() + yc] in magarray):
                    self.deductlife()
                    return


class Dragon(StarWars):
                                                                                                # BOSS DRAGON
    def __init__(self, name, x, y):
        StarWars.__init__(self, name, "ENEMY")
        # super().__init__(name,"ENEMY")
        self.__posx = x
        self.__posy = y
        self.__sizex = 30
        self.__sizey = 4
        self.__bosslives = 30
        self.__dragonbody = [
            [Back.BLACK+' ',Back.BLACK+ ' ', Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ', Fore.RED + Back.BLACK+',', Fore.RED + Back.BLACK+  '.', Back.BLACK+' ',Back.BLACK+ ' ',Back.BLACK+ ' ', Back.BLACK+' ',Back.BLACK+ ' ', Back.BLACK+' ',Back.BLACK+ ' ',
                Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ', Back.BLACK+' ',Back.BLACK+ ' ',Back.BLACK+ ' ',Back.BLACK+ ' '],
            [Back.BLACK+' ',Back.BLACK+ ' ', Fore.BLUE + Back.BLACK + '/', Fore.BLUE + Back.BLACK + ',', Fore.YELLOW + Back.BLACK +',',Fore.BLUE + Back.BLACK + ';',Fore.BLUE + Back.BLACK + '\'', Fore.BLUE + Back.BLACK +';',Fore.BLUE + Back.BLACK + ';',Fore.BLUE + Back.BLACK + '.', Back.BLACK+' ', Back.BLACK+' ', Fore.LIGHTGREEN_EX + Back.BLACK+',', Fore.BLUE + Back.BLACK +';', Fore.BLUE + Back.BLACK +';',
            Fore.YELLOW + Back.BLACK +';',Fore.RED + Back.BLACK + '.',Fore.MAGENTA + Back.BLACK + '.', Back.BLACK+' ',Back.BLACK+ ' ', Fore.MAGENTA + Back.BLACK + ',',Fore.MAGENTA + Back.BLACK + ',',Fore.BLUE + Back.BLACK + ';', Fore.YELLOW +Back.BLACK +'.',Fore.YELLOW +Back.BLACK +'.', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ', Fore.LIGHTGREEN_EX + Back.BLACK + '\'', Back.BLACK+' '],
            [Fore.RED + Back.BLACK + '.', Fore.RED + Back.BLACK + '\'', Fore.RED + Back.BLACK + ',', Fore.LIGHTBLUE_EX + Back.BLACK + '\'', Fore.LIGHTBLUE_EX + Back.BLACK + '\'', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ',Fore.LIGHTYELLOW_EX + Back.BLACK +  '`', Fore.LIGHTYELLOW_EX + Back.BLACK +':', Fore.LIGHTYELLOW_EX + Back.BLACK +':', Fore.LIGHTYELLOW_EX + Back.BLACK +';', Fore.RED+Back.BLACK +':', Fore.RED+Back.BLACK +'\'', Back.BLACK+' ',
            Fore.LIGHTGREEN_EX+Back.BLACK+'`', Fore.LIGHTGREEN_EX+Back.BLACK+'`', Fore.BLUE + Back.BLACK+';', Fore.BLUE + Back.BLACK+';', Fore.BLUE + Back.BLACK+';', Fore.LIGHTRED_EX + Back.BLACK+';', Fore.LIGHTRED_EX + Back.BLACK+'\'',Back.BLACK+ ' ', Back.BLACK+' ',Back.BLACK+ ' ', Fore.MAGENTA+Back.BLACK+'`',Fore.MAGENTA+Back.BLACK+ '.',Fore.MAGENTA+Back.BLACK+ '.', Fore.RED + Back.BLACK+'\'',Back.BLACK+ ' '],
            [Fore.YELLOW+Back.BLACK+'`', Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Back.BLACK+' ',Fore.BLACK+Back.BLACK+ ',', Fore.BLACK+Back.BLACK+ ',',Fore.MAGENTA+Back.BLACK+'/', Fore.WHITE+Back.BLACK+'\'', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ',
                Back.BLACK+' ', Fore.RED+Back.BLACK+',',Fore.RED+Back.BLACK+',', Fore.CYAN+Back.BLACK+'/', Fore.CYAN+Back.BLACK+'/',Back.BLACK+ ' ',Back.BLACK+ ' ', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ', Back.BLACK+' ',Back.BLACK+ ' ', Back.BLACK+' ',Back.BLACK+ ' ', Back.BLACK+' ']
        ]
        self.__invincible = 0
        self.__relaxtime = 2
        self.__shottime = 1
        self.__firstshot = 0

    def retlife(self):
        return self.__bosslives

    def incfir(self):                                                                       #Setting the flag
        self.__firstshot = self.__firstshot + 8

    def cleardragon(self, Gboard):
        for x in range(self.__sizey - 1):
            for y in range(self.__sizex - 1):
                Gboard.putobject(self.__posy + x, self.__posx + y, ' ')                      #Clears space occupied by dragon on gameboard

    def retrelax(self):
        return self.__relaxtime

    def retfirstshot(self):
        return self.__firstshot

    def retshottime(self):
        return self.__shottime

    def setinvincible(self, value):
        self.__invincible = value

    def checkbosslife(self):
        if(self.__bosslives <= 0):
            return 1

    def Deductlife(self, Gboard):
        if(Gboard.retscrf() == 0):
            return
        if(self.__invincible == 1):
            return
        else:
            self.__bosslives = self.__bosslives - 1

    def retsx(self):
        return self.__sizex

    def retsy(self):
        return self.__sizey

    def retxco(self):
        return self.__posx

    def retyco(self):
        return self.__posy

    def incshottime(self, curtime):
        self.__shottime = curtime                                                           #Update the shottime of the latest snow ball

    def placedragon(self, px, py, Gboard):
        for x in range(self.__sizey-1):
            for y in range(self.__sizex-1):
                Gboard.putobject(py+x, px+y, self.__dragonbody[x][y])
        # print("Dragon printed")

    def positionupdate(self, py, Gboard):
        self.cleardragon(Gboard)
        self.__posy = py
        Gboard.updragarray(self)                                                            #Updates position of the dragon
        self.placedragon(self.__posx, py, Gboard)


class DragonBullet(Bullet):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.__Speed = -3

    def place_bullet(self, Gboard, x, y):
        Gboard.putobject(y, x, Fore.WHITE + Back.LIGHTBLACK_EX + '◎')

    def update_bullet_pos(self, Gboard):
        self._posx = self._posx - 2
        # print("Updated")

    def move_bullet(self, Gboard):
        Gboard.putobject(self._posy, self._posx, Fore.WHITE + Back.LIGHTBLACK_EX  + '◎')

    
    ############# OVERRIDING COLLISION FUNCTIONS POLYMORPHISM ###################
    
    def bulletcollision(self, Gboard, Hero):
        Heropos = []
        for i in range(Hero.retheight()):
            for j in range(Hero.retheight()):
                Heropos.append([Hero.retx() + i, Hero.rety() + j])
        if([self._posx, self._posy] in Heropos):
            return 1
        else:
            return 0


