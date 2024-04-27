import pygame
from pygame.locals import *
from entity import GameObject       # players are entities
from bullet import Bullet       # player can make bullets
from platformManager import Platform   # player needs to know platform locations

class Player(GameObject):
    def __init__(self):
        # initial position
        self.rect = pygame.Rect(100, 550, 20, 20)

        # velocities
        self.x_velocity = 0
        self.y_velocity = 0

        # initial player health
        self.max_health = 8 if GameObject.ability_statuses.health_increase else 5 
        self.current_health = self.max_health

        # player abilities
        self.unlocked_double_jump = False
        self.unlocked_dash = False
        self.unlocked_bullets = False
        self.unlocked_higher_health = False

        # invincibility frames
        self.i_frames = 0
        
        # seeing if double jump has been used and how long the player has been off the ground for
        self.double_jump = False
        self.double_jump_counter = 0    # frames since first jump

        # values used for dodging
        self.dodge_counter = 0
        self.x_dir = 0           # tracks last direction faced

        # cooldown for bullets
        self.bullet_counter = 0

        # counters for showing save + exit screen
        self.show_save = 0
        self.show_exit = 0

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

        # updates i_frames
        if self.i_frames > 0:
            self.i_frames -= 1

        # ensures player health is correct and caps current to not be greater than max
        self.max_health = 8 if GameObject.ability_statuses.health_increase else 5
        self.current_health = min(self.current_health, self.max_health)

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
                    self.y_velocity = -12
                elif self.double_jump and self.double_jump_counter > 5 and GameObject.ability_statuses.double_jump:
                    self.y_velocity = -12
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
                    self.show_saved_text()
                    if GameObject.world_x == 0 and GameObject.world_y == 8:
                        self.save = 1
                    if GameObject.world_x == 2 and GameObject.world_y == 7:
                        self.save = 2


    # called by main if the player is trying to leave the world bounds when not allowed
    def stop_escape(self):
        if not 0 < self.rect.x < (GameObject.window_width - 20) or not 0 < self.rect.y < (GameObject.window_height - 20):
            self.show_exit_warning()
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
    

    # gives 2 seconds of invincibility
    def give_i_frames(self):
        self.i_frames = 120
    
    # checks if has invincibility
    def has_no_i_frames(self):
        return self.i_frames <= 0


    # caps velocity upwards at 5; used when transitioning to higher levels
    def cap_upward_speed(self):
        self.y_velocity = max(self.y_velocity, 5)
    
    def reset_health(self):
        self.current_health = self.max_health


    # sets the exit status counter back up to max
    def show_exit_warning(self):
        self.exit_status = 100

    # decrements the exit status counter by 1
    def reduce_exit_warning_timer(self):
        self.exit_status -= 1
    
    # tells if the exit timer has finished counting
    def showing_exit_warning(self):
        return (self.exit_status > 0)


    # sets the save status counter back up to max
    def show_saved_text(self):
        self.show_save = 100

    # decrements the save status counter by 1
    def reduce_save_timer(self):
        self.show_save -= 1
    
    # tells if the save timer has finished counting
    def showing_saved_text(self):
        return (self.show_save > 0)

    # tells if the player has just saved
    def just_saved(self):
        return (self.show_save == 100)


    def draw(self):
        if self.i_frames > 0:  # if player has i_frames, draw a lighter blue.
            pygame.draw.rect(GameObject.window, (100, 100, 255), self.rect)
        elif self.i_frames != -50:
            pygame.draw.rect(GameObject.window, (0, 0, 255), self.rect)