import os
import colorama
import time
import sys
import signal
from scenery import Scenery
from entities import Magnet
from gameboard import GameBoard
from getkey import Get, input_to
from characters import StarWars, Mandalorian,DragonBullet,Dragon
from math import floor
# from enemy import Dragon
from termcolor import cprint
import pyfiglet

def displaygameover():
    os.system('clear')
    for x in range(7):
        print()
    if(timeup == 1):                                                            # If time up 
        cprint(pyfiglet.figlet_format("TIME ' S UP (-_-)") , 'blue', 'on_white', attrs = ['bold'])
        tempstr = "GAME OVER"
        cprint(pyfiglet.figlet_format(tempstr) , 'red', 'on_yellow', attrs = ['bold'])
    if(timeup == 0):                                                                                    # WIN GAME
        cprint(pyfiglet.figlet_format("YOU SAVED BABY YODA") , 'red', 'on_white', attrs = ['bold'])
        
    str2 = "YOUR SCORE IS  "                                                                #PRINTING SCORE
    str1 = str2
    cprint(pyfiglet.figlet_format(str1) , 'blue', 'on_green',attrs=['bold'])
    cprint(pyfiglet.figlet_format(str(Hero.retscore())) , 'white','on_red',attrs=['bold'] )
    for x in range(7):
        print()
    sys.exit(0)
        
def gameover(Gboard, Hero, Drago):
    if(Drago.retlife() <= 0):
        Drago.cleardragon(Gboard)
        while(Hero.retx() <= Gboard.retcol() - 6):
            scene.display_board(Hero, Drago)
            inp = input_to(Get())
            Hero.Board_update(scene, inp, Drago)
            if(inp == 'q'):
                exit()
            Hero.moveMandolorian(scene, inp)                                # After you kill the dragon , you have to reach rightmost end to save baby yoda
            Hero.check_lives()
        displaygameover()     


def signal_handler(signal, frame):                                           # SIGINT interrupt handler
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

print("Good Morning Gamer!")
print("Enter your name to play the Mandalorian")
name = input()                                                                 # Take name of the player

GameStartTime = time.time()                                                     #Initialise game start time
timeup = 0
scene = GameBoard(34, 200,GameStartTime, 100, 0)                                #Initialise Board
scene.play_board()
scene.place_coins()                                                             #Place coins on board
scene.create_magnet()                                                           #Place magnet on board
scene.create_beams()                                                            #Create lazer beams  on board

ground = Scenery()
ground.create_sky(scene)                                                        #Creating Sky and Ground
ground.create_ground(scene)

Hero = Mandalorian(3, 3, 3, scene.retrow() - 5, name,"Hero")                       #Creating and Placing Mando in the chamber
Hero.placeHero(3, scene.retrow() - 5,scene)
Drago = Dragon("Shindu", scene.retcol()-34,scene.retrow() - 16)                 # Creating Boss Dragon

scene.createdragon(Drago)
while(True):
    os.system('clear')
    
    if(floor(time.time() - GameStartTime) >= 120):
        timeup = 1                                                              #Timer run out
        displaygameover()
        
    if(scene.retwinstart() <= scene.retcol() - 100):
        scene.scroll(Hero, Drago)                                                #Scrolling till you meet Boss Dragon
    else:
        scene.updscrf()
    if(scene.retwinstart() >= Hero.retx()):
        Hero.Board_update(scene, 'd',Drago)                                      # Automatically push Mando if he hits the lefmost part of the moving frame
        Hero.moveMandolorian(scene, 'd')
    game = Drago.checkbosslife()
    if(game == 1):
        gameover(scene, Hero,Drago)
    scene.display_board(Hero, Drago)
    inp = input_to(Get())                                                        # Getting keyboard input
    Hero.Board_update(scene, inp,Drago)
    if(inp == 'q'):
        exit()
    Hero.moveMandolorian(scene, inp)
    Hero.check_lives()
