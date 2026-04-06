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
import random 
import gif_pygame
import json  # <-- Make sure json is imported up here
from network import Network  

# 1. script_dir MUST be defined first
script_dir = os.path.dirname(os.path.abspath(__file__))

# 2. NOW you can put the account setup here!
# ==========================================
# --- ACCOUNT SYSTEM SETUP ---
users = {}
accounts_file = os.path.join(script_dir, "accounts.json")
try:
    with open(accounts_file, "r") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

def save_accounts():
    with open(accounts_file, "w") as f:
        json.dump(users, f, indent=4)
# --- UNLOCKED CARS SYSTEM ---
unlocked_cars = {}
unlocked_file = os.path.join(script_dir, "unlocked_cars.json")
try:
    with open(unlocked_file, "r") as f:
        unlocked_cars = json.load(f)
except FileNotFoundError:
    unlocked_cars = {}

def save_unlocked_cars():
    with open(unlocked_file, "w") as f:
        json.dump(unlocked_cars, f, indent=4)
# ==========================================

# ==========================================
# --- POINTS SYSTEM ---
user_points = {}
points_file = os.path.join(script_dir, "points.json")
try:
    with open(points_file, "r") as f:
        user_points = json.load(f)
except FileNotFoundError:
    user_points = {}

def save_points():
    with open(points_file, "w") as f:
        json.dump(user_points, f, indent=4)

points_awarded = False
# ==========================================
# --- ABBREVIATION SYSTEM ---
user_abbrs = {}
abbrs_file = os.path.join(script_dir, "abbrs.json")
try:
    with open(abbrs_file, "r") as f:
        user_abbrs = json.load(f)
except FileNotFoundError:
    user_abbrs = {}

def save_abbrs():
    with open(abbrs_file, "w") as f:
        json.dump(user_abbrs, f, indent=4)

abbrInputed = ""
abbrTyping = False
# ==========================================
# ==========================================
# --- DRIVER INVENTORY SYSTEM ---
owned_drivers = {}
drivers_file = os.path.join(script_dir, "owned_drivers.json")
try:
    with open(drivers_file, "r") as f:
        owned_drivers = json.load(f)
except FileNotFoundError:
    owned_drivers = {}

def save_drivers():
    with open(drivers_file, "w") as f:
        json.dump(owned_drivers, f, indent=4)

market_search_input = ""
market_typing = False
market_results = []       
market_selected = None    
market_loaded_img = None  
market_msg = ""

# --- NEW: Inventory Variables ---
inventory_page = 0
inventory_loaded_imgs = {}
# --------------------------------
# ==========================================
# --- ACTIVE SQUAD SYSTEM ---
active_driver = {}
active_driver_file = os.path.join(script_dir, "active_driver.json")
try:
    with open(active_driver_file, "r") as f:
        active_driver = json.load(f)
except FileNotFoundError:
    active_driver = {}

def save_active_driver():
    with open(active_driver_file, "w") as f:
        json.dump(active_driver, f, indent=4)
# ==========================================
# --- DYNAMIC PRICING ---
DRIVER_PRICES = {
    # Primes & Legends
    "Hamilton2019": 3500, "Vettel": 3500, "HamiltonMercedes": 3000, 
    "HamiltonMclaren": 2800, "Rosberg": 2500, "Ricciardo": 2000, 
    "Bottas2019": 1800, "Bottas2020": 1800, "SainzFerrari": 1500, "VettelAston": 1200,
    
    # Current Top Tier
    "Verstappen": 3000, "Norris": 2500, "Leclerc": 2200, "Hamilton": 2000, 
    "Piastri": 1800, "Sainz": 1600, "Russell": 1600, "Alonso": 1500, 
    
    # Midfield / Rookies
    "Hulkenberg": 1000, "Albon": 1000, "Gasly": 900, "Perez": 900, 
    "Ocon": 800, "Tsunoda": 800, "Colapinto": 1000, "Antonelli": 1200, # High hype rookie tax
    "Bearman": 900, "Lawson": 900, "Bortoleto": 800, "Hadjar": 800,
    "Ricciardo2024": 800, "Magnussen": 700, "Bottas2024": 700,
    
    # Lower F1 / Ex-F1
    "Guanyu": 600, "MickSchumacher": 600, "De Vries": 500, "Sargeant": 400,

    # Teams
    "Redbull": 5000, "Mclaren": 4800, "ferrari": 4500, "Mercedes": 4000, 
    "AstonMartin": 2500, "Alpine": 2000, "Haas": 2000, "VCARB": 1800, 
    "Williams": 1500, "Cadillac": 1200, "Audi": 1000
}
DEFAULT_F1_PRICE = 500
TIER_PRICES = {"F2": 200, "F3": 100, "F4": 50} # Your F2/F3/F4 cards will auto-use these!

# ==========================================

# --- ADD THIS FUNCTION BACK IN ---
def find_driver_card(name):
    base_dir = os.path.join(script_dir, "F1Cards")
    sub_dirs = ["", "F2", "F3", "F4"]
    for sub in sub_dirs:
        path = os.path.join(base_dir, sub, f"{name}.png")
        if os.path.exists(path):
            return path
    return None
# ---------------------------------


def draw_card_stats(surface, driver_name, card_x, card_y):
    # --- BULLETPROOF DICTIONARY MATCHING ---
    # 1. Strip ALL spaces and make the requested name lowercase
    clean_name = driver_name.replace(" ", "").lower()
    
    # 2. Strip ALL spaces and make the dictionary keys lowercase
    bulletproof_stats = {k.replace(" ", "").lower(): v for k, v in driver_stats.items()}
    
    # 3. Look it up!
    stats = bulletproof_stats.get(clean_name, {"OVR": 75, "EXP": 75, "RAC": 75, "AWA": 75, "PAC": 75})
    # ---------------------------------------
    
    # Your perfectly calibrated coordinates!
    positions = {
        "OVR": (card_x + 30, card_y + 73),
        "EXP": (card_x + 21, card_y + 236),
        "RAC": (card_x + 69, card_y + 235),
        "AWA": (card_x + 115, card_y + 235),
        "PAC": (card_x + 163, card_y + 235),
    }

    # ... (Keep the rest of the loop exactly the same below this!) ...


    for stat_name, position in positions.items():
        val_str = str(int(stats[stat_name])).zfill(2) # Turns '8' into '08'
        x_offset = 0
        
        # Draw each digit side-by-side
        for digit in val_str:
            if digit in rating_images:
                surface.blit(rating_images[digit], (position[0] + x_offset, position[1]))
                x_offset += 22 # Shift right for the second digit (slightly wider than the 20px width)
# ==========================================
def get_boosted_speed(base_speed, driver_name):
    if not driver_name: return base_speed
    
    clean_name = driver_name.replace(" ", "").lower()
    bulletproof_stats = {k.replace(" ", "").lower(): v for k, v in driver_stats.items()}
    stats = bulletproof_stats.get(clean_name, {"PAC": 75})
    pace = stats["PAC"]
    
    # 75 Pace is baseline. Every point above/below adds/subtracts 0.1 maxSpeed
    boost = (pace - 75) * 0.1 
    
    # Hard floor of 5.0 so a terrible driver doesn't make the car go backwards!
    return max(5.0, base_speed + boost)

def search_driver_cards(query):
    if not query: return []
    
    base_dir = os.path.join(script_dir, "F1Cards")
    sub_dirs = ["", "F2", "F3", "F4"]
    results = []
    query_lower = query.lower()
    
    for sub in sub_dirs:
        folder_path = os.path.join(base_dir, sub)
        if not os.path.exists(folder_path): continue
        
        for file in os.listdir(folder_path):
            if file.endswith(".png") and query_lower in file.lower():
                name = file.replace(".png", "")
                
                # Ignore utility assets
                if name in ["Empty", "GoldTemplate", "pack"]: continue
                
                # Determine Price
                price = DEFAULT_F1_PRICE
                if sub in TIER_PRICES: price = TIER_PRICES[sub]
                
                # Override with specific F1 price if they are a top driver
                for key, val in DRIVER_PRICES.items():
                    if key.lower() in name.lower():
                        price = val
                        break
                        
                results.append({"name": name, "path": os.path.join(folder_path, file), "price": price})
    
    return results[:6] # Return max 6 results to fit on screen
# ==========================================

loggedInUser = None
typing = False
UsernameTyping = False
passwordTyping = False
UsernameInputed = ""
passwordInputed = ""
UsernameExist = False
passwordExist = False
show_last_char = False
last_key_time = 0
# ==========================================

# 3. The rest of your normal setup continues below...
pygame.init()
pygame.joystick.init()

# *********SETUP**********

windowWidth = 1280
windowHeight = 720

# Add these to your variable setup
my_lobby_id = None
my_player_index = None
my_grid_order = [] # Used to sync the starting grid
available_lobbies = {} # Dictionary of {ID: Count}

screen = pygame.display.set_mode((windowWidth, windowHeight))
clock = pygame.time.Clock()  
#different track options images
bahrainTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\bahrain.png")).convert(), (12800,7200))
bahrainTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\bahrainLine.png")).convert_alpha(), (12800,7200))

bahrainMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\BahrainMinimap.png")), (256,144))
# ==========================================
# ==========================================
# --- DRIVER RATINGS SYSTEM ---
ovr_images = {}
stat_images = {}

OVR_W, OVR_H = 30, 30    
STAT_W, STAT_H = 18, 18  

for i in range(10):
    num_path = os.path.join(script_dir, "F1Cards", "RatingNumbers", f"{i}.png")
    if os.path.exists(num_path):
        img = pygame.image.load(num_path).convert_alpha()
        ovr_images[str(i)] = pygame.transform.scale(img, (OVR_W, OVR_H))
        stat_images[str(i)] = pygame.transform.scale(img, (STAT_W, STAT_H))

# Current Live Stats 
driver_stats = {
    # --- HISTORICAL / PRIME F1 ---
    "Hamilton2019":     {"OVR": 97, "EXP": 95, "RAC": 98, "AWA": 96, "PAC": 98},
    "Vettel":           {"OVR": 96, "EXP": 90, "RAC": 95, "AWA": 94, "PAC": 99}, 
    "HamiltonMercedes": {"OVR": 95, "EXP": 99, "RAC": 96, "AWA": 97, "PAC": 94},
    "HamiltonMclaren":  {"OVR": 94, "EXP": 75, "RAC": 94, "AWA": 85, "PAC": 98},
    "Rosberg":          {"OVR": 91, "EXP": 88, "RAC": 90, "AWA": 92, "PAC": 93},
    "Ricciardo":        {"OVR": 90, "EXP": 85, "RAC": 95, "AWA": 88, "PAC": 90}, 
    "Bottas2020":       {"OVR": 89, "EXP": 85, "RAC": 87, "AWA": 88, "PAC": 92},
    "SainzFerrari":     {"OVR": 89, "EXP": 82, "RAC": 89, "AWA": 92, "PAC": 88},
    "Bottas2019":       {"OVR": 88, "EXP": 80, "RAC": 86, "AWA": 86, "PAC": 91},
    "VettelAston":      {"OVR": 86, "EXP": 99, "RAC": 85, "AWA": 95, "PAC": 80},

    # --- CURRENT F1 GRID ---
    "Verstappen": {"OVR": 96, "EXP": 88, "RAC": 97, "AWA": 95, "PAC": 98},
    "Norris":     {"OVR": 93, "EXP": 80, "RAC": 92, "AWA": 88, "PAC": 95},
    "Leclerc":    {"OVR": 92, "EXP": 82, "RAC": 91, "AWA": 89, "PAC": 96},
    "Hamilton":   {"OVR": 91, "EXP": 99, "RAC": 92, "AWA": 95, "PAC": 91},
    "Piastri":    {"OVR": 90, "EXP": 65, "RAC": 90, "AWA": 86, "PAC": 92},
    "Sainz":      {"OVR": 89, "EXP": 84, "RAC": 90, "AWA": 92, "PAC": 88},
    "Russell":    {"OVR": 89, "EXP": 78, "RAC": 89, "AWA": 88, "PAC": 91},
    "Alonso":     {"OVR": 88, "EXP": 99, "RAC": 94, "AWA": 96, "PAC": 85},
    "Hulkenberg": {"OVR": 85, "EXP": 92, "RAC": 84, "AWA": 88, "PAC": 85},
    "Albon":      {"OVR": 85, "EXP": 76, "RAC": 84, "AWA": 86, "PAC": 86},
    "Gasly":      {"OVR": 84, "EXP": 82, "RAC": 84, "AWA": 85, "PAC": 84},
    "Perez":      {"OVR": 84, "EXP": 90, "RAC": 83, "AWA": 82, "PAC": 85},
    "Ocon":       {"OVR": 83, "EXP": 83, "RAC": 85, "AWA": 80, "PAC": 84},
    "Tsunoda":    {"OVR": 83, "EXP": 74, "RAC": 82, "AWA": 78, "PAC": 85},
    "Ricciardo2024":{"OVR":81, "EXP": 95, "RAC": 80, "AWA": 82, "PAC": 80},
    "Magnussen":  {"OVR": 80, "EXP": 88, "RAC": 85, "AWA": 75, "PAC": 80},
    "Bottas2024": {"OVR": 80, "EXP": 92, "RAC": 79, "AWA": 84, "PAC": 78},
    "Guanyu":     {"OVR": 78, "EXP": 70, "RAC": 78, "AWA": 76, "PAC": 77},
    "MickSchumacher":{"OVR":77, "EXP": 60, "RAC": 76, "AWA": 75, "PAC": 78},
    "De Vries":   {"OVR": 76, "EXP": 50, "RAC": 75, "AWA": 77, "PAC": 75},
    "Sargeant":   {"OVR": 75, "EXP": 55, "RAC": 74, "AWA": 72, "PAC": 78},
    "Pearce":     {"OVR": 65, "EXP": 40, "RAC": 64, "AWA": 65, "PAC": 66}, 
    "Hayes":      {"OVR": 64, "EXP": 35, "RAC": 65, "AWA": 62, "PAC": 65}, 

    # --- 2025 ROOKIES ---
    "Antonelli":  {"OVR": 81, "EXP": 30, "RAC": 80, "AWA": 75, "PAC": 86},
    "Bearman":    {"OVR": 81, "EXP": 45, "RAC": 82, "AWA": 80, "PAC": 82},
    "Colapinto":  {"OVR": 81, "EXP": 40, "RAC": 83, "AWA": 78, "PAC": 82},
    "Lawson":     {"OVR": 80, "EXP": 45, "RAC": 81, "AWA": 79, "PAC": 81},
    "Bortoleto":  {"OVR": 79, "EXP": 35, "RAC": 80, "AWA": 78, "PAC": 81},
    "Hadjar":     {"OVR": 79, "EXP": 35, "RAC": 82, "AWA": 75, "PAC": 82},

    # --- F2 DRIVERS (70-78 Range) ---
    "Mini":         {"OVR": 78, "EXP": 30, "RAC": 77, "AWA": 76, "PAC": 80},
    "Lindblad":     {"OVR": 78, "EXP": 20, "RAC": 76, "AWA": 74, "PAC": 82},
    "Fornaroli":    {"OVR": 77, "EXP": 35, "RAC": 79, "AWA": 80, "PAC": 76},
    "Browning":     {"OVR": 77, "EXP": 30, "RAC": 78, "AWA": 76, "PAC": 78},
    "Beganovic":    {"OVR": 76, "EXP": 30, "RAC": 75, "AWA": 75, "PAC": 78},
    "Martins":      {"OVR": 76, "EXP": 45, "RAC": 74, "AWA": 72, "PAC": 79},
    "Maini":        {"OVR": 75, "EXP": 40, "RAC": 75, "AWA": 74, "PAC": 76},
    "Crawford":     {"OVR": 75, "EXP": 45, "RAC": 76, "AWA": 75, "PAC": 75},
    "Verschoor":    {"OVR": 74, "EXP": 60, "RAC": 75, "AWA": 78, "PAC": 72},
    "Miyata":       {"OVR": 74, "EXP": 50, "RAC": 74, "AWA": 76, "PAC": 73},
    "Marti":        {"OVR": 73, "EXP": 30, "RAC": 72, "AWA": 70, "PAC": 76},
    "Dunne":        {"OVR": 73, "EXP": 25, "RAC": 75, "AWA": 71, "PAC": 75},
    "Goethe":       {"OVR": 72, "EXP": 30, "RAC": 71, "AWA": 73, "PAC": 73},
    "arthurLeclerc":{"OVR": 72, "EXP": 45, "RAC": 70, "AWA": 72, "PAC": 74},
    "Meguetounif":  {"OVR": 71, "EXP": 25, "RAC": 72, "AWA": 69, "PAC": 73},
    "Montoya":      {"OVR": 71, "EXP": 25, "RAC": 70, "AWA": 71, "PAC": 72},
    "Stanek":       {"OVR": 70, "EXP": 40, "RAC": 71, "AWA": 72, "PAC": 69},
    "Cordeel":      {"OVR": 70, "EXP": 45, "RAC": 68, "AWA": 70, "PAC": 70},
    "Esterson":     {"OVR": 69, "EXP": 20, "RAC": 69, "AWA": 68, "PAC": 70},
    "Shields":      {"OVR": 68, "EXP": 20, "RAC": 68, "AWA": 67, "PAC": 69},

    # --- F3 DRIVERS (60-69 Range) ---
    "Tramnitz":       {"OVR": 69, "EXP": 25, "RAC": 68, "AWA": 67, "PAC": 71},
    "Tsolov":         {"OVR": 68, "EXP": 25, "RAC": 69, "AWA": 65, "PAC": 70},
    "Taponen":        {"OVR": 68, "EXP": 15, "RAC": 67, "AWA": 66, "PAC": 72},
    "Stenshorne":     {"OVR": 68, "EXP": 20, "RAC": 68, "AWA": 67, "PAC": 69},
    "Câmara":         {"OVR": 67, "EXP": 15, "RAC": 66, "AWA": 65, "PAC": 70},
    "Boyo":           {"OVR": 67, "EXP": 25, "RAC": 67, "AWA": 68, "PAC": 66}, 
    "Boya":           {"OVR": 67, "EXP": 25, "RAC": 67, "AWA": 68, "PAC": 66},
    "Leon":           {"OVR": 66, "EXP": 20, "RAC": 65, "AWA": 67, "PAC": 66}, 
    "León":           {"OVR": 66, "EXP": 20, "RAC": 65, "AWA": 67, "PAC": 66},
    "Ugochukwu":      {"OVR": 66, "EXP": 15, "RAC": 64, "AWA": 63, "PAC": 69},
    "Voisin":         {"OVR": 66, "EXP": 20, "RAC": 66, "AWA": 68, "PAC": 65},
    "Strømsted":      {"OVR": 65, "EXP": 15, "RAC": 65, "AWA": 64, "PAC": 67},
    "Wharton":        {"OVR": 65, "EXP": 15, "RAC": 64, "AWA": 63, "PAC": 68},
    "Ramos":          {"OVR": 64, "EXP": 20, "RAC": 64, "AWA": 65, "PAC": 63},
    "Wurz":           {"OVR": 64, "EXP": 20, "RAC": 63, "AWA": 64, "PAC": 65},
    "Pino":           {"OVR": 63, "EXP": 15, "RAC": 64, "AWA": 62, "PAC": 64},
    "Naël":           {"OVR": 63, "EXP": 15, "RAC": 62, "AWA": 63, "PAC": 65},
    "Badoer":         {"OVR": 63, "EXP": 10, "RAC": 62, "AWA": 61, "PAC": 66},
    "Giusti":         {"OVR": 62, "EXP": 15, "RAC": 63, "AWA": 62, "PAC": 63},
    "Hoepen":         {"OVR": 62, "EXP": 20, "RAC": 61, "AWA": 64, "PAC": 62},
    "Zagazeta":       {"OVR": 62, "EXP": 20, "RAC": 62, "AWA": 60, "PAC": 63},
    "Bilinski":       {"OVR": 61, "EXP": 15, "RAC": 61, "AWA": 62, "PAC": 62},
    "Domingues":      {"OVR": 61, "EXP": 15, "RAC": 60, "AWA": 61, "PAC": 63},
    "Sharp":          {"OVR": 61, "EXP": 10, "RAC": 61, "AWA": 60, "PAC": 62},
    "Inthraphuvasak": {"OVR": 60, "EXP": 15, "RAC": 60, "AWA": 59, "PAC": 61},
    "Benavides":      {"OVR": 60, "EXP": 15, "RAC": 59, "AWA": 60, "PAC": 60},
    "Marinangeli":    {"OVR": 60, "EXP": 10, "RAC": 59, "AWA": 58, "PAC": 62},
    "Lacorte":        {"OVR": 59, "EXP": 10, "RAC": 58, "AWA": 59, "PAC": 60},
    "Johnson":        {"OVR": 59, "EXP": 10, "RAC": 59, "AWA": 58, "PAC": 59},
    "Xie":            {"OVR": 58, "EXP": 10, "RAC": 57, "AWA": 58, "PAC": 59},
    "Ho":             {"OVR": 58, "EXP": 10, "RAC": 58, "AWA": 57, "PAC": 58},
    "Hedley":         {"OVR": 58, "EXP": 10, "RAC": 57, "AWA": 56, "PAC": 59},

    # --- F4 DRIVERS (50-59 Range) ---
    "Nakamura":    {"OVR": 59, "EXP": 5, "RAC": 58, "AWA": 57, "PAC": 62},
    "Slater":      {"OVR": 58, "EXP": 10, "RAC": 57, "AWA": 58, "PAC": 60}, 
    "Saeter":      {"OVR": 58, "EXP": 10, "RAC": 57, "AWA": 58, "PAC": 60},
    "Gomez":       {"OVR": 57, "EXP": 5, "RAC": 56, "AWA": 55, "PAC": 60},
    "Bondarev":    {"OVR": 56, "EXP": 5, "RAC": 55, "AWA": 56, "PAC": 58},
    "Consani":     {"OVR": 56, "EXP": 5, "RAC": 56, "AWA": 54, "PAC": 57},
    "Olivieri":    {"OVR": 55, "EXP": 5, "RAC": 54, "AWA": 55, "PAC": 56},
    "Wheldon":     {"OVR": 55, "EXP": 5, "RAC": 55, "AWA": 54, "PAC": 56},
    "Hanna":       {"OVR": 54, "EXP": 5, "RAC": 53, "AWA": 55, "PAC": 55},
    "Popov":       {"OVR": 54, "EXP": 5, "RAC": 54, "AWA": 53, "PAC": 55},
    "Vinci":       {"OVR": 53, "EXP": 5, "RAC": 52, "AWA": 52, "PAC": 54},
    "Severiukhin": {"OVR": 53, "EXP": 5, "RAC": 53, "AWA": 51, "PAC": 54},
    "Chi":         {"OVR": 52, "EXP": 5, "RAC": 51, "AWA": 52, "PAC": 53},

    # --- ALL 11 TEAMS ---
    "Mclaren":     {"OVR": 95, "EXP": 90, "RAC": 92, "AWA": 88, "PAC": 98},
    "ferrari":     {"OVR": 93, "EXP": 99, "RAC": 91, "AWA": 85, "PAC": 95},
    "Redbull":     {"OVR": 92, "EXP": 95, "RAC": 94, "AWA": 92, "PAC": 92},
    "Mercedes":    {"OVR": 90, "EXP": 96, "RAC": 90, "AWA": 92, "PAC": 90},
    "AstonMartin": {"OVR": 83, "EXP": 85, "RAC": 82, "AWA": 84, "PAC": 82},
    "Alpine":      {"OVR": 82, "EXP": 90, "RAC": 81, "AWA": 76, "PAC": 83},
    "Haas":        {"OVR": 82, "EXP": 75, "RAC": 83, "AWA": 84, "PAC": 81},
    "VCARB":       {"OVR": 81, "EXP": 80, "RAC": 82, "AWA": 80, "PAC": 82},
    "Williams":    {"OVR": 80, "EXP": 98, "RAC": 80, "AWA": 78, "PAC": 80},
    "Cadillac":    {"OVR": 78, "EXP": 40, "RAC": 78, "AWA": 75, "PAC": 80},
    "Audi":        {"OVR": 75, "EXP": 85, "RAC": 76, "AWA": 78, "PAC": 75} 
}

def draw_card_stats(surface, driver_name, card_x, card_y):
    # --- BULLETPROOF DICTIONARY MATCHING ---
    clean_name = driver_name.replace(" ", "").lower()
    bulletproof_stats = {k.replace(" ", "").lower(): v for k, v in driver_stats.items()}
    
    stats = bulletproof_stats.get(clean_name, {"OVR": 75, "EXP": 75, "RAC": 75, "AWA": 75, "PAC": 75})
    # ---------------------------------------
    
    positions = {
        "OVR": (card_x + 30, card_y + 73),
        "EXP": (card_x + 21, card_y + 236),
        "RAC": (card_x + 69, card_y + 235),
        "AWA": (card_x + 115, card_y + 235),
        "PAC": (card_x + 163, card_y + 235),
    }

    for stat_name, position in positions.items():
        val_str = str(int(stats[stat_name])).zfill(2)
        x_offset = 0
        
        if stat_name == "OVR":
            current_dict = ovr_images
            spacing = OVR_W
        else:
            current_dict = stat_images
            spacing = STAT_W

        for digit in val_str:
            if digit in current_dict:
                surface.blit(current_dict[digit], (position[0] + x_offset, position[1]))
                x_offset += spacing
# ==========================================
# Track-relative checkpoints (where they sit on the 12800x7200 image)
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

my_checkpoint_index = 0  # Which gate are we looking for next?

silverstoneTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstone.png")).convert(), (12800,7200))
silverstoneTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneLine.png")).convert_alpha(), (12800,7200))
silverstoneMinimap = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneMinimap.png")), (256,144))

# --- STARTING GRID POSITIONS ---
bahrain_grid = [
    (-6550.0, -6261.0, 0),
    (-6653.0, -6132.0, 0),
    (-6750.0, -6254.0, 9),
    (-6846.0, -6104.0, 9),
    (-6959.0, -6264.0, 0),
    (-7061.0, -6119.0, 3),
    (-7172.0, -6241.0, 9),
    (-7270.0, -6133.0, 0),
    (-7379.0, -6255.0, -6),
    (-7477.0, -6135.0, 0)
]
silverstone_grid = []
# -------------------------------

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
Audi = pygame.image.load(os.path.join(script_dir, r"assets\Audi.png")).convert_alpha()
Cadillac = pygame.image.load(os.path.join(script_dir, r"assets\Cadillac.png")).convert_alpha()

car = Alpine
car_name = "Alpine"

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
    pygame.image.load(os.path.join(script_dir, r"assets\lights0.png")), (520, 560)
)
lights1 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, r"assets\lights1.png")), (520, 560)
)
lights2 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, r"assets\lights2.png")), (520, 560)
)
lights3 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, r"assets\lights3.png")), (520, 560)
)
lights4 = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, r"assets\lights4.png")), (520, 560)
)

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
crashbg = pygame.transform.scale(
    pygame.image.load(os.path.join(script_dir, r"assets\crash.png")), (1280, 720)
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
    global DRS, carDRS, car_name  # Explicitly add car_name here
    
    if DRS == False:
        # This ensures it uses the LATEST car_name selected in the menu
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

# MULTIPLAYER: Don't connect until the user wants to!
n = None 

# Car Grid definition for both selection and networking logic
all_teams = [
            (Mclaren, 20, 80, 'Mclaren'), (Mercedes, 180, 80, 'Mercedes'),
            (Redbull, 340, 80, 'Redbull'), (VCARB, 500, 80, 'VCARB'),
            (ferrari, 660, 80, 'ferrari'), (Williams, 820, 80, 'Williams'),
            (AstonMartin, 100, 350, 'AstonMartin'), (Haas, 260, 350, 'Haas'),
            (Audi, 420, 350, 'Audi'), (Alpine, 580, 350, 'Alpine'), 
            (Cadillac, 740, 350, 'Cadillac')
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
    #keyboard pressed
    keys = pygame.key.get_pressed()
    
    mouseX, mouseY = pygame.mouse.get_pos()

    # *********EVENTS**********
    for ev in pygame.event.get():    # controller toggle

        if ev.type == pygame.JOYDEVICEADDED:
            joystick = pygame.joystick.Joystick(ev.device_index)
            controller = True
        elif ev.type == pygame.JOYDEVICEREMOVED:
            controller = False 
        if ev.type == pygame.QUIT: 
            break                   
        # mouse click events
        # mouse click events
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                
                if gamestate == "main":
                    if 300 < mouseX < 940:
                        # --- UPDATED: 4-Button Layout with Market ---
                        if 220 < mouseY < 320: # RACE
                            if loggedInUser: gamestate = "carSelect" 
                        elif 340 < mouseY < 440: # MARKET
                            if loggedInUser: 
                                gamestate = "market"
                                market_search_input, market_msg, market_searched_img = "", "", None
                        elif 460 < mouseY < 560: # SETTINGS
                            gamestate = "settings"
                        elif 580 < mouseY < 680: # ONLINE
                            if loggedInUser:
                                gamestate = "onlineMenu"
                                if n is None or n.p is None: n = Network()
                        # --------------------------------------------
                        
                    # Account Button Click (Top Right)
                    elif 1050 < mouseX < 1250 and 30 < mouseY < 90:
                        gamestate = "accountMenu" if loggedInUser else "authMenu"

                # --- UPDATED: Market Screen Clicks ---
                elif gamestate == "market":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "main"
                        market_typing = False
                    
                    # Search Box Click
                    elif 300 < mouseX < 760 and 150 < mouseY < 230:
                        market_typing = True
                    else:
                        market_typing = False

                    # Click on a live search result
                    list_y = 250
                    for res in market_results:
                        if 300 < mouseX < 760 and list_y < mouseY < list_y + 50:
                            market_selected = res
                            market_msg = ""
                            try:
                                loaded = pygame.image.load(res["path"]).convert_alpha()
                                # --- UPDATED: Fixed aspect ratio to 228x300 ---
                                market_loaded_img = pygame.transform.scale(loaded, (228, 300))
                            except:
                                market_loaded_img = None
                        list_y += 60

                    # Purchase Button Click
                    if market_selected and market_loaded_img and 800 < mouseX < 1000 and 600 < mouseY < 660:
                        my_pts = user_points.get(loggedInUser, 0)
                        my_drivers = owned_drivers.get(loggedInUser, [])
                        card_name = market_selected["name"]
                        card_price = market_selected["price"]
                        
                        # --- NEW: List of valid playable teams ---
                        game_teams = ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]
                        
                        if card_name in my_drivers:
                            market_msg = "You already own this card!"
                        elif my_pts >= card_price:
                            user_points[loggedInUser] -= card_price
                            save_points()
                            
                            # 1. Add to your visual inventory
                            my_drivers.append(card_name)
                            owned_drivers[loggedInUser] = my_drivers
                            save_drivers()
                            
                            # 2. If it's a team, unlock it for racing!
                            for team in game_teams:
                                # We check in lowercase just in case your image file is named slightly differently (e.g. "Ferrari.png" vs "ferrari")
                                if card_name.lower() == team.lower():
                                    my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"])
                                    if team not in my_unlocked:
                                        my_unlocked.append(team)
                                        unlocked_cars[loggedInUser] = my_unlocked
                                        save_unlocked_cars()
                                    break # Stop searching once we find a match
                            
                            market_msg = f"Purchased {card_name}!"
                        else:
                            market_msg = f"Need {card_price - my_pts} more PTS."

                # --- NEW: Authentication Selection Menu ---
                elif gamestate == "authMenu":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "main"
                    elif 300 < mouseX < 940 and 270 < mouseY < 370: # Sign Up
                        gamestate = "signUp"
                        UsernameInputed, passwordInputed = "", ""
                        typing = False
                    elif 300 < mouseX < 940 and 430 < mouseY < 530: # Sign In
                        gamestate = "signIn"
                        UsernameInputed, passwordInputed = "", ""
                        typing = False

                # --- NEW: Sign Up & Sign In Menus ---
                elif gamestate == "signUp" or gamestate == "signIn":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "authMenu"
                        typing = False
                    
                    # Input boxes selection (Adjusted heights to fit 3 boxes)
                    elif 300 < mouseX < 940 and 150 < mouseY < 230:
                        typing, UsernameTyping, passwordTyping, abbrTyping = True, True, False, False
                    elif 300 < mouseX < 940 and 260 < mouseY < 340:
                        typing, passwordTyping, UsernameTyping, abbrTyping = True, True, False, False
                    elif gamestate == "signUp" and 300 < mouseX < 940 and 370 < mouseY < 450:
                        typing, abbrTyping, UsernameTyping, passwordTyping = True, True, False, False
                    else:
                        typing = False

                    # Submit Buttons
                    if 440 < mouseX < 840 and 480 < mouseY < 560:
                        if gamestate == "signUp":
                            # Require exactly 3 letters for the tag
                            if not UsernameExist and UsernameInputed != "" and passwordInputed != "" and len(abbrInputed) == 3:
                                users[UsernameInputed] = passwordInputed
                                save_accounts()
                                
                                # Save the 3-letter tag
                                user_abbrs[UsernameInputed] = abbrInputed.upper()
                                save_abbrs()
                                
                                if UsernameInputed not in unlocked_cars:
                                    unlocked_cars[UsernameInputed] = ["Alpine"]
                                    save_unlocked_cars()
                                
                                loggedInUser = UsernameInputed
                                gamestate = "main"
                                
                        elif gamestate == "signIn":
                            if UsernameInputed in users and users[UsernameInputed] == passwordInputed:
                                loggedInUser = UsernameInputed
                                gamestate = "main"

                # --- Account Info Menu Clicks ---
                elif gamestate == "accountMenu":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "main"
                    elif 440 < mouseX < 840 and 550 < mouseY < 630: # Sign Out Button
                        loggedInUser = None
                        gamestate = "main"
                        
                    # --- NEW: View Cards Button Click ---
                    elif 750 < mouseX < 1150 and 280 < mouseY < 360:
                        gamestate = "inventory"
                        inventory_page = 0
                        # Pre-load the card images so the grid is fast!
                        my_drivers = owned_drivers.get(loggedInUser, [])
                        for drv in my_drivers:
                            if drv not in inventory_loaded_imgs:
                                path = find_driver_card(drv)
                                if path:
                                    try:
                                        img = pygame.image.load(path).convert_alpha()
                                        # Scale for grid (190x250) keeps the aspect ratio
                                        inventory_loaded_imgs[drv] = pygame.transform.scale(img, (228, 300)) 
                                    except: pass

                # --- NEW: Inventory Screen Clicks ---
                elif gamestate == "inventory":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "accountMenu"
                        
                    my_drivers = owned_drivers.get(loggedInUser, [])
                    max_pages = max(0, (len(my_drivers) - 1) // 8)
                    
                    # Pagination Clicks
                    if 50 < mouseX < 150 and 330 < mouseY < 390 and inventory_page > 0:
                        inventory_page -= 1
                    elif 1130 < mouseX < 1230 and 330 < mouseY < 390 and inventory_page < max_pages:
                        inventory_page += 1

                elif gamestate == "onlineMenu": 
                    # --- ADD THIS BACK BUTTON LOGIC ---
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"
                    
                    # Host Button 
                    elif 300 < mouseX < 940 and 270 < mouseY < 370: 
                        if n is not None and n.p is not None:
                            reply = n.send(["CREATE", [trackX, trackY, angle, car_name, "LOBBY"]])
                            if reply:
                                my_lobby_id, my_player_index = reply[0], reply[1]
                                gamestate = "hostLobby"
                                
                    # Join Button
                    elif 300 < mouseX < 940 and 430 < mouseY < 530:
                        if n is not None and n.p is not None:
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
                            
                            # --- UPDATED: Require at least 2 players to start ---
                            can_start = False
                            if isinstance(lobby_data, list):
                                active_players = [p for p in lobby_data if p is not None]
                                if len(active_players) >= 2:
                                    can_start = True
                                    # Ensure no one is currently stuck in a racing state
                                    for p in active_players:
                                        if len(p) > 4 and p[4] == "RACING":
                                            can_start = False
                                            break
                            # ----------------------------------------------------
                            
                            if can_start:
                                gamestate = "start"
                                
                                # --- CALCULATE RANDOM GRID ORDER ---
                                active_p = [i for i, p in enumerate(lobby_data) if p is not None]
                                random.shuffle(active_p)
                                my_grid_order = active_p
                                
                                # Find our own spot in the shuffled list
                                my_pos_index = my_grid_order.index(my_player_index)
                                
                                # Reset coordinates based on randomized grid assignment
                                if currentTrack == bahrainTrack and len(bahrain_grid) > my_pos_index:
                                    trackX, trackY, angle = bahrain_grid[my_pos_index]
                                elif currentTrack == silverstoneTrack: 
                                    trackX, trackY, angle = -7270.0, -5668.0, -39
                                
                                my_checkpoint_index = 0
                                lightSound.set_volume(1)
                                lightSound.play() 
                                time = -7
                                lap = 0
                                points_awarded = False
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
                    my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]
                    
                    for img, x, y, name in all_teams:
                        if x < mouseX < x + 185 and y < mouseY < y + 274:
                            # --- UPDATED: Allow selection if it's unlocked AND (not taken OR is Alpine) ---
                            if (name not in taken_cars or name == "Alpine") and name in my_unlocked:
                                car = img
                                car_name = name 
                                
                                speed_map = {'Mclaren': 15, 'Mercedes': 14.5, 'Redbull': 14, 'VCARB': 13.5, 
                                            'ferrari': 13, 'Williams': 12.5, 'AstonMartin': 12, 
                                            'Haas': 11.5, 'Audi': 11, 'Alpine': 10.5, 'Cadillac': 10}
                                maxSpeed = speed_map[name]
                                carMaxSpeed = maxSpeed

                # stats screen back to main menu
                elif gamestate == "stats":
                    # PLAY AGAIN BUTTON
                    if 320 < mouseX < 620 and 600 < mouseY < 680:
                        # Go to lobby if online, or track select if offline
                        gamestate = "hostLobby" if my_lobby_id is not None else "ChooseTrack"
                        lap = 0
                        points_awarded = False
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
                        points_awarded = False
                        lap1time, lap2time, lap3time = 0, 0, 0
                        speed = 0
                        lightsOut = False
                        lights = -1
                        if n is not None and n.p is not None and my_lobby_id is not None:
                            n.send(["LEAVE", my_lobby_id, my_player_index])
                        my_lobby_id = None
                        my_player_index = None
                        taken_cars = []

                # track selection screen
                if gamestate == "ChooseTrack":
                    # bahrain track selection
                    if 480 < mouseX < 835 and 50 < mouseY < 287:
                        currentTrack = bahrainTrack
                        gamestate = "start"
                        
                        # --- SINGLE PLAYER DEFAULTS TO POLE POSITION ---
                        trackX, trackY, angle = bahrain_grid[0]
                        # -----------------------------------------------
                        
                        lightSound.set_volume(100)
                        lightSound.play() 
                        lap = 0
                        points_awarded = False
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
                        points_awarded = False
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
                # car selection screen updates
                if gamestate == "carSelect":
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        gamestate = "main"
                        
                    # --- SIDEBAR BUTTON CLICKS ---
                    elif 950 < mouseX < 1200 and 590 < mouseY < 670: # CONFIRM RACE
                        gamestate = "ChooseTrack"
                    elif 950 < mouseX < 1200 and 490 < mouseY < 570: # REPLACE DRIVER
                        gamestate = "driverSelect"
                        inventory_page = 0
                        my_drivers = owned_drivers.get(loggedInUser, [])
                        for drv in my_drivers:
                            if drv not in inventory_loaded_imgs:
                                path = find_driver_card(drv)
                                if path:
                                    try:
                                        img = pygame.image.load(path).convert_alpha()
                                        inventory_loaded_imgs[drv] = pygame.transform.scale(img, (228, 300)) 
                                    except: pass
                    # -----------------------------
                    else:
                        car_select_grid = [
                            (Mclaren, 50, 80, "Mclaren", 15), (Mercedes, 190, 80, "Mercedes", 14.5),
                            (Redbull, 330, 80, "Redbull", 14), (VCARB, 470, 80, "VCARB", 13.5),
                            (ferrari, 610, 80, "ferrari", 13), (Williams, 750, 80, "Williams", 12.5),
                            (AstonMartin, 120, 360, "AstonMartin", 12), (Haas, 260, 360, "Haas", 11.5),
                            (Audi, 400, 360, "Audi", 11), (Alpine, 540, 360, "Alpine", 10.5), 
                            (Cadillac, 680, 360, "Cadillac", 10)
                        ]
                        
                        my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]

                        for img, x, y, name, speed_val in car_select_grid:
                            if x < mouseX < x + 130 and y < mouseY < y + 195:
                                if name in my_unlocked:
                                    car = img
                                    car_name = name
                                    
                                    # --- UPDATED: Fetch driver specific to THIS car ---
                                    user_squads = active_driver.get(loggedInUser, {})
                                    if not isinstance(user_squads, dict): user_squads = {} # Safety check for old saves
                                    my_drv = user_squads.get(name, "None")
                                    
                                    carMaxSpeed = get_boosted_speed(speed_val, my_drv)
                                    maxSpeed = carMaxSpeed
                                    # --------------------------------------------------

                # --- UPDATED: Driver Select Clicks (Squad Builder) ---
                elif gamestate == "driverSelect":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "carSelect"
                        squad_typing = False
                    
                    # Search Box Click
                    elif 400 < mouseX < 860 and 25 < mouseY < 75:
                        squad_typing = True
                    else:
                        squad_typing = False

                    # 1. Fetch raw drivers and filter out teams!
                    raw_drivers = owned_drivers.get(loggedInUser, [])
                    game_teams_lower = [t.lower() for t in ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]]
                    
                    filtered_drivers = [d for d in raw_drivers if d.lower() not in game_teams_lower]
                    
                    # 2. Apply search filter
                    if squad_search_input:
                        filtered_drivers = [d for d in filtered_drivers if squad_search_input.lower() in d.lower()]

                    max_pages = max(0, (len(filtered_drivers) - 1) // 8)
                    
                    if 50 < mouseX < 150 and 330 < mouseY < 390 and inventory_page > 0: inventory_page -= 1
                    elif 1130 < mouseX < 1230 and 330 < mouseY < 390 and inventory_page < max_pages: inventory_page += 1

                    # Click to Equip Driver
                    start_x, start_y, x_spacing, y_spacing = 70, 110, 290, 320 
                    start_idx = inventory_page * 8
                    end_idx = min(start_idx + 8, len(filtered_drivers))
                    
                    for i in range(start_idx, end_idx):
                        row, col = (i - start_idx) // 4, (i - start_idx) % 4
                        draw_x = start_x + (col * x_spacing)
                        draw_y = start_y + (row * y_spacing)
                        
                        if draw_x < mouseX < draw_x + 228 and draw_y < mouseY < draw_y + 300: 
                            
                            if loggedInUser not in active_driver or not isinstance(active_driver[loggedInUser], dict):
                                active_driver[loggedInUser] = {}
                            
                            # --- NEW: UNEQUIP FROM OTHER CARS FIRST ---
                            target_driver = filtered_drivers[i]
                            
                            # Loop through all your cars and remove this driver if they are equipped elsewhere
                            for existing_car, existing_driver in list(active_driver[loggedInUser].items()):
                                if existing_driver == target_driver:
                                    active_driver[loggedInUser][existing_car] = "None"
                            # ------------------------------------------
                            
                            # Equip the driver to the CURRENT car
                            active_driver[loggedInUser][car_name] = target_driver
                            save_active_driver()
                            
                            base_speed = 10
                            speed_map = {'Mclaren': 15, 'Mercedes': 14.5, 'Redbull': 14, 'VCARB': 13.5, 'ferrari': 13, 'Williams': 12.5, 'AstonMartin': 12, 'Haas': 11.5, 'Audi': 11, 'Alpine': 10.5, 'Cadillac': 10}
                            if car_name in speed_map: base_speed = speed_map[car_name]
                            
                            carMaxSpeed = get_boosted_speed(base_speed, target_driver)
                            maxSpeed = carMaxSpeed
                            gamestate = "carSelect"
                            squad_typing = False
                # -------------------------------------------------


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
            
            # --- NEW: SQUAD BUILDER SEARCH VARIABLES ---
            # (If these aren't initialized at the top of your file, Python will create them here)
            if 'squad_search_input' not in globals(): squad_search_input = ""
            if 'squad_typing' not in globals(): squad_typing = False
            # -------------------------------------------

            if typing and (gamestate == "signUp" or gamestate == "signIn"):
                # ... (Keep your existing sign up typing logic) ...
                pass

            if market_typing and gamestate == "market":
                # ... (Keep your existing market typing logic) ...
                pass

            # --- NEW: SQUAD BUILDER TYPING LOGIC ---
            if squad_typing and gamestate == "driverSelect":
                if ev.key == pygame.K_BACKSPACE:
                    squad_search_input = squad_search_input[:-1]
                elif ev.key == pygame.K_RETURN:
                    squad_typing = False
                else:
                    if len(squad_search_input) <= 20 and (ev.unicode.isalpha() or ev.key == pygame.K_SPACE):
                        squad_search_input += ev.unicode
            # ---------------------------------------
            # --- NEW: Typing Logic ---
            if typing and (gamestate == "signUp" or gamestate == "signIn"):
                if ev.key == pygame.K_BACKSPACE:
                    if UsernameTyping: UsernameInputed = UsernameInputed[:-1]
                    if passwordTyping: passwordInputed = passwordInputed[:-1]
                    if abbrTyping: abbrInputed = abbrInputed[:-1]
                elif ev.key == pygame.K_RETURN:
                    typing = False
                elif ev.key != pygame.K_SPACE:
                    if UsernameTyping and len(UsernameInputed) <= 17: UsernameInputed += ev.unicode
                    if passwordTyping and len(passwordInputed) <= 17:
                        passwordInputed += ev.unicode
                        last_key_time = pygame.time.get_ticks()
                        show_last_char = True
                    
                    # Limit tag to 3 alphabetical characters and force uppercase
                    if abbrTyping and len(abbrInputed) < 3 and ev.unicode.isalpha():
                        abbrInputed += ev.unicode.upper()

                UsernameExist = UsernameInputed in users

            # --- UPDATED: Market Typing (Live Search) ---
            if market_typing and gamestate == "market":
                if ev.key == pygame.K_BACKSPACE:
                    market_search_input = market_search_input[:-1]
                elif ev.key == pygame.K_RETURN:
                    market_typing = False
                else:
                    if len(market_search_input) <= 20 and (ev.unicode.isalpha() or ev.key == pygame.K_SPACE):
                        market_search_input += ev.unicode
                
                # Trigger live search on every keystroke
                market_results = search_driver_cards(market_search_input)
                market_selected = None # Clear selection when typing
                market_msg = ""

            # ... Your existing KEYDOWN events (DRS, Gears) continue below ...
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

    # ==================================================
    # --- MULTIPLAYER SYNC BLOCK ---
    # ==================================================
    current_time = pygame.time.get_ticks()

    if current_time - last_network_update > 30:
        last_network_update = current_time 

        if n is not None and n.p is not None and my_lobby_id is not None:
            if gamestate == "start": my_status = "RACING"
            elif gamestate == "stats": my_status = "FINISHED"
            else: my_status = "LOBBY"
            # Get your custom tag, default to "PLY" if something goes wrong
            my_abbr = user_abbrs.get(loggedInUser, "PLY") if loggedInUser else "GUE"
            
            # INCLUDE THE GRID ORDER AND ABBREVIATION IN THE UPDATE
            lobby_data = n.send(["UPDATE", my_lobby_id, my_player_index,[trackX, trackY, angle, car_name, my_status, my_checkpoint_index, lap, my_grid_order, my_abbr]])

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
                
                # --- ENFORCE UNIQUE AND UNLOCKED CARS ---
                if gamestate == "hostLobby":
                    my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]
                    
                    # UPDATED: Ignore if our current car is Alpine, otherwise check if it was taken
                    if (car_name in taken_cars and car_name != "Alpine") or car_name not in my_unlocked:
                        for img, x, y, name in all_teams:
                            # UPDATED: Auto-equip the first available car (Alpine is always available)
                            if (name not in taken_cars or name == "Alpine") and name in my_unlocked:
                                car = img
                                car_name = name
                                speed_map = {'Mclaren': 15, 'Mercedes': 14.5, 'Redbull': 14, 'VCARB': 13.5, 
                                            'ferrari': 13, 'Williams': 12.5, 'AstonMartin': 12, 
                                            'Haas': 11.5, 'Audi': 11, 'Alpine': 10.5, 'Cadillac': 10}
                                
                                # --- UPDATED: Multiplayer Speed Boost (Per-Car) ---
                                user_squads = active_driver.get(loggedInUser, {})
                                if not isinstance(user_squads, dict): user_squads = {}
                                my_drv = user_squads.get(name, "None")
                                
                                maxSpeed = get_boosted_speed(speed_map[name], my_drv)
                                carMaxSpeed = maxSpeed
                                # --------------------------------------------------
                                break
                # --------------------------------

                # Pull clients into race
                if gamestate == "hostLobby" and my_player_index != 0: 
                    host_data = lobby_data[0] 
                    if isinstance(host_data, list) and len(host_data) > 7 and host_data[4] == "RACING" and host_data[6] == 0:
                        gamestate = "start"
                        
                        # --- RETRIEVE GRID POSITION FROM HOST ---
                        host_grid_order = host_data[7]
                        my_pos_index = 0
                        if my_player_index in host_grid_order:
                            my_pos_index = host_grid_order.index(my_player_index)
                        
                        if currentTrack == bahrainTrack and len(bahrain_grid) > my_pos_index:
                            trackX, trackY, angle = bahrain_grid[my_pos_index]
                        elif currentTrack == silverstoneTrack: 
                            trackX, trackY, angle = -7270.0, -5668.0, -39
                        # -----------------------------------------
                        
                        my_checkpoint_index = 0
                        lightSound.set_volume(1)
                        lightSound.play() 
                        time = -7
                        lap = 0
                        points_awarded = False # <-- ADD THIS LINE
                        lap1time = 0
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
        # Calculate your car's position on the actual 12800x7200 track
        player_track_x = -trackX + 640
        player_track_y = -trackY + 360

        # Check if you hit the NEXT checkpoint
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

        # Create a 1280x720 camera window based on your coordinates
        camera_rect = pygame.Rect(int(-trackX), int(-trackY), windowWidth, windowHeight)

        # draw track using the camera 'area'
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
            elif car == Audi and centerColor == (14, 167, 24):
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Alpine and centerColor == (161, 108, 144):
                speed = 0
                pitstopReset()
                pitstop = False
            # --- NEW: Cadillac Pitstop ---
            elif car == Cadillac and centerColor == (255, 255, 0): # Bright yellow pixel trigger
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
        # --- DRAW OPPONENTS ---
        # ==================================================
        if isinstance(lobby_data, list):
            car_images = {
                "ferrari": ferrari, "Mclaren": Mclaren, "Mercedes": Mercedes,
                "Redbull": Redbull, "VCARB": VCARB, "Williams": Williams,
                "AstonMartin": AstonMartin, "Haas": Haas, "Audi": Audi,
                "Alpine": Alpine, "Cadillac": Cadillac
            }

            for i, p in enumerate(lobby_data):
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
                team_abbr = p_info[8] if len(p_info) > 8 else p_info[3][:3].upper()
                name_text = f1font2.render(team_abbr, True, "white")
                screen.blit(name_text, (start_x + 65, y_pos + 7))

                # 3. Lap Info (Right aligned)
                lap_text = f1font2.render(f"Lap {p_info[6]}", True, (200, 200, 200))
                screen.blit(lap_text, (start_x + box_width - 100, y_pos + 7))
        # ==================================================
    
    # start menu
    if gamestate == "main":
        pygame.mixer.stop()
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        screen.blit(f1logo, (440,100))
        
        # --- UPDATED: Removed Car button, re-spaced the remaining 3 ---
        # format: (y_position, label, requires_login)
        menu_buttons = [
            (220, 'Race', True), 
            (340, 'Market', True), 
            (460, 'Settings', False), 
            (580, 'Online', True)
        ]
        # --------------------------------------------------------------

        for y_pos, label, requires_login in menu_buttons:
            # Check if this specific button should be locked
            is_disabled = requires_login and not loggedInUser
            
            if is_disabled:
                # Draw dark grey locked button
                pygame.draw.rect(screen, (100, 100, 100), (300, y_pos, 640, 100), 0, 20)
                text_surf = f1font.render(label, True, (150, 150, 150))
                
                # Optional: Add a little lock icon/text indicator
                screen.blit(f1font2.render("LOCKED", True, (200, 50, 50)), (320, y_pos + 35))
            else:
                # Normal hover and draw logic
                if 300 < mouseX < 940 and y_pos < mouseY < y_pos + 100:
                    pygame.draw.rect(screen, ("white"), (300, y_pos, 640, 100), 0, 20)
                else:
                    pygame.draw.rect(screen, (220, 220, 220), (300, y_pos, 640, 100), 0, 20)
                text_surf = f1font.render(label, True, ("black"))
            
            # Center the text perfectly
            text_rect = text_surf.get_rect(center=(620, y_pos + 50)) 
            screen.blit(text_surf, text_rect)

        # Draw Account Button in Main Menu
        if 1050 < mouseX < 1250 and 30 < mouseY < 90:
            pygame.draw.rect(screen, ("white"), (1050, 30, 200, 60), 0, 15)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (1050, 30, 200, 60), 0, 15)
        
        acc_label = loggedInUser if loggedInUser else "Account"
        acc_surf = f1font2.render(acc_label[:10], True, "black")
        screen.blit(acc_surf, acc_surf.get_rect(center=(1150, 60)))


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

            # ==========================================
            # --- NEW: AWARD POINTS ONCE (Online Only) ---
            if not points_awarded and loggedInUser and my_lobby_id is not None:
                my_position = 0
                my_data = lobby_data[my_player_index] if len(lobby_data) > my_player_index else None
                
                # Find where our exact data sits in the sorted leaderboard
                if my_data:
                    for idx, p_info in enumerate(players_ranking):
                        if p_info == my_data:
                            my_position = idx + 1 # 1st place is index 0
                            break
                
                # Official F1 Points distribution
                points_map = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
                earned_points = points_map.get(my_position, 0)
                
                if earned_points > 0:
                    current_points = user_points.get(loggedInUser, 0)
                    user_points[loggedInUser] = current_points + earned_points
                    save_points()
                
                points_awarded = True # Lock it so we don't award points again!
            # ==========================================

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
                team_abbr = p_info[8] if len(p_info) > 8 else p_info[3][:3].upper()
                screen.blit(f1font2.render(team_abbr, True, "white"), (start_x + 65, y_pos + 7))

                # --- NEW: Display Points Earned ---
                points_map = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
                earned_pts = points_map.get(idx + 1, 0)
                
                # Only show points if they actually finished the race (Lap > 3)
                if p_info[6] > 3 and earned_pts > 0:
                    pts_text = f"+{earned_pts} PTS"
                    # Draw in gold color, perfectly spaced between the name and the status
                    screen.blit(f1font2.render(pts_text, True, (255, 215, 0)), (start_x + box_width - 280, y_pos + 7))
                # ----------------------------------

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
        
        # back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # ==========================================
        # --- THE GLASS SIDEBAR (Right Side) ---
        sidebar = pygame.Surface((380, 720), pygame.SRCALPHA)
        sidebar.fill((20, 20, 20, 220)) 
        screen.blit(sidebar, (900, 0))
        
        # --- Fetch driver specific to the active car ---
        user_squads = active_driver.get(loggedInUser, {})
        if not isinstance(user_squads, dict): user_squads = {}
        my_drv = user_squads.get(car_name, "None")
        # -----------------------------------------------

        # 1. Auto-Load the Active Driver's Image if missing
        if my_drv != "None" and my_drv not in inventory_loaded_imgs:
            path = find_driver_card(my_drv)
            if path:
                try:
                    img = pygame.image.load(path).convert_alpha()
                    inventory_loaded_imgs[my_drv] = pygame.transform.scale(img, (228, 300)) 
                except: pass

        # 2. Draw Active Driver Card (Top)
        if my_drv in inventory_loaded_imgs:
            card_x, card_y = 976, 20 # Centered perfectly in the sidebar
            screen.blit(inventory_loaded_imgs[my_drv], (card_x, card_y))
            draw_card_stats(screen, my_drv, card_x, card_y)
        else:
            pygame.draw.rect(screen, (50, 50, 50), (976, 20, 228, 300), 0, 10)
            screen.blit(f1font2.render("NO DRIVER", True, (150, 150, 150)), (1000, 150))

        # 3. Dynamic Speed Stats (Shifted Down!)
        base = 10
        speed_map = {'Mclaren': 15, 'Mercedes': 14.5, 'Redbull': 14, 'VCARB': 13.5, 'ferrari': 13, 'Williams': 12.5, 'AstonMartin': 12, 'Haas': 11.5, 'Audi': 11, 'Alpine': 10.5, 'Cadillac': 10}
        if car_name in speed_map: base = speed_map[car_name]
        
        screen.blit(f1font2.render(f"Car: {car_name.upper()}", True, "white"), (950, 330))

        pygame.draw.rect(screen, (40, 40, 40), (950, 370, 280, 100), 0, 15)
        screen.blit(f1font2.render(f"Base Spd: {base}", True, (200, 200, 200)), (970, 385))
        screen.blit(f1font2.render(f"TOP SPD: {round(carMaxSpeed, 1)}", True, (255, 215, 0)), (970, 425))

        # 4. REPLACE Button
        if 950 < mouseX < 1230 and 490 < mouseY < 570: pygame.draw.rect(screen, (100, 200, 255), (950, 490, 280, 80), 0, 15)
        else: pygame.draw.rect(screen, (50, 150, 255), (950, 490, 280, 80), 0, 15)
        equip_text = f1font2.render("REPLACE", True, "black")
        screen.blit(equip_text, equip_text.get_rect(center=(1090, 530)))

        # 5. CONFIRM RACE Button
        if 950 < mouseX < 1230 and 590 < mouseY < 670: pygame.draw.rect(screen, (100, 255, 100), (950, 590, 280, 80), 0, 15)
        else: pygame.draw.rect(screen, (50, 200, 50), (950, 590, 280, 80), 0, 15)
        conf_text = f1font2.render("CONFIRM", True, "black")
        screen.blit(conf_text, conf_text.get_rect(center=(1090, 630)))
        # ==========================================

        # --- REFACTORED CAR DRAWING WITH LOCKS ---
        car_select_grid = [
            (Mclaren, 50, 80, "Mclaren"), (Mercedes, 190, 80, "Mercedes"),
            (Redbull, 330, 80, "Redbull"), (VCARB, 470, 80, "VCARB"),
            (ferrari, 610, 80, "ferrari"), (Williams, 750, 80, "Williams"),
            (AstonMartin, 120, 360, "AstonMartin"), (Haas, 260, 360, "Haas"),
            (Audi, 400, 360, "Audi"), (Alpine, 540, 360, "Alpine"), 
            (Cadillac, 680, 360, "Cadillac")
        ]

        my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]

        for img, x, y, name in car_select_grid:
            is_hovered = x < mouseX < x + 130 and y < mouseY < y + 195
            
            # Base scaled sizes
            normal_size = (110, 165)
            hover_size = (130, 195)
            
            if name not in my_unlocked:
                # Sleek Silhouette Lock
                gray_car = pygame.transform.scale(pygame.transform.rotate(img, -90), normal_size)
                gray_car.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT) # Darker silhouette
                screen.blit(gray_car, (x + 10, y + 15))
                
                # Small badge instead of huge text
                pygame.draw.rect(screen, (200, 50, 50), (x + 20, y + 150, 90, 30), 0, 5)
                screen.blit(pygame.font.SysFont("Arial", 16, bold=True).render("LOCKED", True, "white"), (x + 32, y + 156))
            else:
                # Draw Normal Unlocked Car
                if is_hovered or car == img:
                    # Pop out slightly when selected
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), hover_size), (x, y))
                    if car == img: # Draw a subtle green glow ring for the active car
                        pygame.draw.rect(screen, (100, 255, 100), (x-5, y-5, 140, 205), 3, 15)
                else:
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), normal_size), (x + 10, y + 15))
    # --- UPDATED: Market Screen Visuals ---
    elif gamestate == "market":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Title & Points
        screen.blit(f1font.render("Driver Market", True, ("white")), (450, 60))
        my_pts = user_points.get(loggedInUser, 0)
        screen.blit(f1font2.render(f"Balance: {my_pts} PTS", True, (255, 215, 0)), (950, 60))

        # Search Box (Left Side)
        pygame.draw.rect(screen, "white", (300, 150, 460, 80), 0, 15)
        if market_typing: pygame.draw.rect(screen, (100, 200, 255), (300, 150, 460, 80), 5, 15)
        s_text = f1font.render(market_search_input if market_search_input else "Search Driver...", True, (0,0,0) if market_search_input else (150,150,150))
        screen.blit(s_text, (320, 165))

        # Draw Live Search Results
        list_y = 250
        for res in market_results:
            # Hover effect
            if 300 < mouseX < 760 and list_y < mouseY < list_y + 50:
                pygame.draw.rect(screen, (200, 200, 200), (300, list_y, 460, 50), 0, 10)
            else:
                pygame.draw.rect(screen, (50, 50, 50), (300, list_y, 460, 50), 0, 10)
            
            # Name and Price
            screen.blit(f1font2.render(res["name"], True, "white"), (310, list_y + 10))
            screen.blit(f1font2.render(f"{res['price']} PTS", True, (255, 215, 0)), (620, list_y + 10))
            list_y += 60

        # Draw Selected Card Preview (Right Side)
        if market_selected and market_loaded_img:
            
            # 1. Draw the Base Card
            screen.blit(market_loaded_img, (800, 280))
            
            # --- NEW: 2. Overlay the Dynamic Ratings ---
            draw_card_stats(screen, market_selected["name"], 800, 280)
            # -----------------------------------------
            
            # Draw Purchase Button
            if 800 < mouseX < 1000 and 600 < mouseY < 660: pygame.draw.rect(screen, (100, 255, 100), (800, 600, 200, 60), 0, 15)
            else: pygame.draw.rect(screen, (50, 200, 50), (800, 600, 200, 60), 0, 15)
            screen.blit(f1font2.render(f"BUY ({market_selected['price']})", True, "black"), (820, 615))

        # Status Message
        if market_msg:
            msg_color = (100, 255, 100) if "Purchased" in market_msg else (255, 100, 100)
            screen.blit(f1font2.render(market_msg, True, msg_color), (450, 200 if not market_selected else 620))

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

    # online selection menu
    elif gamestate == "onlineMenu":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Host Button
        if 300 < mouseX < 940 and 270 < mouseY < 370:
            pygame.draw.rect(screen, ("white"), (300, 270, 640, 100), 0, 20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 270, 640, 100), 0, 20)
        screen.blit(f1font.render('Host', True, ("black")), (520, 290))

        # Join Button
        if 300 < mouseX < 940 and 430 < mouseY < 530:
            pygame.draw.rect(screen, ("white"), (300, 430, 640, 100), 0, 20)
        else:
            pygame.draw.rect(screen, (220, 220, 220), (300, 430, 640, 100), 0, 20)
        screen.blit(f1font.render('Join', True, ("black")), (530, 450))

        # --- CONNECTION STATUS FEEDBACK ---
        if n is None or n.p is None:
            error_msg = "ERROR: Cannot reach server. Playing Offline."
            screen.blit(f1font2.render(error_msg, True, (255, 50, 50)), (350, 600))
        else:
            success_msg = "Connected to Official F1 Server"
            screen.blit(f1font2.render(success_msg, True, (50, 255, 50)), (400, 600))
        # ---------------------------------------
    
    elif gamestate == "hostLobby":
        screen.blit(menu, (0,0))
        
        # --- DRAW START BUTTON (HOST ONLY) ---
        if my_player_index == 0:
            
            # --- UPDATED: Require at least 2 players to draw the green button ---
            can_start = False
            active_count = 0
            if isinstance(lobby_data, list):
                active_players = [p for p in lobby_data if p is not None]
                active_count = len(active_players)
                if active_count >= 2:
                    can_start = True
                    for p in active_players:
                        if len(p) > 4 and p[4] == "RACING":
                            can_start = False
                            break
            # --------------------------------------------------------------------
            
            if can_start:
                # Normal Green Button
                if 440 < mouseX < 840 and 630 < mouseY < 690:
                    pygame.draw.rect(screen, (100, 255, 100), (440, 630, 400, 60), 0, 15) 
                else:
                    pygame.draw.rect(screen, (50, 200, 50), (440, 630, 400, 60), 0, 15) 
                screen.blit(f1font2.render("START RACE", True, "black"), (545, 645))
            else:
                # Disabled Gray Button
                pygame.draw.rect(screen, (150, 150, 150), (440, 630, 400, 60), 0, 15)
                
                # Contextual text so the host knows what they are waiting for
                if active_count < 2:
                    btn_text = "NEED MORE PLAYERS"
                    text_x = 480
                else:
                    btn_text = "WAITING ON RACERS..."
                    text_x = 460
                    
                screen.blit(f1font2.render(btn_text, True, "black"), (text_x, 645))
        else:
            # Tell other players to hang tight
            screen.blit(f1font2.render("Waiting for Host to start...", True, "white"), (480, 645))
        # ------------------------------------------
        
        # --- DRAW LEAVE LOBBY BUTTON (Top Right) ---
        if 1050 < mouseX < 1250 and 30 < mouseY < 90:
            # Lighter red when hovered
            pygame.draw.rect(screen, (255, 100, 100), (1050, 30, 200, 60), 0, 15) 
        else:
            # Dark red normally
            pygame.draw.rect(screen, (200, 50, 50), (1050, 30, 200, 60), 0, 15)   
        
        screen.blit(f1font2.render("LEAVE", True, "white"), (1100, 45))

        # Dynamic Capacity Display
        pygame.draw.rect(screen, (40, 40, 40), (300, 20, 640, 80), 0, 20)
        # Inject the my_lobby_id variable here
        cap_text = f"LOBBY #{my_lobby_id}  |  CAPACITY: {players_connected}/10"
        screen.blit(f1font2.render(cap_text, True, "white"), (420, 45))

        # Car Grid with Exclusivity AND Locks
        all_teams = [
            (Mclaren, 20, 80, 'Mclaren'), (Mercedes, 180, 80, 'Mercedes'),
            (Redbull, 340, 80, 'Redbull'), (VCARB, 500, 80, 'VCARB'),
            (ferrari, 660, 80, 'ferrari'), (Williams, 820, 80, 'Williams'),
            (AstonMartin, 100, 350, 'AstonMartin'), (Haas, 260, 350, 'Haas'),
            (Audi, 420, 350, 'Audi'), (Alpine, 580, 350, 'Alpine'), 
            (Cadillac, 740, 350, 'Cadillac')
        ]

        my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]

        for img, x, y, name in all_teams:
            # --- UPDATED: Alpine is never considered "taken" visually ---
            is_taken = name in taken_cars and name != "Alpine"
            is_locked = name not in my_unlocked
            
            if is_taken or is_locked:
                # Gray out taken OR locked cars
                gray_car = pygame.transform.scale(pygame.transform.rotate(img, -90), (185, 274))
                gray_car.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(gray_car, (x, y))
                
                # Show appropriate label based on why they can't pick it
                label_text = "TAKEN" if is_taken else "LOCKED"
                screen.blit(f1font2.render(label_text, True, "red"), (x + 35, y + 100))
            else:
                # Normal selection logic for available & unlocked cars
                if x < mouseX < x + 185 and y < mouseY < y + 274 or car == img:
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), (144, 213)), (x + 20, y + 20))
                else:
                    screen.blit(pygame.transform.scale(pygame.transform.rotate(img, -90), (185, 274)), (x, y))
    elif gamestate == "joinLobby":
        screen.blit(menu, (0,0))
        
        # --- DRAW BACK BUTTON ---
        if 30 < mouseX < 90 and 30 < mouseY < 90:
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else:
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # --- DRAW LOBBY LIST ---
        if not available_lobbies:
            screen.blit(f1font2.render("No active lobbies found. Someone must Host first!", True, "red"), (200, 300))
        else:
            y_offset = 150
            for l_id, count in available_lobbies.items():
                # Hover effect
                if 300 < mouseX < 940 and y_offset < mouseY < y_offset + 80:
                    pygame.draw.rect(screen, "white", (300, y_offset, 640, 80), 0, 15)
                else:
                    pygame.draw.rect(screen, (200, 200, 200), (300, y_offset, 640, 80), 0, 15)
                
                txt = f"Lobby #{l_id}  -  Capacity: {count}/10"
                screen.blit(f1font2.render(txt, True, "black"), (350, y_offset + 25))
                y_offset += 100

    # --- NEW: Authentication Selection Screen ---
    elif gamestate == "authMenu":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Sign Up Button
        if 300 < mouseX < 940 and 270 < mouseY < 370: pygame.draw.rect(screen, ("white"), (300, 270, 640, 100), 0, 20)
        else: pygame.draw.rect(screen, (220, 220, 220), (300, 270, 640, 100), 0, 20)
        screen.blit(f1font.render('Create Account', True, ("black")), (390, 290))

        # Sign In Button
        if 300 < mouseX < 940 and 430 < mouseY < 530: pygame.draw.rect(screen, ("white"), (300, 430, 640, 100), 0, 20)
        else: pygame.draw.rect(screen, (220, 220, 220), (300, 430, 640, 100), 0, 20)
        screen.blit(f1font.render('Sign In', True, ("black")), (520, 450))

    # --- NEW: Sign Up and Sign In Screens ---
    elif gamestate in ["signUp", "signIn"]:
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        title_text = "Sign Up" if gamestate == "signUp" else "Sign In"
        screen.blit(f1font.render(title_text, True, ("white")), (530, 60))

        # Username Box
        pygame.draw.rect(screen, "white", (300, 150, 640, 80), 0, 15)
        if typing and UsernameTyping: pygame.draw.rect(screen, (100, 200, 255), (300, 150, 640, 80), 5, 15)
        
        if gamestate == "signUp" and UsernameExist and UsernameInputed != "":
            pygame.draw.rect(screen, "red", (300, 150, 640, 80), 5, 15)
            screen.blit(f1font2.render("Username Already Exists", True, "red") , (310, 120))
        elif gamestate == "signIn" and not UsernameExist and UsernameInputed != "":
            pygame.draw.rect(screen, "red", (300, 150, 640, 80), 5, 15)
            screen.blit(f1font2.render("Username Does Not Exist", True, "red") , (310, 120))

        u_text = f1font.render(UsernameInputed if UsernameInputed else "Username", True, (0,0,0) if UsernameInputed else (150,150,150))
        screen.blit(u_text, (330, 170))

        # Password Box
        pygame.draw.rect(screen, "white", (300, 260, 640, 80), 0, 15)
        if typing and passwordTyping: pygame.draw.rect(screen, (100, 200, 255), (300, 260, 640, 80), 5, 15)
        
        if show_last_char and (pygame.time.get_ticks() - last_key_time) < 1000:
            p_disp = "●"*(len(passwordInputed)-1) + passwordInputed[-1:]
        else:
            p_disp = "●" * len(passwordInputed)
            show_last_char = False

        p_text = f1font.render(p_disp if passwordInputed else "Password", True, (0,0,0) if passwordInputed else (150,150,150))
        screen.blit(p_text, (330, 280))

        if gamestate == "signIn" and passwordInputed != "":
            if not (UsernameInputed in users and users[UsernameInputed] == passwordInputed):
                pygame.draw.rect(screen, "red", (300, 260, 640, 80), 5, 15)

        # Abbreviation Box (Sign Up Only)
        if gamestate == "signUp":
            pygame.draw.rect(screen, "white", (300, 370, 640, 80), 0, 15)
            if typing and abbrTyping: pygame.draw.rect(screen, (100, 200, 255), (300, 370, 640, 80), 5, 15)
            
            if abbrInputed != "" and len(abbrInputed) < 3:
                pygame.draw.rect(screen, "red", (300, 370, 640, 80), 5, 15)
                screen.blit(f1font2.render("Must be exactly 3 letters", True, "red") , (310, 455))
                
            a_text = f1font.render(abbrInputed if abbrInputed else "3-Letter Tag", True, (0,0,0) if abbrInputed else (150,150,150))
            screen.blit(a_text, (330, 390))

        # Submit Button
        if 440 < mouseX < 840 and 480 < mouseY < 560: pygame.draw.rect(screen, ("white"), (440, 480, 400, 80), 0, 15)
        else: pygame.draw.rect(screen, (220, 220, 220), (440, 480, 400, 80), 0, 15)
        btn_text = "Create Account" if gamestate == "signUp" else "Login"
        screen.blit(f1font.render(btn_text, True, ("black")), (500 if gamestate=="signUp" else 550, 495))

    # --- NEW: Account Info Menu (When Logged In) ---
    elif gamestate == "accountMenu":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        screen.blit(f1font.render("Account Profile", True, ("white")), (430, 100))
        screen.blit(f1font2.render(f"Logged in as: {loggedInUser}", True, ("white")), (430, 180))

        # --- NEW: Display Total Points ---
        my_points = user_points.get(loggedInUser, 0)
        screen.blit(f1font2.render(f"Career Points: {my_points}", True, (255, 215, 0)), (430, 220)) # Drawn in Gold
        # ---------------------------------

        # Display Unlocked Cars 
        my_cars = unlocked_cars.get(loggedInUser, ["Alpine"])
        screen.blit(f1font2.render(f"Your Garage:", True, ("white")), (430, 280))

        # View Cards Button (No more overlapping text!)
        if 750 < mouseX < 1150 and 280 < mouseY < 360: 
            pygame.draw.rect(screen, (100, 200, 255), (750, 280, 400, 80), 0, 15)
        else: 
            pygame.draw.rect(screen, "white", (750, 280, 400, 80), 0, 15)
        screen.blit(f1font.render("View My Cards", True, "black"), (790, 295))
        
        # Draw the Unlocked Cars List
        y_offset = 320 
        for unlocked_car in my_cars:
            screen.blit(f1font2.render(f"- {unlocked_car}", True, (100, 255, 100)), (450, y_offset))
            y_offset += 35


        # Sign Out Button
        if 440 < mouseX < 840 and 550 < mouseY < 630: pygame.draw.rect(screen, (255, 100, 100), (440, 550, 400, 80), 0, 15)
        else: pygame.draw.rect(screen, (200, 50, 50), (440, 550, 400, 80), 0, 15)
        screen.blit(f1font.render('Sign Out', True, ("white")), (520, 560))
    
    # --- UPDATED: Inventory & Squad Equip Screen ---
    elif gamestate in ["inventory", "driverSelect"]:
        screen.blit(menu, (0,0))
        
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Filtering Logic for Drawing
        raw_drivers = owned_drivers.get(loggedInUser, [])
        filtered_drivers = raw_drivers
        
        if gamestate == "driverSelect":
            # 1. Remove Teams
            game_teams_lower = [t.lower() for t in ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]]
            filtered_drivers = [d for d in raw_drivers if d.lower() not in game_teams_lower]
            
            # 2. Apply Search
            if 'squad_search_input' not in globals(): squad_search_input = ""
            if 'squad_typing' not in globals(): squad_typing = False
            
            if squad_search_input:
                filtered_drivers = [d for d in filtered_drivers if squad_search_input.lower() in d.lower()]
                
            # 3. Draw Search Box
            pygame.draw.rect(screen, "white", (400, 25, 460, 50), 0, 15)
            if squad_typing: pygame.draw.rect(screen, (100, 200, 255), (400, 25, 460, 50), 4, 15)
            s_text = f1font2.render(squad_search_input if squad_search_input else "Search Drivers...", True, (0,0,0) if squad_search_input else (150,150,150))
            screen.blit(s_text, (420, 35))
        else:
            screen.blit(f1font.render("My Card Collection", True, ("white")), (400, 30))

        max_pages = max(0, (len(filtered_drivers) - 1) // 8)

        if len(raw_drivers) == 0:
            screen.blit(f1font2.render("You don't own any cards yet! Go to the Market.", True, "red"), (350, 300))
        elif len(filtered_drivers) == 0:
            screen.blit(f1font2.render("No drivers found matching that search.", True, "white"), (450, 300))
        else:
            screen.blit(f1font2.render(f"Page {inventory_page + 1} / {max_pages + 1}", True, "white"), (1050, 45)) 

            # Shifted down slightly to accommodate the search bar
            start_x, start_y, x_spacing, y_spacing = 70, 110, 290, 320 
            start_idx = inventory_page * 8
            end_idx = min(start_idx + 8, len(filtered_drivers))

            for i in range(start_idx, end_idx):
                drv = filtered_drivers[i]
                row, col = (i - start_idx) // 4, (i - start_idx) % 4
                draw_x = start_x + (col * x_spacing)
                draw_y = start_y + (row * y_spacing)
                
                if gamestate == "driverSelect" and draw_x < mouseX < draw_x + 228 and draw_y < mouseY < draw_y + 300:
                    pygame.draw.rect(screen, (100, 255, 100), (draw_x-6, draw_y-6, 240, 312), 0, 12)
                    screen.blit(f1font.render("EQUIP", True, (100, 255, 100)), (draw_x + 40, draw_y + 120))
                
                if drv in inventory_loaded_imgs:
                    screen.blit(inventory_loaded_imgs[drv], (draw_x, draw_y))
                    draw_card_stats(screen, drv, draw_x, draw_y)
                else:
                    pygame.draw.rect(screen, (50,50,50), (draw_x, draw_y, 228, 300), 0, 10)
                    screen.blit(f1font2.render("Loading...", True, "white"), (draw_x + 40, draw_y + 130))

            if inventory_page > 0:
                if 50 < mouseX < 150 and 330 < mouseY < 390: pygame.draw.rect(screen, (200, 200, 200), (50, 330, 100, 60), 0, 15)
                else: pygame.draw.rect(screen, "white", (50, 330, 100, 60), 0, 15)
                screen.blit(f1font2.render("PREV", True, "black"), (65, 345))

            if inventory_page < max_pages:
                if 1130 < mouseX < 1230 and 330 < mouseY < 390: pygame.draw.rect(screen, (200, 200, 200), (1130, 330, 100, 60), 0, 15)
                else: pygame.draw.rect(screen, "white", (1130, 330, 100, 60), 0, 15)
                screen.blit(f1font2.render("NEXT", True, "black"), (1145, 345))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()