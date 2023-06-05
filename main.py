import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid Destroyer")

# Load background image
background_img = pygame.image.load("new.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load player image
player_img = pygame.image.load("cool spaceship.png")
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10

# Set up player bullets
bullet_width = 5
bullet_height = 15
bullet_speed = 5
bullets = []

# Load asteroid image
asteroid_img = pygame.image.load("medium.png")
asteroid_width = 50
asteroid_height = 50
asteroid_speed = 3
asteroids = []
asteroid_spawn_delay = 1000
last_asteroid_spawn_time = pygame.time.get_ticks()

# Set up the game clock
clock = pygame.time.Clock()

# Game state
running = True
game_over = False
score = 0
high_score = 0
lives = 3
stage = 1

# Load sound effects
shoot_sound = pygame.mixer.Sound("shoot.wav")
banglarge = pygame.mixer.Sound("bangLarge.wav")
bangsmall = pygame.mixer.Sound("bangSmall.wav")

# Class definitions for power-ups
class PowerUp:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.width = 30
        self.height = 30
        self.speed = 3

    def update(self):
        self.y += self.speed

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        powerup_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return powerup_rect.colliderect(rect)

class ScoreMultiplierPowerUp(PowerUp):
    def apply_effect(self):
        global score
        score *= 2

# Function to spawn power-ups
def spawn_powerup():
    powerup_x = random.randint(0, WIDTH - powerup_width)
    powerup_y = -powerup_height
    powerups.append(PowerUp(powerup_x, powerup_y, powerup_img))

def spawn_score_multiplier_powerup():
    powerup_x = random.randint(0, WIDTH - powerup_width)
    powerup_y = -powerup_height
    powerups.append(ScoreMultiplierPowerUp(powerup_x, powerup_y, score_multiplier_powerup_img))

# Load power-up images
powerup_img = pygame.image.load("new heart.png")
powerup_width = 20
powerup_height = 20
powerups = []
extralives_spawn_delay = 10000
last_extralives_spawn_time = pygame.time.get_ticks()

score_multiplier_powerup_img = pygame.image.load("star.png")
score_multiplier_spawn_delay = 15000
last_score_multiplier_spawn_time = pygame.time.get_ticks()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5

        # Boundary check for player
        if player_x < 0:
            player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

        # Fire bullets
        if keys[pygame.K_SPACE]:
            bullet_x = player_x + player_width // 2 - bullet_width // 2
            bullet_y = player_y - bullet_height
            bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))
            shoot_sound.play()

        # Update bullet positions
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Update asteroid positions
        if pygame.time.get_ticks() - last_asteroid_spawn_time > asteroid_spawn_delay:
            asteroid_x = random.randint(0, WIDTH - asteroid_width)
            asteroid_y = -asteroid_height
            asteroids.append(pygame.Rect(asteroid_x, asteroid_y, asteroid_width, asteroid_height))
            last_asteroid_spawn_time = pygame.time.get_ticks()

        for asteroid in asteroids:
            asteroid.y += asteroid_speed
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)

        # Update power-up positions
        if pygame.time.get_ticks() - last_extralives_spawn_time > extralives_spawn_delay:
            spawn_powerup()
            last_extralives_spawn_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - last_score_multiplier_spawn_time > score_multiplier_spawn_delay:
            spawn_score_multiplier_powerup()
            last_score_multiplier_spawn_time = pygame.time.get_ticks()

        for powerup in powerups:
            powerup.update()
            if powerup.y > HEIGHT:
                powerups.remove(powerup)
            elif powerup.collide(player_rect):
                powerups.remove(powerup)
                if isinstance(powerup, ScoreMultiplierPowerUp):
                    powerup.apply_effect()
                else:
                    lives += 1

        # Collision detection - player and asteroids
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for asteroid in asteroids:
            if player_rect.colliderect(asteroid):
                asteroids.remove(asteroid)
                lives -= 1
                if lives <= 0:
                    game_over = True
                    if score > high_score:
                        high_score = score
                    score = 0
                    lives = 0

        # Collision detection - bullets and asteroids
        for bullet in bullets:
            for asteroid in asteroids:
                if bullet.colliderect(asteroid):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    banglarge.play()
                    score += 1

        # Update stage based on score
        if score >= 70:
            stage = 3
        elif score >= 50:
            stage = 2
        elif score >= 30:
            stage = 1

    # Draw background
    win.blit(background_img, (0, 0))

    # Draw player
    win.blit(player_img, (player_x, player_y))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(win, (255, 255, 255), bullet)

    # Draw asteroids
    for asteroid in asteroids:
        win.blit(asteroid_img, (asteroid.x, asteroid.y))

    # Draw powerups
    for powerup in powerups:
        powerup.draw(win)

    # Draw score, lives, stage, and game over message
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
    stage_text = font.render("Stage: " + str(stage), True, (255, 255, 255))
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    win.blit(score_text, (10, 10))
    win.blit(lives_text, (10, 50))
    win.blit(stage_text, (10, 90))

    if game_over:
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        running = False

    # Update the display
    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
