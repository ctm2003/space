# Save this file as something meaningful!
# Unless you want your game to be callled skeleton...

import pygame
from pygame.math import Vector2
from random import randint

# Setup
pygame.init()

WHITE = (255, 255, 255)
RED =   (255,   0,   0)
BLACK = (  0,   0,   0)

# Screen
size = [400, 700]
screen = pygame.display.set_mode(size)

# Objects and variables
done = False
clock = pygame.time.Clock()
x_speed = 0
y_speed = 0
small_font = pygame.font.SysFont("Arial", 12)
hit_count = 0
a_down = False
d_down = False
w_down = False
s_down = False
# Make Ship a subclass of Sprite.
# This means that all the operations that the Sprite class has will be
# something that the Ship class can do.
# We say "Ship inherits from Sprite"
class Ship(pygame.sprite.Sprite):
    # All classes must have an __init__ method.
    # All data that a class uses must be initialised in the __init__ method.
    # Each data element is called a field.
    def __init__(self, position):
        # First make sure the base class is initialised.
        pygame.sprite.Sprite.__init__(self)

        # This ship will have a speed as internal data as a Vector2, which
        # set to (0,0) initially.
        self.speed = Vector2(0, 0)

        # Spirtes should have an image field. In this caes we load the image
        # from a file on disk and scale it so it is suitant isble for our screen.
        self.image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(self.image, (46, 78))

        # pygame uses the rect field of a Spirte to draw the Sprite, but also
        # to calculate collisions so we have to initialise it.
        # We take the rect from the image field and then we change the x and y
        # fields of the rect in order to place the Ship on the right spot on the
        # screen.
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

    # The update method of the Sprite class doesn't do anything. The purpose of
    # it is to provide a hook for you to provide a way to update your class in
    # a way that fits with the basic features of pygame.
    # In this caes we just move the rect with the coordinates of the speed vector.
    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y
        if self.rect.centerx > 400:
            self.rect.centerx = 400
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centery > 700:
            self.rect.centery = 700
        if self.rect.centery < 300:
            self.rect.centery = 300

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, -10)

        self.image = pygame.image.load('snowball.png')
        self.image = pygame.transform.scale(self.image, (50, 25))

        self.rect = self.image.get_rect()
        self.rect.x = 175
        self.rect.y = 600

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

class Patty(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.speed = Vector2(0, 7)

        self.image = pygame.image.load('Patrick.png')
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 0

    def update(self):
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

# Handle sprites
# Create as many Sprite groups as you need to make things easy to manage.
# all_sprites contains all the objects we'll ever create. All objects must be
# added to the all_sprites Group for things to work.

all_sprites = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_Patty = pygame.sprite.Group()

player_ship = Ship (Vector2(200,620))
all_sprites.add(player_ship)

p1 = Patty()
all_Patty.add(p1)
all_sprites.add(p1)

def new_bullet():
    bullet = Bullet()
    bullet.rect.centerx = player_ship.rect.centerx
    bullet.rect.centery = player_ship.rect.top
    all_bullets.add(bullet)
    all_sprites.add(bullet)

def new_patty():
    if randint(1,10) == 1:
        p1 = Patty()
        p1.rect.left = randint(0,400 - p1.rect.width)
        all_Patty.add(p1)
        all_sprites.add(p1)

# -------- Main Program Loop -----------
# we use the global variable done to control when to end the game.
while not done:
    # --- Event Processing
    # Get all events from keyboard and/or mouse.
    for event in pygame.event.get():
        # if you click the x in the window top the game will end
        if event.type == pygame.QUIT:
            done = True

        # if you press a key and it is either A or D change the speed of
        # the x_speed variable.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                x_speed = 5
                d_down = True
            if event.key == pygame.K_a:
                x_speed = -5
                a_down = True
            if event.key == pygame.K_s:
                y_speed = 5
                s_down = True
            if event.key == pygame.K_w:
                y_speed = -5
                w_down = True
            if event.key == pygame.K_SPACE:
                new_bullet()


        # When the A or D  key is released change the x_speed to 0.
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_down = False
                if d_down:
                    x_speed = 5
                else:
                    x_speed = 0
            if event.key == pygame.K_d:
                d_down = False
                if a_down:
                    x_speed = -5
                else:
                    x_speed = 0
            if event.key == pygame.K_s:
                s_down = False
                if w_down:
                    x_speed = 5
                else:
                    x_speed = 0
            if event.key == pygame.K_w:
                w_down = False
                if w_down:
                    x_speed = 5
                else:
                    x_speed = 0


    # --- Game Logic
    # Update variables
    player_ship.speed.x = x_speed
    player_ship.speed.y = y_speed
    new_patty()
    all_sprites.update()

    # Collisions    x_speed = 0
    # Read the documentation of groupcollide very carefully and figure out
    # how the arguments work.
    hit_list = pygame.sprite.groupcollide(all_Patty, all_bullets, True, True)
    hit_count += len(hit_list)

    collision = pygame.sprite.spritecollideany(player_ship, all_Patty)
    if collision:
        done = True


    # --- Draw
    # When using Sprite groups it is super easy to update the screen:
    # 1. Clear the screen.
    # 2. Call the draw method of the all_sprites Group using the screen as the
    #    only argument.
    screen.fill(RED)
    all_sprites.draw(screen)


    hit_text = small_font.render("Hits: " + str(hit_count), 1, WHITE)
    screen.blit(hit_text, (10, 10))

    # Update screen
    # pygame will draw the screen in the background and only when it is time
    # to update it will it be shown on the screen.

    clock.tick(30)  # update the screen 30 times every second.
    pygame.display.flip()


# When we break out of the gmae loop there is nothing to do but..
# Close the window and quit.
pygame.quit()
