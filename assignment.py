'''
-----------------------------------------------------------------------------
Program Name: F1 Racing Game
Program Description:

-----------------------------------------------------------------------------
References:

(put a link to your reference here but also add a comment in the code below where you used the reference)
reference #1 to move forward in the direction the car is facing: https://stackoverflow.com/questions/64774900/how-to-get-velocity-x-and-y-from-angle-and-speed
-----------------------------------------------------------------------------

Additional Libraries/Extensions:

(put a list of required extensions so that the user knows that they need to download extra features)

-----------------------------------------------------------------------------

Known bugs:

(put a list of known bugs here, if you have any)

----------------------------------------------------------------------------


Program Reflection:
I think this project deserves a level XXXXXX because ...

 Level 3 Requirements Met:
• 
•  
•  
•  
•  
• 

Features Added Beyond Level 3 Requirements:
• 
•  
•  
•  
•  
• 
-----------------------------------------------------------------------------
'''

import pygame
import math
import os
import time
import random
import gif_pygame

script_dir = os.path.dirname(os.path.abspath(__file__))

pygame.init()

# *********SETUP**********

windowWidth = 1280
windowHeight = 720

ferrari = pygame.image.load(os.path.join(script_dir,os.path.join(script_dir,"ferrari.png")))

screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  
bahrainTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"bahrain.png")), (12800,7200))
bahrainTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"bahrainLine.png")), (12800,7200))

bahrainMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"BahrainMinimap.png")), (256,144))
silverstoneTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"silverstone.png")), (12800,7200))
silverstoneTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"silverstoneLine.png")), (12800,7200))
silverstoneMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"silverstoneMinimap.png")), (256,144))

currentTrack = bahrainTrack
menu = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"menu.png")), (1280,720))
stats = pygame.image.load(os.path.join(script_dir,"board.png"))


f1logo = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"F1logo.png")), (388.5,100))
f1font = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir,"f1font.ttf")), 60)
f1font2 = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir,"f1font.ttf")), 30)

fireworks = gif_pygame.load(os.path.join(script_dir,os.path.join(script_dir,"giphy.gif")))

#teams
ferrari = pygame.image.load(os.path.join(script_dir,"ferrari.png"))
Mclaren = pygame.image.load(os.path.join(script_dir,"Mclaren.png"))
Redbull = pygame.image.load(os.path.join(script_dir,"Redbull.png"))
Mercedes = pygame.image.load(os.path.join(script_dir,"Mercedes.png"))
Williams = pygame.image.load(os.path.join(script_dir,"Williams.png"))
VCARB = pygame.image.load(os.path.join(script_dir,"VCARB.png"))
AstonMartin = pygame.image.load(os.path.join(script_dir,"AstonMartin.png"))
Haas = pygame.image.load(os.path.join(script_dir,"Haas.png"))
Alpine = pygame.image.load(os.path.join(script_dir,"Alpine.png"))
Sauber = pygame.image.load(os.path.join(script_dir,"Sauber.png"))

car = ferrari

#tyres wear colors
tyresG = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"tyresG.png")), (60.5,90.5))
tyresY = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"tyresY.png")), (60.5,90.5))
tyresR = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"tyresR.png")), (60.5,90.5))
tyres = tyresG

#animated tyre images
treads1 = pygame.image.load(os.path.join(script_dir,"treads1.png"))
treads2 = pygame.image.load(os.path.join(script_dir,"treads2.png"))

#starting race lights  countdown
lights0 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"lights0.png")), (520,560))
lights1 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"lights1.png")), (520,560))
lights2 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"lights2.png")), (520,560))
lights3 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"lights3.png")), (520,560))
lights4 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"lights4.png")), (520,560))
lights = -1
lightsOut = False
lightSound = pygame.mixer.Sound(os.path.join(script_dir,"lightSound.mp3"))
lightSound.set_volume(1)


awayWeGo = pygame.mixer.Sound(os.path.join(script_dir,"lightsout.mp3"))
awayWeGo.set_volume(0.1)

lightPlay = True

iAmStupid = pygame.mixer.Sound(os.path.join(script_dir,"iAmStupid.mp3"))
carDRS = pygame.image.load(os.path.join(script_dir,"FerrariDRS.png"))


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
font = pygame.font.Font(os.path.join(script_dir, "font.otf"), 28)
numberFont = pygame.font.Font(os.path.join(script_dir, "numbers.ttf"), 28)

DRS = False

#tyrre wear starting values
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

#penalty variables
pendingPenalty = False
TimePenalty = 0
gamestate = "main"

#car sound effects
carSound = pygame.mixer.Sound(os.path.join(script_dir,"engine.mp3"))
carSound.set_volume(0.1)
carSound.play(-1)

crashbg = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,"crash.png")), (1280,720))
flag = "none"
ii = 0
pitstop = False

gear = 1
carMaxSpeed = maxSpeed

racingLine = False

ERS = 0

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

# *********GAME LOOP**********
while True:
    time += clock.get_time() / 1000

    keys = pygame.key.get_pressed()

    # *********EVENTS**********
    ev = pygame.event.poll()    
    if ev.type == pygame.QUIT: 
        break                   
    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mouseX, mouseY = pygame.mouse.get_pos()
            if gamestate == "main":
                if 300 < mouseX < 940 and 270 < mouseY < 370:
                    gamestate = "ChooseTrack"
                elif 300 < mouseX < 940 and 430 < mouseY < 530:
                    gamestate = "carSelect"
                elif 300 < mouseX < 940 and 570 < mouseY < 670:
                    gamestate = "settings"


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

            if gamestate == "ChooseTrack":
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

                elif 480 < mouseX < 835 and 450 < mouseY < 687:
                    currentTrack = silverstoneTrack
                    gamestate = "start"
                    trackX = -7270.0
                    trackY = -5668.0
                    angle = -39
                    lightSound.play() 
                    time = -7

                elif 30 < mouseX < 90 and 30 < mouseY < 90:
                    gamestate = "main"

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
                
            if gamestate == "crash" or gamestate == "settings":
                if 30 < mouseX < 90 and 30 < mouseY < 90:
                    gamestate = "main"

            if gamestate == "settings":
                if 300 < mouseX < 940 and 270 < mouseY < 370:
                    if racingLine:
                        racingLine = False
                    else:
                        racingLine = True

    if ev.type == pygame.KEYDOWN:  
        if ev.key == pygame.K_SPACE:  
            if DRS == False:
                if car == ferrari:
                    carDRS = pygame.image.load(os.path.join(script_dir,"FerrariDRS.png"))
                elif car == Mclaren:
                    carDRS = pygame.image.load(os.path.join(script_dir,"MclarenDRS.png"))
                elif car == Redbull:
                    carDRS = pygame.image.load(os.path.join(script_dir,"RedbullDRS.png"))
                elif car == Mercedes:
                    carDRS = pygame.image.load(os.path.join(script_dir,"MercedesDRS.png"))
                elif car == Williams:
                    carDRS = pygame.image.load(os.path.join(script_dir,"WilliamsDRS.png"))
                elif car == VCARB:
                    carDRS = pygame.image.load(os.path.join(script_dir,"VCARBDRS.png"))
                elif car == AstonMartin:
                    carDRS = pygame.image.load(os.path.join(script_dir,"AstonMartinDRS.png"))
                elif car == Haas:
                    carDRS = pygame.image.load(os.path.join(script_dir,"HaasDRS.png"))
                elif car == Alpine:
                    carDRS = pygame.image.load(os.path.join(script_dir,"AlpineDRS.png"))
                elif car == Sauber:
                    carDRS = pygame.image.load(os.path.join(script_dir,"SauberDRS.png"))
                DRS = True
            else:
                DRS = False   
        if ev.key == pygame.K_UP and gear != 8:
            gear += 1

        elif ev.key == pygame.K_DOWN and gear != 1:
            gear -= 1

        if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
            maxSpeed = (carMaxSpeed-8) + gear
               
    if gamestate == "start":
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

        if centerColor == (127,127,127) and not keys[pygame.K_LSHIFT]:
            if DRS and speed > 0:
                FLTW -= int(2*speed)
                FRTW -= int(2*speed)
                if not pygame.mixer.music.get_busy():
                    iAmStupid.play()

            elif speed > 0:
                FLTW -= int(speed)
                FRTW -= int(speed)

        if centerColor == (127,127,127) and not keys[pygame.K_LSHIFT]:
            speed = -10
        else:
            if speed < 0:
                speed += 0.2
        
        if centerColor == (28,28,28):
            pitstop = True

        elif centerColor == (36,36,36):
            pitstop = False

        elif centerColor.r == 2 and centerColor.g == 96 and centerColor.b == 0:
            pendingPenalty = True

        if pendingPenalty == True and centerColor == (22,22,22):
            TimePenalty += 3
            pendingPenalty = False

        keys = pygame.key.get_pressed()

        if lightsOut and speed > 0:
            if keys[pygame.K_a]:
                if FLTW < 70:
                    angle+=1.5
                else:
                    angle+=3
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

        if -12142.0 < (trackX + xTravelled) < 0:
            trackX += xTravelled
        if -6347.0 < (trackY + yTravelled) < 0:
            trackY += yTravelled

        if keys[pygame.K_s]:
            if speed > 0:
                speed -= 0.1
        
        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            tyresintact = False

        if keys[pygame.K_w] and lightsOut and tyresintact and speed >= 0:
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

        if lightsOut:
            if 20*speed < 150:
                ii += 0.5
                if ii >= 90:
                    flag = "yellow"
                    ii = 0
            else:
                flag = "none"
                ii = 0

        if tyresintact and lightsOut:
            if DRS:
                if keys[pygame.K_w] and speed < maxSpeed +5:
                    speed += 0.2
            else:
                if speed > maxSpeed:
                    speed -= 0.1

        if currentTrack == bahrainTrack:
            if (round(trackX,0)) > -6502.0 and (round(trackX,0)) < -6419.0 and trackY > -6347 and trackY < -6034 and not crossing:
                lap += 1
                crossing = True

        elif currentTrack == silverstoneTrack:
            if (round(trackX,0)) < -7166.0 and (round(trackX,0)) > -7363.0 and trackY > -5713.0 and trackY < -5461.0 and not crossing:
                lap += 1
                crossing = True

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

        if TimePenalty > 0:
            screen.blit(f1font2.render(("penalty: " + str(TimePenalty)), True, ("white")) , (1050, 250))
        
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
        if currentTrack == bahrainTrack:        
            screen.blit((bahrainMinimap), (20, 550))
        elif currentTrack == silverstoneTrack:
            screen.blit((silverstoneMinimap), (20, 550))

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

        carSound.set_volume(speed / maxSpeed * 0.5)

        minimapX = trackX / -50 + 25
        minimapY = trackY / -50 + 560
        pygame.draw.circle(screen, (255,0,0),(minimapX,minimapY ), 7)
        speed = round(speed,1)
                
        screen.blit(f1font.render(str(ERS), True, (255, 255, 255)) , (600, 700)) 

        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            gamestate = "crash"
    


    mouseX, mouseY = pygame.mouse.get_pos()
    
    if gamestate == "main":
        pygame.mixer.stop()
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        screen.blit(f1logo, (440,100))
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

        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

    elif gamestate == "stats":
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

    elif gamestate == "carSelect":
        screen.blit(menu, (0,0))
        
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

        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

    elif gamestate == "crash":
        screen.blit(crashbg, (0,0))
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        screen.blit(f1font.render("You Crashed", True, ("black")) , (480, 300))

    elif gamestate == "settings":
        screen.blit(menu, (0,0))
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

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