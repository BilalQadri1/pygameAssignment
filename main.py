'''
-----------------------------------------------------------------------------
Program Name: F1 Racing Game
Program Description: A 2D f1 style racing game, with car selection, different tracks, tyre wear, pit stops, DRS, lap timing, and penalties.

-----------------------------------------------------------------------------
References:

(put a link to your reference here but also add a comment in the code below where you used the reference)
reference #1 to move forward in the direction the car is facing: https://stackoverflow.com/questions/64774900/how-to-get-velocity-x-and-y-from-angle-and-speed
-----------------------------------------------------------------------------

Additional Libraries/Extensions:d

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
import json
from network import Network  

# --- ADD THIS DPI FIX RIGHT HERE ---
import ctypes
try:
    # This forces Windows to render the game at true native 4K resolution!
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass # Skips if you are on Mac/Linux
# -----------------------------------
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

# ==========================================
# --- SAVED SESSION SYSTEM ---
session_file = os.path.join(script_dir, "session.json")

def save_session(username):
    with open(session_file, "w") as f:
        json.dump({"loggedInUser": username}, f)

def clear_session():
    if os.path.exists(session_file):
        os.remove(session_file)

def load_session():
    try:
        with open(session_file, "r") as f:
            data = json.load(f)
            return data.get("loggedInUser")
    except (FileNotFoundError, json.JSONDecodeError):
        return None
# ==========================================
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
market_scroll = 0   # <--- ADD THIS LINE

# --- NEW: Inventory Variables ---
inventory_page = 0
inventory_scroll = 0
inventory_loaded_imgs = {}
# ==========================================
# --- PLAYER MARKET SYSTEM ---
market_listings = []
market_file = os.path.join(script_dir, "market_listings.json")
try:
    with open(market_file, "r") as f:
        market_listings = json.load(f)
# --- UPDATED: Catch empty/corrupt files too! ---
except (FileNotFoundError, json.JSONDecodeError): 
    market_listings = []

def save_market():
    with open(market_file, "w") as f:
        json.dump(market_listings, f, indent=4)

market_tab = "BUY"
sell_price_input = ""
sell_price_typing = False
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
# --- NEW: PACK SYSTEM CONFIG ---
PACK_TYPES = {
    "BRONZE": {"cost": 10, "cards": 3, "min_ovr": 50, "max_ovr": 75, "desc": "F2/F3 & Rookies"},
    "GOLD":   {"cost": 50, "cards": 3, "min_ovr": 76, "max_ovr": 89, "desc": "Current F1 Grid"},
    "LEGEND": {"cost": 100, "cards": 2, "min_ovr": 90, "max_ovr": 99, "desc": "Primes & Legends"}
}
pack_opening_results = []
pack_reveal_idx = 0
selected_pack_type = None

# --- NEW: Animation Tracking Variables ---
pack_anim_timer = 0
pack_anim_state = 0  
pack_large_cache = {} # <-- ADD THIS LINE

def generate_pack_content(tier_name):
    config = PACK_TYPES[tier_name]
    eligible_drivers = [name for name, stats in driver_stats.items() 
                        if config["min_ovr"] <= stats["OVR"] <= config["max_ovr"]]
    
    if not eligible_drivers: eligible_drivers = list(driver_stats.keys())

    results = []
    for _ in range(config["cards"]):
        pulled = random.choice(eligible_drivers)
        results.append(pulled)
        if loggedInUser not in owned_drivers:
            owned_drivers[loggedInUser] = []
        owned_drivers[loggedInUser].append(pulled)
        
        game_teams = ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]
        for team in game_teams:
            # --- UPDATED: Strip spaces here too! ---
            if pulled.replace(" ", "").lower() == team.lower():
                my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"])
                if team not in my_unlocked:
                    my_unlocked.append(team)
                    unlocked_cars[loggedInUser] = my_unlocked
                    save_unlocked_cars()
    save_drivers()
    return results
# -------------------------------
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

# CHANGE THIS:
# loggedInUser = None

# TO THIS:
loggedInUser = load_session()
# Safety check: ensure the saved user actually exists in the accounts database
if loggedInUser and loggedInUser not in users:
    loggedInUser = None
    clear_session()
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

import ctypes
import pygame
import os

# 1. Tell Windows this is a distinct, standalone app
# This string can be anything, it just needs to be unique to your game!
myappid = 'bilalqadri.f1racing.game.1.0' 
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except AttributeError:
    pass # Skips if you are on Mac/Linux

# 2. Initialize Pygame
pygame.init()

# 3. Load your .ico file and set it
icon_path = os.path.join(script_dir, r"assets\2418779.ico")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# *********SETUP**********
windowWidth = 1280
windowHeight = 720

# Add these to your variable setup
my_lobby_id = None
my_player_index = None
my_grid_order = [] 
available_lobbies = {} 

# --- UPDATED: NATIVE 4K FULLSCREEN SETUP ---
is_fullscreen = True
# Passing (0,0) and FULLSCREEN forces Pygame to use your monitor's exact native resolution (3840x2160)
real_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# The hidden canvas we draw everything to
screen = pygame.Surface((windowWidth, windowHeight))

# --- NEW: LOAD PACK IMAGES SAFELY ---
pack_img = pygame.image.load(os.path.join(script_dir, r"assets\pack.png")).convert_alpha()
pack_store_img = pygame.transform.smoothscale(pack_img, (200, 290))
# ------------------------------------
# Mouse Scaling Math (Keeps buttons working perfectly when in Fullscreen)
def get_scaled_mouse_pos(real_mouse_pos, current_w, current_h):
    target_ratio = windowWidth / windowHeight
    window_ratio = current_w / current_h

    if window_ratio > target_ratio:
        scale = current_h / windowHeight
        x_offset = (current_w - (windowWidth * scale)) / 2
        y_offset = 0
    else:
        scale = current_w / windowWidth
        x_offset = 0
        y_offset = (current_h - (windowHeight * scale)) / 2

    scaled_x = (real_mouse_pos[0] - x_offset) / scale
    scaled_y = (real_mouse_pos[1] - y_offset) / scale
    return scaled_x, scaled_y
# -----------------------------

clock = pygame.time.Clock()  
#different track options images
bahrainTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, r"assets\bahrain.png")).convert(), (12800,7200))
bahrainTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\bahrainLine.png")).convert_alpha(), (12800,7200))

bahrainMinimap = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\BahrainMinimap.png")), (258, 144))# ==========================================
# --- DRIVER RATINGS SYSTEM ---
ovr_images = {}
stat_images = {}
raw_digits = {} # <-- NEW: Store the high-res originals!

OVR_W, OVR_H = 30, 30    
STAT_W, STAT_H = 18, 18  

for i in range(10):
    num_path = os.path.join(script_dir, "F1Cards", "RatingNumbers", f"{i}.png")
    if os.path.exists(num_path):
        img = pygame.image.load(num_path).convert_alpha()
        raw_digits[str(i)] = img # Save the HD raw image
        
        # Use smoothscale for the default small ones so they look better in the inventory
        ovr_images[str(i)] = pygame.transform.smoothscale(img, (OVR_W, OVR_H))
        stat_images[str(i)] = pygame.transform.smoothscale(img, (STAT_W, STAT_H))

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
    "Nael":           {"OVR": 63, "EXP": 15, "RAC": 62, "AWA": 63, "PAC": 65},
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

def draw_card_stats(surface, driver_name, card_x, card_y, card_w=228):
    # Calculate a dynamic scale multiplier! (If card is 380 wide, scale is ~1.66x)
    scale = card_w / 228.0 
    
    clean_name = driver_name.replace(" ", "").lower()
    bulletproof_stats = {k.replace(" ", "").lower(): v for k, v in driver_stats.items()}
    
    stats = bulletproof_stats.get(clean_name, {"OVR": 75, "EXP": 75, "RAC": 75, "AWA": 75, "PAC": 75})
    
    # Scale all your perfectly calibrated coordinates dynamically
    positions = {
        "OVR": (card_x + 30 * scale, card_y + 73 * scale),
        "EXP": (card_x + 21 * scale, card_y + 236 * scale),
        "RAC": (card_x + 69 * scale, card_y + 235 * scale),
        "AWA": (card_x + 115 * scale, card_y + 235 * scale),
        "PAC": (card_x + 163 * scale, card_y + 235 * scale),
    }

    for stat_name, position in positions.items():
        val_str = str(int(stats[stat_name])).zfill(2)
        x_offset = 0
        
        for digit in val_str:
            if digit in raw_digits: # Pull from the HD raw digits!
                if stat_name == "OVR":
                    current_w, current_h = int(OVR_W * scale), int(OVR_H * scale)
                else:
                    current_w, current_h = int(STAT_W * scale), int(STAT_H * scale)
                    
                # Smoothscale the raw digit down to the EXACT dynamic size we need
                scaled_digit = pygame.transform.smoothscale(raw_digits[digit], (current_w, current_h))
                surface.blit(scaled_digit, (position[0] + x_offset, position[1]))
                
                x_offset += current_w
# ==========================================
# Track-relative checkpoints (where they sit on the 12800x7200 image)
# Track-relative checkpoints (where they sit on the 12800x7200 image)
bahrain_checkpoints = [
    pygame.Rect(6607, 6343, 400, 400),
    pygame.Rect(6205, 6335, 400, 400),
    pygame.Rect(5803, 6331, 400, 400),
    pygame.Rect(5381, 6331, 400, 400),
    pygame.Rect(4973, 6331, 400, 400),
    pygame.Rect(4569, 6346, 400, 400),
    pygame.Rect(4169, 6362, 400, 400),
    pygame.Rect(3771, 6368, 400, 400),
    pygame.Rect(3370, 6368, 400, 400),
    pygame.Rect(2942, 6368, 400, 400),
    pygame.Rect(2544, 6368, 400, 400),
    pygame.Rect(2140, 6367, 400, 400),
    pygame.Rect(1757, 6318, 400, 400),
    pygame.Rect(1827, 5909, 400, 400),
    pygame.Rect(2052, 5644, 400, 400),
    pygame.Rect(1958, 5243, 400, 400),
    pygame.Rect(1922, 4841, 400, 400),
    pygame.Rect(1915, 4438, 400, 400),
    pygame.Rect(1931, 4014, 400, 400),
    pygame.Rect(1993, 3609, 400, 400),
    pygame.Rect(2047, 3206, 400, 400),
    pygame.Rect(2092, 2811, 400, 400),
    pygame.Rect(2163, 2415, 400, 400),
    pygame.Rect(2211, 2001, 400, 400),
    pygame.Rect(2267, 1583, 400, 400),
    pygame.Rect(2345, 1179, 400, 400),
    pygame.Rect(2397, 778, 400, 400),
    pygame.Rect(2438, 446, 400, 400),
    pygame.Rect(2843, 406, 400, 400),
    pygame.Rect(3152, 654, 400, 400),
    pygame.Rect(3409, 976, 400, 400),
    pygame.Rect(3669, 1293, 400, 400),
    pygame.Rect(3969, 1565, 400, 400),
    pygame.Rect(4357, 1811, 400, 400),
    pygame.Rect(4767, 2080, 400, 400),
    pygame.Rect(4816, 2423, 400, 400),
    pygame.Rect(4756, 2721, 400, 400),
    pygame.Rect(4852, 3060, 400, 400),
    pygame.Rect(5243, 3338, 400, 400),
    pygame.Rect(5594, 3590, 400, 400),
    pygame.Rect(5830, 3772, 400, 400),
    pygame.Rect(6173, 4004, 400, 400),
    pygame.Rect(6123, 4395, 400, 400),
    pygame.Rect(5724, 4389, 400, 400),
    pygame.Rect(5323, 4351, 400, 400),
    pygame.Rect(4929, 4309, 400, 400),
    pygame.Rect(4534, 4243, 400, 400),
    pygame.Rect(4121, 4218, 400, 400),
    pygame.Rect(3705, 4195, 400, 400),
    pygame.Rect(3300, 4201, 400, 400),
    pygame.Rect(3157, 4596, 400, 400),
    pygame.Rect(3552, 4770, 400, 400),
    pygame.Rect(3970, 4797, 400, 400),
    pygame.Rect(4402, 4801, 400, 400),
    pygame.Rect(4822, 4801, 400, 400),
    pygame.Rect(5230, 4820, 400, 400),
    pygame.Rect(5644, 4820, 400, 400),
    pygame.Rect(6062, 4820, 400, 400),
    pygame.Rect(6478, 4820, 400, 400),
    pygame.Rect(6904, 4820, 400, 400),
    pygame.Rect(7300, 4820, 400, 400),
    pygame.Rect(7710, 4820, 400, 400),
    pygame.Rect(8044, 4800, 400, 400),
    pygame.Rect(8433, 4695, 400, 400),
    pygame.Rect(8423, 4295, 400, 400),
    pygame.Rect(8228, 3901, 400, 400),
    pygame.Rect(7958, 3605, 400, 400),
    pygame.Rect(7588, 3420, 400, 400),
    pygame.Rect(7208, 3307, 400, 400),
    pygame.Rect(6924, 3096, 400, 400),
    pygame.Rect(6685, 2734, 400, 400),
    pygame.Rect(6643, 2326, 400, 400),
    pygame.Rect(6711, 1910, 400, 400),
    pygame.Rect(6946, 1520, 400, 400),
    pygame.Rect(7149, 1114, 400, 400),
    pygame.Rect(7556, 914, 400, 400),
    pygame.Rect(7950, 1239, 400, 400),
    pygame.Rect(8186, 1541, 400, 400),
    pygame.Rect(8348, 1772, 400, 400),
    pygame.Rect(8557, 2128, 400, 400),
    pygame.Rect(8795, 2534, 400, 400),
    pygame.Rect(8985, 2854, 400, 400),
    pygame.Rect(9211, 3212, 400, 400),
    pygame.Rect(9425, 3559, 400, 400),
    pygame.Rect(9613, 3890, 400, 400),
    pygame.Rect(9826, 4238, 400, 400),
    pygame.Rect(10077, 4578, 400, 400),
    pygame.Rect(10246, 4945, 400, 400),
    pygame.Rect(10436, 5325, 400, 400),
    pygame.Rect(10708, 5672, 400, 400),
    pygame.Rect(10746, 6066, 400, 400),
    pygame.Rect(10511, 6209, 400, 400),
    pygame.Rect(10244, 6331, 400, 400),
    pygame.Rect(9829, 6346, 400, 400),
    pygame.Rect(9423, 6346, 400, 400),
    pygame.Rect(9015, 6356, 400, 400),
    pygame.Rect(8593, 6356, 400, 400),
    pygame.Rect(8196, 6364, 400, 400),
    pygame.Rect(7780, 6363, 400, 400),
    pygame.Rect(7362, 6363, 400, 400),
    pygame.Rect(6998, 6363, 400, 400),
]

my_checkpoint_index = 0  # Which gate are we looking for next?

# --- NEW: Initialize empty Silverstone checkpoints so the game doesn't crash! ---
# Track-relative checkpoints (where they sit on the 12800x7200 image)
# Track-relative checkpoints (where they sit on the 12800x7200 image)
silverstone_checkpoints = [
    pygame.Rect(7471, 5635, 400, 400),
    pygame.Rect(7118, 5344, 400, 400),
    pygame.Rect(6692, 5022, 400, 400),
    pygame.Rect(6266, 4738, 400, 400),
    pygame.Rect(6164, 4335, 400, 400),
    pygame.Rect(6195, 3887, 400, 400),
    pygame.Rect(6239, 3484, 400, 400),
    pygame.Rect(6051, 3050, 400, 400),
    pygame.Rect(5805, 2680, 400, 400),
    pygame.Rect(5449, 2311, 400, 400),
    pygame.Rect(5482, 1915, 400, 400),
    pygame.Rect(5873, 1792, 400, 400),
    pygame.Rect(5829, 1373, 400, 400),
    pygame.Rect(5409, 1329, 400, 400),
    pygame.Rect(5000, 1329, 400, 400),
    pygame.Rect(4702, 1614, 400, 400),
    pygame.Rect(4461, 1930, 400, 400),
    pygame.Rect(4167, 2257, 400, 400),
    pygame.Rect(3796, 2625, 400, 400),
    pygame.Rect(3464, 3012, 400, 400),
    pygame.Rect(3162, 3422, 400, 400),
    pygame.Rect(2795, 3778, 400, 400),
    pygame.Rect(2400, 4163, 400, 400),
    pygame.Rect(2379, 4558, 400, 400),
    pygame.Rect(2662, 4776, 400, 400),
    pygame.Rect(3073, 4813, 400, 400),
    pygame.Rect(3242, 5141, 400, 400),
    pygame.Rect(2953, 5435, 400, 400),
    pygame.Rect(2537, 5291, 400, 400),
    pygame.Rect(2135, 5095, 400, 400),
    pygame.Rect(1755, 4805, 400, 400),
    pygame.Rect(1436, 4354, 400, 400),
    pygame.Rect(1398, 3946, 400, 400),
    pygame.Rect(1368, 3546, 400, 400),
    pygame.Rect(1331, 3131, 400, 400),
    pygame.Rect(1253, 2615, 400, 400),
    pygame.Rect(1237, 2207, 400, 400),
    pygame.Rect(1211, 1793, 400, 400),
    pygame.Rect(1239, 1394, 400, 400),
    pygame.Rect(1635, 1154, 400, 400),
    pygame.Rect(2052, 1032, 400, 400),
    pygame.Rect(2479, 920, 400, 400),
    pygame.Rect(2881, 866, 400, 400),
    pygame.Rect(3285, 863, 400, 400),
    pygame.Rect(3690, 833, 400, 400),
    pygame.Rect(4093, 816, 400, 400),
    pygame.Rect(4492, 684, 400, 400),
    pygame.Rect(4861, 550, 400, 400),
    pygame.Rect(5239, 662, 400, 400),
    pygame.Rect(5654, 729, 400, 400),
    pygame.Rect(6055, 558, 400, 400),
    pygame.Rect(6473, 453, 400, 400),
    pygame.Rect(6851, 719, 400, 400),
    pygame.Rect(7059, 1126, 400, 400),
    pygame.Rect(7475, 1377, 400, 400),
    pygame.Rect(7874, 1583, 400, 400),
    pygame.Rect(8306, 1790, 400, 400),
    pygame.Rect(8780, 2055, 400, 400),
    pygame.Rect(9304, 2321, 400, 400),
    pygame.Rect(10106, 2758, 400, 400),
    pygame.Rect(10857, 3245, 400, 400),
    pygame.Rect(11104, 3482, 400, 400),
    pygame.Rect(11220, 3846, 400, 400),
    pygame.Rect(11095, 4206, 400, 400),
    pygame.Rect(10689, 4408, 400, 400),
    pygame.Rect(10331, 4606, 400, 400),
    pygame.Rect(9933, 4956, 400, 400),
    pygame.Rect(9560, 5336, 400, 400),
    pygame.Rect(9255, 5587, 400, 400),
    pygame.Rect(9423, 5969, 400, 400),
    pygame.Rect(9173, 6327, 400, 400),
    pygame.Rect(8837, 6447, 400, 400),
    pygame.Rect(8439, 6432, 400, 400),
    pygame.Rect(8052, 6097, 400, 400),
]

silverstoneTrack = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstone.png")).convert(), (12800,7200))
silverstoneTrackLine = pygame.transform.scale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneLine.png")).convert_alpha(), (12800,7200))
silverstoneMinimap = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneMinimap.png")), (256, 144))
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
silverstone_grid = [
    (-7270.0, -5668.0, -39),
    (-7419.0, -5604.0, -30),
    (-7429.0, -5799.0, -45),
    (-7610.0, -5768.0, -33),
    (-7612.9, -5938.1, -42),
    (-7779.9, -5891.1, 318),
    (-7786.9, -6067.1, 321),
    (-7945.9, -6026.1, 321),
    (-7958.9, -6192.1, 321),
    (-8120.9, -6159.1, 318),
]
# -------------------------------
currentTrack = bahrainTrack
# --- UPGRADED: Use smoothscale for crispy UI assets ---
menu = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\menu.jpg")).convert(), (1280,720))
stats = pygame.image.load(os.path.join(script_dir,r"assets\board.png")).convert_alpha()

f1logo = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\F1logo.png")).convert_alpha(), (388,100))
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
AstonMartin = pygame.image.load(os.path.join(script_dir, r"assets\Aston.png")).convert_alpha()
Haas = pygame.image.load(os.path.join(script_dir, r"assets\Haas.png")).convert_alpha()
Alpine = pygame.image.load(os.path.join(script_dir, r"assets\Alpine.png")).convert_alpha()
Audi = pygame.image.load(os.path.join(script_dir, r"assets\Audi.png")).convert_alpha()
Cadillac = pygame.image.load(os.path.join(script_dir, r"assets\Cadillac.png")).convert_alpha()

car = Alpine
car_name = "Alpine"

#tyres wear colors
# Minimaps
bahrainMinimap = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\BahrainMinimap.png")), (256,144))
silverstoneMinimap = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\silverstoneMinimap.png")), (256,144))

# Tyres (around line 390)
tyresG = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\tyresG.png")), (60.5,90.5))
tyresY = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\tyresY.png")), (60.5,90.5))
tyresR = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir,r"assets\tyresR.png")), (60.5,90.5))
tyres = tyresG
# --- NEW: TYRE COMPOUND ASSETS ---
try:
    # On-Car Overlays
    soft_overlay = pygame.image.load(os.path.join(script_dir, r"assets\soft.png")).convert_alpha()
    medium_overlay = pygame.image.load(os.path.join(script_dir, r"assets\medium.png")).convert_alpha()
    hard_overlay = pygame.image.load(os.path.join(script_dir, r"assets\hard.png")).convert_alpha()
    
    # Menu Selection Wheels
    soft_wheel = pygame.image.load(os.path.join(script_dir, r"assets\r.png")).convert_alpha()
    medium_wheel = pygame.image.load(os.path.join(script_dir, r"assets\m.png")).convert_alpha()
    hard_wheel = pygame.image.load(os.path.join(script_dir, r"assets\h.png")).convert_alpha()
except:
    print("Warning: Missing Tyre Assets!")

selected_tyre_compound = "Medium" 
# ---------------------------------
#animated tyre images
treads1 = pygame.image.load(os.path.join(script_dir,r"assets\treads1.png"))
treads2 = pygame.image.load(os.path.join(script_dir,r"assets\treads2.png"))

#starting race lights  countdown
# traffic light sprites
# starting race lights countdown
lights0 = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir, r"assets\lights0.png")).convert_alpha(), (520, 560))
lights1 = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir, r"assets\lights1.png")).convert_alpha(), (520, 560))
lights2 = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir, r"assets\lights2.png")).convert_alpha(), (520, 560))
lights3 = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir, r"assets\lights3.png")).convert_alpha(), (520, 560))
lights4 = pygame.transform.smoothscale(pygame.image.load(os.path.join(script_dir, r"assets\lights4.png")).convert_alpha(), (520, 560))

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
# --- CHECKPOINT MAKER SETTINGS ---
CHECKPOINT_RADIUS = 200 
ENABLE_OFFLINE_AI = True 
custom_checkpoints = [] # <-- ADD THIS to hold them live!
# ---------------------------------
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

# car sound (Your existing code)
carSound = pygame.mixer.Sound(os.path.join(script_dir, r"assets\engine.mp3"))
carSound.set_volume(0.1)
carSound.play(-1)

# --- ADD THIS: OPPONENT SPATIAL AUDIO SETUP ---
opponentEngineSound = pygame.mixer.Sound(os.path.join(script_dir, r"assets\engine.mp3"))
pygame.mixer.set_num_channels(32) # Ensure we have enough audio channels for multiplayer
opponent_audio_channels = {} # Tracks which channel belongs to which opponent ID
# ----------------------------------------------

# crash background
crashbg = pygame.transform.smoothscale(
    pygame.image.load(os.path.join(script_dir, r"assets\crash.png")).convert(), (1280, 720)
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
turn_speed = 3

# Load and scale the lock icon to a usable size (35x35 pixels)
lock_img = pygame.image.load(os.path.join(script_dir, r"assets\lock.png")).convert_alpha()
lock_icon = pygame.transform.smoothscale(lock_img, (35, 35))

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

drs_allowed = False # Add this global variable right above the function

# DRS toggle function
def toggleDRS():
    global DRS, carDRS, car_name, drs_allowed 
    
    if DRS == False:
        # Only allow activation if they are within 1 second of the car ahead!
        if drs_allowed:
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

print("Use W/A/S/D to drive the car. Use UP/DOWN arrow keys to change gears. Press SPACE to toggle DRS when available. Select tracks and cars from the menu")

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

# --- NEW: OFFLINE AI INITIALIZATION ---
offline_ai_cars = []
# --------------------------------------

# *********GAME LOOP**********
while True:
    time += clock.get_time() / 1000
    keys = pygame.key.get_pressed()
    
    # --- NEW: DYNAMIC MOUSE TRACKING ---
    current_w, current_h = real_screen.get_size()
    raw_mouse_pos = pygame.mouse.get_pos()
    
    # Convert real window mouse position to 1280x720 game coordinates
    mouseX, mouseY = get_scaled_mouse_pos(raw_mouse_pos, current_w, current_h)
    # -----------------------------------

    # *********EVENTS**********
    for ev in pygame.event.get():    # controller toggle
        if ev.type == pygame.QUIT: 
            break      

        # --- NEW: MOUSE WHEEL EVENTS ---
        if ev.type == pygame.MOUSEWHEEL:
            if gamestate == "market":
                market_scroll -= ev.y * 40 # 40 pixels per scroll tick
                if market_scroll < 0: 
                    market_scroll = 0
            # ADD THIS: Apply scrolling to inventory screens
            elif gamestate in ["inventory", "driverSelect"]:
                inventory_scroll -= ev.y * 40
                if inventory_scroll < 0: 
                    inventory_scroll = 0
        # -------------------------------
        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                
                if gamestate == "main":
                    # --- NEW: Dynamic hitboxes based on exact text width! ---
                    if 250 < mouseY < 300 and 100 < mouseX < 100 + f1font.size('RACE')[0] + 40:
                        if loggedInUser: gamestate = "carSelect" 
                    elif 330 < mouseY < 380 and 100 < mouseX < 100 + f1font.size('MARKET')[0] + 40:
                        if loggedInUser: 
                            gamestate = "market"
                            market_search_input, market_msg, market_searched_img = "", "", None
                    elif 410 < mouseY < 460 and 100 < mouseX < 100 + f1font.size('SETTINGS')[0] + 40:
                        gamestate = "settings"
                    elif 490 < mouseY < 540 and 100 < mouseX < 100 + f1font.size('ONLINE')[0] + 40:
                        if loggedInUser:
                            gamestate = "onlineMenu"
                            if n is None or n.p is None: n = Network()
                    # --- NEW: MAIN MENU STORE CLICK ---
                    elif 570 < mouseY < 620 and 100 < mouseX < 100 + f1font.size('STORE')[0] + 40:
                        if loggedInUser: gamestate = "store"
                    # --- NEW: MAIN MENU QUIT CLICK ---
                    elif 650 < mouseY < 700 and 100 < mouseX < 100 + f1font.size('QUIT')[0] + 40:
                        import sys
                        pygame.quit()
                        sys.exit()
                    
                    # Account Button Click (Top Right)
                    elif 1050 < mouseX < 1250 and 30 < mouseY < 80:
                        gamestate = "accountMenu" if loggedInUser else "authMenu"
                
                # --- NEW: STORE & PACK LOGIC CLICKS ---
                elif gamestate == "store":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: gamestate = "main"
                    
                    x_pos = 150
                    for name, data in PACK_TYPES.items():
                        if x_pos < mouseX < x_pos + 200 and 200 < mouseY < 490:
                            my_pts = user_points.get(loggedInUser, 0)
                            if my_pts >= data["cost"]:
                                user_points[loggedInUser] -= data["cost"]
                                save_points()
                                pack_opening_results = generate_pack_content(name)
                                
                                # Reset everything for the new pack
                                pack_reveal_idx = 0
                                pack_anim_timer = 0
                                pack_anim_state = 0
                                gamestate = "packOpening"
                        x_pos += 350

                elif gamestate == "packOpening":
                    # ONLY allow clicking if the card is fully revealed (State 2)
                    if pack_anim_state == 2:
                        pack_reveal_idx += 1
                        if pack_reveal_idx >= len(pack_opening_results):
                            gamestate = "store" # Pack is empty, go back to store
                        else:
                            # Reset the animation for the NEXT card in the pack!
                            pack_anim_timer = 0
                            pack_anim_state = 0
                # --------------------------------------
                # --- UPDATED: Player Economy Market Clicks ---
                elif gamestate == "market":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "main"
                        market_typing, sell_price_typing = False, False
                        
                    # Tab Clicks
                    elif 120 < mouseX < 220 and 85 < mouseY < 115: 
                        market_tab, market_selected, market_msg = "BUY", None, ""
                        market_scroll = 0
                    elif 230 < mouseX < 330 and 85 < mouseY < 115: 
                        market_tab, market_selected, market_msg = "SELL", None, ""
                        market_scroll = 0
                    elif 340 < mouseX < 440 and 85 < mouseY < 115: 
                        market_tab, market_selected, market_msg = "ACTIVE", None, ""
                        market_scroll = 0
                    
                    # Search Box Click (Only in BUY mode)
                    elif market_tab == "BUY" and 120 < mouseX < 620 and 130 < mouseY < 190:
                        market_typing = True
                        sell_price_typing = False
                        market_scroll = 0
                    # Price Input Click (Only in SELL mode)
                    elif market_tab == "SELL" and market_selected and 800 < mouseX < 1080 and 410 < mouseY < 470:
                        sell_price_typing = True
                        market_typing = False
                    else:
                        market_typing, sell_price_typing = False, False

                    # Determine what list is currently visible
                    visible_list = []
                    my_drivers = owned_drivers.get(loggedInUser, [])
                    
                    if market_tab == "BUY":
                        visible_list = [item for item in market_listings if item["seller"] != loggedInUser]
                        if market_search_input:
                            visible_list = [item for item in visible_list if market_search_input.lower() in item["name"].lower()]
                    elif market_tab == "SELL":
                        visible_list = [{"name": drv, "price": 0} for drv in my_drivers]
                    elif market_tab == "ACTIVE":
                        visible_list = [item for item in market_listings if item["seller"] == loggedInUser]

                    # Click on a list item
                    list_start_y = 210 if market_tab == "BUY" else 140
                    list_y = list_start_y - market_scroll # Apply scroll!
                    
                    # Only register clicks if they happen inside the visible list area
                    if list_start_y < mouseY < 700 and 120 < mouseX < 620:
                        for item in visible_list:
                            if list_y < mouseY < list_y + 60:
                                market_selected = item
                                market_msg = ""
                                sell_price_input = "" # Reset price box
                                
                                path = find_driver_card(item["name"])
                                if path:
                                    try:
                                        loaded = pygame.image.load(path).convert_alpha()
                                        market_loaded_img = pygame.transform.smoothscale(loaded, (228, 300))
                                    except: market_loaded_img = None
                            list_y += 70

                    # --- ACTION BUTTON CLICKS (BUY / LIST / CANCEL) ---
                    if market_selected and market_loaded_img and 800 < mouseX < 1080 and 490 < mouseY < 550:
                        card_name = market_selected["name"]
                        
                        # 1. BUYING A CARD
                        if market_tab == "BUY":
                            my_pts = user_points.get(loggedInUser, 0)
                            card_price = market_selected["price"]
                            
                            if my_pts >= card_price:
                                # Deduct points from buyer
                                user_points[loggedInUser] -= card_price
                                
                                # Give points to seller
                                seller = market_selected["seller"]
                                if seller not in user_points: user_points[seller] = 0
                                user_points[seller] += card_price
                                save_points()
                                
                                # Give card to buyer
                                my_drivers.append(card_name)
                                owned_drivers[loggedInUser] = my_drivers
                                save_drivers()
                                
                                # Check if team unlocked
                                game_teams = ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]
                                for team in game_teams:
                                    # --- UPDATED: Strip spaces so "Aston Martin" matches "AstonMartin" ---
                                    if card_name.replace(" ", "").lower() == team.lower():
                                        my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"])
                                        if team not in my_unlocked:
                                            my_unlocked.append(team) # This ensures "AstonMartin" is saved exactly how the menu wants it
                                            unlocked_cars[loggedInUser] = my_unlocked
                                            save_unlocked_cars()
                                        break
                                
                                # Remove from market
                                market_listings.remove(market_selected)
                                save_market()
                                
                                market_msg = f"Bought {card_name}!"
                                market_selected = None
                            else:
                                market_msg = f"Need {card_price - my_pts} more PTS."
                                
                        # 2. LISTING A CARD FOR SALE
                        elif market_tab == "SELL":
                            if sell_price_input.isnumeric() and int(sell_price_input) > 0:
                                price = int(sell_price_input)
                                
                                # Remove from inventory
                                my_drivers.remove(card_name)
                                owned_drivers[loggedInUser] = my_drivers
                                save_drivers()
                                
                                # Add to market
                                import time as py_time  # Give the module a nickname to bypass your game variable!
                                new_listing = {
                                    "id": py_time.time(), 
                                    "seller": loggedInUser, 
                                    "name": card_name, 
                                    "price": price
                                }
                                market_listings.append(new_listing)
                                save_market()
                                
                                market_msg = f"Listed for {price} PTS!"
                                market_selected = None
                            else:
                                market_msg = "Enter a valid price!"
                                
                        # 3. CANCELLING YOUR LISTING
                        elif market_tab == "ACTIVE":
                            # Return card to inventory
                            my_drivers.append(card_name)
                            owned_drivers[loggedInUser] = my_drivers
                            save_drivers()
                            
                            # --- NEW: Check if returned card unlocks a team! ---
                            game_teams = ["Mclaren", "Mercedes", "Redbull", "VCARB", "ferrari", "Williams", "AstonMartin", "Haas", "Audi", "Alpine", "Cadillac"]
                            for team in game_teams:
                                if card_name.replace(" ", "").lower() == team.lower():
                                    my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"])
                                    if team not in my_unlocked:
                                        my_unlocked.append(team)
                                        unlocked_cars[loggedInUser] = my_unlocked
                                        save_unlocked_cars()
                                    break 
                            # ---------------------------------------------------
                            
                            # Remove from market
                            market_listings.remove(market_selected)
                            save_market()
                            
                            market_msg = f"Listing Cancelled."
                            market_selected = None

                # --- UPDATED: Auth Selection Clicks ---
                elif gamestate == "authMenu":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "main"
                    
                    # 1. Create Account Button Hitbox
                    create_w = f1font.size('SIGN UP')[0] + 40
                    if 100 < mouseX < 100 + create_w and 270 < mouseY < 340:
                        gamestate = "signUp"
                        UsernameInputed, passwordInputed, abbrInputed = "", "", ""
                        typing = False
                        
                    # 2. Sign In Button Hitbox
                    signin_w = f1font.size('SIGN IN')[0] + 40
                    if 100 < mouseX < 100 + signin_w and 350 < mouseY < 420:
                        gamestate = "signIn"
                        UsernameInputed, passwordInputed = "", ""
                        typing = False

               # --- UPDATED: Sign Up & Sign In Mouse Clicks ---
                elif gamestate == "signUp" or gamestate == "signIn":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: # Back Button
                        gamestate = "authMenu"
                        typing = False
                    
                    # 1. Username Input Pill (y=280)
                    elif 100 < mouseX < 700 and 280 < mouseY < 350:
                        typing, UsernameTyping, passwordTyping, abbrTyping = True, True, False, False
                    
                    # 2. Password Input Pill (y=370)
                    elif 100 < mouseX < 700 and 370 < mouseY < 440:
                        typing, passwordTyping, UsernameTyping, abbrTyping = True, True, False, False
                    
                    # 3. Tag Input Pill (Sign Up Only, y=460)
                    elif gamestate == "signUp" and 100 < mouseX < 700 and 460 < mouseY < 530:
                        typing, abbrTyping, UsernameTyping, passwordTyping = True, True, False, False
                    
                    else:
                        typing = False

                    if gamestate == "signUp":
                        # Match the 'CREATE' width from the UI render
                        submit_w = f1font.size('CREATE')[0] + 60
                        if 100 < mouseX < 100 + submit_w and 570 < mouseY < 645:
                            # Require exactly 3 letters for the tag
                            if not UsernameExist and UsernameInputed != "" and passwordInputed != "" and len(abbrInputed) == 3:
                                users[UsernameInputed] = passwordInputed
                                save_accounts()
                                
                                user_abbrs[UsernameInputed] = abbrInputed.upper()
                                save_abbrs()
                                
                                if UsernameInputed not in unlocked_cars:
                                    unlocked_cars[UsernameInputed] = ["Alpine"]
                                    save_unlocked_cars()
                                
                                loggedInUser = UsernameInputed
                                save_session(loggedInUser) # <--- ADD THIS LINE
                                gamestate = "main"

                    elif gamestate == "signIn":
                        # Match the 'LOGIN' width from the UI render
                        submit_w = f1font.size('LOGIN')[0] + 60
                        if 100 < mouseX < 100 + submit_w and 480 < mouseY < 555:
                            if UsernameInputed in users and users[UsernameInputed] == passwordInputed:
                                loggedInUser = UsernameInputed
                                save_session(loggedInUser) # <--- ADD THIS LINE
                                gamestate = "main"

                # --- Account Info Menu Clicks ---
                elif gamestate == "accountMenu":
                    if 30 < mouseX < 90 and 30 < mouseY < 90: gamestate = "main"
                    elif 100 < mouseX < 100 + f1font.size('VIEW MY CARDS')[0] + 40 and 250 < mouseY < 300:
                        gamestate = "inventory"
                        inventory_scroll = 0
                        my_drivers = owned_drivers.get(loggedInUser, [])
                        for drv in my_drivers:
                            if drv not in inventory_loaded_imgs:
                                path = find_driver_card(drv)
                                if path:
                                    try:
                                        img = pygame.image.load(path).convert_alpha()
                                        # --- CHANGED: scale to smoothscale ---
                                        inventory_loaded_imgs[drv] = pygame.transform.smoothscale(img, (228, 300)) 
                                    except: pass
                    elif 100 < mouseX < 100 + f1font.size('SIGN OUT')[0] + 40 and 330 < mouseY < 380:
                        loggedInUser = None
                        clear_session() # <--- ADD THIS LINE
                        gamestate = "main"

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
                    if 30 < mouseX < 90 and 30 < mouseY < 90: gamestate = "main"
                    elif 100 < mouseX < 100 + f1font.size('HOST')[0] + 40 and 250 < mouseY < 300: 
                        if n is not None and n.p is not None:
                            reply = n.send(["CREATE", [trackX, trackY, angle, car_name, "LOBBY"]])
                            if reply:
                                my_lobby_id, my_player_index = reply[0], reply[1]
                                gamestate = "hostLobby"
                    elif 100 < mouseX < 100 + f1font.size('JOIN')[0] + 40 and 330 < mouseY < 380:
                        if n is not None and n.p is not None:
                            lobby_list = n.send(["GET"]) 
                            if lobby_list is not None:
                                available_lobbies = lobby_list
                                gamestate = "joinLobby"
                # --- NEW: TYRE SELECTION CLICKS ---
                elif gamestate == "tyreSelect":
                    if 30 < mouseX < 90 and 30 < mouseY < 90:
                        # Go back depending on online/offline state
                        gamestate = "ChooseTrack" if my_lobby_id is None else "hostLobby"
                    
                    # Hitboxes for the 3 tyre choices
                    elif 240 < mouseX < 460 and 200 < mouseY < 500:
                        selected_tyre_compound = "Soft"
                        gamestate = "start"
                    elif 530 < mouseX < 750 and 200 < mouseY < 500:
                        selected_tyre_compound = "Medium"
                        gamestate = "start"
                    elif 820 < mouseX < 1040 and 200 < mouseY < 500:
                        selected_tyre_compound = "Hard"
                        gamestate = "start"
                        
                    # Apply Top Speed Modifiers instantly!
                    if gamestate == "start":
                        
                        if selected_tyre_compound == "Soft":
                            maxSpeed += 1.0
                            carMaxSpeed += 1.0
                        elif selected_tyre_compound == "Hard":
                            maxSpeed -= 0.5
                            carMaxSpeed -= 0.5
                elif gamestate == "start":
                    # Check for pause button click (top left corner)
                        if 10 < mouseX < 60 and 10 < mouseY < 60:
                            gamestate = "paused"
                # ----------------------------------
                elif gamestate == "paused":
                    # 1. RESUME BUTTON
                    if 490 < mouseX < 790 and 250 < mouseY < 330:
                        gamestate = "start"
                    
                    # 2. MAIN MENU BUTTON
                    elif 490 < mouseX < 790 and 360 < mouseY < 440:
                        # Safety: Leave lobby if online so the server doesn't hang
                        if n is not None and n.p is not None and my_lobby_id is not None:
                            n.send(["LEAVE", my_lobby_id, my_player_index])
                        
                        # Reset networking and race variables
                        my_lobby_id = None
                        my_player_index = None
                        taken_cars = []
                        speed = 0
                        lap = 0
                        gamestate = "main"
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
                    # --- NEW: LEAVE LOBBY BUTTON (Shifted to Sidebar) ---
                    if 950 < mouseX < 1230 and 30 < mouseY < 90:
                        if n is not None and n.p is not None and my_lobby_id is not None: 
                            n.send(["LEAVE", my_lobby_id, my_player_index])
                        
                        my_lobby_id = None
                        my_player_index = None
                        taken_cars = []
                        gamestate = "onlineMenu"

                    # --- NEW: START RACE BUTTON (Shifted to Sidebar) ---
                    if my_player_index == 0:
                        if 950 < mouseX < 1230 and 600 < mouseY < 680:
                            can_start = False
                            if isinstance(lobby_data, list):
                                active_players = [p for p in lobby_data if p is not None]
                                if len(active_players) >= 2:
                                    can_start = True
                                    for p in active_players:
                                        if len(p) > 4 and p[4] == "RACING":
                                            can_start = False
                                            break
                            
                            if can_start:
                                gamestate = "tyreSelect"
                                active_p = [i for i, p in enumerate(lobby_data) if p is not None]
                                random.shuffle(active_p)
                                my_grid_order = active_p
                                
                                my_pos_index = my_grid_order.index(my_player_index)
                                if currentTrack == bahrainTrack and len(bahrain_grid) > my_pos_index:
                                    trackX, trackY, angle = bahrain_grid[my_pos_index]
                                elif currentTrack == silverstoneTrack: 
                                    trackX, trackY, angle = silverstone_grid[my_pos_index]
                                
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

                    # --- NEW: COMPACT CAR SELECTION GRID ---
                    all_teams = [
                        (Mclaren, 50, 130, 'Mclaren'), (Mercedes, 190, 130, 'Mercedes'),
                        (Redbull, 330, 130, 'Redbull'), (VCARB, 470, 130, 'VCARB'),
                        (ferrari, 610, 130, 'ferrari'), (Williams, 750, 130, 'Williams'),
                        (AstonMartin, 120, 360, 'AstonMartin'), (Haas, 260, 360, 'Haas'),
                        (Audi, 400, 360, 'Audi'), (Alpine, 540, 360, 'Alpine'), 
                        (Cadillac, 680, 360, 'Cadillac')
                    ]

                    my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]
                    
                    for img, x, y, name in all_teams:
                        if x < mouseX < x + 130 and y < mouseY < y + 195: # Tighter Hitboxes
                            if (name not in taken_cars or name == "Alpine") and name in my_unlocked:
                                car = img
                                car_name = name 
                                
                                # Updated 2026 Team Speed Hierarchy
                                speed_map = {
                                    'Mercedes': 15.5,    # 1st - Dominant 
                                    'ferrari': 15.0,     # 2nd - Front-runner
                                    'Mclaren': 14.0,     # 3rd - Best of rest
                                    'Haas': 13.0,        # 4th - Midfield leader
                                    'Alpine': 12.5,      # 5th - Midfield star
                                    'Redbull': 12.5,     # 6th - Slumping
                                    'VCARB': 12.0,       # 7th - Racing Bulls
                                    'Audi': 11.5,        # 8th - Improving
                                    'Williams': 11.0,    # 9th - Struggling
                                    'Cadillac': 10.5,    # 10th - Back marker
                                    'AstonMartin': 10.0  # 11th - Back of grid
                                }
                                
                                # Pull the active driver to apply their Pace boost!
                                user_squads = active_driver.get(loggedInUser, {}) if 'active_driver' in globals() else {}
                                if not isinstance(user_squads, dict): user_squads = {}
                                my_drv = user_squads.get(name, "None")
                                
                                carMaxSpeed = get_boosted_speed(speed_map[name], my_drv) if 'get_boosted_speed' in globals() else speed_map[name]
                                maxSpeed = carMaxSpeed

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
                        gamestate = "tyreSelect"
                        
                        # --- NEW: RANDOM GRID POSITIONS ---
                        grid_slots = list(range(10))
                        random.shuffle(grid_slots)
                        my_slot = grid_slots.pop(0) # Take the first random slot for the player
                        trackX, trackY, angle = bahrain_grid[my_slot]
                        # ----------------------------------
                        
                        lightSound.set_volume(100)
                        lightSound.play() 
                        lap, lap1time, lap2time, lap3time, speed = 0, 0, 0, 0, 0
                        points_awarded, lightsOut, pendingPenalty, TimePenalty = False, False, False, 0
                        lights, time = -1, -7
                        FLTW, FRTW, RLTW, RRTW = 99, 99, 99, 99
                        tyresintact = True
                        
                        # --- NEW: SPAWN BAHRAIN AI BOTS ---
                        offline_ai_cars = []
                        if ENABLE_OFFLINE_AI: 
                            teams = [('Mclaren', Mclaren), ('Mercedes', Mercedes), ('Redbull', Redbull), 
                                     ('ferrari', ferrari), ('AstonMartin', AstonMartin), ('Williams', Williams),
                                     ('VCARB', VCARB), ('Haas', Haas), ('Audi', Audi), ('Alpine', Alpine), ('Cadillac', Cadillac)]
                            teams = [t for t in teams if t[0] != car_name] 
                            
                            for i, slot_idx in enumerate(grid_slots): # Loop over the remaining 9 slots
                                gx, gy, ga = bahrain_grid[slot_idx]
                                t_name, t_img = teams[i % len(teams)]
                                
                                team_base_speeds = {
                                    'Mercedes': 15.5, 'ferrari': 15.0, 'Mclaren': 14.0, 'Haas': 13.0, 
                                    'Alpine': 12.5, 'Redbull': 12.5, 'VCARB': 12.0, 'Audi': 11.5, 
                                    'Williams': 11.0, 'Cadillac': 10.5, 'AstonMartin': 10.0
                                }
                                base_spd = team_base_speeds.get(t_name, 12.0) + random.uniform(-0.5, 1.0)
                                
                                comp = random.choice(["Soft", "Medium", "Hard"])
                                if comp == "Soft": base_spd += 1.0
                                elif comp == "Hard": base_spd -= 0.5
                                
                                offline_ai_cars.append({
                                    'name': t_name, 'img': t_img, 'trackX': gx, 'trackY': gy, 'angle': ga, 
                                    'speed': 0, 'maxSpeed': base_spd, 
                                    'turn_speed': 3.0, 'wp': 0, 'lap': 0,
                                    'offset_x': random.randint(int(-CHECKPOINT_RADIUS * 0.5), int(CHECKPOINT_RADIUS * 0.5)), 
                                    'offset_y': random.randint(int(-CHECKPOINT_RADIUS * 0.5), int(CHECKPOINT_RADIUS * 0.5)),
                                    'mistake_timer': 0,
                                    'tyre': comp,
                                    'reaction_delay': random.randint(5, 45) # 5 to 45 frame delay at lights out
                                })
                    # silverstone track selection
                    elif 480 < mouseX < 835 and 450 < mouseY < 687:
                        currentTrack = silverstoneTrack
                        gamestate = "tyreSelect"
                        
                        # --- NEW: RANDOM GRID POSITIONS ---
                        grid_slots = list(range(10))
                        random.shuffle(grid_slots)
                        my_slot = grid_slots.pop(0) 
                        trackX, trackY, angle = silverstone_grid[my_slot]
                        # ----------------------------------
                        
                        lightSound.set_volume(100)
                        lightSound.play() 
                        lap, lap1time, lap2time, lap3time, speed = 0, 0, 0, 0, 0
                        points_awarded, lightsOut, pendingPenalty, TimePenalty = False, False, False, 0
                        lights, time = -1, -7
                        FLTW, FRTW, RLTW, RRTW = 99, 99, 99, 99
                        tyresintact = True

                        # --- NEW: SPAWN SILVERSTONE AI BOTS ---
                        offline_ai_cars = []
                        if ENABLE_OFFLINE_AI: 
                            teams = [('Mclaren', Mclaren), ('Mercedes', Mercedes), ('Redbull', Redbull), 
                                     ('ferrari', ferrari), ('AstonMartin', AstonMartin), ('Williams', Williams),
                                     ('VCARB', VCARB), ('Haas', Haas), ('Audi', Audi), ('Alpine', Alpine), ('Cadillac', Cadillac)]
                            teams = [t for t in teams if t[0] != car_name] 
                            
                            for i, slot_idx in enumerate(grid_slots): 
                                gx, gy, ga = silverstone_grid[slot_idx]
                                t_name, t_img = teams[i % len(teams)]
                                base_spd = 13.0 + random.uniform(-0.5, 1.5)
                                
                                comp = random.choice(["Soft", "Medium", "Hard"])
                                if comp == "Soft": base_spd += 1.0
                                elif comp == "Hard": base_spd -= 0.5
                                
                                offline_ai_cars.append({
                                    'name': t_name, 'img': t_img, 'trackX': gx, 'trackY': gy, 'angle': ga, 
                                    'speed': 0, 'maxSpeed': base_spd, 
                                    'turn_speed': 3.0, 'wp': 0, 'lap': 0,
                                    'offset_x': random.randint(int(-CHECKPOINT_RADIUS * 0.5), int(CHECKPOINT_RADIUS * 0.5)),
                                    'offset_y': random.randint(int(-CHECKPOINT_RADIUS * 0.5), int(CHECKPOINT_RADIUS * 0.5)),
                                    'mistake_timer': 0,
                                    'tyre': comp,
                                    'reaction_delay': random.randint(5, 45) # 5 to 45 frame delay at lights out
                                })
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
                        inventory_scroll = 0
                        my_drivers = owned_drivers.get(loggedInUser, [])
                        for drv in my_drivers:
                            if drv not in inventory_loaded_imgs:
                                path = find_driver_card(drv)
                                if path:
                                    try:
                                        img = pygame.image.load(path).convert_alpha()
                                        # --- CHANGED: scale to smoothscale ---
                                        inventory_loaded_imgs[drv] = pygame.transform.smoothscale(img, (228, 300)) 
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

                    # Click to Equip Driver
                    start_x, start_y, x_spacing, y_spacing = 70, 110, 290, 320 
                    clip_y_start = 90 # Start checking clicks below the header
                    
                    for i in range(len(filtered_drivers)):
                        row, col = i // 4, i % 4
                        draw_x = start_x + (col * x_spacing)
                        draw_y = start_y + (row * y_spacing) - inventory_scroll # Apply Scroll Offset
                        
                        # Only allow equipping if they click INSIDE the visible scroll area!
                        if mouseY >= clip_y_start:
                            if draw_x < mouseX < draw_x + 228 and draw_y < mouseY < draw_y + 300: 
                                
                                if loggedInUser not in active_driver or not isinstance(active_driver[loggedInUser], dict):
                                    active_driver[loggedInUser] = {}
                                
                                target_driver = filtered_drivers[i]
                                
                                # Unequip from other cars
                                for existing_car, existing_driver in list(active_driver[loggedInUser].items()):
                                    if existing_driver == target_driver:
                                        active_driver[loggedInUser][existing_car] = "None"
                                
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
                    if 30 < mouseX < 90 and 30 < mouseY < 90: gamestate = "main"
                    elif 100 < mouseX < 100 + f1font.size('RACING LINE')[0] + 40 and 250 < mouseY < 300: 
                        racingLine = not racingLine
        # keyboard events
        if ev.type == pygame.KEYDOWN:  
            # --- ADD THE ESCAPE CHECK HERE ---
            if ev.key == pygame.K_ESCAPE:
                if gamestate == "start":
                    gamestate = "paused"
                elif gamestate == "paused":
                    gamestate = "start"
            # ----------------------------------

            # (Your existing grid mapping, F11 toggle, and typing logic follows...)
            if ev.key == pygame.K_g and gamestate == "start":
                print(f"    ({round(trackX, 1)}, {round(trackY, 1)}, {int(angle)}),")
                
            # --- NEW: CHECKPOINT MAKER TOOL ---
            if ev.key == pygame.K_c and gamestate == "start":
                # 1. Get exact center of car
                px = -trackX + 640
                py = -trackY + 360
                
                # 2. Create the Rect and save it
                rect_x = int(px - CHECKPOINT_RADIUS)
                rect_y = int(py - CHECKPOINT_RADIUS)
                rect_w = int(CHECKPOINT_RADIUS * 2)
                
                custom_checkpoints.append(pygame.Rect(rect_x, rect_y, rect_w, rect_w))
                print(f"Added Gate {len(custom_checkpoints)}")
                
            # Press 'Z' to Undo the last placement
            elif ev.key == pygame.K_z and gamestate == "start":
                if len(custom_checkpoints) > 0:
                    custom_checkpoints.pop()
                    print(f"Undo! {len(custom_checkpoints)} gates remaining.")
                    
            # Press 'P' to Print the final list to the console
            elif ev.key == pygame.K_p and gamestate == "start":
                print("\n# --- COPY & PASTE THIS INTO YOUR CODE ---")
                print("new_track_checkpoints = [")
                for rect in custom_checkpoints:
                    print(f"    pygame.Rect({rect.x}, {rect.y}, {rect.width}, {rect.height}),")
                print("]\n# ----------------------------------------")
            # --------------------------------------------------
            
            # --- NEW: SQUAD BUILDER SEARCH VARIABLES ---
            # (If these aren't initialized at the top of your file, Python will create them here)
            if 'squad_search_input' not in globals(): squad_search_input = ""
            if 'squad_typing' not in globals(): squad_typing = False
            # -------------------------------------------
                        
            # --- NEW: Sell Price Typing ---
            if sell_price_typing and gamestate == "market" and market_tab == "SELL":
                if ev.key == pygame.K_BACKSPACE:
                    sell_price_input = sell_price_input[:-1]
                elif ev.key == pygame.K_RETURN:
                    sell_price_typing = False
                elif ev.unicode.isnumeric():
                    if len(sell_price_input) < 7: # Max 9,999,999 PTS
                        sell_price_input += ev.unicode
            # ------------------------------

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
                if 'active_drs_zones' in globals() and active_drs_zones.get(car_name, False):
                    toggleDRS()
            if ev.key == pygame.K_UP and gear != 8:
                gear += 1

            elif ev.key == pygame.K_DOWN and gear != 1:
                gear -= 1

            if ev.key == pygame.K_UP or ev.key == pygame.K_DOWN:
                maxSpeed = (carMaxSpeed-8) + gear

        # --- NEW: CATCH TITLE BAR MAXIMIZE ---
        elif ev.type == pygame.VIDEORESIZE:
            # If we aren't in F11 mode, let the user maximize or drag the window!
            if not is_fullscreen:
                real_screen = pygame.display.set_mode((ev.w, ev.h), pygame.RESIZABLE)
        # -------------------------------------

        # --- SQUAD BUILDER SEARCH VARIABLES ---

    # ==================================================
    # --- MULTIPLAYER SYNC BLOCK ---
    # ==================================================
    current_time = pygame.time.get_ticks()

    if current_time - last_network_update > 30:
        last_network_update = current_time 

        if n is not None and n.p is not None and my_lobby_id is not None:
            if gamestate == "start": 
                my_status = "RACING"
            elif gamestate == "stats": 
                my_status = "FINISHED"
            else: 
                my_status = "LOBBY"
            # Get your custom tag, default to "PLY" if something goes wrong
            my_abbr = user_abbrs.get(loggedInUser, "PLY") if loggedInUser else "GUE"
            
            # INCLUDE THE GRID ORDER AND ABBREVIATION IN THE UPDATE
            t_compound = selected_tyre_compound if 'selected_tyre_compound' in globals() else "Medium"
            lobby_data = n.send(["UPDATE", my_lobby_id, my_player_index,[trackX, trackY, angle, car_name, my_status, my_checkpoint_index, lap, my_grid_order, my_abbr, t_compound]])

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
                        gamestate = "tyreSelect"
                        
                        # --- RETRIEVE GRID POSITION FROM HOST ---
                        host_grid_order = host_data[7]
                        my_pos_index = 0
                        if my_player_index in host_grid_order:
                            my_pos_index = host_grid_order.index(my_player_index)
                        
                        if currentTrack == bahrainTrack and len(bahrain_grid) > my_pos_index:
                            trackX, trackY, angle = bahrain_grid[my_pos_index]
                        elif currentTrack == silverstoneTrack: 
                            trackX, trackY, angle = silverstone_grid[my_pos_index]
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

    if gamestate == "start":
        # --- NEW: TYRE WEAR SNAPSHOT ---
        old_FLTW, old_FRTW, old_RLTW, old_RRTW = FLTW, FRTW, RLTW, RRTW
        
        # Calculate your car's position...
        player_track_x = -trackX + 640
        player_track_y = -trackY + 360
        
        # ==========================================
        # ==========================================
        # --- NEW: OFFLINE AI BOT LOGIC & FAKE LOBBY ---
        if my_lobby_id is None: 
            my_player_index = 0
            my_abbr = user_abbrs.get(loggedInUser, "PLY") if loggedInUser else "GUE"
            
            # 1. Put the actual player in index 0 of the fake lobby
            t_compound = selected_tyre_compound if 'selected_tyre_compound' in globals() else "Medium"
            lobby_data = [[trackX, trackY, angle, car_name, "RACING", my_checkpoint_index, lap, [], my_abbr, t_compound]]
            
            # 2. Update Bots
            if lightsOut: 
                active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
                if active_checkpoints:
                    import math
                    import random 
                    
                    for i, ai in enumerate(offline_ai_cars):
                        # Grab the checkpoint and add the AI's personal racing line offset
                        target_rect = active_checkpoints[ai["wp"]]
                        target_x = target_rect.centerx + ai['offset_x']
                        target_y = target_rect.centery + ai['offset_y']
                        
                        ai_map_x, ai_map_y = -ai['trackX'] + 640, -ai['trackY'] + 360
                        dx, dy = target_x - ai_map_x, target_y - ai_map_y
                        
                        # --- UPDATED AI PROGRESS TRACKING ---
                        distance = math.sqrt(dx**2 + dy**2)
                        
                        # Add a 50px buffer so they don't overshoot it at high speeds!
                        if distance < CHECKPOINT_RADIUS + 50: 
                            # Update the AI's waypoint so the leaderboard sees its progress
                            ai['wp'] = (ai['wp'] + 1) % len(active_checkpoints)
                            
                            # If they cross the final checkpoint (index 0), increment their lap
                            if ai['wp'] == 0: 
                                ai['lap'] += 1
                        # ------------------------------------
                            
                        target_angle = math.degrees(math.atan2(dy, -dx))
                        diff = (target_angle - ai['angle'] + 180) % 360 - 180
                        
                        # --- THE MISTAKE SYSTEM ---
                        # 0.5% chance per frame to lose focus and understeer into a corner!
                        if random.random() < 0.005 and ai['mistake_timer'] == 0:
                            ai['mistake_timer'] = random.randint(20, 60) # Panic for 20-60 frames
                            
                        if ai['mistake_timer'] > 0:
                            ai['mistake_timer'] -= 1
                            active_turn_speed = ai['turn_speed'] * 0.3 # Terrible understeer!
                        else:
                            active_turn_speed = ai['turn_speed']
                        # --------------------------
                        
                        if diff > 3: ai['angle'] += active_turn_speed
                        elif diff < -3: ai['angle'] -= active_turn_speed
                            
                        # --- REACTION TIME SYSTEM ---
                        if ai.get('reaction_delay', 0) > 0:
                            ai['reaction_delay'] -= 1
                            t_speed = 0 # Keep foot off the gas while reacting!
                        else:
                            # Dynamic Braking & Throttle
                            if abs(diff) > 50: t_speed = ai['maxSpeed'] * 0.4 
                            elif abs(diff) > 25: t_speed = ai['maxSpeed'] * 0.8 
                            else: 
                                t_speed = ai['maxSpeed'] 
                                
                                # AI DRS ACTIVATION
                                if 'active_drs_zones' in globals() and active_drs_zones.get(ai['name'], False):
                                    t_speed += 2.0 
                        # ----------------------------
                        
                        if ai['speed'] < t_speed: 
                            ai['speed'] += 0.2
                        elif ai['speed'] > t_speed: 
                            ai['speed'] -= 0.5
                            
                        # Move AI Forward
                        rad = math.radians(ai['angle'])
                        ai['trackX'] += ai['speed'] * math.cos(rad)
                        ai['trackY'] += ai['speed'] * -math.sin(rad)
                        
                        # --- AI VS AI COLLISION SYSTEM ---
                        for j, other_ai in enumerate(offline_ai_cars):
                            if i != j:
                                c_dx = ai['trackX'] - other_ai['trackX']
                                c_dy = ai['trackY'] - other_ai['trackY']
                                c_dist = math.sqrt(c_dx**2 + c_dy**2)
                                
                                if 0 < c_dist < 70:
                                    # Add the same 5-pixel buffer for bots
                                    overlap = (70 - c_dist) + 5
                                    
                                    # Push bots apart more aggressively
                                    ai['trackX'] += (c_dx / c_dist) * overlap * 1.2
                                    ai['trackY'] += (c_dy / c_dist) * overlap * 1.2
                                    
                                    # Drop bot speed significantly on impact
                                    ai['speed'] *= 0.5
                        # ---------------------------------
                        
                        # --- AI VS PLAYER COLLISION ---
                        p_dx = ai['trackX'] - trackX
                        p_dy = ai['trackY'] - trackY
                        p_dist = math.sqrt(p_dx**2 + p_dy**2)
                        
                        if 0 < p_dist < 70:
                            overlap = 70 - p_dist
                            # Push AI away from Player! (Your existing code pushes the player away from them!)
                            ai['trackX'] += (p_dx / p_dist) * overlap * 0.5
                            ai['trackY'] += (p_dy / p_dist) * overlap * 0.5
                            ai['speed'] *= 0.8 
                        # ------------------------------
                        
        # 3. Push AI into the lobby data
        for ai in offline_ai_cars:
            lobby_data.append([ai['trackX'], ai['trackY'], ai['angle'], ai['name'], "RACING", ai['wp'], ai['lap'], [], ai['name'][:3].upper(), ai.get('tyre', 'Medium')])
        # ==========================================
        # --- NEW: MULTIPLAYER CAR COLLISION & SLIPSTREAM ---
        if isinstance(lobby_data, list):
            import math 
            
            in_slipstream = False
            
            for i, p in enumerate(lobby_data):
                # Only check against active opponents
                if i != my_player_index and p is not None and len(p) >= 2:
                    other_x, other_y = p[0], p[1]
                    
                    # 1. Calculate the distance vector FROM player TO opponent
                    dx = trackX - other_x
                    dy = trackY - other_y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    min_distance = 70 
                    
                    # --- UPGRADED: MULTIPLAYER COLLISION RESOLUTION ---
                    if 0 < distance < min_distance:
                        # 1. Calculate overlap PLUS a 5-pixel buffer to prevent sticking
                        overlap = (min_distance - distance) + 5 
                        
                        # 2. Stronger Shove: Move the player out of the collision zone immediately
                        trackX += (dx / distance) * overlap * 1.2
                        trackY += (dy / distance) * overlap * 1.2
                        
                        # 3. Smart Speed Scrub: Check if you hit them or they hit YOU
                        angleRadians = math.radians(angle)
                        fwd_x = math.cos(angleRadians)
                        fwd_y = -math.sin(angleRadians)
                        
                        # Vector pointing from you TO the opponent
                        to_opp_x = -dx 
                        to_opp_y = -dy 
                        
                        # Dot product measures alignment (>0 means they are in front, <0 means behind)
                        dot_impact = (fwd_x * to_opp_x) + (fwd_y * to_opp_y)
                        
                        # Only punish your speed if YOU rear-ended THEM (they are in front of you)
                        if dot_impact > 0:
                            if abs(speed) > 1:
                                speed *= 0.5 # Scrub speed for hitting a car ahead
                        # If dot_impact is <= 0, they rear-ended you! You keep your momentum.
                    # --------------------------------------------------
                    # --- NEW: SLIPSTREAM (DRAFTING) LOGIC ---
                    elif min_distance <= distance < 400: # Drafting range up to 400 pixels
                        # Calculate player's forward direction
                        angleRadians = math.radians(angle)
                        fwd_x = math.cos(angleRadians)
                        fwd_y = -math.sin(angleRadians)
                        
                        # Normalize the vector pointing to the opponent
                        dir_x = dx / distance
                        dir_y = dy / distance
                        
                        # Dot product gives us the alignment (1.0 = perfectly in front)
                        dot = (fwd_x * dir_x) + (fwd_y * dir_y)
                        
                        # If dot > 0.96, the opponent is in a narrow cone directly in front of us!
                        if dot > 0.96:
                            in_slipstream = True

            # --- APPLY THE SLIPSTREAM BOOST ---
            if in_slipstream and speed > 5:
                # Temporarily increase our maximum speed cap
                draft_max = maxSpeed + 2.0
                
                if speed < draft_max:
                    speed += 0.05 # Add extra acceleration to "suck" the player forward
        # ==========================================
        
        # (Your existing drawing and network code continues below)


        # Create a 1280x720 camera window based on your coordinates
        camera_rect = pygame.Rect(int(-trackX), int(-trackY), windowWidth, windowHeight)

        # draw track using the camera 'area'
        if currentTrack == bahrainTrack:
            if racingLine:
                screen.blit(bahrainTrackLine, (0, 0), area=camera_rect)
            else:
                screen.blit(bahrainTrack, (0, 0), area=camera_rect)

        # ... (Your track drawing code)
        elif currentTrack == silverstoneTrack:
            if racingLine:
                screen.blit(silverstoneTrackLine, (0, 0), area=camera_rect)
            else:
                screen.blit(silverstoneTrack, (0, 0), area=camera_rect)

        # --- ADD THIS: DRAW LIVE CHECKPOINTS ---
        for idx, rect in enumerate(custom_checkpoints):
            # Translate absolute map coordinates to your camera's screen coordinates
            screen_x = rect.x + trackX
            screen_y = rect.y + trackY
            
            # Create a transparent green surface
            gate_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            gate_surf.fill((0, 255, 0, 80)) # 80 is the transparency (0-255)
            
            # Draw a solid green border around it
            pygame.draw.rect(gate_surf, (0, 255, 0), (0, 0, rect.width, rect.height), 4)
            
            screen.blit(gate_surf, (screen_x, screen_y))
            
            # Draw the checkpoint number in the center so you know the order
            num_txt = f1font2.render(str(idx), True, "white")
            screen.blit(num_txt, num_txt.get_rect(center=(screen_x + rect.width//2, screen_y + rect.height//2)))
        
        # ---------------------------------------
         
        centerColor = screen.get_at((616, 444))

        # --- NEW: ANTI-WALL STUCK SYSTEM ---
        if 'safe_trackX' not in globals():
            safe_trackX, safe_trackY = trackX, trackY
            
        # If we are safely on the track (not touching a wall), save this location!
        if centerColor != (127, 127, 127):
            safe_trackX = trackX
            safe_trackY = trackY
        # -----------------------------------

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
            elif car == Audi and centerColor == (94, 17, 0): # <--- UPDATED AUDI COLOR
                speed = 0
                pitstopReset()
                pitstop = False
            elif car == Alpine and centerColor == (161, 108, 144):
                speed = 0
                pitstopReset()
                pitstop = False
            # --- NEW: Cadillac Pitstop ---
            elif car == Cadillac and centerColor == (113, 113, 113): # <--- UPDATED CADILLAC COLOR
                speed = 0
                pitstopReset()
                pitstop = False

        # Wall crash detection - Adjusted for easier gameplay
        if centerColor == (127,127,127):
            if DRS and speed > 0:
                # Reduced from 2*speed to 0.5*speed
                FLTW -= int(0.5 * speed)
                FRTW -= int(0.5 * speed)
                if not pygame.mixer.music.get_busy():
                    iAmStupid.play()

            elif speed > 0:
                # Reduced from int(speed) to int(0.2*speed)
                FLTW -= int(0.2 * speed)
                FRTW -= int(0.2 * speed)

        # --- UPGRADED WALL COLLISION ---
        if centerColor == (127, 127, 127):
            # Snap the car back to the last known safe spot on the asphalt
            trackX = safe_trackX
            trackY = safe_trackY
            
            # Bounce the car by reversing the speed and cutting momentum in half
            speed *= -0.5 
            
            # If we were stationary and an AI shoved us into the wall, give a tiny push back
            if abs(speed) < 1:
                speed = -1
        else:
            if speed < 0:
                speed += 0.2
        # -------------------------------
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
        # --- DRAW OPPONENTS & SPATIAL AUDIO ---
        # ==================================================
        if isinstance(lobby_data, list):
            car_images = {
                "ferrari": ferrari, "Mclaren": Mclaren, "Mercedes": Mercedes,
                "Redbull": Redbull, "VCARB": VCARB, "Williams": Williams,
                "AstonMartin": AstonMartin, "Haas": Haas, "Audi": Audi,
                "Alpine": Alpine, "Cadillac": Cadillac
            }
            
            max_hear_distance = 1500.0 # Distance in pixels before engine fades to 0

            for i, p in enumerate(lobby_data):
                if p is not None and i != my_player_index and len(p) > 4 and p[4] in ["RACING", "FINISHED"]:
                    
                    p_trackX, p_trackY, p_angle, p_car_name = p[0], p[1], p[2], p[3]
                    p_tyre = p[9] if len(p) > 9 else "Medium"
                    
                    opponentX_on_screen = 500 + (trackX - p_trackX)
                    opponentY_on_screen = 300 + (trackY - p_trackY)
                    
                    if p_car_name in car_images:
                        opponent_img = car_images[p_car_name]
                        screen.blit(pygame.transform.rotate(opponent_img, p_angle), (opponentX_on_screen, opponentY_on_screen))
                        
                        # Draw Opponent Tyre Overlays
                        if p_tyre == "Soft" and 'soft_overlay' in globals():
                            screen.blit(pygame.transform.rotate(soft_overlay, p_angle), (opponentX_on_screen, opponentY_on_screen))
                        elif p_tyre == "Medium" and 'medium_overlay' in globals():
                            screen.blit(pygame.transform.rotate(medium_overlay, p_angle), (opponentX_on_screen, opponentY_on_screen))
                        elif p_tyre == "Hard" and 'hard_overlay' in globals():
                            screen.blit(pygame.transform.rotate(hard_overlay, p_angle), (opponentX_on_screen, opponentY_on_screen))
                    
                    # --- NEW: SPATIAL AUDIO ENGINE ---
                    # 1. Calculate raw distance
                    dx = p_trackX - trackX
                    dy = p_trackY - trackY
                    distance = math.sqrt(dx**2 + dy**2)

                    if distance < max_hear_distance:
                        # 1. EXPONENTIAL FALLOFF: Sounds much more natural than linear fading
                        # Squaring the falloff makes close cars loud and far cars trail off smoothly
                        base_vol = max(0.0, 1.0 - (distance / max_hear_distance))
                        dist_vol = (base_vol ** 2) * 0.7  # 0.7 is the max volume cap

                        # 2. Calculate Player's "Right" Vector
                        player_rad = math.radians(angle)
                        right_x = math.sin(player_rad)
                        right_y = math.cos(player_rad)

                        # 3. Calculate Pan (-1.0 to 1.0)
                        raw_pan = (dx * right_x + dy * right_y) / distance if distance > 0 else 0
                        
                        # Soften the extreme edges so it never hits absolute 100% in one ear
                        # (Pure 100% left/right sounds very unnatural in headphones)
                        clamped_pan = max(-0.85, min(0.85, raw_pan))

                        # 4. CONSTANT POWER PANNING
                        # Map from [-1, 1] to [0, 1]
                        pan_normalized = (clamped_pan + 1.0) / 2.0 
                        
                        # Use quarter-sine waves to keep the acoustic power perfectly flat
                        left_vol = dist_vol * math.cos(pan_normalized * (math.pi / 2))
                        right_vol = dist_vol * math.sin(pan_normalized * (math.pi / 2))

                        # 5. Play and update the dedicated channel
                        if i not in opponent_audio_channels or not opponent_audio_channels[i].get_busy():
                            channel = pygame.mixer.find_channel()
                            if channel:
                                channel.play(opponentEngineSound, loops=-1)
                                opponent_audio_channels[i] = channel

                        if i in opponent_audio_channels:
                            opponent_audio_channels[i].set_volume(left_vol, right_vol)
                    else:
                        # Mute them to save CPU and channels if they are too far away
                        if i in opponent_audio_channels:
                            opponent_audio_channels[i].stop()
                            del opponent_audio_channels[i]
        # ==================================================

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
            # --- NEW: AUTO-DISABLE DRS IF YOU LOSE THE 1-SECOND GAP ---
            if DRS and 'active_drs_zones' in globals():
                if not active_drs_zones.get(car_name, False):
                    DRS = False # SNAP WING CLOSED!
            # ----------------------------------------------------------
            if DRS:
                if keys[pygame.K_w] and speed < maxSpeed +5:
                    speed += 0.2

            else:
                if speed > maxSpeed:
                    speed -= 0.1
        # --- NEW: UNIFIED LAP & CHECKPOINT SYSTEM (WITH SKIP PENALTIES) ---
        active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
        if active_checkpoints:
            num_gates = len(active_checkpoints)
            
            # Check the target gate AND the next 8 gates to catch skips/cuts
            for offset in range(8):
                check_idx = (my_checkpoint_index + offset) % num_gates
                gate = active_checkpoints[check_idx]
                
                if gate.collidepoint(player_track_x, player_track_y):
                    # If offset > 0, the player skipped some gates!
                    if offset > 0:
                        pendingPenalty = True
                        TimePenalty += (offset * 3) # Add 3 seconds per missed checkpoint
                        
                    my_checkpoint_index = check_idx + 1
                    
                    # If we cross the finish line (wrap around the array)
                    if my_checkpoint_index >= num_gates:
                        my_checkpoint_index = 0
                        lap += 1 # Syncs perfectly with AI logic
                        
                    break # Stop checking gates this frame once we register a hit
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
            
            # --- NEW: Show available prompt ---
            if 'active_drs_zones' in globals() and active_drs_zones.get(car_name, False) and speed > 0:
                screen.blit(f1font2.render("DRS AVAILABLE", True, (0, 255, 0)) , (500, 100))
            # ----------------------------------
        # --- NEW: DRAW COMPOUND OVERLAY & APPLY WEAR MATH ---
        # 1. Draw the transparent overlay over the car
        if selected_tyre_compound == "Soft" and 'soft_overlay' in globals():
            screen.blit(pygame.transform.rotate(soft_overlay, angle), (500, 300))
        elif selected_tyre_compound == "Medium" and 'medium_overlay' in globals():
            screen.blit(pygame.transform.rotate(medium_overlay, angle), (500, 300))
        elif selected_tyre_compound == "Hard" and 'hard_overlay' in globals():
            screen.blit(pygame.transform.rotate(hard_overlay, angle), (500, 300))
            
        # 2. Modify the degradation rate based on the compound!
        if selected_tyre_compound == "Soft":
            FLTW -= (old_FLTW - FLTW) * 0.5 # 50% extra wear
            FRTW -= (old_FRTW - FRTW) * 0.5
            RLTW -= (old_RLTW - RLTW) * 0.5
            RRTW -= (old_RRTW - RRTW) * 0.5
        elif selected_tyre_compound == "Hard":
            FLTW += (old_FLTW - FLTW) * 0.5 # 50% wear refunded
            FRTW += (old_FRTW - FRTW) * 0.5
            RLTW += (old_RLTW - RLTW) * 0.5
            RRTW += (old_RRTW - RRTW) * 0.5
        # ----------------------------------------------------
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

        # ==================================================
        # --- NEW EXACT-SCALE MINIMAP LOGIC (DYNAMIC) ---
        team_colors = {
            'Mercedes': (0, 210, 190), 'ferrari': (220, 0, 0), 'Redbull': (0, 0, 150),
            'Mclaren': (255, 128, 0), 'AstonMartin': (0, 110, 80), 'Alpine': (255, 105, 180),
            'Williams': (0, 90, 255), 'VCARB': (20, 52, 203), 'Haas': (200, 200, 200),
            'Audi': (220, 20, 20), 'Cadillac': (255, 200, 0)
        }

        # 1. Dynamically calculate the scale based on the active minimap's UI size!
        active_minimap = bahrainMinimap if currentTrack == bahrainTrack else silverstoneMinimap
        mm_w, mm_h = active_minimap.get_size()
        
        # Original track is 12800x7200. Divide by minimap size to get the exact scale factor
        scale_x = 12800 / mm_w
        scale_y = 7200 / mm_h

        # 2. Draw all opponents first (so they stay underneath you)
        if isinstance(lobby_data, list):
            for i, p in enumerate(lobby_data):
                if p is not None and i != my_player_index and len(p) > 4 and p[4] in ["RACING", "FINISHED"]:
                    p_trackX, p_trackY, p_car_name = p[0], p[1], p[3]
                    
                    # Convert network coordinates to real screen pixels
                    p_real_x = -p_trackX + 640
                    p_real_y = -p_trackY + 360
                    
                    # Apply the dynamic scale and UI offset
                    p_minimap_x = 20 + (p_real_x / scale_x)
                    p_minimap_y = 550 + (p_real_y / scale_y)
                    
                    dot_color = team_colors.get(p_car_name, (255, 255, 255))
                    pygame.draw.circle(screen, dot_color, (int(p_minimap_x), int(p_minimap_y)), 5)
                    pygame.draw.circle(screen, (0, 0, 0), (int(p_minimap_x), int(p_minimap_y)), 5, 1)

        # 3. Draw the Player's Dot last (Ensures it is ALWAYS on top)
        player_real_x = -trackX + 640
        player_real_y = -trackY + 360
        minimapX = 20 + (player_real_x / scale_x)
        minimapY = 550 + (player_real_y / scale_y)
        
        pygame.draw.circle(screen, (255, 0, 0), (int(minimapX), int(minimapY)), 7)
        pygame.draw.circle(screen, (255, 255, 255), (int(minimapX), int(minimapY)), 7, 2)
        
        speed = round(speed,1)
        # ==================================================
                
        # crash detection
        if FLTW <= 0 or FRTW <= 0 or RLTW <= 0 or RRTW <= 0:
            gamestate = "crash"

        # yellow flag display
        if flag == "yellow":
            screen.blit(f1font2.render("YELLOW FLAG", True, (255, 255, 0)) , (500, 600))

        # ==================================================
        # --- DRAW LEADERBOARD (LIVE F1 TIMING GAPS) ---
        if isinstance(lobby_data, list):
            
            def get_progress_score(p):
                if p is None or len(p) < 7: return 0
                
                # Index 6 = Laps, Index 5 = Next Checkpoint
                laps, chk_idx = p[6], p[5]
                dist = 0
                
                active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
                
                if active_checkpoints and chk_idx < len(active_checkpoints):
                    gate = active_checkpoints[chk_idx]
                    # Map coordinates back to 12800x7200 space
                    p_x, p_y = -p[0] + 640, -p[1] + 360
                    dist = math.sqrt((gate.centerx - p_x)**2 + (gate.centery - p_y)**2)
                
                # --- FIXED: Increased Lap multiplier to 1,000,000 so it always outscores checkpoints! ---
                return (laps * 1000000) + (chk_idx * 2000) + (2000 - min(dist, 2000))

            # Sort players dynamically using their exact pixel progress
            players_ranking = sorted(
                [p for p in lobby_data if p is not None and len(p) > 6], 
                key=get_progress_score, 
                reverse=True
            )

            # =======================================================
            # --- NEW: CALCULATE DRS ZONES FOR EVERYONE (AI & PLAYER) ---
            if 'active_drs_zones' not in globals():
                active_drs_zones = {}
                
            active_checkpoints = bahrain_checkpoints if currentTrack == bahrainTrack else silverstone_checkpoints
            total_gates = len(active_checkpoints) if active_checkpoints else 1
            
            for idx, p_info in enumerate(players_ranking):
                p_name = p_info[3]
                p_wp = p_info[5]
                p_laps = p_info[6]
                
                # Condition 1: Must have passed at least 5 checkpoints since the start
                checkpoints_passed = (p_laps * total_gates) + p_wp
                if checkpoints_passed < 5:
                    active_drs_zones[p_name] = False
                    continue
                
                # Condition 2: Check the gap to the car directly ahead
                if idx > 0:
                    score_ahead = get_progress_score(players_ranking[idx - 1])
                    score_current = get_progress_score(p_info)
                    
                    time_diff = max(0.0, (score_ahead - score_current) / 800.0)
                    
                    # --- NEW: STICKY DRS BUFFER ---
                    # Check if they already had DRS activated on the last frame
                    currently_active = active_drs_zones.get(p_name, False)
                    
                    if time_diff <= 1.0:
                        # Unlock immediately if within 1 second
                        active_drs_zones[p_name] = True
                    elif currently_active and time_diff <= 1.5:
                        # Keep it unlocked until they drop 1.5s behind!
                        active_drs_zones[p_name] = True 
                    else:
                        # Snap closed ONLY if they fall completely out of the slipstream
                        active_drs_zones[p_name] = False 
                    # ------------------------------
                else:
                    active_drs_zones[p_name] = False # The Leader never gets DRS!
            # =======================================================

            # =======================================================
            # --- NEW: CALCULATE IF DRS IS ALLOWED & AUTO-CLOSE ---
            drs_allowed = False
            
            if my_player_index is not None and len(lobby_data) > my_player_index:
                my_data = lobby_data[my_player_index]
                if my_data in players_ranking:
                    my_rank = players_ranking.index(my_data)
                    
                    # 1. Reset trackers at the start of a new race (time < 0)
                    if 'previous_rank' not in globals() or time < 0:
                        previous_rank = my_rank
                    if 'drs_close_timer' not in globals() or time < 0:
                        drs_close_timer = 0
                        
                    # 2. Detect an overtake! (Lower index = higher position)
                    if my_rank < previous_rank and DRS:
                        drs_close_timer = 180 # 3 seconds * 60 FPS
                        
                    previous_rank = my_rank # Save for next frame
                    
                    # 3. Handle the countdown
                    if drs_close_timer > 0:
                        drs_close_timer -= 1
                        if drs_close_timer <= 0:
                            DRS = False # SNAP DRS CLOSED!
                    
                    # 4. Standard DRS 1-Second Gap Check
                    if my_rank > 0: # If we are NOT the leader
                        score_ahead = get_progress_score(players_ranking[my_rank - 1])
                        score_current = get_progress_score(my_data)
                        
                        # Use your existing conversion math (800 pixels = ~1 second)
                        time_diff = max(0.0, (score_ahead - score_current) / 800.0)
                        
                        # Unlock DRS if the gap is 1.0s or less!
                        if 0 < time_diff <= 1.0:
                            drs_allowed = True
            # =======================================================
            start_x = 20
            start_y = 100
            row_height = 45
            box_width = 300

            for idx, p_info in enumerate(players_ranking[:10]): 
                y_pos = start_y + (idx * row_height)
                
                # 1. Position Box
                pos_color = (220, 0, 0) if idx == 0 else (30, 30, 30)
                pygame.draw.rect(screen, pos_color, (start_x, y_pos, 50, row_height - 2))
                
                pos_text = f1font2.render(str(idx + 1), True, "white")
                pos_rect = pos_text.get_rect(center=(start_x + 25, y_pos + (row_height // 2)))
                screen.blit(pos_text, pos_rect)

                # 2. Team Name Plate
                # --- UPDATED: HIGHLIGHT THE LOCAL PLAYER ---
                if p_info == lobby_data[my_player_index]:
                    row_bg_color = (0, 90, 190) # Distinct Blue for you
                else:
                    row_bg_color = (20, 20, 20) # Standard dark grey for others
                
                pygame.draw.rect(screen, row_bg_color, (start_x + 50, y_pos, box_width - 50, row_height - 2))
                # -------------------------------------------
                
                team_abbr = p_info[8] if len(p_info) > 8 else p_info[3][:3].upper()
                name_text = f1font2.render(team_abbr, True, "white")
                screen.blit(name_text, (start_x + 65, y_pos + 7))

                # 3. LIVE TIMING GAP (Interval to car ahead)
                if idx == 0:
                    gap_text = "LEADER"
                    color = (255, 215, 0) # Gold for leader
                else:
                    # Calculate gap from the car directly ahead of this player
                    score_ahead = get_progress_score(players_ranking[idx - 1])
                    score_current = get_progress_score(p_info)
                    
                    # Convert progress score difference to an estimated time in seconds
                    # (800 is our math tuner to convert Pygame pixels to seconds)
                    time_diff = max(0.0, (score_ahead - score_current) / 800.0)
                    
                    if time_diff > 100: # If the gap is huge, they are lapped
                        gap_text = "+1 LAP"
                        color = (200, 200, 200)
                    else:
                        gap_text = f"+{time_diff:.1f}s"
                        
                        # Make the text Purple if they are within DRS range (< 1.0s)
                        color = (216, 85, 255) if time_diff <= 1.0 else (255, 255, 255)
                        
                # Draw the gap perfectly right-aligned inside the box
                gap_surf = f1font2.render(gap_text, True, color)
                screen.blit(gap_surf, (start_x + box_width - 15 - gap_surf.get_width(), y_pos + 7))

                # --- HUD PAUSE BUTTON ---
        pause_rect = pygame.Rect(10, 10, 50, 50)
        pygame.draw.rect(screen, (50, 50, 50, 180), pause_rect, 0, 10) # Translucent glass
        if pause_rect.collidepoint(mouseX, mouseY):
            pygame.draw.rect(screen, "white", pause_rect, 2, 10)
        
        # Draw two vertical bars for the pause icon
        pygame.draw.rect(screen, "white", (24, 22, 6, 26))
        pygame.draw.rect(screen, "white", (40, 22, 6, 26))
        # ==================================================
    
    # start menu
    if gamestate == "main":
        pygame.mixer.stop()
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        
        # Shifted F1 Logo to the left to align with the new menu
        screen.blit(f1logo, (100, 80)) 
        
        # format: (y_position, label, requires_login)
        menu_buttons = [
            (250, 'RACE', True), 
            (330, 'MARKET', True), 
            (410, 'SETTINGS', False), 
            (490, 'ONLINE', True),
            (570, 'STORE', True), 
            (650, 'QUIT', False)  # <--- ADD THIS LINE
        ]

        for y_pos, label, requires_login in menu_buttons:
            is_disabled = requires_login and not loggedInUser
            
            # 1. Measure the text width dynamically
            text_width = f1font.size(label)[0]
            
            # 2. Size the button rect perfectly (Text Width + 20px padding on each side)
            button_rect = pygame.Rect(100, y_pos, text_width + 40, 70) 
            is_hovered = button_rect.collidepoint(mouseX, mouseY)
            
            if is_disabled:
                text_surf = f1font.render(label, True, (100, 100, 100))
                screen.blit(text_surf, (120, y_pos + 5))
                # Replace "LOCKED" text with the lock icon
                screen.blit(lock_icon, (130 + text_width, y_pos + 18))
            else:
                if is_hovered:
                    # Sleek F1-style pill outline tightly wrapping the text!
                    pygame.draw.rect(screen, (30, 30, 40), button_rect, 0, 25) 
                    pygame.draw.rect(screen, (220, 220, 220), button_rect, 2, 25) 
                    text_surf = f1font.render(label, True, (255, 255, 255)) 
                else:
                    text_surf = f1font.render(label, True, (180, 180, 180)) 
                
                screen.blit(text_surf, (120, y_pos + 5)) 


        # Draw Account Button in Main Menu
        acc_label = loggedInUser if loggedInUser else "Account"
        acc_hovered = 1050 < mouseX < 1250 and 30 < mouseY < 80
        acc_rect = pygame.Rect(1050, 30, 200, 50)
        
        if acc_hovered:
            pygame.draw.rect(screen, (30, 30, 40), acc_rect, 0, 25)
            pygame.draw.rect(screen, (220, 220, 220), acc_rect, 2, 25)
            acc_surf = f1font2.render(acc_label[:10], True, "white")
        else:
            pygame.draw.rect(screen, (50, 50, 50), acc_rect, 0, 25)
            acc_surf = f1font2.render(acc_label[:10], True, (200, 200, 200))
            
        screen.blit(acc_surf, acc_surf.get_rect(center=acc_rect.center))

        # --- NEW: Show Points underneath the Account Button ---
        if loggedInUser:
            my_pts = user_points.get(loggedInUser, 0)
            pts_surf = f1font2.render(f"{my_pts} PTS", True, (255, 215, 0)) # Gold text
            # Center it perfectly below the account pill
            screen.blit(pts_surf, pts_surf.get_rect(center=(acc_rect.centerx, acc_rect.bottom + 20)))
        # ----------------------------------------------------


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
            # --- NEW: AWARD POINTS ONCE (Online & Offline) ---
            if not points_awarded and loggedInUser:
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

                # 2. Name Plate
                # --- UPDATED: HIGHLIGHT THE LOCAL PLAYER ---
                if p_info == lobby_data[my_player_index]:
                    row_bg_color = (0, 90, 190)
                else:
                    row_bg_color = (20, 20, 20)

                pygame.draw.rect(screen, row_bg_color, (start_x + 50, y_pos, box_width - 50, row_height - 2))
                team_abbr = p_info[8] if len(p_info) > 8 else p_info[3][:3].upper()
                screen.blit(f1font2.render(team_abbr, True, "white"), (start_x + 65, y_pos + 7))
                # -------------------------------------------

                # --- NEW: Display Points Earned ---
                points_map = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
                earned_pts = points_map.get(idx + 1, 0)
                
                # Removed the lap > 3 check so trailing bots get their points shown too!
                if earned_pts > 0:
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
        # Updated 2026 Team Speed Hierarchy
        speed_map = {
            'Mercedes': 15.5,    # 1st - Dominant 
            'ferrari': 15.0,     # 2nd - Front-runner
            'Mclaren': 14.0,     # 3rd - Best of rest
            'Haas': 13.0,        # 4th - Midfield leader
            'Alpine': 12.5,      # 5th - Midfield star
            'Redbull': 12.5,     # 6th - Slumping
            'VCARB': 12.0,       # 7th - Racing Bulls
            'Audi': 11.5,        # 8th - Improving
            'Williams': 11.0,    # 9th - Struggling
            'Cadillac': 10.5,    # 10th - Back marker
            'AstonMartin': 10.0  # 11th - Back of grid
        }
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
                gray_car = pygame.transform.smoothscale(pygame.transform.rotate(img, -90), normal_size)
                gray_car.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT) 
                screen.blit(gray_car, (x + 10, y + 15))
                
                # Draw lock icon centered near the bottom of the car silhouette
                screen.blit(lock_icon, (x + 48, y + 145))
            else:
                if is_hovered or car == img:
                    # --- CHANGED: scale to smoothscale ---
                    screen.blit(pygame.transform.smoothscale(pygame.transform.rotate(img, -90), hover_size), (x, y))
                    if car == img: 
                        pygame.draw.rect(screen, (100, 255, 100), (x-5, y-5, 140, 205), 3, 15)
                else:
                    # --- CHANGED: scale to smoothscale ---
                    screen.blit(pygame.transform.smoothscale(pygame.transform.rotate(img, -90), normal_size), (x + 10, y + 15))
    # --- UPDATED: Player Economy Visuals ---
    elif gamestate == "market":
        screen.blit(menu, (0,0))
        
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Header
        screen.blit(f1font.render("PLAYER MARKET", True, "white"), (120, 20))
        my_pts = user_points.get(loggedInUser, 0)
        balance_text = f1font2.render(f"BALANCE: {my_pts} PTS", True, (255, 215, 0))
        screen.blit(balance_text, (1230 - balance_text.get_width(), 40)) 

        # --- DRAW TABS ---
        tabs = [("BUY", 120), ("SELL", 230), ("ACTIVE", 340)]
        for t_name, t_x in tabs:
            t_rect = pygame.Rect(t_x, 85, 100, 35)
            is_hovered = t_rect.collidepoint(mouseX, mouseY)
            
            if market_tab == t_name:
                pygame.draw.rect(screen, (100, 200, 255), t_rect, 0, 10)
                t_color = "black"
            else:
                pygame.draw.rect(screen, (50, 50, 60) if is_hovered else (30, 30, 40), t_rect, 0, 10)
                t_color = "white"
                
            t_surf = f1font2.render(t_name, True, t_color)
            screen.blit(t_surf, t_surf.get_rect(center=t_rect.center))

        # ==========================================
        # LEFT PANEL: LISTS & SEARCH
        # ==========================================
        visible_list = []
        my_drivers = owned_drivers.get(loggedInUser, [])
        list_start_y = 140
        
        if market_tab == "BUY":
            list_start_y = 210
            # Search Box (Only needed in BUY)
            search_rect = pygame.Rect(120, 130, 500, 60)
            pygame.draw.rect(screen, (30, 30, 40), search_rect, 0, 15)
            if market_typing: pygame.draw.rect(screen, (100, 200, 255), search_rect, 2, 15)
            else: pygame.draw.rect(screen, (100, 100, 100), search_rect, 2, 15)
            s_text = f1font2.render(market_search_input if market_search_input else "Search Driver...", True, "white" if market_search_input else (150,150,150))
            screen.blit(s_text, (140, 145))
            
            # Fetch valid listings
            visible_list = [item for item in market_listings if item["seller"] != loggedInUser]
            if market_search_input:
                visible_list = [item for item in visible_list if market_search_input.lower() in item["name"].lower()]
                
        elif market_tab == "SELL":
            visible_list = [{"name": drv, "price": 0} for drv in my_drivers]
            
        elif market_tab == "ACTIVE":
            visible_list = [item for item in market_listings if item["seller"] == loggedInUser]

        # --- NEW: CLAMP SCROLL & APPLY CLIPPING ---
        # Calculate max scroll so we can't scroll down into the void
        max_scroll = max(0, (len(visible_list) * 70) - (700 - list_start_y))
        market_scroll = max(0, min(market_scroll, max_scroll))
        
        list_y = list_start_y - market_scroll
        
        # Clip the screen! Anything drawn outside this rect is ignored
        clip_rect = pygame.Rect(120, list_start_y, 500, 700 - list_start_y)
        screen.set_clip(clip_rect)

        # Draw the List
        for item in visible_list:
            row_rect = pygame.Rect(120, list_y, 500, 60)
            
            # Make sure we only highlight the item if the mouse is inside the clipping area
            is_hovered = row_rect.collidepoint(mouseX, mouseY) and clip_rect.collidepoint(mouseX, mouseY)
            is_selected = (market_selected == item)
            
            if is_selected:
                pygame.draw.rect(screen, (50, 50, 70), row_rect, 0, 15)
                pygame.draw.rect(screen, "white", row_rect, 2, 15)
            elif is_hovered:
                pygame.draw.rect(screen, (40, 40, 50), row_rect, 0, 15)
                pygame.draw.rect(screen, (200, 200, 200), row_rect, 2, 15)
            else:
                pygame.draw.rect(screen, (20, 20, 25, 200), row_rect, 0, 15) 

            display_name = item["name"]
            if len(display_name) > 12: display_name = display_name[:10] + "..."
            screen.blit(f1font2.render(display_name, True, "white"), (140, list_y + 15))
            
            if market_tab == "BUY" or market_tab == "ACTIVE":
                price_text = f1font2.render(f"{item['price']} PTS", True, (255, 215, 0))
                screen.blit(price_text, (600 - price_text.get_width(), list_y + 15)) 
            
            list_y += 70

        # RESTORE THE SCREEN: Remove the clip so the rest of the game can draw normally!
        screen.set_clip(None)

        # ==========================================
        # RIGHT PANEL: CARD PREVIEW & ACTIONS
        # ==========================================
        sidebar = pygame.Surface((480, 560), pygame.SRCALPHA)
        sidebar.fill((20, 20, 20, 220)) 
        screen.blit(sidebar, (700, 120))

        if market_selected and market_loaded_img:
            card_x, card_y = 826, 130 
            screen.blit(market_loaded_img, (card_x, card_y))
            draw_card_stats(screen, market_selected["name"], card_x, card_y)
            
            btn_rect = pygame.Rect(800, 490, 280, 60)
            btn_hover = btn_rect.collidepoint(mouseX, mouseY)
            
            # Action Contexts
            if market_tab == "BUY":
                # Seller Info
                seller_txt = f1font2.render(f"Seller: {market_selected['seller']}", True, (150, 150, 150))
                screen.blit(seller_txt, seller_txt.get_rect(center=(940, 460)))
                
                if btn_hover:
                    pygame.draw.rect(screen, (30, 80, 30), btn_rect, 0, 25) 
                    pygame.draw.rect(screen, (100, 255, 100), btn_rect, 2, 25) 
                    btn_txt = f1font2.render(f"BUY ({market_selected['price']})", True, "white")
                else:
                    pygame.draw.rect(screen, (20, 50, 20), btn_rect, 0, 25)
                    pygame.draw.rect(screen, (50, 150, 50), btn_rect, 2, 25)
                    btn_txt = f1font2.render(f"BUY ({market_selected['price']})", True, (200, 200, 200))
                    
            elif market_tab == "SELL":
                # Price Input Box
                input_rect = pygame.Rect(800, 440, 280, 40)
                pygame.draw.rect(screen, (30, 30, 40), input_rect, 0, 10)
                if sell_price_typing: pygame.draw.rect(screen, (100, 200, 255), input_rect, 2, 10)
                else: pygame.draw.rect(screen, (100, 100, 100), input_rect, 2, 10)
                
                disp_price = sell_price_input if sell_price_input else "Enter Price..."
                p_color = "white" if sell_price_input else (150, 150, 150)
                p_surf = f1font2.render(disp_price, True, p_color)
                screen.blit(p_surf, p_surf.get_rect(center=input_rect.center))
                
                if btn_hover:
                    pygame.draw.rect(screen, (80, 80, 30), btn_rect, 0, 25) 
                    pygame.draw.rect(screen, (255, 215, 0), btn_rect, 2, 25) 
                    btn_txt = f1font2.render("LIST CARD", True, "white")
                else:
                    pygame.draw.rect(screen, (50, 50, 20), btn_rect, 0, 25)
                    pygame.draw.rect(screen, (150, 150, 50), btn_rect, 2, 25)
                    btn_txt = f1font2.render("LIST CARD", True, (200, 200, 200))

            elif market_tab == "ACTIVE":
                if btn_hover:
                    pygame.draw.rect(screen, (80, 30, 30), btn_rect, 0, 25) 
                    pygame.draw.rect(screen, (255, 100, 100), btn_rect, 2, 25) 
                    btn_txt = f1font2.render("CANCEL LISTING", True, "white")
                else:
                    pygame.draw.rect(screen, (50, 20, 20), btn_rect, 0, 25)
                    pygame.draw.rect(screen, (150, 50, 50), btn_rect, 2, 25)
                    btn_txt = f1font2.render("CANCEL LISTING", True, (200, 200, 200))
            
            screen.blit(btn_txt, btn_txt.get_rect(center=btn_rect.center))
            
            if market_msg:
                msg_color = (255, 100, 100) if "Need" in market_msg or "valid" in market_msg else (100, 255, 100)
                msg_surf = f1font2.render(market_msg, True, msg_color)
                screen.blit(msg_surf, msg_surf.get_rect(center=(940, 575)))
        else:
            screen.blit(f1font2.render("SELECT A CARD", True, (100, 100, 100)), (830, 380))
            if market_msg:
                msg_color = (100, 255, 100)
                msg_surf = f1font2.render(market_msg, True, msg_color)
                screen.blit(msg_surf, msg_surf.get_rect(center=(940, 420)))

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
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))
        screen.blit(f1logo, (100, 80)) 
        
        btn_label = 'RACING LINE'
        text_width = f1font.size(btn_label)[0]
        btn_rect = pygame.Rect(100, 250, text_width + 40, 70)
        
        if btn_rect.collidepoint(mouseX, mouseY):
            pygame.draw.rect(screen, (30, 30, 40), btn_rect, 0, 25)
            pygame.draw.rect(screen, (220, 220, 220), btn_rect, 2, 25)
            t_surf = f1font.render(btn_label, True, "white")
        else:
            t_surf = f1font.render(btn_label, True, (180, 180, 180))
            
        screen.blit(t_surf, (120, 255))
        
        status = "ON" if racingLine else "OFF"
        color = (100, 255, 100) if racingLine else (255, 100, 100)
        screen.blit(f1font.render(status, True, color), (160 + text_width, 255))

    # online selection menu
    elif gamestate == "onlineMenu":
        screen.blit(menu, (0,0))
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))
        screen.blit(f1logo, (100, 80)) 

        for y_pos, label in [(250, 'HOST'), (330, 'JOIN')]:
            text_width = f1font.size(label)[0]
            btn_rect = pygame.Rect(100, y_pos, text_width + 40, 70)
            if btn_rect.collidepoint(mouseX, mouseY):
                pygame.draw.rect(screen, (30, 30, 40), btn_rect, 0, 25)
                pygame.draw.rect(screen, (220, 220, 220), btn_rect, 2, 25)
                t_surf = f1font.render(label, True, "white")
            else:
                t_surf = f1font.render(label, True, (180, 180, 180))
            screen.blit(t_surf, (120, y_pos + 5))

        if n is None or n.p is None: screen.blit(f1font2.render("ERROR: Cannot reach server. Playing Offline.", True, (255, 50, 50)), (100, 600))
        else: screen.blit(f1font2.render("Connected to Official F1 Server", True, (50, 255, 50)), (100, 600))

    elif gamestate == "hostLobby":
        screen.blit(menu, (0,0))
        
        # ==========================================
        # --- THE GLASS SIDEBAR (Right Side) ---
        sidebar = pygame.Surface((380, 720), pygame.SRCALPHA)
        sidebar.fill((20, 20, 20, 220)) 
        screen.blit(sidebar, (900, 0))

        # --- DRAW LEAVE LOBBY BUTTON (Top of Sidebar) ---
        if 950 < mouseX < 1230 and 30 < mouseY < 90:
            pygame.draw.rect(screen, (255, 100, 100), (950, 30, 280, 60), 0, 15) 
        else:
            pygame.draw.rect(screen, (200, 50, 50), (950, 30, 280, 60), 0, 15)   
        leave_text = f1font2.render("LEAVE LOBBY", True, "white")
        screen.blit(leave_text, leave_text.get_rect(center=(1090, 60)))

        # Fetch driver specific to the active car
        user_squads = active_driver.get(loggedInUser, {}) if 'active_driver' in globals() else {}
        if not isinstance(user_squads, dict): user_squads = {}
        my_drv = user_squads.get(car_name, "None")

        if my_drv != "None" and my_drv not in inventory_loaded_imgs:
            path = find_driver_card(my_drv)
            if path:
                try:
                    img = pygame.image.load(path).convert_alpha()
                    inventory_loaded_imgs[my_drv] = pygame.transform.scale(img, (228, 300)) 
                except: pass

        # Draw Active Driver Card (Middle of Sidebar)
        if my_drv in inventory_loaded_imgs:
            card_x, card_y = 976, 110 
            screen.blit(inventory_loaded_imgs[my_drv], (card_x, card_y))
            draw_card_stats(screen, my_drv, card_x, card_y)
        else:
            pygame.draw.rect(screen, (50, 50, 50), (976, 110, 228, 300), 0, 10)
            screen.blit(f1font2.render("NO DRIVER", True, (150, 150, 150)), (1000, 240))

        # Active Car Stats
        screen.blit(f1font2.render(f"Car: {car_name.upper()}", True, "white"), (950, 440))
        screen.blit(f1font2.render(f"TOP SPD: {round(carMaxSpeed, 1)}", True, (255, 215, 0)), (950, 480))

        # --- DRAW START BUTTON (Bottom of Sidebar, HOST ONLY) ---
        if my_player_index == 0:
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
            
            if can_start:
                if 950 < mouseX < 1230 and 600 < mouseY < 680:
                    pygame.draw.rect(screen, (100, 255, 100), (950, 600, 280, 80), 0, 15) 
                else:
                    pygame.draw.rect(screen, (50, 200, 50), (950, 600, 280, 80), 0, 15) 
                start_txt = f1font2.render("START RACE", True, "black")
                screen.blit(start_txt, start_txt.get_rect(center=(1090, 640)))
            else:
                pygame.draw.rect(screen, (150, 150, 150), (950, 600, 280, 80), 0, 15)
                btn_text = "NEED PLAYERS" if active_count < 2 else "WAITING..."
                wait_txt = f1font2.render(btn_text, True, "black")
                screen.blit(wait_txt, wait_txt.get_rect(center=(1090, 640)))
        else:
            screen.blit(f1font2.render("Waiting for Host...", True, "white"), (970, 630))
        # ==========================================

        # Dynamic Capacity Display (Shifted Left)
        pygame.draw.rect(screen, (40, 40, 40), (50, 20, 600, 80), 0, 20)
        cap_text = f"LOBBY #{my_lobby_id}  |  CAPACITY: {players_connected}/10"
        screen.blit(f1font2.render(cap_text, True, "white"), (120, 45))

        # Compact Car Grid with Sleek Badges
        all_teams = [
            (Mclaren, 50, 130, 'Mclaren'), (Mercedes, 190, 130, 'Mercedes'),
            (Redbull, 330, 130, 'Redbull'), (VCARB, 470, 130, 'VCARB'),
            (ferrari, 610, 130, 'ferrari'), (Williams, 750, 130, 'Williams'),
            (AstonMartin, 120, 360, 'AstonMartin'), (Haas, 260, 360, 'Haas'),
            (Audi, 400, 360, 'Audi'), (Alpine, 540, 360, 'Alpine'), 
            (Cadillac, 680, 360, 'Cadillac')
        ]

        my_unlocked = unlocked_cars.get(loggedInUser, ["Alpine"]) if loggedInUser else ["Alpine"]

        for img, x, y, name in all_teams:
            is_taken = name in taken_cars and name != "Alpine"
            is_locked = name not in my_unlocked
            is_hovered = x < mouseX < x + 130 and y < mouseY < y + 195
            
            normal_size = (110, 165)
            hover_size = (130, 195)
            
            if is_taken or is_locked:
                # Gray silhouette
                gray_car = pygame.transform.smoothscale(pygame.transform.rotate(img, -90), normal_size)
                gray_car.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(gray_car, (x + 10, y + 15))
                
                if is_locked:
                    # Use icon for locked cars
                    screen.blit(lock_icon, (x + 48, y + 145))
                elif is_taken:
                    # Keep the "TAKEN" badge for clarity in multiplayer
                    pygame.draw.rect(screen, (200, 50, 50), (x + 20, y + 150, 90, 30), 0, 5)
                    screen.blit(pygame.font.SysFont("Arial", 16, bold=True).render("TAKEN", True, "white"), (x + 35, y + 156))
            else:
                if is_hovered or car == img:
                    screen.blit(pygame.transform.smoothscale(pygame.transform.rotate(img, -90), hover_size), (x, y))
                    if car == img:
                        pygame.draw.rect(screen, (100, 255, 100), (x-5, y-5, 140, 205), 3, 15)
                else:
                    screen.blit(pygame.transform.smoothscale(pygame.transform.rotate(img, -90), normal_size), (x + 10, y + 15))
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
    # --- UPDATED: Auth Selection Screen (F1 Style) ---
    elif gamestate == "authMenu":
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        
        # Back button (Standard Circle)
        if 30 < mouseX < 90 and 30 < mouseY < 90: 
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: 
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Logo and Alignment
        screen.blit(f1logo, (100, 80)) 
        
        # Button Configuration
        auth_buttons = [
            (270, 'SIGN UP', "signUp"), 
            (350, 'SIGN IN', "signIn")
        ]

        for y_pos, label, target_state in auth_buttons:
            # 1. Measure text width for a tight "Pill" fit
            text_width = f1font.size(label)[0]
            button_rect = pygame.Rect(100, y_pos, text_width + 40, 70)
            is_hovered = button_rect.collidepoint(mouseX, mouseY)
            
            if is_hovered:
                # Sleek F1-style pill: Translucent dark fill with white glow border
                pygame.draw.rect(screen, (30, 30, 40, 200), button_rect, 0, 25) 
                pygame.draw.rect(screen, (255, 255, 255), button_rect, 2, 25) 
                text_surf = f1font.render(label, True, (255, 255, 255)) 
            else:
                # Idle state: Subtle grey text and dark pill
                pygame.draw.rect(screen, (20, 20, 25, 180), button_rect, 0, 25)
                text_surf = f1font.render(label, True, (180, 180, 180)) 
            
            screen.blit(text_surf, (120, y_pos + 5))
    # --- UPDATED: Sign Up and Sign In Screens (F1 Style) ---
    elif gamestate in ["signUp", "signIn"]:
        screen.blit(menu, (0,0))
        fireworks.render(screen,(0,0))
        
        # Back button (Standard Circle)
        if 30 < mouseX < 90 and 30 < mouseY < 90: 
            pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: 
            pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        # Logo and Title Alignment
        screen.blit(f1logo, (100, 80)) 
        title_text = "SIGN UP" if gamestate == "signUp" else "SIGN IN"
        screen.blit(f1font.render(title_text, True, ("white")), (120, 190))

        # --- INPUT FIELD CONFIGURATION ---
        # We use the same 'Pill' logic as the main menu buttons
        input_fields = [
            ("Username", UsernameInputed, UsernameTyping, 280),
            ("Password", passwordInputed, passwordTyping, 370)
        ]
        if gamestate == "signUp":
            input_fields.append(("3-Letter Tag", abbrInputed, abbrTyping, 460))

        for label, value, is_typing, y_pos in input_fields:
            # Draw the Input Pill
            field_rect = pygame.Rect(100, y_pos, 600, 70)
            
            # Background: Dark translucent like the sidebar
            pygame.draw.rect(screen, (20, 20, 20, 200), field_rect, 0, 25)
            
            # Border: Glows blue if typing, red if error, grey if idle
            border_color = (100, 200, 255) if is_typing else (100, 100, 100)
            
            # Error checking for username
            if label == "Username" and UsernameInputed != "":
                if (gamestate == "signUp" and UsernameExist) or (gamestate == "signIn" and not UsernameExist):
                    border_color = (255, 50, 50)
            
            pygame.draw.rect(screen, border_color, field_rect, 2, 25)

            # Render Text (Password masking)
            display_val = value
            if label == "Password" and value != "":
                if show_last_char and (pygame.time.get_ticks() - last_key_time) < 1000:
                    display_val = "●"*(len(value)-1) + value[-1:]
                else:
                    display_val = "●" * len(value)
            
            # If empty, show placeholder in grey
            final_text = display_val if value != "" else label
            text_color = (255, 255, 255) if value != "" else (120, 120, 120)
            
            screen.blit(f1font.render(final_text, True, text_color), (130, y_pos + 5))

        # --- SUBMIT BUTTON (Matches Main Menu 'RACE' Button) ---
        submit_label = "CREATE" if gamestate == "signUp" else "LOGIN"
        submit_width = f1font.size(submit_label)[0] + 60
        submit_y = 570 if gamestate == "signUp" else 480
        submit_rect = pygame.Rect(100, submit_y, submit_width, 75)
        
        is_hovered = submit_rect.collidepoint(mouseX, mouseY)
        
        if is_hovered:
            pygame.draw.rect(screen, (255, 255, 255), submit_rect, 0, 25) # White fill on hover
            btn_text_color = (0, 0, 0)
        else:
            pygame.draw.rect(screen, (220, 0, 0), submit_rect, 2, 25) # Red outline idle
            btn_text_color = (220, 0, 0)
            
        screen.blit(f1font.render(submit_label, True, btn_text_color), (submit_rect.x + 30, submit_rect.y + 7))

        # Helper Error Messages
        if gamestate == "signUp" and UsernameExist and UsernameInputed != "":
            screen.blit(f1font2.render("USER ALREADY ON GRID", True, (255, 50, 50)), (110, 255))
        elif gamestate == "signUp" and len(abbrInputed) > 0 and len(abbrInputed) < 3:
             screen.blit(f1font2.render("TAG MUST BE 3 LETTERS", True, (255, 50, 50)), (110, 535))

    # Account Menu
    elif gamestate == "accountMenu":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))
        
        # Left Side: Logo and F1-Style Buttons
        screen.blit(f1logo, (100, 80)) 
        
        for y_pos, label in [(250, 'VIEW MY CARDS'), (330, 'SIGN OUT')]:
            text_width = f1font.size(label)[0]
            btn_rect = pygame.Rect(100, y_pos, text_width + 40, 70)
            
            if btn_rect.collidepoint(mouseX, mouseY):
                pygame.draw.rect(screen, (30, 30, 40), btn_rect, 0, 25)
                pygame.draw.rect(screen, (220, 220, 220), btn_rect, 2, 25)
                t_surf = f1font.render(label, True, "white" if label == "VIEW MY CARDS" else (255, 100, 100))
            else:
                t_surf = f1font.render(label, True, (180, 180, 180))
            screen.blit(t_surf, (120, y_pos + 5))

        # ==========================================
        # --- THE GLASS PROFILE SIDEBAR ---
        sidebar = pygame.Surface((580, 720), pygame.SRCALPHA)
        sidebar.fill((20, 20, 20, 220)) 
        screen.blit(sidebar, (700, 0))

        screen.blit(f1font.render("ACCOUNT", True, "white"), (750, 50))
        pygame.draw.line(screen, (100, 100, 100), (750, 110), (1230, 110), 2)
        
        screen.blit(f1font2.render("USER PROFILE", True, (150, 150, 150)), (750, 140))
        screen.blit(f1font2.render(str(loggedInUser), True, (100, 200, 255)), (750, 175))
        
        screen.blit(f1font2.render("CAREER BALANCE", True, (150, 150, 150)), (750, 230))
        screen.blit(f1font2.render(f"{user_points.get(loggedInUser, 0)} PTS", True, (255, 215, 0)), (750, 265))
        
        screen.blit(f1font2.render("YOUR GARAGE", True, (150, 150, 150)), (750, 330))
        
        # Draw the Unlocked Cars in a clean 2-column grid
        my_cars = unlocked_cars.get(loggedInUser, ["Alpine"])
        x_offset = 750
        y_offset = 370
        
        for i, car_name in enumerate(my_cars):
            col = i % 2
            row = i // 2
            draw_x = x_offset + (col * 240) 
            draw_y = y_offset + (row * 45)
            
            # Subtle dark pill background for each car name
            pygame.draw.rect(screen, (40, 40, 40), (draw_x, draw_y, 220, 35), 0, 10)
            screen.blit(f1font2.render(car_name, True, (100, 255, 100)), (draw_x + 15, draw_y + 5))
        # ==========================================
    
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
                
            # 3. Draw Search Box (Sleek Glass Style)
            search_rect = pygame.Rect(400, 25, 460, 50)
            pygame.draw.rect(screen, (30, 30, 40), search_rect, 0, 15) 
            if squad_typing: pygame.draw.rect(screen, (100, 200, 255), search_rect, 2, 15) 
            else: pygame.draw.rect(screen, (100, 100, 100), search_rect, 2, 15) 
            
            s_text = f1font2.render(squad_search_input if squad_search_input else "Search Drivers...", True, "white" if squad_search_input else (150,150,150))
            screen.blit(s_text, (420, 35))
        else:
            screen.blit(f1font.render("My Card Collection", True, ("white")), (400, 30))

        if len(raw_drivers) == 0:
            screen.blit(f1font2.render("You don't own any cards yet! Go to the Market.", True, "red"), (350, 300))
        elif len(filtered_drivers) == 0:
            screen.blit(f1font2.render("No drivers found matching that search.", True, "white"), (450, 300))
        else:
            # --- SCROLLING LOGIC ---
            start_x, start_y, x_spacing, y_spacing = 70, 110, 290, 320 
            clip_y_start = 90
            
            import math
            # Calculate max scroll to prevent infinite scrolling
            total_rows = math.ceil(len(filtered_drivers) / 4)
            total_height = total_rows * y_spacing
            visible_height = 720 - start_y
            max_scroll = max(0, total_height - visible_height + 50) # Added 50px buffer at bottom
            
            inventory_scroll = max(0, min(inventory_scroll, max_scroll))

            # Apply Screen Clipping (Cards scroll under the header elements)
            clip_rect = pygame.Rect(0, clip_y_start, 1280, 720 - clip_y_start)
            screen.set_clip(clip_rect)

            for i in range(len(filtered_drivers)):
                drv = filtered_drivers[i]
                row, col = i // 4, i % 4
                draw_x = start_x + (col * x_spacing)
                draw_y = start_y + (row * y_spacing) - inventory_scroll
                
                # Performance bump: Only draw cards if they are currently inside the screen view!
                if draw_y + 300 > clip_y_start and draw_y < 720:
                    if gamestate == "driverSelect" and draw_x < mouseX < draw_x + 228 and draw_y < mouseY < draw_y + 300:
                        pygame.draw.rect(screen, (100, 255, 100), (draw_x-6, draw_y-6, 240, 312), 0, 12)
                        screen.blit(f1font.render("EQUIP", True, (100, 255, 100)), (draw_x + 40, draw_y + 120))
                    
                    if drv in inventory_loaded_imgs:
                        screen.blit(inventory_loaded_imgs[drv], (draw_x, draw_y))
                        draw_card_stats(screen, drv, draw_x, draw_y)
                    else:
                        pygame.draw.rect(screen, (50,50,50), (draw_x, draw_y, 228, 300), 0, 10)
                        screen.blit(f1font2.render("Loading...", True, "white"), (draw_x + 40, draw_y + 130))

            # Lift the screen clip boundary so the rest of your UI displays correctly
            screen.set_clip(None)
    # --- NEW: STORE & PACK OPENING RENDERER ---
    elif gamestate == "store":
        screen.blit(menu, (0,0))
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        screen.blit(f1font.render("PACK STORE", True, "white"), (120, 30))
        balance_txt = f1font2.render(f"BALANCE: {user_points.get(loggedInUser, 0)} PTS", True, (255, 215, 0))
        screen.blit(balance_txt, (1230 - balance_txt.get_width(), 40))

        x_pos = 150
        for name, data in PACK_TYPES.items():
            is_hovered = x_pos < mouseX < x_pos + 200 and 200 < mouseY < 490
            
            draw_y = 190 if is_hovered else 200
            screen.blit(pack_store_img, (x_pos, draw_y))
            
            name_surf = f1font2.render(name, True, "white")
            screen.blit(name_surf, name_surf.get_rect(center=(x_pos + 100, 520)))
            
            cost_surf = f1font2.render(f"{data['cost']} PTS", True, (255, 215, 0))
            screen.blit(cost_surf, cost_surf.get_rect(center=(x_pos + 100, 550)))
            
            desc_surf = pygame.font.SysFont("Arial", 18).render(data["desc"], True, (200, 200, 200))
            screen.blit(desc_surf, desc_surf.get_rect(center=(x_pos + 100, 580)))
            x_pos += 350

    elif gamestate == "packOpening":
        screen.blit(menu, (0, 0))
        # Darken background to make the pack pop
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) 
        screen.blit(overlay, (0, 0))

        current_card = pack_opening_results[pack_reveal_idx]
        card_path = find_driver_card(current_card)

        # --- THE ANIMATION ENGINE ---
        pack_anim_timer += 1

        # PHASE 0: Shaking and Pulsing Pack
        if pack_anim_state == 0:
            # 1. Intensity increases over time
            intensity = pack_anim_timer / 10 
            shake_x = random.randint(int(-intensity), int(intensity))
            shake_y = random.randint(int(-intensity), int(intensity))

            # 2. Breathing/Pulsing effect using Sine waves
            scale = 1.0 + math.sin(pack_anim_timer * 0.2) * 0.05
            w, h = int(300 * scale), int(435 * scale)

            # Draw the pack perfectly centered, applying the shake offsets
            scaled_pack = pygame.transform.smoothscale(pack_img, (w, h))
            rect = scaled_pack.get_rect(center=(640 + shake_x, 360 + shake_y))
            screen.blit(scaled_pack, rect)

            # Move to the flash phase after ~75 frames (a little over 1 second)
            if pack_anim_timer > 75:
                pack_anim_state = 1
                pack_anim_timer = 0

        # PHASE 1: The Burst (White Flash)
        elif pack_anim_state == 1:
            if card_path:
                # 1. The Baking Method: Create the large card safely
                # --- NO MORE PIXEL CRUSHING ---
                if current_card not in pack_large_cache:
                    raw = pygame.image.load(card_path).convert_alpha()
                    
                    # 1. Scale the raw image DIRECTLY to the massive reveal size
                    base = pygame.transform.smoothscale(raw, (380, 500))
                    
                    # 2. Tell our new function that the card is 380px wide so it scales the HD numbers!
                    draw_card_stats(base, current_card, 0, 0, card_w=380) 
                    
                    # 3. Save to cache
                    pack_large_cache[current_card] = base
                # 2. Draw from the safe cache
                card_img = pack_large_cache[current_card]
                card_rect = card_img.get_rect(center=(640, 360))
                screen.blit(card_img, card_rect)

            # Calculate flash transparency (fades out fast)
            alpha = max(0, 255 - (pack_anim_timer * 12))
            
            if alpha > 0:
                flash = pygame.Surface((1280, 720), pygame.SRCALPHA)
                flash.fill((255, 255, 255, alpha))
                screen.blit(flash, (0, 0))
            else:
                pack_anim_state = 2 # Flash is done, move to idle

        # PHASE 2: The Idle Reveal
        elif pack_anim_state == 2:
            if card_path:
                # Same fast-loading logic as Phase 1!
                # --- NO MORE PIXEL CRUSHING ---
                if current_card not in pack_large_cache:
                    raw = pygame.image.load(card_path).convert_alpha()
                    
                    # 1. Scale the raw image DIRECTLY to the massive reveal size
                    base = pygame.transform.smoothscale(raw, (380, 500))
                    
                    # 2. Tell our new function that the card is 380px wide so it scales the HD numbers!
                    draw_card_stats(base, current_card, 0, 0, card_w=380) 
                    
                    # 3. Save to cache
                    pack_large_cache[current_card] = base
                card_img = pack_large_cache[current_card]
                card_rect = card_img.get_rect(center=(640, 360))
                screen.blit(card_img, card_rect)

            # Show the prompt so the user knows they can click now
            prompt = "CLICK TO REVEAL NEXT" if pack_reveal_idx < len(pack_opening_results)-1 else "CLICK TO FINISH"
            prompt_surf = f1font2.render(prompt, True, "white")
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(640, 680)))
    # ------------------------------------------
    elif gamestate == "tyreSelect":
        screen.blit(menu, (0,0))
        
        # Back button
        if 30 < mouseX < 90 and 30 < mouseY < 90: pygame.draw.circle(screen, ("white"), (60, 60), 33)
        else: pygame.draw.circle(screen, ("light grey"), (60, 60), 30)
        screen.blit(f1font2.render("←", True, ("black")) , (47, 47))

        title = f1font.render("SELECT TYRE COMPOUND", True, "white")
        screen.blit(title, title.get_rect(center=(640, 80)))

        # 1. Soft Compound Block
        s_rect = pygame.Rect(240, 200, 220, 300)
        pygame.draw.rect(screen, (40, 20, 20) if s_rect.collidepoint(mouseX, mouseY) else (30, 30, 35), s_rect, 0, 20)
        pygame.draw.rect(screen, (255, 100, 100), s_rect, 2, 20)
        if 'soft_wheel' in globals(): screen.blit(pygame.transform.smoothscale(soft_wheel, (180, 180)), (260, 220))
        screen.blit(f1font2.render("SOFT", True, (255, 100, 100)), (310, 420))
        screen.blit(f1font2.render("+1.0 SPD", True, "white"), (285, 460))

        # 2. Medium Compound Block
        m_rect = pygame.Rect(530, 200, 220, 300)
        pygame.draw.rect(screen, (40, 40, 20) if m_rect.collidepoint(mouseX, mouseY) else (30, 30, 35), m_rect, 0, 20)
        pygame.draw.rect(screen, (255, 215, 0), m_rect, 2, 20)
        if 'medium_wheel' in globals(): screen.blit(pygame.transform.smoothscale(medium_wheel, (180, 180)), (550, 220))
        screen.blit(f1font2.render("MEDIUM", True, (255, 215, 0)), (580, 420))
        screen.blit(f1font2.render("BALANCED", True, "white"), (565, 460))

        # 3. Hard Compound Block
        h_rect = pygame.Rect(820, 200, 220, 300)
        pygame.draw.rect(screen, (40, 40, 40) if h_rect.collidepoint(mouseX, mouseY) else (30, 30, 35), h_rect, 0, 20)
        pygame.draw.rect(screen, (200, 200, 200), h_rect, 2, 20)
        if 'hard_wheel' in globals(): screen.blit(pygame.transform.smoothscale(hard_wheel, (180, 180)), (840, 220))
        screen.blit(f1font2.render("HARD", True, (200, 200, 200)), (890, 420))
        screen.blit(f1font2.render("-0.5 SPD", True, "white"), (870, 460))

    elif gamestate == "paused":
        # Keep engine sound quiet while paused
        carSound.set_volume(0)
                # Stop all opponent audio channels
        for channel in opponent_audio_channels.values():
            channel.stop()
        opponent_audio_channels.clear()

        # Draw a dark translucent overlay over the last frame of the race
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        pause_title = f1font.render("GAME PAUSED", True, "white")
        screen.blit(pause_title, pause_title.get_rect(center=(640, 150)))
        
        # RESUME BUTTON
        res_rect = pygame.Rect(490, 250, 300, 80)
        res_hov = res_rect.collidepoint(mouseX, mouseY)
        pygame.draw.rect(screen, (100, 255, 100) if res_hov else (50, 200, 50), res_rect, 0, 15)
        res_txt = f1font2.render("RESUME", True, "black")
        screen.blit(res_txt, res_txt.get_rect(center=res_rect.center))
        
        # MAIN MENU BUTTON
        men_rect = pygame.Rect(490, 360, 300, 80)
        men_hov = men_rect.collidepoint(mouseX, mouseY)
        pygame.draw.rect(screen, (255, 100, 100) if men_hov else (200, 50, 50), men_rect, 0, 15)
        men_txt = f1font2.render("MAIN MENU", True, "white")
        screen.blit(men_txt, men_txt.get_rect(center=men_rect.center))
    # ==========================================
    # --- DYNAMIC RESOLUTION RENDERER ---
    # 1. Figure out how much to scale the canvas
    target_ratio = windowWidth / windowHeight
    window_ratio = current_w / current_h

    if window_ratio > target_ratio:
        scale = current_h / windowHeight
    else:
        scale = current_w / windowWidth

    # 2. Scale the canvas SMOOTHLY!
    scaled_width = int(windowWidth * scale)
    scaled_height = int(windowHeight * scale)
    
    # --- CRITICAL: THIS MUST BE SMOOTHSCALE, NOT SCALE ---
    scaled_screen = pygame.transform.smoothscale(screen, (scaled_width, scaled_height))
    # -----------------------------------------------------

    # 3. Calculate where to center it
    x_offset = (current_w - scaled_width) // 2
    y_offset = (current_h - scaled_height) // 2

    # 4. Wipe the real window black (for letterbox bars), then blit the game
    real_screen.fill((0, 0, 0))
    real_screen.blit(scaled_screen, (x_offset, y_offset))
    # ==========================================

    pygame.display.flip()
    clock.tick(60)

pygame.quit()