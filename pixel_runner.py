import pygame
import sys
import random
import time

pygame.init()


class backgrounds():
    def __init__(self):
        self.width = 800
        self.height = 550
        self.screen = pygame.display.set_mode((self.width, self.height))
        # background images
        self.sky_img = pygame.image.load(r"images\Sky.png")
        self.sky_img = pygame.transform.scale(self.sky_img, (800, 550))
        self.ground_img = pygame.image.load(r"images\ground.png")
        self.ground_img = pygame.transform.scale(self.ground_img, (830, 150))
        self.ground_rect = self.ground_img.get_rect(topleft=[0, 450])

        self.menu_icon = pygame.image.load(r"images\player_stand.png")
        self.menu_icon = pygame.transform.scale(self.menu_icon, (70, 80))
        self.gameover_img = pygame.image.load(r"images\game_over.xcf")
        # buttons
        self.restart_button = pygame.image.load(r"images\replay.png")
        self.restart_button = pygame.transform.scale(self.restart_button, (40,40))
        self.restart_button_rect = self.restart_button.get_rect(center=[ 550, 250])
        self.exit_button = pygame.image.load(r"images\exit.png")
        self.exit_button = pygame.transform.scale(self.exit_button, (40, 40))
        self.exit_button_rect = self.exit_button.get_rect(center=[200, 250])
        # settings
        self.clock = pygame.time.Clock()
        self.score = 0
        self.game_over = False
        self.score_counter = 0
        self.ground_velocity = -4
        self.distance = 0
        self.font = pygame.font.SysFont(None, 40)
        
    def score_and_highscore(self):
        global highscore
        text = self.font.render(f"Score : {self.score}", True, "black")
        if not self.game_over:
            self.distance += 1
            if self.distance >= 50:
                self.score += 1
                self.score_counter += 1
                self.distance = 0

            with open(r"images\highscore.txt", "r+") as file:
                highscore = file.read()
            if self.score > int(highscore):
                highscore = self.score
            with open(r"images\highscore.txt", "r+") as file:
                file.write(str(highscore))
        self.screen.blit(text, (10, 10))
        highscore_text = self.font.render(
            f"Highscore : {highscore}", True, "black")
        self.screen.blit(highscore_text, (580, 10))

    def draw_screen(self):
        self.clock.tick(80)
        pygame.display.update()
        self.screen.blit(self.sky_img, (0, 0))
        self.screen.blit(self.ground_img, (self.ground_rect.topleft))
        
        if not self.game_over:
            self.ground_rect.x += self.ground_velocity
        if self.ground_rect.x <= -30:
            self.ground_rect.x = 0
 
        self.score_and_highscore()
        

    def game_over_and_reset(self):
        if self.game_over:
            self.screen.blit(self.gameover_img, (220, 100))
            self.screen.blit(self.restart_button, (self.restart_button_rect.center))
            self.screen.blit(self.exit_button, (self.exit_button_rect.center))
            mouse = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()
            if  (mouse_button[0] == 1 or mouse_button[2] == 1) and self.restart_button_rect.collidepoint(mouse):
                self.score = 0
                self.ground_velocity = -4
                alien.velocity = 0
                obstacle_group.empty()
                flies_group.empty()
                alien.rect.bottomleft = alien.position
                alien.rect.x = 50
                alien.cooldown = 30
                self.game_over = False
                game_loop()
            elif  (mouse_button[0] == 1 or mouse_button[2]) and self.exit_button_rect.collidepoint(mouse) :
               
                sys.exit()

window = backgrounds()



class player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # settings
        self.position = position
        self.index = 0
        self.timer = 0
        self.allow_jump = True
        self.velocity = 0
        self.gravity = 0.5
        self.cooldown = 30
        self.jump_range = -14
        #imgaes
        self.player_list = [pygame.image.load(f"images\\player_img_{i}.png" ) for i in range(3)]
       
        self.image = self.player_list[self.index]
        self.rect = self.image.get_rect(bottomleft=self.position)
        self.rect.x = 50

    def update(self):
        # movement
        
        if not window.game_over:
            self.rect.y += self.velocity
            self.velocity += self.gravity
            
        # animation
            self.image = self.player_list[self.index]
            self.timer += 1
            if self.timer >= self.cooldown:
                self.index += 1
                self.timer = 0
            if self.index >= 2:
                self.index = 0
            if self.rect.bottom >= 450:
                self.rect.bottom = 450
                self.allow_jump = True
            if self.rect.bottom < 450:
                self.allow_jump = False
                self.index = 2
        if pygame.sprite.spritecollide(self, obstacle_group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(self, flies_group, False, pygame.sprite.collide_mask):
            window.game_over = True

alien = player(window.ground_rect.topleft)
alien_group = pygame.sprite.Group()
alien_group.add(alien)




class obstacles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f"images\\obstacle_{random.randint(0,2)}.png")
        self.image = pygame.transform.scale(self.image, (60, 70))
        self.rect = self.image.get_rect(bottomleft=[x, y])
        self.velocity = window.ground_velocity
      
    def update(self):
        if not window.game_over:
            self.rect.x += window.ground_velocity
        if self.rect.x <= -10:
            self.kill()
            
            
obstacle_group = pygame.sprite.Group()

def create_obstacle():
    if not window.game_over:
        cactus = obstacles(random.randint(830, 930), 460)
        print(cactus.velocity)
        obstacle_group.add(cactus)




class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_list = [pygame.image.load(f"images\\Fly{i}.png")for i in range(1, 3)]
        self.index = 0
        self.animation_timer = 0
        self.image = self.image_list[self.index]
        self.image = pygame.transform.scale(self.image,(40,40))
        self.rect = self.image.get_rect(center=[x, y])
        self.velocity = random.randint(window.ground_velocity*3,window.ground_velocity-3)
    def update(self):
        if not window.game_over:
            self.rect.x += self.velocity
            cooldown = 10
            self.image = self.image_list[self.index]
            self.animation_timer += 1
            if self.animation_timer >= cooldown:
                self.index += 1
                self.animation_timer = 0
            if self.index >= len(self.image_list):
                self.index = 0
            if self.rect.x <= -50:
                self.kill()
            self.image = self.image_list[self.index]

flies_group = pygame.sprite.Group()

def create_flies():
    if not window.game_over:
        fly = Fly(random.randint(830, 950), random.randint(220,260))
        flies_group.add(fly)




def main_menu():
    while True:

        pygame.display.update()
        start_button = pygame.image.load(
            r"images\start_button.jpg")
        start_button = pygame.transform.scale(start_button, (80, 38))
        start_button_rect = start_button.get_rect()
        start_button_rect.center = [380, 350]
        font = pygame.font.SysFont("joysticks monospace", 80)
        text = font.render("Pixel Runner", True, "blue")
        window.screen.blit(window.sky_img, (0, 0))
        window.screen.blit(window.ground_img, (0, 480))
        window.screen.blit(text, (250, 100))
        window.screen.blit(window.menu_icon, (380, 200))
        window.screen.blit(start_button, (start_button_rect.center))

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and start_button_rect.collidepoint(mouse_pos):
                window.screen.fill("black")
                game_loop()










def game_loop():
    # timers
    global obstacle_cooldown
    global obstacle_timer
    global flies_cooldown
    global flies_timer
    obstacle_timer = 0
    obstacle_cooldown = 150
    flies_cooldown = 300
    flies_timer = 0
    while True:
     
        window.draw_screen()
        
        alien_group.draw(window.screen)
        alien_group.update()
        
        flies_group.draw(window.screen)
        flies_group.update() 
        
        
        obstacle_timer += 1
        flies_timer += 1
        if obstacle_timer >= obstacle_cooldown and len(obstacle_group) <= 5:
            create_obstacle()
            obstacle_timer = 0
        obstacle_group.draw(window.screen)
        obstacle_group.update()
   
        
        
        if window.score >= 50 and flies_timer >= flies_cooldown and len(flies_group) <= 5:
            create_flies()
            flies_timer = 0
            flies_cooldown = random.randint(200,300)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and alien.allow_jump:
                    alien.velocity = alien.jump_range
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if alien.rect.collidepoint(pos) and alien.allow_jump:
                    alien.velocity = alien.jump_range
                    
        
        if window.score >= 30:
            alien.cooldown = 20
            window.ground_velocity = -5
            alien.jump_range = -12
        if window.score >= 60:
            window.ground_velocity = -8
            alien.cooldown = 10
            alien.jump_range = -11
        if window.game_over:
            window.game_over_and_reset()
            
            
            
            
main_menu()