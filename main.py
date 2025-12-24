import math
import pygame
import sys

# PYGAME INITIALIZATION
pygame.init()

# Sound system initialize 
pygame.mixer.init()

# SCREEN SETUP
WIDTH, HEIGHT = 1080, 670
# FULLSCREEN FLAG
fullscreen = False

# Screen create kar rahe hain jahan sab draw hoga
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Window ke upar title dikhane ke liye
pygame.display.set_caption("1D Collision Simulator")

# Fonts define kar rahe hain taaki text screen pe likh sake
FONT = pygame.font.SysFont(None, 28)
BIGFONT = pygame.font.SysFont(None, 40)
TITLEFONT = pygame.font.SysFont(None, 48)


# Colors define 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
BLUE = (0, 150, 255)
RED = (255, 80, 80)
GREEN = (0, 255, 120)
ORANGE = (255, 200, 0)

# SOUND LOADING
# Collision ke time jo sound bajega usko load kar rahe hain
# Ye file sounds folder ke andar honi chahiye
collision_sound = pygame.mixer.Sound("sounds/collision.wav")

# Default volume 50% rakha hai
volume = 0.5
collision_sound.set_volume(volume)

# Ye flag decide karega sound bajega ya nahi
sound_on = True

# ================= INPUT VALIDATION LIMITS =================
# Ye limits invalid inputs ko rokne ke liye hain
MIN_MASS = 0.1                 # Mass zero ya negative nahi ho sakta
MAX_VELOCITY = 20              # Velocity ki safe limit

# Error message dikhane ke liye variables
error_message = ""
error_timer = 0                # Frames ke hisaab se error auto-hide hoga
# ==========================================================

# INPUT BOX CLASS
# Ye class user se mass aur velocity input lene ke liye banayi hai
class InputBox:
    def __init__(self, x, y, w, h):
        # Input box ka area (position + size)
        self.rect = pygame.Rect(x, y, w, h)

        # Box ke andar jo text user likhega
        self.text = ""

        # Ye batata hai box active hai ya nahi
        self.active = False

        # Cursor blink ke liye variables
        # Isse box ke andar typing realistic lagegi
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        # Mouse click se check karte hain box pe click hua ya nahi
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        # Keyboard input tabhi lena hai jab box active ho
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                # Backspace dabane pe last character delete
                self.text = self.text[:-1]
            else:
                # Sirf numbers, dot aur minus allow kar rahe hain
                # Extra check: multiple dots ya minus avoid karne ke liye
                if (
                    event.unicode.isdigit()
                    or (event.unicode == "." and "." not in self.text)
                    or (event.unicode == "-" and self.text == "")
                ):
                    self.text += event.unicode

    def draw(self):
        # Input box ka white background (rounded look ke saath)
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=12)

        # Active hone pe blue border, warna black
        pygame.draw.rect(
            screen,
            BLUE if self.active else BLACK,
            self.rect,
            2,
            border_radius=12
        )

        # Text ko screen pe render kar rahe hain
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 18))

        # Cursor blink logic
        # Ye har kuch frames me cursor ko on/off karta hai
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer % 30 == 0:
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_x = self.rect.x + 10 + txt.get_width() + 2
                cursor_y = self.rect.y + 14
                pygame.draw.line(
                    screen,
                    BLACK,
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + 25),
                    2
                )

    def get_value(self):
        # Input value ko return karte hain
        return self.text.strip()

    def clear(self):
        # Reset ke time input box empty karne ke liye
        self.text = ""
        self.active = False

# INPUT BOXES (START SCREEN)
form_start_y = 190
form_gap = 70

input_boxes = [
    InputBox(440, form_start_y + 0 * form_gap, 200, 55),
    InputBox(440, form_start_y + 1 * form_gap, 200, 55),
    InputBox(440, form_start_y + 2 * form_gap, 200, 55),
    InputBox(440, form_start_y + 3 * form_gap, 200, 55),
]
active_box_index = 0
input_boxes[0].active = True


# BUTTONS
start_button = pygame.Rect(420, form_start_y + 4 * form_gap + 10, 220, 55)
pause_button = pygame.Rect(800, 20, 170, 45)
reset_button = pygame.Rect(800, 75, 170, 45)

slider_bar = pygame.Rect(WIDTH - 260, 500, 200, 5)
slider_knob_x = slider_bar.x + int(volume * slider_bar.width)
sound_button = pygame.Rect(WIDTH - 240, 520, 160, 40)

# CONSTRAINTS INFO BOX (RIGHT SIDE - ABOVE VOLUME SLIDER)
# Right margin se thoda left, volume slider ke upar
constraints_box = pygame.Rect(
    WIDTH - 300,     # X position (right side)
    100,             # Y position (volume slider ke upar)
    260,             # Width
    120              # Height
)

# PHYSICS VARIABLES
x1, x2 = 200, 800
v1 = v2 = 0
m1 = m2 = 1

MIN_RADIUS = 1
MAX_RADIUS = 45

def compute_radius(mass):
    return max(
        MIN_RADIUS,
        min(MAX_RADIUS, int(4 + math.sqrt(mass) * 6))
    )

radius1 = compute_radius(m1)
radius2 = compute_radius(m2)


simulation_started = False
paused = False
collision_happened = False

# RESET FUNCTION
def reset_simulation():
    global x1, x2, v1, v2, m1, m2, radius1, radius2
    global simulation_started, paused, collision_happened
    global error_message, error_timer

    x1, x2 = 200, 800
    v1 = v2 = 0
    m1 = m2 = 1

    radius1 = compute_radius(m1)
    radius2 = compute_radius(m2)

    simulation_started = False
    paused = False
    collision_happened = False

    error_message = ""
    error_timer = 0

    for box in input_boxes:
        box.clear()
    global active_box_index
    active_box_index = 0
    for i, box in enumerate(input_boxes):
        box.active = (i == 0)


# MAIN LOOP
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((235, 235, 235))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
                    # FULLSCREEN TOGGLE (F key)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

        # START SCREEN INPUT 
        if not simulation_started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                input_boxes[active_box_index].active = False
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    active_box_index = (active_box_index - 1) % len(input_boxes)
                else:
                    active_box_index = (active_box_index + 1) % len(input_boxes)
                input_boxes[active_box_index].active = True
            for box in input_boxes:
                box.handle_event(event)

            #  (ENTER → START simulation)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    m1 = float(input_boxes[0].get_value())
                    m2 = float(input_boxes[1].get_value())
                    v1 = float(input_boxes[2].get_value())
                    v2 = float(input_boxes[3].get_value())

                    if m1 <= 0 or m2 <= 0:
                        raise ValueError("Mass must be greater than 0")

                    radius1 = compute_radius(m1)
                    radius2 = compute_radius(m2)

                    if abs(v1) > MAX_VELOCITY or abs(v2) > MAX_VELOCITY:
                        raise ValueError(
                            f"Velocity must be between -{MAX_VELOCITY} and {MAX_VELOCITY}"
                        )
                    error_message = ""
                    simulation_started = True

                except ValueError as e:
                    error_message = str(e)
                    error_timer = 180

                except:
                    error_message = "Invalid input"
                    error_timer = 180

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                try:
                    m1 = float(input_boxes[0].get_value())
                    m2 = float(input_boxes[1].get_value())
                    v1 = float(input_boxes[2].get_value())
                    v2 = float(input_boxes[3].get_value())
                        # MASS VALIDATION
                    if m1 <= 0 or m2 <= 0:
                        raise ValueError("Mass must be greater than 0")
                    radius1 = compute_radius(m1)
                    radius2 = compute_radius(m2)
                    # VELOCITY RANGE CHECK
                    if abs(v1) > MAX_VELOCITY or abs(v2) > MAX_VELOCITY:
                        raise ValueError(
                            f"Velocity must be between -{MAX_VELOCITY} and {MAX_VELOCITY}"
                        )
                        # Sab valid hai to simulation start
                    error_message = ""
                    simulation_started = True

                except ValueError as e:
                    error_message = str(e)
                    error_timer = 180   # ~3 seconds

                except:
                    error_message = "Invalid input"
                    error_timer = 180   # ~3 seconds

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos) and simulation_started:
                paused = not paused

        if event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.collidepoint(event.pos):
                reset_simulation()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if sound_button.collidepoint(event.pos):
                sound_on = not sound_on

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if pygame.mouse.get_pressed()[0]:
                if slider_bar.collidepoint(pygame.mouse.get_pos()):
                    slider_knob_x = max(
                        slider_bar.x,
                        min(pygame.mouse.get_pos()[0], slider_bar.x + slider_bar.width)
                    )
                    volume = (slider_knob_x - slider_bar.x) / slider_bar.width
                    collision_sound.set_volume(volume)

    # START SCREEN UI
    if not simulation_started:
        title = TITLEFONT.render("1D Collision Simulator", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 90))

        labels = [
            "Mass of Object 1",
            "Mass of Object 2",
            "Velocity of Object 1",
            "Velocity of Object 2"
        ]

        for i, text in enumerate(labels):
            screen.blit(
                FONT.render(text, True, BLACK),
                (220, form_start_y + i * form_gap + 18)
            )

        for box in input_boxes:
            box.draw()

        pygame.draw.rect(screen, GREEN, start_button, border_radius=14)
        screen.blit(
            BIGFONT.render("START", True, BLACK),
            (start_button.x + 65, start_button.y + 12)
        )

        # ERROR MESSAGE DISPLAY (CENTERED)
        if error_message:
            err = FONT.render(error_message, True, RED)
            screen.blit(
                err,
                (WIDTH // 2 - err.get_width() // 2, start_button.y + 70)
            )
                    # INPUT CONSTRAINTS BOX (STATIC)
        # Ye box hamesha visible rahega, blink nahi karega
        pygame.draw.rect(screen, (245, 245, 245), constraints_box, border_radius=12)
        pygame.draw.rect(screen, BLACK, constraints_box, 2, border_radius=12)

        title = FONT.render("Input Constraints:", True, BLACK)
        screen.blit(title, (constraints_box.x + 15, constraints_box.y + 10))

        c1 = FONT.render("• Mass > 0", True, BLACK)
        screen.blit(c1, (constraints_box.x + 15, constraints_box.y + 45))

        c2 = FONT.render(
            f"• Velocity range: -{MAX_VELOCITY} to {MAX_VELOCITY}",
            True,
            BLACK
        )
        screen.blit(c2, (constraints_box.x + 15, constraints_box.y + 75))


    # SIMULATION SCREEN
    else:
        pygame.draw.circle(screen, BLUE, (int(x1), HEIGHT // 2), radius1)
        pygame.draw.circle(screen, RED, (int(x2), HEIGHT // 2), radius2)

        info1 = FONT.render(f"Object 1 | Mass: {m1} | Velocity: {v1:.2f}", True, BLACK)
        info2 = FONT.render(f"Object 2 | Mass: {m2} | Velocity: {v2:.2f}", True, BLACK)

        screen.blit(info1, (40, HEIGHT // 2 - 90))
        screen.blit(info2, (40, HEIGHT // 2 + 40))

        if not paused:
            x1 += v1
            x2 += v2

            if x1 <= radius1 or x1 >= WIDTH - radius1:
                v1 = -v1
            if x2 <= radius2 or x2 >= WIDTH - radius2:
                v2 = -v2

            if abs(x1 - x2) < (radius1 + radius2) and not collision_happened:
                if sound_on:
                    collision_sound.play()

                new_v1 = (v1 * (m1 - m2) + 2 * m2 * v2) / (m1 + m2)
                new_v2 = (v2 * (m2 - m1) + 2 * m1 * v1) / (m1 + m2)

                v1, v2 = new_v1, new_v2
                collision_happened = True

            if abs(x1 - x2) >= (radius1 + radius2):
                collision_happened = False

        pygame.draw.rect(screen, ORANGE, pause_button, border_radius=10)
        screen.blit(
            FONT.render("RESUME" if paused else "PAUSE", True, BLACK),
            (pause_button.x + 45, pause_button.y + 12)
        )

        pygame.draw.rect(screen, GRAY, reset_button, border_radius=10)
        screen.blit(
            FONT.render("RESET", True, BLACK),
            (reset_button.x + 55, reset_button.y + 12)
        )

    # SOUND UI (COMMON)
    pygame.draw.rect(screen, GRAY, sound_button, border_radius=10)
    sound_text = "Sound: ON" if sound_on else "Sound: OFF"
    screen.blit(FONT.render(sound_text, True, BLACK),
                (sound_button.x + 15, sound_button.y + 10))

    pygame.draw.rect(screen, BLACK, slider_bar)
    pygame.draw.circle(screen, RED, (slider_knob_x, slider_bar.y + 2), 8)
    screen.blit(
        FONT.render("Volume", True, BLACK),
        (slider_bar.x, slider_bar.y - 25)
    )

    # ERROR MESSAGE TIMER (auto hide)
    if error_timer > 0:
        error_timer -= 1
    else:
        error_message = ""

    pygame.display.update()
    clock.tick(60)

pygame.quit()
