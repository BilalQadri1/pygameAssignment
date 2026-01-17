'''
-----------------------------------------------------------------------------
Program Name: F1 Racing Game
Program Description: A 2D f1 style racing game, with car selection, different tracks, tyre wear, pit stops, DRS, lap timing, and penalties.

-----------------------------------------------------------------------------
References:

(put a link to your reference here but also add a comment in the code below where you used the reference)
reference #1 to move forward in the direction the car is facing: https://stackoverflow.com/questions/64774900/how-to-get-velocity-x-and-y-from-angle-and-speed
-----------------------------------------------------------------------------

Additional Libraries/Extensions:

(put a list of required extensions so that the user knows that they need to download extra features)
pygame
math
os
time
gif_pygame
packaging
-----------------------------------------------------------------------------

Known bugs:

(put a list of known bugs here, if you have any)

----------------------------------------------------------------------------


Program Reflection:
I think this project deserves a level XXXXXX because ...

 Level 3 Requirements Met:
• The game uses user events (keyboard and/or mouse input from the user)
• All user input is sanitized (ie, won’t crash your program)
• The program must use a variable.
• Use appropriate data types (int, String, long).
• Use conditional structures (if-statement, boolean operators).
• Use loop structures (for, while).
• Create and use custom functions.
• Encapsulate the final program to include multiple screens with a menu system to move between them. (For example: an intro screen, main screen, and end screen).
• The program should have clear instructions on how to use/play.
• The program must have a soundtrack and sounds.
• The program uses images
• Coding decisions should make sense and not include grossly inefficient code.
• The program must have collision detection
• The program must have a custom downloaded font
• Frequent comments to help future readers understand code.
• Proper Indentation
• Use names that are descriptive and make sense when making variables, lists, methods etc….
• Names are as short as possible without losing descriptive meaning..
• Names use proper naming conventions such as CamelCase for Java or snake_case for Python and capitalized Object names etc…


Features Added Beyond Level 3 Requirements:
• The program has multiple tracks
• The program has a menu system
• The program has a pit stop feature
• The program has a DRS system
• The program has lap timing
• The program has penalties
• The program has tyre wear mechanics
• The program has car selection
• The program has a racing line toggle
• The program has a crash screen
• The program has a controller support toggle
• The program has animated tyre treads
• The program has a starting lights countdown
• The program has a minimap
• The program has animated fireworks on the main menu
• The program has yellow flag mechanics
• The program has different car max speeds and acceleration based on real life data
• The program has gear shifting mechanics that affect max speed
• The program has sound effects for various actions
• The program has a settings menu
• The program has a car engine sound that changes volume based on speed
• The program has pit stop tyre wear reset mechanics
• The program has a tyre wear color system
• The program has a penalty system for cutting corners
• The program has a sound effect for starting lights out
• 
-----------------------------------------------------------------------------
'''

import pygame
import math
import os
import time
import gif_pygame

script_dir = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.joystick.init()

# *********SETUP**********

windowWidth = 1280
windowHeight = 720


screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  
#different track options images
bahrainTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\bahrain.png")), (12800,7200))
bahrainTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\bahrainLine.png")), (12800,7200))

bahrainMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\BahrainMinimap.png")), (256,144))
silverstoneTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\silverstone.png")), (12800,7200))
silverstoneTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\silverstoneLine.png")), (12800,7200))
silverstoneMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\silverstoneMinimap.png")), (256,144))

currentTrack = bahrainTrack
menu = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\menu.png")), (1280,720))
stats = pygame.image.load(os.path.join(script_dir,r"assets\board.png"))


f1logo = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"assets\F1logo.png")), (388.5,100))
f1font = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir, r"assets\f1font.ttf")), 60)
f1font2 = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir, r"assets\f1font.ttf")), 30)

fireworks = gif_pygame.load(os.path.join(script_dir,os.path.join(script_dir, r"assets\giphy.gif")))

#teams
ferrari = pygame.image.load(os.path.join(script_dir,r"assets\ferrari.png"))
Mclaren = pygame.image.load(os.path.join(script_dir,"assets\Mclaren.png"))
Redbull = pygame.image.load(os.path.join(script_dir,"assets\Redbull.png"))
Mercedes = pygame.image.load(os.path.join(script_dir,"assets\Mercedes.png"))
Williams = pygame.image.load(os.path.join(script_dir,"assets\Williams.png"))
VCARB = pygame.image.load(os.path.join(script_dir,"assets\VCARB.png"))
AstonMartin = pygame.image.load(os.path.join(script_dir,"assets\AstonMartin.png"))
Haas = pygame.image.load(os.path.join(script_dir,"assets\Haas.png"))
Alpine = pygame.image.load(os.path.join(script_dir,"assets\Alpine.png"))
Sauber = pygame.image.load(os.path.join(script_dir,"assets\Sauber.png"))
car = ferrari

#tyres wear colors
tyresG = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\tyresG.png")), (60.5,90.5))
tyresY = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\tyresY.png")), (60.5,90.5))
tyresR = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\tyresR.png")), (60.5,90.5))
tyres = tyresG

#animated tyre images
treads1 = pygame.image.load(os.path.join(script_dir,r"assets\treads1.png"))
treads2 = pygame.image.load(os.path.join(script_dir,r"assets\treads2.png"))

#starting race lights  countdown
# traffic light sprites
lights0 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\lights0.png")), (520, 560)
)
lights1 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\lights1.png")), (520, 560)
)
lights2 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\lights2.png")), (520, 560)
)
lights3 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\lights3.png")), (520, 560)
)
lights4 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\lights4.png")), (520, 560)
)

lights = -1
lightsOut = False

lightSound = pygame.mixer.Sound(os.path.join(script_dir, "assets\lightSound.mp3"))
lightSound.set_volume(1)

# starting sound effects
awayWeGo = pygame.mixer.Sound(os.path.join(script_dir, "assets\lightsout.mp3"))
awayWeGo.set_volume(0.1)

lightPlay = True

iAmStupid = pygame.mixer.Sound(os.path.join(script_dir, "assets\iAmStupid.mp3"))
carDRS = pygame.image.load(os.path.join(script_dir, "assets\FerrariDRS.png"))

# reset all variables at the start
speed = 0
trackX = -6685
trackY = -6261
trackSize = 1
angle = 0
lap = 0
crossing = False
maxSpeed = 11

time = 0
lap1time = 0
lap2time = 0
lap3time = 0

font = pygame.font.Font(os.path.join(script_dir, r"assets\font.otf"), 28)
numberFont = pygame.font.Font(os.path.join(script_dir, r"assets\numbers.ttf"), 28)

DRS = False

# tyre wear starting values
FLTW = 99
FLTWC = tyresG

FRTW = 99
FRTWC = tyresG

RLTW = 99
RLTWC = tyresG

RRTW = 99
RRTWC = tyresG

tyresintact = True
i = 0

# penalty variables
pendingPenalty = False
TimePenalty = 0
gamestate = "main"

# car sound
carSound = pygame.mixer.Sound(os.path.join(script_dir, "assets\engine.mp3"))
carSound.set_volume(0.1)
carSound.play(-1)

# crash background
crashbg = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, "assets\crash.png")), (1280, 720)
)

# yellow flag variables
flag = "none"
ii = 0

pitstop = False

# starting gear and max speed
gear = 1
carMaxSpeed = maxSpeed

# racing line off by default
racingLine = False

# turning speed and controller
controller = False
turn_speed = 3


# Pitstop reset function
def pitstopReset():
    global FLTW, FLTWC, FRTW, FRTWC, RLTW, RLTWC, RRTW, RRTWC, tyresintact
    FLTW = 99
    FLTWC = tyresG
    FRTW = 99
    FRTWC = tyresG
    RLTW = 99
    RLTWC = tyresG
    RRTW = 99
    RRTWC = tyresG
    tyresintact = True

# DRS toggle function
def toggleDRS():
    global DRS, carDRS
    if DRS == False:
        if car == ferrari:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\FerrariDRS.png"))
        elif car == Mclaren:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\MclarenDRS.png"))
        elif car == Redbull:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\RedbullDRS.png"))
        elif car == Mercedes:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\MercedesDRS.png"))
        elif car == Williams:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\WilliamsDRS.png"))
        elif car == VCARB:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\VCARBDRS.png"))
        elif car == AstonMartin:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\AstonMartinDRS.png"))
        elif car == Haas:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\HaasDRS.png"))
        elif car == Alpine:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\AlpineDRS.png"))
        elif car == Sauber:
            carDRS = pygame.image.load(os.path.join(script_dir,"assets\SauberDRS.png"))
        DRS = True
    else:
        DRS = False   

print("Use W/A/S/D or a controller to drive the car. Use UP/DOWN arrow keys or controller buttons to change gears. Press SPACE to toggle DRS when available. Select tracks and cars from the menu")
speed2 = 0
player2X = 0
player2Y = 0
angle2 = 0
car2 = Mercedes
# *********GAME LOOP**********
while True:
    # time tracking
    time += clock.get_time() / 1000
    #keyboard pressed
    keys = pygame.key.get_pressed()

    # *********EVENTS**********
    ev = pygame.event.poll()   
    # controller toggle
    if ev.type == pygame.JOYDEVICEADDED:
        joystick = pygame.joystick.Joystick(ev.device_index)
        controller = True
    elif ev.type == pygame.JOYDEVICEREMOVED:
        controller = False 
    if ev.type == pygame.QUIT: 
        break                   
    # mouse click events
    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mouseX, mouseY = pygame.mouse.get_pos()
            if gamestate == "main":
                # choose between menus
                if 300 < mouseX < 940 and 270 < mouseY < 370:
                    gamestate = "ChooseTrack"
                elif 300 < mouseX < 940 and 430 < mouseY < 530:
                    gamestate = "carSelect"
                elif 300 < mouseX < 940 and 570 < mouseY < 670:
                    gamestate = "settings"

            # stats screen back to main menu
            if gamestate == "stats":
                if 520 < mouseX < 1160 and 500 < mouseY < 600:
                    gamestate = "main"
                    lap = 0
                    lap1time = 0
                    lap2time = 0
                    lap3time = 0
                    speed = 0
                    lightsOut = False
                    lights = -1
            # track selection screen
            if gamestate == "ChooseTrack":
                # bahrain track selection
                if 480 < mouseX < 835 and 50 < mouseY < 287:
                    currentTrack = bahrainTrack
                    gamestate = "start"
                    trackX = -6685.0
                    trackY = -6261.0
                    angle = 0
                    lightSound.set_volume(100)
                    lightSound.play() 
                    lap = 0
                    lap1time = 0
                    lap2time = 0
                    lap3time = 0
                    speed = 0
                    lightsOut = False
                    lights = -1
                    FLTW = 99
                    FRTW = 99
                    RLTW = 99
                    RRTW = 99
                    tyresintact = True
                    pendingPenalty = False
                    TimePenalty = 0
                    time = -7
                # silverstone track selection
                elif 480 < mouseX < 835 and 450 < mouseY < 687:
                    currentTrack = silverstoneTrack
                    gamestate = "start"
                    trackX = -7270.0
                    trackY = -5668.0
                    angle = -39
                    lightSound.set_volume(100)
                    lightSound.play() 
                    lap = 0
                    lap1time = 0
                    lap2time = 0
                    lap3time = 0
                    speed = 0
                    lightsOut = False
                    lights = -1
                    FLTW = 99
                    FRTW = 99
                    RLTW = 99
                    RRTW = 99
                    tyresintact = True
                    pendingPenalty = False
                    TimePenalty = 0
                    time = -7
                # back to main menu
                elif 30 < mouseX < 90 and 30 < mouseY < 90:
                    gamestate = "main"
            # car selection screen
            if gamestate == "carSelect":
                if 30 < mouseX < 90 and 30 < mouseY < 90:
                    gamestate = "main"
                elif 120 < mouseX < 305 and 20 < mouseY < 294:
                    car =   Mclaren
                    carMaxSpeed = 15
                    maxSpeed = carMaxSpeed
                elif 320 < mouseX < 515 and 20 < mouseY < 294:
                    car = Mercedes
                    carMaxSpeed = 14.5
                    maxSpeed = carMaxSpeed
                elif 520 < mouseX < 715 and 20 < mouseY < 294:
                    car = Redbull
                    carMaxSpeed = 14
                    maxSpeed = carMaxSpeed
                elif 720 < mouseX < 915 and 20 < mouseY < 294:
                    car = VCARB
                    carMaxSpeed = 13.5
                    maxSpeed = carMaxSpeed
                elif 920 < mouseX < 1115 and 20 < mouseY < 294 :
                    car =   ferrari
                    carMaxSpeed = 13
                    maxSpeed = carMaxSpeed
                elif 120 < mouseX < 305 and 350 < mouseY < 624 :
                    car = Williams
                    carMaxSpeed = 12.5
                    maxSpeed = carMaxSpeed
                elif 320 < mouseX < 515 and 350 < mouseY < 624 :
                    car = AstonMartin
                    carMaxSpeed = 12
                    maxSpeed = carMaxSpeed
                elif 520 < mouseX < 715 and 350 < mouseY < 624 :
                    car = Haas
                    carMaxSpeed = 11.5
                    maxSpeed = carMaxSpeed
                elif 720 < mouseX < 915 and 350 < mouseY < 624 :
                    car = Sauber
                    carMaxSpeed = 11
                    maxSpeed = carMaxSpeed
                elif 920 < mouseX < 1115 and 350 < mouseY < 624 :
                    car = Alpine
                    carMaxSpeed = 10.5
                    maxSpeed = carMaxSpeed
            # crash and settings screen back to main menu
            if gamestate == "crash" or gamestate == "settings":
                if 30 < mouseX < 90 and 30 < mouseY < 90:
                    gamestate = "main"
            # racing line toggle in settings
            if gamestate == "settings":
                if 300 < mouseX < 940 and 270 < mouseY < 370:
                    if racingLine:
                        racingLine = False
                    else:
                        racingLine = True
    # keyboard events
    if ev.type == pygame.KEYDOWN:  
        if ev.key == pygame.K_SPACE:  
            toggleDRS()
        if ev.key == pygame.K_UP and gear != 8:
            gear += 1

        elif ev.key == pygame.K_DOWN and gear != 1:
            gear -= 1

        if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
            maxSpeed = (carMaxSpeed-8) + gear
    # controller button events
    if ev.type == pygame.JOYBUTTONDOWN:
        if ev.button == 0:  
            toggleDRS()

        elif ev.button == 6 and gear != 8:
            gear += 1

        elif ev.button == 7 and gear != 1:
            gear -= 1

        if ev.button == 6 or ev.button == 7:
            maxSpeed = (carMaxSpeed-8) + gear
    # game states
    if gamestate == "start":
        # turn using controller
        if controller and lightsOut and tyresintact:
            angle -= (joystick.get_axis(0) * turn_speed)

        # draw track
        if currentTrack == bahrainTrack:
            if racingLine:
                screen.blit(bahrainTrackLine, (trackX,trackY))
            else:
                screen.blit(bahrainTrack, (trackX,trackY))

        elif currentTrack == silverstoneTrack:
            if racingLine:
                screen.blit(silverstoneTrackLine, (trackX,trackY))
            else:
                screen.blit(silverstoneTrack, (trackX,trackY))
        
        centerColor = screen.get_at((616, 444))

        # pitstop mechanics
        if pitstop:
            if car == Mclaren and centerColor == (172,104,10):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Mercedes and centerColor == (8,174,168):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Redbull and centerColor == (36,40,55):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == VCARB and centerColor == (174,156,8):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == ferrari and centerColor == (87,18,31):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Williams and centerColor == (28,69,109):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == AstonMartin and centerColor == (8, 96, 82):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Haas and centerColor == (174, 174, 174):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Sauber and centerColor == (14, 167, 24):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Alpine and centerColor == (161, 108, 144):
                speed = 0
                pitstopReset()
                pitstop = False

        # wall crash detection
        if centerColor == (127,127,127):
            if DRS and speed > 0:
                FLTW -= int(2*speed)
                FRTW -= int(2*speed)
                if not pygame.mixer.music.get_busy():
                    iAmStupid.play()

            elif speed > 0:
                FLTW -= int(speed)
                FRTW -= int(speed)

        if centerColor == (127,127,127):
            speed = -10
        else:
            if speed < 0:
                speed += 0.2
        # pitstop zone detection
        if centerColor == (28,28,28):
            pitstop = True

        elif centerColor == (36,36,36):
            pitstop = False
        # corner cutting penalty detection
        elif centerColor.r == 2 and centerColor.g == 96 and centerColor.b == 0:
            pendingPenalty = True

        if pendingPenalty == True and centerColor == (22,22,22):
            TimePenalty += 3
            pendingPenalty = False

        keys = pygame.key.get_pressed()
        # turning using keyboard
        if lightsOut and speed > 0:
            if keys[pygame.K_a]:
                if FLTW < 70:
                    turn_speed = 1.5
                else:
                    turn_speed = 3
                angle+=turn_speed
                if speed > 0:
                    FLTW -= 0.001

            if keys[pygame.K_d]:
                if FRTW < 70:
                    angle-=1.5
                else:
                    angle-=3
                if speed > 0:
                    FRTW -= 0.01

        # Reference #1
        angleRadians = math.radians(angle)
        xTravelled = round(speed * math.cos(angleRadians) ,0)
        yTravelled = round(speed * -math.sin(angleRadians) ,0)
        # End Reference #1

        # move track when car moves
        if -12142.0 < (trackX + xTravelled) < 0:
            trackX += xTravelled
        if -6347.0 < (trackY + yTravelled) < 0:
            trackY += yTravelled

        # acceleration and deceleration
        if controller and lightsOut and tyresintact:
            if joystick.get_button(4):
                if speed > 0:
                    speed -= 0.1
        #tyre wear check
        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            tyresintact = False

        # accelerate using keyboard
        if keys[pygame.K_w] and lightsOut and tyresintact:
            if speed < maxSpeed:
                speed += 0.1
            if RRTW >= 0 and RLTW >= 0:
                if DRS:
                    RLTW -= 0.01
                    RRTW -= 0.01
                else:
                    RLTW -= 0.005
                    RRTW -= 0.005
        # accelerate using controller
        elif controller and lightsOut and tyresintact:
            if joystick.get_button(5) and speed >= 0:
                if speed < maxSpeed:
                    speed += 0.1
                if RRTW >= 0 and RLTW >= 0:
                    if DRS:
                        RLTW -= 0.01
                        RRTW -= 0.01
                    else:
                        RLTW -= 0.005
                        RRTW -= 0.005
        else:
            if speed > 0:
                speed -= 0.1

        if speed > maxSpeed:
            speed -= 0.1

        # yellow flag mechanics
        if lightsOut:
            if 20*speed < 150:
                ii += 0.5
                if ii >= 90:
                    flag = "yellow"
                    ii = 0
            else:
                flag = "none"
                ii = 0

        # DRS mechanics
        if tyresintact and lightsOut:
            if DRS:
                if keys[pygame.K_w] and speed < maxSpeed +5:
                    speed += 0.2
                elif controller:
                    if joystick.get_button(5) and speed < maxSpeed +5:
                        speed += 0.2
            else:
                if speed > maxSpeed:
                    speed -= 0.1
        # lap complete detection
        if currentTrack == bahrainTrack:
            if (round(trackX,0)) > -6502.0 and (round(trackX,0)) < -6419.0 and trackY > -6347 and trackY < -6034 and not crossing:
                lap += 1
                crossing = True

        elif currentTrack == silverstoneTrack:
            if (round(trackX,0)) < -7166.0 and (round(trackX,0)) > -7363.0 and trackY > -5713.0 and trackY < -5461.0 and not crossing:
                lap += 1
                crossing = True
        # lap timing
        if lap == 1:
            lap1time = round( time,2)
        elif lap == 2:
            lap2time = round(time - lap1time,2)

        elif lap == 3:
            lap3time =  round(time - lap2time - lap1time,2)

        if currentTrack == bahrainTrack:
            if not ((round(trackX,0)) > -6502.0 and (round(trackX,0)) < -6419.0 and trackY > -6347 and trackY < -6034):
                crossing = False
        elif currentTrack == silverstoneTrack:
            if not ((round(trackX,0)) < -7166.0 and (round(trackX,0)) > -7363.0 and trackY > -5713.0 and trackY < -5461.0):
                crossing = False

        screen.blit(f1font2.render(("lap # " + str(lap)), True, (255, 255, 255)) , (20, 20)) 
        screen.blit(numberFont.render((str(int(20*speed))), True, (255, 255, 255)) , (600, 20)) 
        screen.blit(f1font.render(str(gear), True, (255, 255, 255)) , (600, 650)) 
        
        screen.blit(f1font2.render(("lap 1: " +str(lap1time)), True, ("white")) , (1050, 20))
        if lap2time > 0:
            screen.blit(f1font2.render(("lap 2: " +str(lap2time)), True, ("white")) , (1050, 50))
        if lap3time > 0:
            screen.blit(f1font2.render(("lap 3: " +str(lap3time)), True, ("white")) , (1050, 80)) 

        if lap == 2:
            if lap1time < lap2time:
                screen.blit(f1font2.render(("lap 1: " +str(lap1time)), True, (85, 26, 139)) , (1050, 20))
            else:
                screen.blit(f1font2.render(("lap 2: " +str(lap2time)), True, (85, 26, 139)) , (1050, 50))

        if lap >= 3 :
            if lap1time < lap2time and lap1time < lap3time:
                screen.blit(f1font2.render(("lap 1: " +str(lap1time)), True, (85, 26, 139)) , (1050, 20))
            else:
                if lap2time < lap3time:
                    screen.blit(f1font2.render(("lap 2: " +str(lap2time)), True, (85, 26, 139)) , (1050, 50))
                else:
                    screen.blit(f1font2.render(("lap 3: " +str(lap3time)), True, (85, 26, 139)) , (1050, 80))

        if lap > 3:
            gamestate = "stats"
        # penalty display
        if TimePenalty > 0:
            screen.blit(f1font2.render(("penalty: " + str(TimePenalty)), True, ("white")) , (1050, 250))
        # tyre wear display
        if FLTW > 80:
            FLTWC = tyresG
        elif FLTW > 50:
            FLTWC = tyresY
        else:
            FLTWC = tyresR
        if FRTW > 80:
            FRTWC = tyresG
        elif FRTW > 50:
            FRTWC = tyresY
        else:
            FRTWC = tyresR
        if RLTW > 80:
            RLTWC = tyresG
        elif RLTW > 50:
            RLTWC = tyresY
        else:
            RLTWC = tyresR
        if RRTW > 80:
            RRTWC = tyresG
        elif RRTW > 50:
            RRTWC = tyresY
        else:
            RRTWC = tyresR
        
        screen.blit((FLTWC), (1118, 510))
        screen.blit((FRTWC), (1200, 510))
        screen.blit((RLTWC), (1118, 610))
        screen.blit((RRTWC), (1200, 610))

        screen.blit(f1font2.render(str(int(FLTW)), True, (255, 255, 255)) , (1125, 535))
        screen.blit(f1font2.render(str(int(FRTW)), True, (255, 255, 255)) , (1208, 535))
        screen.blit(f1font2.render(str(int(RLTW)), True, (255, 255, 255)) , (1125, 640))
        screen.blit(f1font2.render(str(int(RRTW)), True, (255, 255, 255)) , (1208, 640))

        # minimap display
        if currentTrack == bahrainTrack:        
            screen.blit((bahrainMinimap), (20, 550))
        elif currentTrack == silverstoneTrack:
            screen.blit((silverstoneMinimap), (20, 550))

        # car display and tyre tread animation
        if DRS:
            screen.blit(pygame.transform.rotate(carDRS, angle), (500, 300))
            screen.blit(f1font2.render("DRS ACTIVE", True, (255, 255, 255)) , (520, 100))
        else:
            screen.blit(pygame.transform.rotate(car, angle), (500, 300))
        if speed > 0:
            if i < 1:
                screen.blit(pygame.transform.rotate(treads1, angle), (500, 300))
                i += 0.1
            elif i < 2:
                screen.blit(pygame.transform.rotate(treads2, angle), (500, 300))
                i += 0.1
            else:
                i = 0  

        screen.blit(pygame.transform.rotate(car2, angle2), (trackX + player2X, trackY + player2Y))

        # starting lights display and mechanics and sound
        if -1 > lights <= 0:
            screen.blit(lights0, (380, 110))
        elif 0 > lights <= 1:
            screen.blit(lights1, (380, 110))
        elif 1 > lights <= 2:
            screen.blit(lights2, (380, 110))
        elif 2 > lights <= 3:
            screen.blit(lights3, (380, 110))
        elif 3 > lights <= 4:
            screen.blit(lights4, (380, 110))
        elif round(lights,0) >= 3:
            lightsOut = True
            
        if lights <= 3:
            lights += 0.01
        elif lights < 99:
            lightsOut == True
            if not pygame.mixer.music.get_busy():
                awayWeGo.play()
            lights = 100
        # adjust car sound volume based on speed
        carSound.set_volume(speed / maxSpeed * 0.5)

        # draw car position on minimap
        minimapX = trackX / -50 + 25
        minimapY = trackY / -50 + 560
        pygame.draw.circle(screen, (255,0,0),(minimapX,minimapY ), 7)
        speed = round(speed,1)
                
        # crash detection
        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            gamestate = "crash"

        # yellow flag display
        if flag == "yellow":
            screen.blit(f1font2.render("YELLOW FLAG", True, (255, 255, 0)) , (500, 600))

    mouseX, mouseY = pygame.mouse.get_pos()
    
    # start menu
    if gamestate == "main":
        pygame.mixer.stop()
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        screen.blit(f1logo, (440,100))
        # hover effects for buttons
        if 300 < mouseX < 940 and 430 < mouseY < 530:
            pygame.draw.rect(screen, ("white"),  (300, 430, 640, 100),0,20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 430, 640, 100),0,20)

        if 300 < mouseX < 940 and 270 < mouseY < 370:
            pygame.draw.rect(screen, ("white"), (300, 270, 640, 100),0,20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 270, 640, 100),0,20)

        if 300 < mouseX < 940 and 570 < mouseY < 670:
            pygame.draw.rect(screen, ("white"), (300, 570, 640, 100),0,20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 570, 640, 100),0,20)

        screen.blit(f1font.render('Car', True, ("black")) , (540, 450)) 
        screen.blit(f1font.render('Race', True, ("black")) , (520, 290))
        screen.blit(f1font.render('Settings', True, ("black")) , (470, 590))

    elif gamestate == "ChooseTrack":
        screen.blit(menu, (0,0))
        # hover effects for track selection
        if 480 < mouseX < 835 and 50 < mouseY < 287:
            pygame.draw.rect(screen, ("white"), (480, 50, 355, 237),0,20)
        else:
            pygame.draw.rect(screen, ("light grey"), (480, 50, 355, 237),0,20)

        if 480 < mouseX < 835 and 450 < mouseY < 687:
            pygame.draw.rect(screen, ("white"), (480, 450, 355, 237),0,20)
        else:
            pygame.draw.rect(screen, ("light grey"), (480, 450, 355, 237),0,20)

        screen.blit(bahrainMinimap, (530,100))
        screen.blit(silverstoneMinimap, (530,500))
        # back button
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

    elif gamestate == "stats":
        # final stats screen
        screen.blit(stats, (0,0))
        screen.blit(pygame.transform.scale(pygame.transform.rotate(car, -90), (206, 304)), (130,200))
        screen.blit(f1font.render((str(lap1time)) + "s", True, ("black")) , (800, 205))
        screen.blit(f1font.render((str(lap2time)) + "s", True, ("black")) , (800, 315))
        screen.blit(f1font.render((str(lap3time)) + "s", True, ("black")) , (800, 425))
        if 520 < mouseX < 1160 and 500 < mouseY < 600:
            pygame.draw.rect(screen, ("white"),  (520, 500, 640, 100),0,30)
        else:
            pygame.draw.rect(screen, ("light grey"), (520, 500, 640, 100),0,30)
        screen.blit(f1font.render('Main Menu', True, ("dark grey")) , (640, 520))

    # car selection menu
    elif gamestate == "carSelect":
        screen.blit(menu, (0,0))
        # car selection with hover effects
        if 120 < mouseX < 305 and 20 < mouseY < 294 or car == Mclaren:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Mclaren, -90), (144, 213)), (140,40))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Mclaren, -90), (185, 274)), (120,20))
        if 320 < mouseX < 515 and 20 < mouseY < 294 or car == Mercedes:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Mercedes, -90), (144, 213)), (340,40))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Mercedes, -90), (185, 274)), (320,20))
        if 520 < mouseX < 715 and 20 < mouseY < 294 or car == Redbull:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Redbull, -90), (144, 213)), (540,40))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Redbull, -90), (185, 274)), (520,20))
        if 720 < mouseX < 915 and 20 < mouseY < 294 or car == VCARB:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(VCARB, -90), (144, 213)), (740,40))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(VCARB, -90), (185, 274)), (720,20))
        if 920 < mouseX < 1115 and 20 < mouseY < 294 or car == ferrari:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(ferrari, -90), (144, 213)), (940,40))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(ferrari, -90), (185, 274)), (920,20))
        if 120 < mouseX < 305 and 350 < mouseY < 624 or car == Williams:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Williams, -90), (144, 213)), (140,370))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Williams, -90), (185, 274)), (120,350))
        if 320 < mouseX < 515 and 350 < mouseY < 624 or car == AstonMartin:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(AstonMartin, -90 ), (144, 213)), (340,370))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(AstonMartin, -90 ), (185, 274)), (320,350))
        if 520 < mouseX < 715 and 350 < mouseY < 624 or car == Haas:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Haas, -90), (144, 213)), (540,370))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Haas, -90), (185, 274)), (520,350))
        if 720 < mouseX < 915 and 350 < mouseY < 624 or car == Sauber:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Sauber, -90), (144, 213)), (740,370))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Sauber, -90), (185, 274)), (720,350))
        if 920 < mouseX < 1115 and 350 < mouseY < 624 or car == Alpine:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Alpine, -90), (144, 213)), (940,370))
        else:
            screen.blit(pygame.transform.scale(pygame.transform.rotate(Alpine, -90), (185, 274)), (920,350))

        # back button
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

    elif gamestate == "crash":
        # crash screen
        screen.blit(crashbg, (0,0))
        # back button
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        screen.blit(f1font.render("You Crashed", True, ("black")) , (480, 300))
    # settings menu
    elif gamestate == "settings":
        screen.blit(menu, (0,0))
        # back button
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))
        # racing line toggle with hover effect
        if 300 < mouseX < 940 and 270 < mouseY < 370:
            pygame.draw.rect(screen, ("white"), (300, 270, 640, 100),0,20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 270, 640, 100),0,20)
        if racingLine:
            pygame.draw.rect(screen, ("green"), (300, 270, 640, 100),0,20)
        screen.blit(f1font.render("Racing Line", True, ("black")) , (420, 300))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit() 