#ΠΑΛΙΟ ΜΟΥ PROJECT ΜΙΝΙ GAME RACE ΜΕ ΚΟΥΤΑΚΙΑ,οπως αυτα στα Instagram reels...

# Εισαγωγή των απαραίτητων βιβλιοθηκών
import pygame
import random

# Αρχικοποίηση της Pygame
pygame.init()

# Ορισμός σταθερών
WIDTH, HEIGHT = 800, 600  # Διαστάσεις παραθύρου
BOX_SIZE = 30             # Μέγεθος κάθε κουτιού
NUM_BOXES = 4             # Αριθμός κουτιών
TARGET_Y = 50             # Y-θέση γραμμής τερματισμού
GAME_DURATION = 30        # Διάρκεια παιχνιδιού σε δευτερόλεπτα

# Παλέτα χρωμάτων
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
COLORS = [BLUE, YELLOW, RED, GREEN]  # Λίστα χρωμάτων για τα κουτιά

# Δημιουργία παραθύρου παιχνιδιού
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Boxes - Custom Map")  # Τίτλος παραθύρου

# Σχεδιασμός χάρτη με πλατφόρμες και εμπόδια
PLATFORMS = [
    pygame.Rect(0, HEIGHT-40, WIDTH, 40),  # Κύριο πάτωμα
    pygame.Rect(200, 500, 400, 20),        # Πλατφόρμα 1
    pygame.Rect(100, 400, 200, 20),        # Πλατφόρμα 2
    pygame.Rect(500, 300, 200, 20),        # Πλατφόρμα 3 
    pygame.Rect(0, 200, 150, 20),          # Πλατφόρμα 4
    pygame.Rect(300, 150, 200, 20)         # Πλατφόρμα 5
]

OBSTACLES = [
    pygame.Rect(400, 450, 50, 50),  # Αριστερό εμπόδιο
    pygame.Rect(600, 350, 30, 80),  # Μεσαίο εμπόδιο
    pygame.Rect(200, 250, 80, 30)   # Δεξιό εμπόδιο
]

# Κλάση που αναπαριστά τα κουτιά του παιχνιδιού
class Box:
    def __init__(self, color):
        # Αρχικές θέσεις και ταχύτητες
        self.x = random.randint(0, WIDTH - BOX_SIZE)  # Τυχαία X θέση
        self.y = random.randint(HEIGHT//2, HEIGHT - BOX_SIZE)  # Τυχαία Y θέση
        self.speed_y = 5   # Κατακόρυφη ταχύτητα
        self.speed_x = 5   # Οριζόντια ταχύτητα
        self.color = color # Χρώμα κουτιού
        self.finished = False  # Κατάσταση τερματισμού

    def get_rect(self):
        # Επιστρέφει το ορθογώνιο του κουτιού για collision detection
        return pygame.Rect(self.x, self.y, BOX_SIZE, BOX_SIZE)

    def move(self):
        if self.finished:
            return  # Αν έχει τερματίσει, σταματάει η κίνηση

        # Κίνηση στον οριζόντιο άξονα
        self.x += self.speed_x
        self.check_collisions('x')  # Έλεγχος συγκρούσεων X άξονα

        # Κίνηση στον κάθετο άξονα
        self.y -= self.speed_y
        self.check_collisions('y')  # Έλεγχος συγκρούσεων Y άξονα

        # Έλεγχος τερματισμού
        if self.y + BOX_SIZE <= TARGET_Y:
            self.finished = True
            self.y = TARGET_Y - BOX_SIZE  # Σταθεροποίηση θέσης

    def check_collisions(self, axis):
        # Έλεγχος συγκρούσεων με πλατφόρμες και όρια οθόνης
        box_rect = self.get_rect()

        # Έλεγχος με όλα τα στοιχεία χάρτη
        for platform in PLATFORMS + OBSTACLES:
            if box_rect.colliderect(platform):
                if axis == 'x':  # Οριζόντια σύγκρουση
                    if self.speed_x > 0:  # Κίνηση προς τα δεξιά
                        self.x = platform.left - BOX_SIZE
                    elif self.speed_x < 0:  # Κίνηση προς τα αριστερά
                        self.x = platform.right
                    self.speed_x *= -1  # Ανάκλαση ταχύτητας
                elif axis == 'y':  # Κατακόρυφη σύγκρουση
                    if self.speed_y > 0:  # Κίνηση προς τα πάνω
                        self.y = platform.bottom
                    elif self.speed_y < 0:  # Κίνηση προς τα κάτω
                        self.y = platform.top - BOX_SIZE
                    self.speed_y *= -1  # Ανάκλαση ταχύτητας

        # Σύγκρουση με πλαϊνά όρια οθόνης
        if self.x < 0:
            self.x = 0
            self.speed_x *= -1
        elif self.x + BOX_SIZE > WIDTH:
            self.x = WIDTH - BOX_SIZE
            self.speed_x *= -1

    def draw(self):
        # Σχεδίαση του κουτιού στην οθόνη
        pygame.draw.rect(screen, self.color, (self.x, self.y, BOX_SIZE, BOX_SIZE))

    # Συνάρτηση σύγκρουσης μεταξύ κουτιών (προσοχή: αυτή η μέθοδος είναι εκτός κλάσης και ίσως χρειαστεί να μεταφερθεί)
    def check_collision(self, other):
        if self.finished or other.finished:
            return
            
        rect1 = self.get_rect()
        rect2 = other.get_rect()
        
        if rect1.colliderect(rect2):
            # Υπολογισμός επικάλυψης
            overlap_x = min(rect1.right - rect2.left, rect2.right - rect1.left)
            overlap_y = min(rect1.bottom - rect2.top, rect2.bottom - rect1.top)
            
            if overlap_x < overlap_y:  # Οριζόντια σύγκρουση
                if rect1.centerx < rect2.centerx:
                    correction = (rect1.right - rect2.left) / 2
                else:
                    correction = (rect2.right - rect1.left) / 2
                self.x -= correction
                other.x += correction
                self.speed_x *= -1
                other.speed_x *= -1
            else:  # Κατακόρυφη σύγκρουση
                if rect1.centery < rect2.centery:
                    correction = (rect1.bottom - rect2.top) / 2
                else:
                    correction = (rect2.bottom - rect1.top) / 2
                self.y -= correction
                other.y += correction
                self.speed_y *= -1
                other.speed_y *= -1

# Συνάρτηση σχεδίασης χάρτη
def draw_map():
    # Σχεδίαση πλατφορμών
    for platform in PLATFORMS:
        pygame.draw.rect(screen, GREY, platform)
    
    # Σχεδίαση εμποδίων
    for obstacle in OBSTACLES:
        pygame.draw.rect(screen, RED, obstacle)


# Αρχικοποίηση παιχνιδιού
boxes = [Box(color) for color in COLORS]  # Δημιουργία κουτιών
font = pygame.font.Font(None, 74)         # Γραμματοσειρά για τα αποτελέσματα
timer_font = pygame.font.Font(None, 50)   # Γραμματοσειρά για το χρονομέτρο

running = True             # Ελεγχος λειτουργίας παιχνιδιού
finished_boxes = []        # Λίστα τερματισμένων κουτιών
start_time = pygame.time.get_ticks()  # Χρόνος έναρξης

# Κύρια λούπα παιχνιδιού
while running:
    screen.fill(BLACK)  # Καθαρισμός οθόνης
    draw_map()  # Σχεδίαση χάρτη
    
    # Άσπρη περιοχή πάνω από τη γραμμή τερματισμού
    screen.fill(WHITE, (0, 0, WIDTH, TARGET_Y))  # <-- Προσθήκη εδώ
    
    # Γκρι γραμμή τερματισμού
    pygame.draw.line(screen, GREY, (0, TARGET_Y), (WIDTH, TARGET_Y), 2)
    
    # Χρονομέτρο (αλλαγή χρώματος κειμένου σε μαύρο)
    current_time = pygame.time.get_ticks() - start_time
    remaining_time = max(GAME_DURATION - (current_time // 1000), 0)
    timer_text = timer_font.render(f"Time: {remaining_time}", True, BLACK)  # Αλλαγή εδώ
    screen.blit(timer_text, (10, 10))
    
    # Επεξεργασία συμβάντων
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Αν πατηθεί το 'X'
            running = False

    # Κίνηση και σύγκρουση κουτιών
    for box in boxes:
        box.move()  # Ενημέρωση θέσεων
    
    # Έλεγχος συγκρούσεων μεταξύ κουτιών
    for i in range(len(boxes)):
        box = boxes[i]
        if box.finished:
            continue
        for j in range(i + 1, len(boxes)):
            other = boxes[j]
            if not other.finished:
                box.check_collision(other)  # Έλεγχος σύγκρουσης
    
    # Σχεδίαση όλων των κουτιών
    for box in boxes:
        box.draw()
    
    # Ενημέρωση λίστας τερματισμένων
    for box in boxes:
        if box.finished and box not in finished_boxes:
            finished_boxes.append(box)
    
    # Έλεγχος συνθηκών τερματισμού
    time_up = remaining_time <= 0             # Έλεγχος λήξης χρόνου
    all_finished = len(finished_boxes) == len(boxes)  # Έλεγχος ολοκλήρωσης
    
    if time_up or all_finished:
        running = False  # Τερματισμός παιχνιδιού
    
    pygame.display.flip()  # Ανανέωση οθόνης
    pygame.time.delay(30)  # Καθυστέρηση για σταθερό frame rate

# Επεξεργασία αποτελεσμάτων όταν λήξει ο χρόνος
if time_up:
    for box in boxes:
        if not box.finished:
            finished_boxes.append(box)  # Προσθήκη υπολοίπων κουτιών
    finished_boxes.sort(key=lambda b: b.y)  # Ταξινόμηση με βάση την απόσταση από τερματισμό

# Εμφάνιση τελικής κατάταξης
screen.fill(BLACK)
for i, box in enumerate(finished_boxes):
    position = i + 1
    # Ορισμός κατάληξης θέσης (1st, 2nd, κλπ)
    suffix = "st" if position == 1 else "nd" if position == 2 else "rd" if position == 3 else "th"
    text = font.render(f"{position}{suffix} Place", True, box.color)  # Δημιουργία κειμένου
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 80))  # Θέση κειμένου
    screen.blit(text, text_rect)  # Σχεδίαση κειμένου

pygame.display.flip()  # Τελική ανανέωση οθόνης
pygame.time.delay(4000)  # Καθυστέρηση 4 δευτερολέπτων

pygame.quit()  # Τερματισμός Pygame
