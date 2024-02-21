import pygame, sys
import button
import json

pygame.init()
     
SCREEN = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Game")


#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define fonts
TEXT_COL = (255, 255, 255)

#Data
data = {
    'X': SCREEN.get_width() / 2,
    'Y': SCREEN.get_height() / 2,
}

class Paddle:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.speed = speed

    def move(self, direction):
        if direction == "UP" and self.rect.top > 0:
            self.rect.y -= self.speed
        elif direction == "DOWN" and self.rect.bottom < SCREEN.get_height():
            self.rect.y += self.speed

class Ball:
    def __init__(self, x, y, speed, player_paddle, enemy_paddle):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.speed = speed
        self.player_paddle = player_paddle
        self.enemy_paddle = enemy_paddle

    def move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Ball collisions with walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN.get_height():
            self.speed[1] = -self.speed[1]

        # Ball collisions with paddles
        if self.rect.colliderect(self.player_paddle.rect) or self.rect.colliderect(self.enemy_paddle.rect):
            self.speed[0] = -self.speed[0]

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))

def play():
    pygame.display.set_caption('Play')

    clock = pygame.time.Clock()
    dt = 0

    #game variables
    game_paused = False

    player_paddle = Paddle(10, SCREEN.get_height() // 2 - 50, 10)
    enemy_paddle = Paddle(SCREEN.get_width() - 30, SCREEN.get_height() // 2 - 50, 5)
    ball = Ball(SCREEN.get_width() // 2 - 10, SCREEN.get_height() // 2 - 10, [5, 5], player_paddle, enemy_paddle)

    player_pos = pygame.Vector2(data['X'], data['Y'])

    SCREEN.fill('black')

    while True:
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = True
                    data['X'] = player_pos.x         
                    data['Y'] = player_pos.y
                    options()
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            pygame.display.update()

        SCREEN.fill('black')

        #check if game is paused
        if game_paused == True:
            pass
        else:
            draw_text("Press ESC to pause", font, TEXT_COL, 10, 10)

            pygame.draw.circle(SCREEN, "red", (int(ball.rect.x), int(ball.rect.y)), 10)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                player_paddle.move("UP")
            if keys[pygame.K_s]:
                player_paddle.move("DOWN")

            pygame.draw.rect(SCREEN, (255, 255, 255), player_paddle.rect)
            pygame.draw.rect(SCREEN, (255, 255, 255), enemy_paddle.rect)

            if ball.rect.centery < enemy_paddle.rect.centery:
                enemy_paddle.move("UP")
            elif ball.rect.centery > enemy_paddle.rect.centery:
                enemy_paddle.move("DOWN")

            # Draw the enemy paddle
            pygame.draw.rect(SCREEN, (255, 255, 255), enemy_paddle.rect)

            ball.move()
                
            pygame.display.flip()

        dt = clock.tick(60) / 1000

def options():
    pygame.display.set_caption('Options')

    SCREEN.fill('black')

    draw_text("PAUSED", font, TEXT_COL, 550, 300)

    #game variables
    game_paused = True

    while True:
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = False
                    with open('pause.txt','w') as pause_file:
                        json.dump(data,pause_file)
                    play()
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            pygame.display.update()

def main_menu():
    pygame.display.set_caption('Menu')

    #load buttons
    start_img = pygame.image.load('projects/pong/images/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('projects/pong/images/exit_btn.png').convert_alpha()

    start_button = button.Button(250, 300, start_img, 1)
    exit_button = button.Button(700, 300, exit_img, 1)

    while True: 
        #event handler
        for event in pygame.event.get():
            #quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((202, 228, 241))
        if start_button.draw(SCREEN) == True:
            play()
        if exit_button.draw(SCREEN) == True:
            pygame.quit()
            sys.exit()
            
        pygame.display.update()

main_menu()
