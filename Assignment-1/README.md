
DOCUMENTATION By:
    B.SRIVATHSAN
    2018101049

                **********************************    DASS ASSIGNMENT 1 ************************************

TASK:
    The assignment is to replicate/create a variant of Jetpack Joyride game in the Linux Terminal

RUNNING THE GAME:

    Run the joyride.py file in python3 to launch the game in the Linux Terminal

REQUIREMENTS:
    Libraries of termcolor , coloroma installed in python3

GAMEPLAY:
    
    1.The task of this game is to save the cutest alien ever,BABY YODA.You have to kill the boss dragon in order to save him
    2.You will be playing as The Mandalorian.You have a sword to smash the enemies.
    3.The game has a lot of Obstacles and Scorables.
    4.The obstacles include
        (i)  A running timer : The clock is ticking fast.You need to kill the boss and exit out of the chamber before the timer runs out.
       (ii)  Lazer Beams : If you hit the lazer beams your life will get reduced.
      (iii)  Borders: You can't exit out of the chamber until you defeat the Boss Dragon. You cant go beyond the sky and beneath the ground.Also the                        entire chamber will be scrolling and moving back with a velocity.You will eventually have to face the dragon as you wouldn't be                     able to go beside the windowframe :P
       (iv) A Magnet which will always pull you towards itself and won't let you escape

    5.The POWER UPS include:
        (i) A speed boost which can be used.It increases the speed of Mandolorian as well as the scrolling speed of the Chamber
       (ii) A shield which can be used to protect yourself against Lazer Beams and Magnet. However the shield can't protect you from Dragon's Snow Balls.
    6.You can shoot Bullets to destroy lazer beams and attack boss dragon.Bullets won't destroy magnets.The dragon also shoots Snow Balls
    7.You can collect coins.Each coin will give you a score of 10.
    8.You start with 10 lives and once you meet the boss , you have to kill the Boss Dragon which has 40 lives
    9. Wait for 10 seconds for the shield to get recharged

CONTROLS:
        _______________________________________
        |      Movement       |       Key      |
        |---------------------|----------------|
        |   Move left  	      |        a       |
        |   Move right 	      |        d       |
        |   Use JETPACK       |        w       |
        |   Fire Bullet       |        b       |
        |   USE Shield        |     Spacebar   |
        |   USE Speedboost    |        p       |
        |_____________________|________________|

FEATURES and OOPS CONCEPTS :
    Inheritance:
        Class StarWars is the parent class of all characters in the game
        Dragon and Mandalorian inherit from it
    Abstraction:
        All the variables are declared as private or protected.The data attributes are only accessible by member functions
        Getter and Setter functions are included for each class to manipulate data members
    Encapsulation:
        Every entity is declared as a class.Class being a collection of items of different data types makes it easy.
    
    Polymorphism:
        The class DragonBullets inherits from the class Bullet.METHOD OVERRIDING is done here.
        The methods placebullet() , update_bullet_pos() and bulletcollision() are completely overwritten facilitating Method Overriding and hence Polymorphism


ASSUMPTIONS:
    1.Once you hit a magnet your life gets reduced
    2.Getting near the dragon does not affect the dragon.Only bullets can kill dragon
    3.When a bullet collides with a coin, it passes through it and appears on the other side of it
    4.Dragon shoots a snowball every 3 seconds
    5. Once you kill the boss, game starts flickering a bit before you reach the end