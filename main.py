import pygame
import sys
import math

pygame.init()

# ------------------ SCREEN SETUP ------------------
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1D Collision Simulator")

FONT = pygame.font.SysFont(None, 32)
BIGFONT = pygame.font.SysFont(None, 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (0, 150, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 120)

# INPUT BOX CLASS
class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

            self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 8, self.rect.y + 8))

    def get_value(self):
        return self.text.strip()


# ------------------ UI ELEMENTS ------------------
input_boxes = [
    InputBox(180, 50, 150, 40),     # mass1
    InputBox(180, 110, 150, 40),    # mass2
    InputBox(180, 170, 150, 40),    # vel1
    InputBox(180, 230, 150, 40),    # vel2
]

shape_options = ["Circle", "Square", "Triangle"]
shape_index = 0

start_button = pygame.Rect(150, 320, 200, 60)


# --------------------------------------------------
# DRAW SELECTABLE SHAPE BOX
# --------------------------------------------------
def draw_shape_selector():
    global shape_index
    label = FONT.render("Object Shape:", True, BLACK)
    screen.blit(label, (50, 290))

    pygame.draw.rect(screen, WHITE, (180, 280, 150, 40))
    pygame.draw.rect(screen, BLACK, (180, 280, 150, 40), 2)

    shape_text = FONT.render(shape_options[shape_index], True, BLACK)
    screen.blit(shape_text, (190, 290))


# --------------------------------------------------
# DRAW START BUTTON
# --------------------------------------------------
def draw_start_button():
    pygame.draw.rect(screen, GREEN, start_button)
    text = BIGFONT.render("START", True, BLACK)
    screen.blit(text, (start_button.x + 45, start_button.y + 12))


# --------------------------------------------------
# OBJECT DRAW
# --------------------------------------------------
def draw_object(x, y, shape, color, label):
    text = FONT.render(label, True, BLACK)
    screen.blit(text, (x, y - 30))

    if shape == "Circle":
        pygame.draw.circle(screen, color, (x, y), 25)
    elif shape == "Square":
        pygame.draw.rect(screen, color, (x - 25, y - 25, 50, 50))
    elif shape == "Triangle":
        pygame.draw.polygon(screen, color, [(x, y - 30), (x - 30, y + 25), (x + 30, y + 25)])


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------
clock = pygame.time.Clock()
running = True
simulation_started = False

# physics variables
x1, x2 = 200, 800
v1 = v2 = 0
m1 = m2 = 1
shape = "Circle"

while running:
    screen.fill((230, 230, 230))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not simulation_started:
            for box in input_boxes:
                box.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    # Validate inputs
                    values = [box.get_value() for box in input_boxes]
                    if all(values):  # no empty values
                        try:
                            m1 = float(values[0])
                            m2 = float(values[1])
                            v1 = float(values[2])
                            v2 = float(values[3])
                            shape = shape_options[shape_index]
                            simulation_started = True
                        except:
                            pass

                # Change shape on click
                if 180 <= event.pos[0] <= 330 and 280 <= event.pos[1] <= 320:
                    shape_index = (shape_index + 1) % len(shape_options)

    # -------------------- UI or Simulation ---------------------
    if not simulation_started:
        # LEFT INPUT PANEL
        labels = ["Mass of Object 1", "Mass of Object 2", "Velocity of O1", "Velocity of O2"]
        for i, text in enumerate(labels):
            label = FONT.render(text, True, BLACK)
            screen.blit(label, (20, 60 + (i * 60)))

        for box in input_boxes:
            box.draw(screen)

        draw_shape_selector()
        draw_start_button()

    else:
        # Draw moving objects
        draw_object(int(x1), HEIGHT // 2, shape, BLUE, "Object1")
        draw_object(int(x2), HEIGHT // 2, shape, RED, "Object2")

        # Update positions
        x1 += v1
        x2 += v2

        # Wall collisions
        if x1 <= 50 or x1 >= WIDTH - 50:
            v1 = -v1
        if x2 <= 50 or x2 >= WIDTH - 50:
            v2 = -v2

        # Object collision
        if abs(x1 - x2) < 50:
            new_v1 = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
            new_v2 = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)
            v1, v2 = new_v1, new_v2

        # Show velocities
        vtext = FONT.render(f"V1: {v1:.2f}     V2: {v2:.2f}", True, BLACK)
        screen.blit(vtext, (20, 20))

    pygame.display.update()
    clock.tick(60)
pygame.quit()