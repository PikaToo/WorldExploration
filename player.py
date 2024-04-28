import pygame
from pygame.locals import *
from entity import Entity       # players are entities
from bullet import Bullet       # player can make bullets
from gameObject import GameObject
from platformManager import Platform   # player needs to know platform locations

class Player(Entity):
    def __init__(self):
        # initial rect, color, and velocities
        super().__init__(100, 550, 20, (0, 0, 255), 0, 0)
        
        # player abilities
        self.unlocked_double_jump = False
        self.unlocked_dash = False
        self.unlocked_bullets = False
        self.unlocked_higher_health = False
        
        # seeing if double jump has been used and how long the player has been off the ground for
        self.double_jump = False
        self.double_jump_counter = 0    # frames since first jump

        # values used for dodging
        self.dodge_counter = 0
        self.x_dir = 0           # tracks last direction faced

        # cooldown for bullets
        self.bullet_counter = 0

        # check to see if allowed to exit the room. only false when a boss is alive.
        self.exit_status = True

        # seeing if holding jump button, used to make sure you press it instead of holding
        self.previous_w_value = False
        self.on_ground = False

        # bad that saving is done like this TODO: fix
        self.save = 0
        self.FPS_clock = None
        self.FPS = 60
    
    # updates player by moving and applying anything required
    def update(self):
        key = pygame.key.get_pressed()
        
        # x-movement from pressing movement keys
        # first sets values to 0 in case no button is pressed
        x_movement = 0
        if key[K_d]:
            x_movement = 5
            self.x_dir = 1
        if key[K_a]:
            x_movement = -5
            self.x_dir = -1

        # dashing
        if key[K_SPACE] and self.dodge_counter >= 40 and GameObject.ability_statuses.dash:
            self.x_velocity = self.x_dir * 25
            self.dodge_counter = 0
        if self.dodge_counter < 40:
            self.dodge_counter += 1

        # decreasing x velocity
        if self.x_velocity > 0:
            self.x_velocity -= 1
        if self.x_velocity < 0:
            self.x_velocity += 1

        # y-movement
        # can only press jump, not hold.
        if not self.previous_w_value:
            if key[K_w]:
                if self.on_ground:
                    self.y_velocity = -13
                elif self.double_jump and self.double_jump_counter > 5 and GameObject.ability_statuses.double_jump:
                    self.y_velocity = -13
                    self.double_jump = False
        self.previous_w_value = key[K_w]

        if not self.on_ground:                  # if not on the ground, gravity applies
            self.y_velocity += 0.6              # and double-jump counter starts
            self.double_jump_counter += 1

        # clamps velocity (velocity can't exceed terminal velocity)
        self.y_velocity = max(-20, min(self.y_velocity, 20))

        # moves first in x direction and then y direction
        self.move_linear(x_movement + self.x_velocity, 0)   # moving by x from movent press + velocity
        self.move_linear(0, self.y_velocity)

        if GameObject.ability_statuses.blaster:
            self.shoot()

    def shoot(self):
        # counting upwards until it reaches 15 where it stops.
        # doesn't need to stop, only doing so to avoid very large numbers
        if self.bullet_counter < 15:
            self.bullet_counter += 1

        # gets mouse vectors for shooting. if no keyboard inputs are registered, uses them.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_diff = mouse_x - self.rect.x
        y_diff = mouse_y - self.rect.y

        # if keyboard controls are used.
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_DOWN] or key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
            y_diff = x_diff = 0
            if key[pygame.K_UP]:
                y_diff = -1
            if key[pygame.K_DOWN]:
                y_diff = 1
            if key[pygame.K_LEFT]:
                x_diff = -1
            if key[pygame.K_RIGHT]:
                x_diff = 1

        # using values obtained to get a vector to determine how the bullet will travel
        if not (abs(x_diff) + abs(y_diff)) == 0:  # first making sure no divide by 0 error
            x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
            y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y

            valid_key_pressed = key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_UP] or key[pygame.K_DOWN] or \
                pygame.mouse.get_pressed()[0]

            # firing. can only fire 4 times a second
            if valid_key_pressed and self.bullet_counter >= 15:
                # bullet direction is set based on vectors
                Bullet(self.rect.x + 5, self.rect.y + 5, x_vector * 20, y_vector * 20, "player", 10, 0, 1)
                self.bullet_counter = 0

    def move_linear(self, x, y):
        self.rect.x += x  # move by x, which is the sum of regular movement + velocity (from dashing)

        self.on_ground = False  # assumes you are in free-fall
        self.rect.y += y  # moves you by velocity

        for platform in Platform.platforms:  # platform collision detection
            if platform.type == "platform":
                if (self.rect.bottom == platform.rect.top) and \
                    (self.rect.left in range (platform.rect.left - self.rect.width, platform.rect.right)):
                    self.on_ground = True
            if self.rect.colliderect(platform.rect):
                if platform.type == "platform":
                    if x > 0:
                        self.rect.right = platform.rect.left
                    if x < 0:
                        self.rect.left = platform.rect.right

                    if y > 0:
                        self.rect.bottom = platform.rect.top
                        self.on_ground = True  # if you are touching the ground, these 2 are set as true.
                        self.double_jump = True  # allows you to jump and resets double jump ability.
                        self.double_jump_counter = 0  # sets counter for double jump to 0, used to prevent
                        self.y_velocity = 0
                    if y < 0:  # both jumps from immediately occuring back-to-back.
                        self.rect.top = platform.rect.bottom

                if platform.type == "load":
                    if GameObject.world_x == 0 and GameObject.world_y == 8:
                        self.save = 1
                    if GameObject.world_x == 2 and GameObject.world_y == 7:
                        self.save = 2


    # called by main if the player is trying to leave the world bounds when not allowed
    def stop_escape(self):
        if self.rect.x < 0:
            self.rect.x = 0
            self.x_velocity = 8
        if self.rect.x > GameObject.window_width - 20:
            self.rect.x = GameObject.window_width - 20
            self.x_velocity = -8
        if self.rect.y < 0:
            self.rect.y = 0
            self.y_velocity = 8
        if self.rect.y > GameObject.window_height - 20:
            self.rect.y = GameObject.window_height - 20
            self.y_velocity = -8

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def set_position(self, position):
        self.rect.x, self.rect.y = position

    def player_pos_change(self, save_point):
        if save_point == 1:
            self.rect.x = 100
            self.rect.y = 550
        if save_point == 1:
            self.rect.x = 843
            self.rect.y = 400
        if save_point == 2:
            self.rect.x = 663
            self.rect.y = 280
        

    # caps velocity upwards at 5; used when transitioning to higher levels
    def cap_upward_speed(self):
        self.y_velocity = max(self.y_velocity, 5)
