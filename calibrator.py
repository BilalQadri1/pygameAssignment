import pygame
import os

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("F1 Card Stat Calibrator")
font = pygame.font.SysFont("Arial", 20)

CARD_W, CARD_H = 228, 300
card_x, card_y = 286, 150 

# ==========================================
# --- SIZING CONTROLS ---
# Change these to adjust the size of the numbers!
OVR_W, OVR_H = 30, 30    # Bigger size for Overall
STAT_W, STAT_H = 18, 18  # Smaller size for EXP, RAC, AWA, PAC
# ==========================================

card_img = None
image_path = "F1Cards\Bearman.png" 
if os.path.exists(image_path):
    card_img = pygame.image.load(image_path).convert_alpha()
    card_img = pygame.transform.scale(card_img, (CARD_W, CARD_H))

# Load Two Sets of Number Photos
ovr_images = {}
stat_images = {}

for i in range(10):
    num_path = os.path.join("F1Cards", "RatingNumbers", f"{i}.png")
    if os.path.exists(num_path):
        img = pygame.image.load(num_path).convert_alpha()
        ovr_images[str(i)] = pygame.transform.scale(img, (OVR_W, OVR_H))
        stat_images[str(i)] = pygame.transform.scale(img, (STAT_W, STAT_H))
    else:
        dummy = pygame.Surface((30, 30), pygame.SRCALPHA)
        dummy.fill((200, 0, 0, 150))
        ovr_images[str(i)] = dummy
        stat_images[str(i)] = dummy

# Update the bounding boxes to match the new widths
stats = [
    {"name": "OVR", "rect": pygame.Rect(50, 100, OVR_W * 2, OVR_H), "is_ovr": True},
    {"name": "EXP", "rect": pygame.Rect(50, 160, STAT_W * 2, STAT_H), "is_ovr": False},
    {"name": "RAC", "rect": pygame.Rect(50, 210, STAT_W * 2, STAT_H), "is_ovr": False},
    {"name": "AWA", "rect": pygame.Rect(50, 260, STAT_W * 2, STAT_H), "is_ovr": False},
    {"name": "PAC", "rect": pygame.Rect(50, 310, STAT_W * 2, STAT_H), "is_ovr": False}
]

dragging = None
offset_x, offset_y = 0, 0

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i in range(len(stats)-1, -1, -1):
                if stats[i]["rect"].collidepoint(mx, my):
                    dragging = i
                    offset_x = stats[i]["rect"].x - mx
                    offset_y = stats[i]["rect"].y - my
                    break
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = None
        elif event.type == pygame.MOUSEMOTION and dragging is not None:
            mx, my = event.pos
            stats[dragging]["rect"].x = mx + offset_x
            stats[dragging]["rect"].y = my + offset_y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                print("\n--- COPY AND PASTE THIS TO AI ---")
                print("    positions = {")
                for s in stats:
                    rel_x = s["rect"].x - card_x
                    rel_y = s["rect"].y - card_y
                    print(f'        "{s["name"]}": (card_x + {rel_x}, card_y + {rel_y}),')
                print("    }")
                print("---------------------------------\n")

    # Draw Card
    if card_img: screen.blit(card_img, (card_x, card_y))
    else: pygame.draw.rect(screen, (100, 100, 100), (card_x, card_y, CARD_W, CARD_H))

    # Draw Stats
    for s in stats:
        w = OVR_W if s["is_ovr"] else STAT_W
        img_dict = ovr_images if s["is_ovr"] else stat_images
        
        screen.blit(img_dict["9"], (s["rect"].x, s["rect"].y))
        screen.blit(img_dict["9"], (s["rect"].x + w, s["rect"].y)) # Draw second digit shifted over
        
        if dragging == stats.index(s):
            pygame.draw.rect(screen, (255, 255, 255), s["rect"], 1)
        
        label = font.render(s["name"], True, (255, 255, 255))
        screen.blit(label, (s["rect"].x, s["rect"].y - 20))

    pygame.display.flip()
pygame.quit()