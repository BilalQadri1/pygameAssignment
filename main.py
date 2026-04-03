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
'''

import pygame
import math
import os
import time
import gif_pygame
from network import Network  # MULTIPLAYER IMPORT

script_dir = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.joystick.init()

# *********SETUP**********

windowWidth = 1280
windowHeight = 720

# Add these to your variable setup
my_lobby_id = None
my_player_index = None
available_lobbies = {} # Dictionary of {ID: Count}

screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  
#different track options images
bahrainTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\bahrain.png")).convert(), (12800,7200))
bahrainTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\bahrainLine.png")).convert_alpha(), (12800,7200))

bahrainMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\BahrainMinimap.png")), (256,144))

# --- LIVE CHECKPOINT LISTS ---
# Increased to 600x600 based on your track run!
bahrain_checkpoints = [
    pygame.Rect(6176, 6295, 600, 600),
    pygame.Rect(4646, 6271, 600, 600),
    pygame.Rect(2666, 6271, 600, 600),
    pygame.Rect(1784, 6097, 600, 600),
    pygame.Rect(1963, 5291, 600, 600),
    pygame.Rect(1976, 3769, 600, 600),
    pygame.Rect(2224, 1679, 600, 600),
    pygame.Rect(2452, 433, 600, 600),
    pygame.Rect(3429, 1014, 600, 600),
    pygame.Rect(4423, 1763, 600, 600),
    pygame.Rect(4780, 2593, 600, 600),
    pygame.Rect(5309, 3359, 600, 600),
    pygame.Rect(6076, 4218, 600, 600),
    pygame.Rect(5052, 4217, 600, 600),
    pygame.Rect(3281, 4149, 600, 600),
    pygame.Rect(3720, 4654, 600, 600),
    pygame.Rect(5329, 4693, 600, 600),
    pygame.Rect(6825, 4740, 600, 600),
    pygame.Rect(8225, 4618, 600, 600),
    pygame.Rect(8104, 3728, 600, 600),
    pygame.Rect(7112, 3190, 600, 600),
    pygame.Rect(6571, 2345, 600, 600),
    pygame.Rect(6820, 1530, 600, 600),
    pygame.Rect(7409, 788, 600, 600),
    pygame.Rect(8338, 1819, 600, 600),
    pygame.Rect(8999, 2936, 600, 600),
    pygame.Rect(9777, 4153, 600, 600),
    pygame.Rect(10477, 5385, 600, 600),
    pygame.Rect(10110, 6195, 600, 600),
    pygame.Rect(7883, 6279, 600, 600),
]
silverstone_checkpoints = []

my_checkpoint_index = 0  # Which gate are we looking for next?

silverstoneTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstone.png")).convert(), (12800,7200))
silverstoneTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneLine.png")).convert_alpha(), (12800,7200))
silverstoneMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneMinimap.png")), (256,144))

currentTrack = bahrainTrack
menu = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\menu.png")), (1280,720))
stats = pygame.image.load(os.path.join(script_dir,r"assets\board.png"))


f1logo = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\F1logo.png")), (388.5,100))
f1font = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir, r"assets\f1font.ttf")), 60)
f1font2 = pygame.font.Font(os.path.join(script_dir,os.path.join(script_dir, r"assets\f1font.ttf")), 30)

fireworks = gif_pygame.load(os.path.join(script_dir,os.path.join(script_dir, r"assets\giphy.gif")))

# teams - Removed manual scaling to prevent squishing
ferrari = pygame.image.load(os.path.join(script_dir, r"assets\ferrari.png")).convert_alpha()
Mclaren = pygame.image.load(os.path.join(script_dir, r"assets\Mclaren.png")).convert_alpha()
Redbull = pygame.image.load(os.path.join(script_dir, r"assets\Redbull.png")).convert_alpha()
Mercedes = pygame.image.load(os.path.join(script_dir, r"assets\Mercedes.png")).convert_alpha()
Williams = pygame.image.load(os.path.join(script_dir, r"assets\Williams.png")).convert_alpha()
VCARB = pygame.image.load(os.path.join(script_dir, r"assets\VCARB.png")).convert_alpha()
AstonMartin = pygame.image.load(os.path.join(script_dir, r"assets\AstonMartin.png")).convert_alpha()
Haas = pygame.image.load(os.path.join(script_dir, r"assets\Haas.png")).convert_alpha()
Alpine = pygame.image.load(os.path.join(script_dir, r"assets\Alpine.png")).convert_alpha()
Sauber = pygame.image.load(os.path.join(script_dir, r"assets\Sauber.png")).convert_alpha()

car = ferrari
car_name = "ferrari"

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
lights0 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\lights0.png")), (520, 560))
lights1 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\lights1.png")), (520, 560))
lights2 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\lights2.png")), (520, 560))
lights3 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\lights3.png")), (520, 560))
lights4 = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\lights4.png")), (520, 560))

lights = -1
lightsOut = False

lightSound = pygame.mixer.Sound(os.path.join(script_dir, r"assets\lightSound.mp3"))
lightSound.set_volume(1)

# starting sound effects
awayWeGo = pygame.mixer.Sound(os.path.join(script_dir, r"assets\lightsout.mp3"))
awayWeGo.set_volume(0.1)

lightPlay = True

iAmStupid = pygame.mixer.Sound(os.path.join(script_dir, r"assets\iAmStupid.mp3"))
carDRS = pygame.image.load(os.path.join(script_dir, r"assets\FerrariDRS.png"))

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
carSound = pygame.mixer.Sound(os.path.join(script_dir, r"assets\engine.mp3"))
carSound.set_volume(0.1)
carSound.play(-1)

# crash background
crashbg = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\crash.png")), (1280, 720))

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
    global DRS, carDRS, car_name
    
    if DRS == False:
        drs_path = os.path.join(script_dir, f"assets\\{car_name}DRS.png")
        carDRS = pygame.image.load(drs_path).convert_alpha()
        DRS = True
    else:
        DRS = False

# Add this near your other functions
def get_taken_cars(lobby_data, my_id):
    taken = []
    for p_id, p_data in lobby_data["players"].items():
        if p_id != my_id:
            taken.append(p_data[3]) # Index 3 is the car name string
    return taken

print("Use W/A/S/D or a controller to drive the car. Use UP/DOWN arrow keys or controller buttons to change gears. Press SPACE to toggle DRS when available. Select tracks and cars from the menu")

car2 = Mercedes  # Default opponent car sprite

# MULTIPLAYER: Connect to the server before the loop starts
n = None

# Car Grid definition for both selection and networking logic
all_teams = [
    (Mclaren, 120, 130, 'Mclaren'), (Mercedes, 320, 130, 'Mercedes'),
    (Redbull, 520, 130, 'Redbull'), (VCARB, 720, 130, 'VCARB'),
    (ferrari, 920, 130, 'ferrari'), (Williams, 120, 400, 'Williams'),
    (AstonMartin, 320, 400, 'AstonMartin'), (Haas, 520, 400, 'Haas'),
    (Sauber, 720, 400, 'Sauber'), (Alpine, 920, 400, 'Alpine')
]

# Initialize this so the game doesn't crash on the first frame
taken_cars = [] 
players_connected = 0
last_network_update = 0
lobby_data = []

# *********GAME LOOP**********
while True:

    # time tracking
    time += clock.get_time() / 1000
    keys = pygame.key.get_pressed()

    # Get mouse position globally to prevent NameError
    mouseX, mouseY = pygame.mouse.get_pos()

    # *********EVENTS**********
    for ev in pygame.event.get():
        if ev.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(ev.device_index)
            controller = True
        elif ev.type == pygame.JOYDEVICEREMOVED:
            controller = False 
        if ev.type == pygame.QUIT: 
            break                   
        
        # mouse click events - using elif chain to prevent ghost clicks
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                
                if gamestate == "main":
                    if 300 < mouseX < 940:
                        if 220 < mouseY < 320: gamestate = "ChooseTrack"
                        elif 340 < mouseY < 440: gamestate = "carSelect"
                        elif 460 < mouseY < 560: gamestate = "settings"
                        elif 580 < mouseY < 680: 
                            gamestate = "onlineMenu"
                            # Force a reconnection attempt if it previously failed!
                            if n is None or n.p is None:
                                n = Network()

                elif gamestate == "onlineMenu": 
                    # --- ADD THIS BACK BUTTON LOGIC ---
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"
                    # Host Button
                    elif 300 < mouseX < 940 and 270 < mouseY < 370: 
                        if n is not None and n.p is not None:  # <--- UPDATED LINE
                            reply = n.send(["CREATE", [trackX, trackY, angle, car_name, "LOBBY"]])
                            if reply:
                                my_lobby_id, my_player_index = reply[0], reply[1]
                                gamestate = "hostLobby"
                    # Join Button
                    elif 300 < mouseX < 940 and 430 < mouseY < 530:
                        if n is not None and n.p is not None:  # <--- UPDATED LINE
                            lobby_list = n.send(["GET"]) 
                            if lobby_list is not None:
                                available_lobbies = lobby_list
                                gamestate = "joinLobby"

                elif gamestate == "joinLobby": 
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "onlineMenu"
                    elif available_lobbies:
                        y_offset = 150
                        for l_id, count in available_lobbies.items():
                            if 300 < mouseX < 940 and y_offset < mouseY < y_offset + 80:
                                reply = n.send(["JOIN", l_id, [trackX, trackY, angle, car_name, "LOBBY"]])
                                
                                # --- SAFE JOIN CHECK ---
                                # Only enter if the server sends back a list [l_id, p_id]
                                if isinstance(reply, list): 
                                    my_lobby_id, my_player_index = reply[0], reply[1]
                                    gamestate = "hostLobby"
                                # -----------------------
                                
                            y_offset += 100

                elif gamestate == "hostLobby":
                    # START RACE CLICK LOGIC (HOST ONLY)
                    if my_player_index == 0:
                        if 440 < mouseX < 840 and 630 < mouseY < 690:
                            
                            # --- NEW: Check if anyone is still out on the track ---
                            can_start = True
                            if isinstance(lobby_data, list):
                                for p in lobby_data:
                                    # If a player exists and their status is RACING
                                    if p is not None and len(p) > 4 and p[4] == "RACING":
                                        can_start = False
                                        break
                            
                            # Only execute start if everyone is FINISHED or in the LOBBY
                            if can_start:
                                gamestate = "start"
                                # Reset coordinates based on track
                                if currentTrack == bahrainTrack: trackX, trackY, angle = -6685.0, -6261.0, 0
                                elif currentTrack == silverstoneTrack: trackX, trackY, angle = -7270.0, -5668.0, -39
                                
                                my_checkpoint_index = 0
                                lightSound.set_volume(1)
                                lightSound.play() 
                                time = -7
                                lap = 0
                                lap1time, lap2time, lap3time = 0, 0, 0
                                speed = 0
                                lightsOut = False
                                lights = -1
                                crossing = False
                                FLTW, FRTW, RLTW, RRTW = 99, 99, 99, 99
                                tyresintact = True
                                pendingPenalty = False
                                TimePenalty = 0
                    
                    # LEAVE LOBBY CLICK LOGIC
                    if 1050 < mouseX < 1250 and 30 < mouseY < 90:
                        if n is not None and n.p is not None and my_lobby_id is not None: 
                            n.send(["LEAVE", my_lobby_id, my_player_index])
                        
                        my_lobby_id = None
                        my_player_index = None
                        taken_cars = []
                        gamestate = "onlineMenu"

                    # CAR SELECTION GRID LOGIC
                    for img, x, y, name in all_teams:
                        if x < mouseX < x + 185 and y < mouseY < y + 274:
                            if name not in taken_cars:
                                car = img
                                car_name = name 
                                
                                speed_map = {'Mclaren': 15, 'Mercedes': 14.5, 'Redbull': 14, 'VCARB': 13.5, 
                                            'ferrari': 13, 'Williams': 12.5, 'AstonMartin': 12, 
                                            'Haas': 11.5, 'Sauber': 11, 'Alpine': 10.5}
                                maxSpeed = speed_map[name]
                                carMaxSpeed = maxSpeed

                elif gamestate == "stats":
                    # PLAY AGAIN BUTTON
                    if 320 < mouseX < 620 and 600 < mouseY < 680:
                        # Go to lobby if online, or track select if offline
                        gamestate = "hostLobby" if my_lobby_id is not None else "ChooseTrack"
                        lap = 0
                        lap1time, lap2time, lap3time = 0, 0, 0
                        speed = 0
                        lightsOut = False
                        lights = -1
                        my_checkpoint_index = 0
                        FLTW, FRTW, RLTW, RRTW = 99, 99, 99, 99
                        tyresintact = True
                        pendingPenalty = False
                        TimePenalty = 0
                        crossing = False

                    # MAIN MENU (LEAVE) BUTTON
                    elif 660 < mouseX < 960 and 600 < mouseY < 680:
                        gamestate = "main"
                        lap = 0
                        lap1time, lap2time, lap3time = 0, 0, 0
                        speed = 0
                        lightsOut = False
                        lights = -1
                        if n is not None and n.p is not None and my_lobby_id is not None:
                            n.send(["LEAVE", my_lobby_id, my_player_index])
                        my_lobby_id = None
                        my_player_index = None
                        taken_cars = []
                        # -----------------------------

                elif gamestate == "ChooseTrack":
                    if 480 < mouseX < 835 and 50 < mouseY < 287:
                        currentTrack = bahrainTrack
                        gamestate = "start"
                        trackX = -6685.0
                        trackY = -6261.0
                        angle = 0
                        lightSound.set_volume(100)
                        lightSound.play() 
                        lap = 0
                        my_checkpoint_index = 0 # RESET CHECKPOINT
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
                        lightSound.set_volume(100)
                        lightSound.play() 
                        lap = 0
                        my_checkpoint_index = 0 # RESET CHECKPOINT
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
                    elif 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"

                elif gamestate == "carSelect":
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"
                    elif 120 < mouseX < 305 and 20 < mouseY < 294:
                        car = Mclaren
                        car_name = "Mclaren" 
                        carMaxSpeed = 15
                        maxSpeed = carMaxSpeed
                    elif 320 < mouseX < 515 and 20 < mouseY < 294:
                        car = Mercedes
                        car_name = "Mercedes" 
                        carMaxSpeed = 14.5
                        maxSpeed = carMaxSpeed
                    elif 520 < mouseX < 715 and 20 < mouseY < 294:
                        car = Redbull
                        car_name = "Redbull"
                        carMaxSpeed = 14
                        maxSpeed = carMaxSpeed
                    elif 720 < mouseX < 915 and 20 < mouseY < 294:
                        car = VCARB
                        car_name = "VCARB"
                        carMaxSpeed = 13.5
                        maxSpeed = carMaxSpeed
                    elif 920 < mouseX < 1115 and 20 < mouseY < 294:
                        car = ferrari
                        car_name = "ferrari"
                        carMaxSpeed = 13
                        maxSpeed = carMaxSpeed
                    elif 120 < mouseX < 305 and 400 < mouseY < 674:
                        car = Williams
                        car_name = "Williams"
                        carMaxSpeed = 12.5
                        maxSpeed = carMaxSpeed
                    elif 320 < mouseX < 515 and 400 < mouseY < 674:
                        car = AstonMartin
                        car_name = "AstonMartin"
                        carMaxSpeed = 12
                        maxSpeed = carMaxSpeed
                    elif 520 < mouseX < 715 and 400 < mouseY < 674:
                        car = Haas
                        car_name = "Haas"
                        carMaxSpeed = 11.5
                        maxSpeed = carMaxSpeed 
                    elif 720 < mouseX < 915 and 400 < mouseY < 674:
                        car = Sauber
                        car_name = "Sauber"
                        carMaxSpeed = 11
                        maxSpeed = carMaxSpeed
                    elif 920 < mouseX < 1115 and 400 < mouseY < 674:
                        car = Alpine
                        car_name = "Alpine"
                        carMaxSpeed = 10.5
                        maxSpeed = carMaxSpeed
                    
                elif gamestate == "crash" or gamestate == "settings":
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"
                    # racing line toggle in settings
                    if gamestate == "settings" and 300 < mouseX < 940 and 270 < mouseY < 370:
                        racingLine = not racingLine

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
            
            # --- THE LIVE CHECKPOINT CREATOR TOOL ---
            if ev.key == pygame.K_p:
                actual_x = int(-trackX + 640)
                actual_y = int(-trackY + 360)
                
                # Now creating 600x600 boxes by default!
                new_rect = pygame.Rect(actual_x - 300, actual_y - 300, 600, 600)
                
                # Instantly add it to the active track's list so it draws on screen
                if currentTrack == bahrainTrack:
                    bahrain_checkpoints.append(new_rect)
                elif currentTrack == silverstoneTrack:
                    silverstone_checkpoints.append(new_rect)
                
                # Print the exact code to the terminal for you to copy later
                print(f"pygame.Rect({new_rect.x}, {new_rect.y}, {new_rect.width}, {new_rect.height}),")
            # ------------------------------------------

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

    # ==================================================
    # --- MULTIPLAYER SYNC BLOCK ---
    # ==================================================
    current_time = pygame.time.get_ticks()

    if current_time - last_network_update > 30:
        last_network_update = current_time 

        if n is not None and n.p is not None and my_lobby_id is not None:
            # --- NEW STATUS LOGIC ---
            if gamestate == "start": my_status = "RACING"
            elif gamestate == "stats": my_status = "FINISHED"
            else: my_status = "LOBBY"
            # ------------------------
            
            lobby_data = n.send(["UPDATE", my_lobby_id, my_player_index,[trackX, trackY, angle, car_name, my_status, my_checkpoint_index, lap]])

            if lobby_data == "SERVER_DEAD":
                print("Connection to the server was lost!")
                my_lobby_id = None
                my_player_index = None
                taken_cars = []
                gamestate = "onlineMenu"

            elif lobby_data == "CLOSED":
                print("Host left! Lobby destroyed.")
                my_lobby_id = None
                my_player_index = None
                taken_cars = []
                gamestate = "onlineMenu" 
            
            elif isinstance(lobby_data, list):
                players_connected = len([p for p in lobby_data if isinstance(p, list)])
                taken_cars = [p[3] for i, p in enumerate(lobby_data) if isinstance(p, list) and len(p) >= 4 and i != my_player_index]
                
                # Pull clients into race
                if gamestate == "hostLobby" and my_player_index != 0: 
                    host_data = lobby_data[0] 
                    # Only pull if host is RACING and on Lap 0 (prevents getting sucked into ongoing races)
                    if isinstance(host_data, list) and len(host_data) > 6 and host_data[4] == "RACING" and host_data[6] == 0:
                        gamestate = "start"
                        if currentTrack == bahrainTrack: trackX, trackY, angle = -6685.0, -6261.0, 0
                        elif currentTrack == silverstoneTrack: trackX, trackY, angle = -7270.0, -5668.0, -39
                        
                        my_checkpoint_index = 0
                        lightSound.set_volume(1)
                        lightSound.play() 
                        time = -7
                        lap = 0
                        speed = 0
                        lightsOut = False
                        lights = -1
                        crossing = False
                        FLTW, FRTW, RLTW, RRTW = 99, 99, 99, 99
                        tyresintact = True
                        pendingPenalty = False
                        TimePenalty = 0
    # ==================================================

    # game states
    if gamestate == "start":
        
        # Calculate car position on the track image
        player_track_x = -trackX + 640
        player_track_y = -trackY + 360

        # Select which checkpoints to use
        active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
        
        if active_checkpoints:
            next_gate = active_checkpoints[my_checkpoint_index]
            if next_gate.collidepoint(player_track_x, player_track_y):
                my_checkpoint_index += 1
            if my_checkpoint_index >= len(active_checkpoints):
                my_checkpoint_index = 0

        # turn using controller
        if controller and lightsOut and tyresintact:
            angle -= (joystick.get_axis(0) * turn_speed)

        camera_rect = pygame.Rect(int(-trackX), int(-trackY), windowWidth, windowHeight)

        if currentTrack == bahrainTrack:
            if racingLine:
                screen.blit(bahrainTrackLine, (0, 0), area=camera_rect)
            else:
                screen.blit(bahrainTrack, (0, 0), area=camera_rect)

        elif currentTrack == silverstoneTrack:
            if racingLine:
                screen.blit(silverstoneTrackLine, (0, 0), area=camera_rect)
            else:
                screen.blit(silverstoneTrack, (0, 0), area=camera_rect)
        
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

        angleRadians = math.radians(angle)
        xTravelled = round(speed * math.cos(angleRadians) ,0)
        yTravelled = round(speed * -math.sin(angleRadians) ,0)

        # move track when car moves
        if -12142.0 < (trackX + xTravelled) < 0:
            trackX += xTravelled
        if -6347.0 < (trackY + yTravelled) < 0:
            trackY += yTravelled
            
        # ==================================================
        # --- DRAW OPPONENTS ---
        if isinstance(lobby_data, list):
            car_images = {
                "ferrari": ferrari, "Mclaren": Mclaren, "Mercedes": Mercedes,
                "Redbull": Redbull, "VCARB": VCARB, "Williams": Williams,
                "AstonMartin": AstonMartin, "Haas": Haas, "Sauber": Sauber,
                "Alpine": Alpine
            }

            for i, p in enumerate(lobby_data):
                # Now checks if they are RACING or FINISHED
                if p is not None and i != my_player_index and len(p) > 4 and p[4] in ["RACING", "FINISHED"]:
                    p_trackX, p_trackY, p_angle, p_car_name = p[0], p[1], p[2], p[3]
                    
                    opponentX_on_screen = 500 + (trackX - p_trackX)
                    opponentY_on_screen = 300 + (trackY - p_trackY)
                    
                    if p_car_name in car_images:
                        opponent_img = car_images[p_car_name]
                        screen.blit(pygame.transform.rotate(opponent_img, p_angle), (opponentX_on_screen, opponentY_on_screen))
        # ==================================================

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
        if FLTW > 80: FLTWC = tyresG
        elif FLTW > 50: FLTWC = tyresY
        else: FLTWC = tyresR
        
        if FRTW > 80: FRTWC = tyresG
        elif FRTW > 50: FRTWC = tyresY
        else: FRTWC = tyresR
        
        if RLTW > 80: RLTWC = tyresG
        elif RLTW > 50: RLTWC = tyresY
        else: RLTWC = tyresR
        
        if RRTW > 80: RRTWC = tyresG
        elif RRTW > 50: RRTWC = tyresY
        else: RRTWC = tyresR
        
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

        # starting lights display and mechanics and sound
        if -1 > lights <= 0: screen.blit(lights0, (380, 110))
        elif 0 > lights <= 1: screen.blit(lights1, (380, 110))
        elif 1 > lights <= 2: screen.blit(lights2, (380, 110))
        elif 2 > lights <= 3: screen.blit(lights3, (380, 110))
        elif 3 > lights <= 4: screen.blit(lights4, (380, 110))
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

        # ==================================================
        # ==================================================
        # --- DRAW LEADERBOARD ---
        if isinstance(lobby_data, list):
            def get_rank(p):
                # Ensure the player exists and has all 7 data points
                if p is None or len(p) < 7: return (-1, -1, 0)
                
                laps, chk_idx = p[6], p[5]
                dist = 0
                
                # Tie-breaker calculation based on distance to NEXT gate
                if active_checkpoints and chk_idx < len(active_checkpoints):
                    gate = active_checkpoints[(chk_idx + 1) % len(active_checkpoints)]
                    p_x, p_y = -p[0] + 640, -p[1] + 360
                    dist = math.sqrt((gate.centerx - p_x)**2 + (gate.centery - p_y)**2)
                
                # Return negative distance so smaller dist = higher rank
                return (laps, chk_idx, -dist)

            # Sort players using the advanced tie-breaker function
            players_ranking = sorted(
                [p for p in lobby_data if p is not None and len(p) > 6], 
                key=get_rank, 
                reverse=True
            )

            # --- NEW F1 STYLE UI DRAWING ---
            start_x = 20
            start_y = 100
            row_height = 45
            box_width = 300

            for idx, p_info in enumerate(players_ranking[:10]): # Show up to 10 players
                y_pos = start_y + (idx * row_height)
                
                # 1. Position Box (Red for 1st place, Dark Grey for the rest)
                pos_color = (220, 0, 0) if idx == 0 else (30, 30, 30)
                pygame.draw.rect(screen, pos_color, (start_x, y_pos, 50, row_height - 2))
                
                # Draw position number perfectly centered in its box
                pos_text = f1font2.render(str(idx + 1), True, "white")
                pos_rect = pos_text.get_rect(center=(start_x + 25, y_pos + (row_height // 2)))
                screen.blit(pos_text, pos_rect)

                # 2. Name & Data Plate (Darker background)
                pygame.draw.rect(screen, (20, 20, 20), (start_x + 50, y_pos, box_width - 50, row_height - 2))
                
                # Draw Team Name (Abbreviated to 3 uppercase letters just like F1!)
                team_abbr = p_info[3][:3].upper()
                name_text = f1font2.render(team_abbr, True, "white")
                screen.blit(name_text, (start_x + 65, y_pos + 7))

                # 3. Lap Info (Right aligned)
                # Later you can replace this with actual lap times if you sync them over the network!
                lap_text = f1font2.render(f"Lap {p_info[6]}", True, (200, 200, 200))
                screen.blit(lap_text, (start_x + box_width - 100, y_pos + 7))
        # ==================================================


    # start menu
    if gamestate == "main":
        pygame.mixer.stop()
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        screen.blit(f1logo, (440,100))
        
        menu_buttons = [
            (220, 'Race'), 
            (340, 'Car'), 
            (460, 'Settings'), 
            (580, 'Online')
        ]

        for y_pos, label in menu_buttons:
            if 300 < mouseX < 940 and y_pos < mouseY < y_pos + 100:
                pygame.draw.rect(screen, ("white"), (300, y_pos, 640, 100), 0, 20)
            else:
                pygame.draw.rect(screen, (220, 220, 220), (300, y_pos, 640, 100), 0, 20)
            
            text_surf = f1font.render(label, True, ("black"))
            text_rect = text_surf.get_rect(center=(620, y_pos + 50)) 
            screen.blit(text_surf, text_rect)

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
        # final stats screen background
        screen.blit(menu, (0,0))
        
        # Title
        title_text = f1font.render("FINAL STANDINGS", True, ("black"))
        screen.blit(title_text, title_text.get_rect(center=(640, 70)))

        # --- DRAW FULL LEADERBOARD ---
        if isinstance(lobby_data, list):
            def get_rank(p):
                if p is None or len(p) < 7: return (-1, -1, 0)
                laps, chk_idx = p[6], p[5]
                dist = 0
                active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
                if active_checkpoints and chk_idx < len(active_checkpoints):
                    gate = active_checkpoints[(chk_idx + 1) % len(active_checkpoints)]
                    p_x, p_y = -p[0] + 640, -p[1] + 360
                    dist = math.sqrt((gate.centerx - p_x)**2 + (gate.centery - p_y)**2)
                return (laps, chk_idx, -dist)

            players_ranking = sorted(
                [p for p in lobby_data if p is not None and len(p) > 6], 
                key=get_rank, 
                reverse=True
            )

            start_x = 340
            start_y = 120
            row_height = 45
            box_width = 600

            for idx, p_info in enumerate(players_ranking[:10]):
                y_pos = start_y + (idx * row_height)
                
                # Position Box
                pos_color = (220, 0, 0) if idx == 0 else (30, 30, 30)
                pygame.draw.rect(screen, pos_color, (start_x, y_pos, 50, row_height - 2))
                pos_text = f1font2.render(str(idx + 1), True, "white")
                screen.blit(pos_text, pos_text.get_rect(center=(start_x + 25, y_pos + (row_height // 2))))

                # Name Plate
                pygame.draw.rect(screen, (20, 20, 20), (start_x + 50, y_pos, box_width - 50, row_height - 2))
                team_abbr = p_info[3][:3].upper()
                screen.blit(f1font2.render(team_abbr, True, "white"), (start_x + 65, y_pos + 7))

                # Status (Check if they finished lap 3)
                status_text = "FINISHED" if p_info[6] > 3 else f"Lap {p_info[6]}"
                color = (50, 255, 50) if p_info[6] > 3 else (200, 200, 200)
                screen.blit(f1font2.render(status_text, True, color), (start_x + box_width - 150, y_pos + 7))

        # --- DRAW PLAY AGAIN BUTTON ---
        if 320 < mouseX < 620 and 600 < mouseY < 680:
            pygame.draw.rect(screen, ("white"),  (320, 600, 300, 80), 0, 30)
        else:
            pygame.draw.rect(screen, ("light grey"), (320, 600, 300, 80), 0, 30)
            
        btn1_text = f1font2.render('Play Again', True, ("black"))
        screen.blit(btn1_text, btn1_text.get_rect(center=(470, 640)))

        # --- DRAW MAIN MENU BUTTON ---
        if 660 < mouseX < 960 and 600 < mouseY < 680:
            pygame.draw.rect(screen, ("white"),  (660, 600, 300, 80), 0, 30)
        else:
            pygame.draw.rect(screen, ("light grey"), (660, 600, 300, 80), 0, 30)
            
        btn2_text = f1font2.render('Main Menu', True, ("black"))
        screen.blit(btn2_text, btn2_text.get_rect(center=(810, 640)))

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

    elif gamestate == "onlineMenu":
        screen.blit(menu, (0,0))
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        if 300 < mouseX < 940 and 270 < mouseY < 370:
            pygame.draw.rect(screen, ("white"), (300, 270, 640, 100), 0, 20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 270, 640, 100), 0, 20)
        screen.blit(f1font.render('Host', True, ("black")), (520, 290))

        if 300 < mouseX < 940 and 430 < mouseY < 530:
            pygame.draw.rect(screen, ("white"), (300, 430, 640, 100), 0, 20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 430, 640, 100), 0, 20)
        screen.blit(f1font.render('Join', True, ("black")), (530, 450))

        # --- NEW: CONNECTION STATUS FEEDBACK ---
        if n is None or n.p is None:
            # Draw a red error message if disconnected
            error_msg = "ERROR: Cannot reach server. Playing Offline."
            screen.blit(f1font2.render(error_msg, True, (255, 50, 50)), (350, 600))
        else:
            # Draw a green success message if connected
            success_msg = "Connected to Official F1 Server"
            screen.blit(f1font2.render(success_msg, True, (50, 255, 50)), (400, 600))
        # ---------------------------------------
    
    elif gamestate == "hostLobby":
        screen.blit(menu, (0,0))
        
        if my_player_index == 0:
            if 440 < mouseX < 840 and 630 < mouseY < 690:
                pygame.draw.rect(screen, (100, 255, 100), (440, 630, 400, 60), 0, 15) 
            else:
                pygame.draw.rect(screen, (50, 200, 50), (440, 630, 400, 60), 0, 15) 
            screen.blit(f1font2.render("START RACE", True, "black"), (545, 645))
        else:
            screen.blit(f1font2.render("Waiting for Host to start...", True, "white"), (480, 645))
        
        if 1050 < mouseX < 1250 and 30 < mouseY < 90:
            pygame.draw.rect(screen, (255, 100, 100), (1050, 30, 200, 60), 0, 15) 
        else:
            pygame.draw.rect(screen, (200, 50, 50), (1050, 30, 200, 60), 0, 15)   
        screen.blit(f1font2.render("LEAVE", True, "white"), (1100, 45))

        pygame.draw.rect(screen, (40, 40, 40), (300, 20, 640, 80), 0, 20)
        cap_text = f"LOBBY #{my_lobby_id}  |  CAPACITY: {players_connected}/10"
        screen.blit(f1font2.render(cap_text, True, "white"), (420, 45))

        for img, x, y, name in all_teams:
            is_taken = name in taken_cars
            if is_taken:
                gray_car = pygame.transform.scale(pygame.transform.rotate(img, -90), (185, 274))
                gray_car.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(gray_car, (x, y))
                screen.blit(f1font2.render("TAKEN", True, "red"), (x + 40, y + 100))
            else:
                if x < mouseX < x + 185 and y < mouseY < y + 274 or car == img:
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), (144, 213)), (x + 20, y + 20))
                else:
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), (185, 274)), (x, y))

    elif gamestate == "joinLobby":
        screen.blit(menu, (0,0))
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        if not available_lobbies:
            screen.blit(f1font2.render("No active lobbies found. Someone must Host first!", True, "red"), (200, 300))
        else:
            y_offset = 150
            for l_id, count in available_lobbies.items():
                if 300 < mouseX < 940 and y_offset < mouseY < y_offset + 80:
                    pygame.draw.rect(screen, "white", (300, y_offset, 640, 80), 0, 15)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), (300, y_offset, 640, 80), 0, 15)
                
                txt = f"Lobby #{l_id}  -  Capacity: {count}/10"
                screen.blit(f1font2.render(txt, True, "black"), (350, y_offset + 25))
                y_offset += 100

    pygame.display.flip()
    clock.tick(60)

pygame.quit()