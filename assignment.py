'''
-----------------------------------------------------------------------------
Program Name: (never put your personal name or information on the Internet)
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
pygame.init()

# *********SETUP**********

windowWidth = 1280
windowHeight = 720
screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  
bahrainTrack = pygame.transform.scale(pygame.image.load("bahrain.png"), (12800,7200))
bahrainMinimap = pygame.transform.scale(pygame.image.load("BahrainMinimap.png"), (256,144))
silverstoneTrack = pygame.transform.scale(pygame.image.load("silverstone.png"), (12800,7200))
silverstoneMinimap = pygame.transform.scale(pygame.image.load("silverstoneMinimap.png"), (256,144))

CurrentTrack = bahrainTrack
menu = pygame.transform.scale(pygame.image.load("menu.png"), (1280,720))
stats = pygame.image.load("board.png")

car = pygame.image.load("ferrari.png")

f1logo = pygame.transform.scale(pygame.image.load("F1logo.png"), (388.5,100))
f1font = pygame.font.Font("f1font.ttf", 60)
f1font2 = pygame.font.Font("f1font.ttf", 30)

fireworks = gif_pygame.load("giphy.gif")

#teams
ferrari = pygame.image.load("ferrari.png")
Mclaren = pygame.image.load("Mclaren.png")
Redbull = pygame.image.load("Redbull.png")
Mercedes = pygame.image.load("Mercedes.png")
Williams = pygame.image.load("Williams.png")
VCARB = pygame.image.load("VCARB.png")
AstonMartin = pygame.image.load("AstonMartin.png")
Haas = pygame.image.load("Haas.png")
Alpine = pygame.image.load("Alpine.png")
Sauber = pygame.image.load("Sauber.png")

#tyres wear colors
tyresG = pygame.transform.scale(pygame.image.load("tyresG.png"), (60.5,90.5))
tyresY = pygame.transform.scale(pygame.image.load("tyresY.png"), (60.5,90.5))
tyresR = pygame.transform.scale(pygame.image.load("tyresR.png"), (60.5,90.5))
tyres = tyresG

#animated tyre images
treads1 = pygame.image.load("treads1.png")
treads2 = pygame.image.load("treads2.png")

#starting race lights  countdown
lights0 = pygame.transform.scale(pygame.image.load("lights0.png"), (520,560))
lights1 = pygame.transform.scale(pygame.image.load("lights1.png"), (520,560))
lights2 = pygame.transform.scale(pygame.image.load("lights2.png"), (520,560))
lights3 = pygame.transform.scale(pygame.image.load("lights3.png"), (520,560))
lights4 = pygame.transform.scale(pygame.image.load("lights4.png"), (520,560))
lights = -1
lightsOut = False
lightSound = pygame.mixer.Sound(os.path.join("lightSound.mp3"))
awayWeGo = pygame.mixer.Sound(os.path.join("lightsout.mp3"))
lightPlay = True

iAmStupid = pygame.mixer.Sound(os.path.join("iAmStupid.mp3"))
carDRS = pygame.image.load("FerrariDRS.png")


speed = 0
trackX = -6685 
trackY = -6261
trackSize = 1
angle = 0
lap = 0
crossing = False
maxSpeed = 11
script_dir = os.path.dirname(os.path.abspath(__file__))
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
trackLimitsWarning = 0
pendingPenalty = False
TimePenalty = 0
gamestate = "main"

#car sound effects
carSound = pygame.mixer.Sound(os.path.join("engine.mp3"))
carSound.set_volume(0)
carSound.play(-1)

flag = "none"
ii = 0
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
                    lightSound.play()
            if gamestate == "stats":
                if 520 < mouseX < 1160 and 500 < mouseY < 600:
                    gamestate = "main"
            if gamestate == "ChooseTrack":
                if 480 < mouseX < 835 and 50 < mouseY < 287:
                    CurrentTrack = bahrainTrack
                    gamestate = "start"
                elif 480 < mouseX < 835 and 450 < mouseY < 687:
                    CurrentTrack = silverstoneTrack
                    gamestate = "start"
                    trackX = -7607.0
                    trackY = -5660.0
                    angle = -39

    if ev.type == pygame.KEYDOWN:  
        if ev.key == pygame.K_SPACE:  
            if DRS == False:
                if car == ferrari:
                    carDRS = pygame.image.load("FerrariDRS.png")
                elif car == Mclaren:
                    carDRS = pygame.image.load("MclarenDRS.png")
                elif car == Redbull:
                    carDRS = pygame.image.load("RedbullDRS.png")
                elif car == Mercedes:
                    carDRS = pygame.image.load("MercedesDRS.png")
                elif car == Williams:
                    carDRS = pygame.image.load("WilliamsDRS.png")
                elif car == VCARB:
                    carDRS = pygame.image.load("VCARBDRS.png")
                elif car == AstonMartin:
                    carDRS = pygame.image.load("AstonMartinDRS.png")
                elif car == Haas:
                    carDRS = pygame.image.load("HaasDRS.png")
                elif car == Alpine:
                    carDRS = pygame.image.load("AlpineDRS.png")
                elif car == Sauber:
                    carDRS = pygame.image.load("SauberDRS.png")
                DRS = True
            else:
                DRS = False   
               
    
    if gamestate == "start":
        screen.blit(CurrentTrack, (trackX,trackY))

        frontColor = screen.get_at((640, 360))
        
        if frontColor == (127,127,127):
            if DRS:
                FLTW = 0
                FRTW = 0
                iAmStupid.play()
                carSound.set_volume(0)

            else:
                FLTW -= 10
                FRTW -= 10
            speed = -5
        
        centerColor = screen.get_at((640, 360))
        if centerColor.r == 2 and centerColor.g == 96 and centerColor.b == 0:
            pendingPenalty = True

        if pendingPenalty == True and centerColor == (22,22,22):
            if trackLimitsWarning < 3:
                trackLimitsWarning += 1
                print("track limits warning #" + str(trackLimitsWarning))
            else:
                TimePenalty += 3
                pendingPenalty = False


        keys = pygame.key.get_pressed()

        if lightsOut and speed > 0:
            if keys[pygame.K_a]:
                angle+=3
                FLTW -= 0.001
            if keys[pygame.K_d]:
                angle-=3
                FRTW -= 0.01
        
        # Reference #1
        angleRadians = math.radians(angle)
        xTravelled = round(speed * math.cos(angleRadians) ,0)
        yTravelled = round(speed * -math.sin(angleRadians) ,0)
        # End Reference #1
        if CurrentTrack == bahrainTrack:
            if -12142.0 < (trackX + xTravelled) < 0:
                trackX += xTravelled
            if -6347.0 < (trackY + yTravelled) < 0:
                trackY += yTravelled
        else:
            trackX += xTravelled
            trackY += yTravelled

        if keys[pygame.K_1]:
            car =   Mclaren
            maxSpeed = 15
        elif keys[pygame.K_2]:
            car = Mercedes
            maxSpeed = 14.5
        elif keys[pygame.K_3]:
            car = Redbull
            maxSpeed = 14
        elif keys[pygame.K_4]:
            car = VCARB
            maxSpeed = 13.5
        elif keys[pygame.K_5]:
            car = ferrari
            maxSpeed = 13
        elif keys[pygame.K_6]:
            car = Williams
            maxSpeed = 12.5
        elif keys[pygame.K_7]:
            car = AstonMartin
            maxSpeed = 12
        elif keys[pygame.K_8]:
            car = Haas
            maxSpeed = 11.5
        elif keys[pygame.K_9]:
            car = Sauber
            maxSpeed = 11
        elif keys[pygame.K_0]:
            car = Alpine
            maxSpeed = 10.5


        if keys[pygame.K_s]:
            if speed > 0:
                speed -= 0.1
        


        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            tyresintact = False

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
        else:
            if speed > 0:
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

        if (round(trackX,0)) < -6600.0 and (round(trackX,0)) > -6650.0 and trackY > -6347 and trackY < -6034 and not crossing:
            lap += 1
            crossing = True


        
        if lap == 1:
            lap1time = round( time,2)
        elif lap == 2:
            lap2time = round(time - lap1time,2)

        elif lap == 3:
            lap3time =  round(time - lap2time - lap1time,2)
        if not ((round(trackX,0)) < -6600.0 and (round(trackX,0)) > -6650.0 and trackY > -6347 and trackY < -6034):
            crossing = False


        screen.blit(f1font2.render(("lap # " + str(lap)), True, (255, 255, 255)) , (20, 20)) 
        screen.blit(numberFont.render((str(int(20*speed))), True, (255, 255, 255)) , (600, 20)) 
        
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
        if CurrentTrack == bahrainTrack:        
            screen.blit((bahrainMinimap), (20, 550))
        else:
            screen.blit((silverstoneMinimap), (20, 550))


        

        if DRS:
            screen.blit(pygame.transform.rotate(carDRS, angle), (500, 300))
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
            lights += random.uniform(0.01, 0.02)
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


    mouseX, mouseY = pygame.mouse.get_pos()



    if gamestate == "main":
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

        screen.blit(f1font.render('Settings', True, ("black")) , (440, 450)) 
        screen.blit(f1font.render('Race', True, ("black")) , (520, 290))

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
    print(angle)
    pygame.display.flip()
    clock.tick(60)


pygame.quit()