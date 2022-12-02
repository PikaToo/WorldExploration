import pygame
import sys
import random
import level
import mobs
from pygame.locals import *

# Game set up
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
window_width = 1200
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('World Exploration')
icon = pygame.Surface((20, 20))
pygame.display.set_icon(icon)

# initializing font for later use
pygame.font.init()
font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 20)

# lists of all platforms, bullets, enemies, and whether each boss is dead or alive.
platforms = []
bullets = []
enemies = []
explosions = []
boss_statuses = [True, True, True, True, True, True, True, True, True, True]
ability_statuses = [False, False, False, False, False]

world = level.level()
gold = 0

# current position on the map. starts at 0, 0, the top left.
world_y = 0
world_x = 0

save_point = (0, boss_statuses, ability_statuses, 0)   # point, bosses, abilities, gold, minimap

# TODO:
# cannon enemy
#
# add more enemies and levels
#   add more enemy AIs
#       remember it uses the built-in counter of the enemy
#   ensure normal enemy have a boss status (enemy[6]) of -1.
#   remember there are also only so many characters. numbers are reserved for bosses, so only letters left.
#       lowercase and uppercase should be different, though, so that opens up more.
#       different enemies can have the same AI.
#   have enemy counters start at -60 so there is a period of rest when entering a room.
#
# powerups
#   provide passive buffs (e.g. more health, more damage, etc.)
#       buffs + all effects are visible in pause menu
#   some are hidden
#   rocket jump
#   increased max health (also increase enemy damage to keep balance)
#   higher damage bullets
#   triple jump
#
# transport gates
#
# add some sort of boss door or indicator that the next screen is a boss fight.
#
# consider moving pausing and some functions into a separate script


class Platform(pygame.sprite.Sprite):
    # used to add a platform to the list of platforms.
    def __init__(self, pos, size, type):
        self.rect = pygame.Rect(pos[0], pos[1], size, size)
        platforms.append([self.rect, type])


class Bullet(object):
    # used to add a bullet to the list of bullets
    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, owner, size, gravity, damage):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        bullets.append([self.rect, x_velocity, y_velocity, owner, gravity, damage])


class Enemy(object):
    # used to add an enemy to the list of enemies
    def __init__(self, x_pos, y_pos, color, size, counter, enemy_AI, enemy_health, boss, other, damage):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        max_enemy_health = enemy_health
        x_velocity = y_velocity = 0
        enemies.append([self.rect, [x_velocity, y_velocity], counter, enemy_AI,
                        [enemy_health, max_enemy_health], color, boss, other, damage])


class Explosion(object):
    # used to add an enemy gold-death explosion to the list
    def __init__(self, x_pos, y_pos, size):
        if size <= 0:
            return
        if size > 1:
            self.rect = pygame.Rect(x_pos, y_pos, 2, 2)
            x_vel = random.randint(-size, size)
            y_vel = -8 + size/10
            explosions.append([self.rect, x_vel, y_vel])
            Explosion(x_pos, y_pos, size - 1)


def move_explosions():
    for explosion in explosions:
        explosion[2] += 0.3
        if explosion[1] > 0:
            explosion[1] -= 0.6
        if explosion[1] < 0:
            explosion[1] += 0.6
        explosion[0].y += explosion[2]
        explosion[0].x += explosion[1]

        explosion_particle_alive = True
        for platform in platforms:
            if explosion[0].colliderect(platform[0]) and explosion_particle_alive:
                explosions.remove(explosion)
                explosion_particle_alive = False

        if explosion_particle_alive:
            pygame.draw.rect(window, (255, 255, 0), explosion[0])


class Player(object):
    def __init__(self):
        # initial position
        self.rect = pygame.Rect(100, 550, 20, 20)

        self.x_velocity = 0  # used for dashing
        self.y_velocity = 0  # used for gravity and jumps

        # seeing if double jump has been used and how long the player has been off the ground for
        self.double_jump = False
        self.double_jump_counter = 0

        # values used for dodging
        self.dodge_counter = 0
        self.x_dir = 0

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

    def move(self, invincibility):  # movement inputs invincibility status solely for changing color upon hit
        key = pygame.key.get_pressed()

        # x-movement
        # first sets values to 0 in case no button is pressed
        x_movement = 0
        if key[K_d]:
            x_movement = 5
            self.x_dir = 25
        if key[K_a]:
            x_movement = -5
            self.x_dir = -25

        # dashing
        if key[K_SPACE] and self.dodge_counter >= 40 and ability_statuses[1]:
            self.x_velocity = self.x_dir
            self.dodge_counter = 0
        if self.dodge_counter < 40:
            self.dodge_counter += 1

        x_movement += self.x_velocity  # changing x by velocity
        # changing x
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
                elif self.double_jump and self.double_jump_counter > 5 and ability_statuses[0]:
                    self.y_velocity = -12
                    self.double_jump = False
        if key[K_w]:
            self.previous_w_value = True
        else:
            self.previous_w_value = False

        if not self.on_ground:                  # if not on the ground, gravity applies
            self.y_velocity += 0.6              # and double-jump counter starts
            self.double_jump_counter += 1

        if self.y_velocity > 20:           # terminal velocity
            self.y_velocity = 20
        if self.y_velocity < -20:
            self.y_velocity = -20

        self.move_linear(x_movement, 0, -50)
        self.move_linear(0, self.y_velocity, invincibility)

        if ability_statuses[2]:
            self.shoot()

    def shoot(self):
        # counting upwards until it reaches 20 where it stops.
        # doesn't need to stop, only doing so to avoid very large numbers
        if self.bullet_counter < 20:
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

    def move_linear(self, x, y, invincibility):
        global save_point
        self.rect.x += x  # move by x, which is the sum of dashing + regular movement

        self.on_ground = False  # assumes you are in free-fall
        self.rect.y += y  # moves you by velocity

        for platform in platforms:  # platform collision detection
            if platform[1] == "platform":
                if (self.rect.bottom == platform[0].top) and \
                    (self.rect.left in range (platform[0].left - self.rect.width, platform[0].right)):
                    self.on_ground = True
            if self.rect.colliderect(platform[0]):
                if platform[1] == "platform":
                    if x > 0:
                        self.rect.right = platform[0].left
                    if x < 0:
                        self.rect.left = platform[0].right

                    if y > 0:
                        self.rect.bottom = platform[0].top
                        self.on_ground = True  # if you are touching the ground, these 2 are set as true.
                        self.double_jump = True  # allows you to jump and resets double jump ability.
                        self.double_jump_counter = 0  # sets counter for double jump to 0, used to prevent
                        self.y_velocity = 0
                    if y < 0:  # both jumps from immediately occuring back-to-back.
                        self.rect.top = platform[0].bottom

                if platform[1] == "upgrade":  # if the platform was an upgrade token, calls another function
                    text1 = text2 = ""
                    if world_y == 2 and world_x == 1:
                        ability_statuses[0] = True
                        text1 = "Unlocked double jump."
                        text2 = "Press W while in the air to use."
                    if world_y == 3 and world_x == 0:
                        ability_statuses[1] = True
                        text1 = "Unlocked dash."
                        text2 = "Press space to use."
                    if world_y == 3 and world_x == 5:
                        ability_statuses[2] = True
                        text1 = "Unlocked blaster."
                        text2 = "Press arrow keys or click the mouse to use."
                    if world_y == 8 and world_x == 0:
                        ability_statuses[3] = True
                        text1 = "Health has been increased."
                        text2 = "You now have more health."

                    # getting a surface for the fade into black effect
                    s = pygame.Surface((1200, 600))  # making a surface to get a transparent rect
                    s.set_alpha(12)  # alpha level
                    s.fill((0, 0, 0))  # black

                    counter = 0
                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()

                        if counter < 50:  # first 50 ticks are on fading to black
                            window.blit(s, (0, 0))
                        if counter > 50:  # after 50 ticks, shows text.
                            window.blit(font.render(text1, False, (255, 255, 255)), (50, 200))
                            window.blit(small_font.render("Press P to leave this menu.", False, (255, 255, 255)),
                                        (50, 400))
                            window.blit(medium_font.render(text2, False, (255, 255, 255)), (50, 280))

                        key = pygame.key.get_pressed()  # exit through p
                        if key[K_p]:
                            break

                        fpsClock.tick(FPS)
                        pygame.display.update()
                        counter += 1
                if platform[1] == "load":
                    self.show_save = 100
                    if world_x == 0 and world_y == 8:
                        save_game(1)
                    if world_x == 2 and world_y == 7:
                        save_game(2)

        if invincibility > 0:  # if have i_frames, drawn a lighter blue.
            pygame.draw.rect(window, (100, 100, 255), self.rect)  # draws player
        elif invincibility != -50:
            pygame.draw.rect(window, (0, 0, 255), self.rect)  # draws player

    def check_for_new_stage(self, health):
        global world_x, world_y, boss_statuses
        if health > 0:
            if self.exit_status:  # only can change level if exits are open (i.e. bosses are dead)
                if self.rect.x < 10:  # moving by x
                    world_x -= 1
                    self.rect.x = window_width - 30
                if self.rect.x + 10 > window_width:
                    self.rect.x = 10
                    world_x += 1
                if self.rect.y < 10:  # moving by y
                    world_y -= 1
                    self.rect.y = window_height - 30
                if self.rect.y + 10 > window_height:
                    self.rect.y = 30
                    world_y += 1
                    if self.y_velocity > 5:         # preventing high gravity upon level switch
                        self.y_velocity = 5
            else:  # if exits are closed, shows text and prevents movement.
                if not 0 < self.rect.x < (window_width - 20) or not 0 < self.rect.y < (window_height - 20):
                    self.show_exit = 100
                if self.rect.x < 0:
                    self.rect.x = 0
                    self.x_velocity = 8
                if self.rect.x > window_width - 20:
                    self.rect.x = window_width - 20
                    self.x_velocity = -8
                if self.rect.y < 0:
                    self.rect.y = 0
                    self.y_velocity = 8
                if self.rect.y > window_height - 20:
                    self.rect.y = window_height - 20
                    self.y_velocity = -8
                # doesn't entirely block movement since this comes before the movement function in main(),
                # but it has to or else there will be problems with collision as this is the function that
                # sets the world level.

    def player_pos_change(self):
        if save_point[0] == 1:
            self.rect.x = 100
            self.rect.y = 550
        if save_point[0] == 1:
            self.rect.x = 843
            self.rect.y = 400
        if save_point[0] == 2:
            self.rect.x = 663
            self.rect.y = 280


player = Player()  # defining player here instead of main because it is used before the main loop.


def draw_health_bar(bar_position, bar_span, bar_percent, back_color, front_color):
    bar = pygame.Rect(bar_position[0], bar_position[1], bar_span[0], bar_span[1])
    current_bar = pygame.Rect(bar_position[0], bar_position[1], bar_span[0] * bar_percent, bar_span[1])
    pygame.draw.rect(window, back_color, bar)
    pygame.draw.rect(window, front_color, current_bar)


def draw_platforms(platform_list, wall_color):
    for platform in platform_list:
        if platform[1] == "platform":               # these 2 platforms are just drawn in respective colors
            pygame.draw.rect(window, wall_color, platform[0])
        if platform[1] == "load":
            pygame.draw.rect(window, (255, 100, 0), platform[0])
        if platform[1] == "upgrade":                # upgrade (unlock token) decides if it should exist
            # checks world location and if the ability is not unlocked before revealing self
            if world_y == 2 and world_x == 1 and not ability_statuses[0]:
                pygame.draw.rect(window, (200, 200, 0), platform[0])
            elif world_y == 3 and world_x == 0 and not ability_statuses[1]:
                pygame.draw.rect(window, (200, 200, 0), platform[0])
            elif world_y == 3 and world_x == 5 and not ability_statuses[2]:
                pygame.draw.rect(window, (200, 200, 0), platform[0])
            elif world_y == 8 and world_x == 0 and not ability_statuses[3]:
                pygame.draw.rect(window, (200, 200, 0), platform[0])
            else:
                platforms.remove(platform)


def save_game(point):
    global save_point
    save_point = (point, boss_statuses, ability_statuses, gold)


def load_game(save_data):
    # sets the load data and configures the world x/y and player abilities based on that.
    global world_y, world_x, boss_statuses, ability_statuses, gold
    if save_data[0] == 0:
        world_x = 0
        world_y = 0
    if save_data[0] == 1:
        world_x = 0
        world_y = 8
    if save_data[0] == 2:
        world_x = 2
        world_y = 7
    if save_data[0] == 99:
        world_x = 4
        world_y = 12
    boss_statuses = save_data[1]
    ability_statuses = save_data[2]
    gold = save_data[3]
    player.player_pos_change()


# function that runs when asked to input a load, only used after menu. put here for reducing menu function size.
def ask_for_load():
    global save_point
    name = ""
    # temp_code = 9901 1111 1111 1111 0000 0000
    # name = "990011111111111100000000"
    message = font.render("Enter your load code.", True, (255, 255, 255))
    valid_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()

            if evt.type == KEYDOWN:
                if str(evt.unicode) in valid_numbers and len(name) < 24:
                    name = name + str(evt.unicode)          # types numbers
                if evt.key == K_BACKSPACE:
                    name = name[:-1]                        # backspaces
                if evt.key == K_RETURN:
                    if len(name) != 24:                     # code must be 20 characters to work
                        name = ""
                        message = font.render("Invalid load code.", True, (255, 255, 255))
                    else:
                        # processes the save data
                        s_point = int(name[0] + name[1])                        # name[0 -> 1] used for save point.
                                                                                # 2 values
                        # initial values for the loading loop
                        s_ability_list = []
                        s_boss_list = []

                        i = 2
                        while i <= 19:
                            if i <= 11:
                                if int(name[i]) == 1:                   # name[2 -> 11] used for bosses
                                    s_boss_list.append(True)            # 10 values
                                else:
                                    s_boss_list.append(False)
                            elif i <= 19:                               # name[12 -> 19] used for abilities
                                if int(name[i]) == 1:                   # 8 values
                                    s_ability_list.append(True)
                                else:
                                    s_ability_list.append(False)
                            i += 1

                        s_gold = int(name[20] + name[21] + name[22] + name[23])     # name[20 - 23] used for gold
                                                                                    # 4 values
                        save_point = (s_point, s_boss_list, s_ability_list, s_gold)

                        return  # breaks loop

        # formatting the load code to make it more legible
        formatted_code = ""
        iteration = 0
        for character in name:
            iteration += 1
            formatted_code += character
            if iteration % 4 == 0:              # can't just check length of the formatted_code since it changes
                formatted_code += "  "

        # drawing everything
        window.fill((0, 0, 0))
        message_rect = message.get_rect()
        message_rect.x = 400
        message_rect.y = 200
        window.blit(message, message_rect)
        message_rect.x = 300
        message_rect.y = 250
        window.blit(font.render(formatted_code, True, (200, 200, 200)), message_rect)
        pygame.display.flip()


def main_menu():
    # getting locations of all buttons
    x_location = 340                                                # used to easily change their x later if needed
    new_rect = pygame.Rect(x_location, 500, 185, 50)
    load_rect = pygame.Rect(x_location + 300, 500, 185, 50)
    back_new_rect = pygame.Rect(x_location - 5, 495, 195, 60)
    back_load_rect = pygame.Rect(x_location + 295,  495, 195, 60)

    while True:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()
        mouse_x, mouse_y = pygame.mouse.get_pos()                   # getting mouse pos for collision checks later
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

        window.fill((0, 0, 0))

        load_back_color = new_back_color = (30, 30, 30)             # setting background color for both buttons

        if mouse_rect.colliderect(new_rect):                        # if button collides, changes back color
            new_back_color = (200, 200, 50)
            if pygame.mouse.get_pressed()[0]:                       # ends screen if new is clicked
                return
        if mouse_rect.colliderect(load_rect):                       # switches to load screen if load is clicked
            load_back_color = (200, 200, 50)
            if pygame.mouse.get_pressed()[0]:
                ask_for_load()
                return

        # drawing the back of the buttons
        pygame.draw.rect(window, new_back_color, back_new_rect)
        pygame.draw.rect(window, load_back_color, back_load_rect)

        # drawing the buttons
        pygame.draw.rect(window, (50, 50, 50), new_rect)
        pygame.draw.rect(window, (50, 50, 50), load_rect)

        # drawing the text on buttons
        window.blit(font.render(" New Game", True, (255, 255, 255)), new_rect)
        window.blit(font.render(" Load Game", True, (255, 255, 255)), load_rect)

        # game title
        large_font = pygame.font.SysFont('arial', 150)
        window.blit(large_font.render("World Explorer", True, (200, 200, 255)), pygame.Rect(50, 50, 195, 60))
        pygame.draw.rect(window, (0, 0, 255), pygame.Rect(950, 100, 100, 100))

        pygame.display.flip()


def main():
    global boss_statuses, enemies, platforms, bullets, explosions, gold
    # setting theme colors based on location, using a list where 1st two values are y-value range and 3rd is color
    background_color_palette = [
        [0, 5,  (0, 0, 0),     0, 4,   (100, 100, 100)],    # tutorial colors
        [6, 8,  (0, 10, 0),    5, 9,   (50, 60, 50)],       # grass colors
        [9, 12, (0, 0, 10),    10, 12, (50, 50, 60)]]       # ice colors
    # color values (pink) incase none was assigned.
    background_color = (255, 100, 100)
    wall_color = (255, 100, 100)

    # getting save file and loading
    main_menu()
    load_game(save_point)

    # initial values
    i_frames = 0
    previous_stage = 0
    holding_escape = False
    damage_counter = [0, 0]
    health = 5
    if ability_statuses[3]:
        health = 8
    fade_counter = 0                            # these 3 are fading stuff initial values
    fade_screen = pygame.Surface((1200, 600))   # making a surface to get a transparent rect
    fade_screen.fill((0, 0, 0))                 # making surface black

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # iterating through the color list defined earlier.
        for potential_value in background_color_palette:
            if potential_value[0] <= world_y <= potential_value[1]:     # first half is background color
                background_color = potential_value[2]
            if potential_value[3] <= world_y <= potential_value[4]:     # second half is wall color
                wall_color = potential_value[5]
        window.fill(background_color)

        # setting total health baesd on abilities
        total_health = 5
        if ability_statuses[3]:
            total_health = 8
        if health > total_health:
            health = total_health

        # checking to see if player has changed stages, also seeing if they died
        player.check_for_new_stage(health)

        # changing everything if the player died
        if health <= 0:
            health = total_health
            load_game(save_point)

        # building the stage
        if not (world_y + 1) > len(world) and not (world_x + 1) > len(world[0]):    # making sure level exists
            stage = world[world_y][world_x]
        if stage != previous_stage:
            platforms = []
            enemies = []
            bullets = []
            explosions = []
            wall_x = wall_y = 0
            fade_counter = 10

            for row in stage:
                for value in row:
                    if value == "W":
                        Platform((wall_x, wall_y), 30, "platform")
                    if value == "U":
                        Platform((wall_x + 5, wall_y + 5), 15, "upgrade")
                    if value == "L":
                        Platform((wall_x + 5, wall_y + 5), 15, "load")
                    # Enemy(x_pos, y_pos, color, size, counter, enemy_AI, enemy_health, boss, other, damage)
                    if value == "0" and boss_statuses[0]:
                        Enemy(wall_x, wall_y, (255, 0, 0), 20, -60, "Target", 8, 0, False, 1)
                    if value == "1" and boss_statuses[1]:
                        Enemy(wall_x, wall_y, (100, 200, 100), 25, -60, "Harmer", 20, 1, False, 1)
                    if value == "F":
                        Enemy(wall_x, wall_y, (100, 50, 0), 20, -60, "Follower", 5, -1, False, 1)
                    if value == "S":
                        Enemy(wall_x, wall_y, (100, 100, 0), 30, -60, "Shooter", 3, -1, False, 1)
                    if value == "B":
                        Enemy(wall_x, wall_y, (255, 200, 80), 25, -60, "Bird", 3, -1, False, 1)
                    if value == "I":
                        Enemy(wall_x, wall_y, (200, 200, 255), 20, -60, "Icey Follower", 8, -1, False, 1)
                    if value == "C":
                        Enemy(wall_x, wall_y, (150, 150, 255), 30, -60, "Cold Bird", 6, -1, False, 1)
                    if value == "P":
                        Enemy(wall_x, wall_y, (40, 40, 40), 40, -60, "Pewer (Cannon)", 15, -1, False, 2)
                    wall_x += 30
                wall_y += 30
                wall_x = 0

        previous_stage = stage  # setting this for the next frame to use

        # platform stuff. done elsewhere.
        draw_platforms(platforms, wall_color)

        # enemy stuff
        player.exit_status = True
        for enemy in enemies:
            mob = mobs.Mob(enemy)                    # add information to the function for processing

            if mob.healths[0] <= 0:                            # if death is true, does some things
                gold += mob.gold
                Explosion(enemy[0].x + (enemy[0].width / 2), enemy[0].y + (enemy[0].height / 2), mob.gold + 1)
                if mob.healths != -1:
                    boss_statuses[mob.boss_status] = False
                enemies.remove(enemy)

            else:                               # if death isn't true, does everything else
                if enemy[6] != -1:
                    if boss_statuses[enemy[6]]:   # checks to see if the boss status of the enemy is true
                        player.exit_status = False

                mob.movement(player.rect, platforms)  # moves enemies, gives them player and platform location
                if mob.fired:                               # if the mob fired, fires with info taken from them
                    Bullet(mob.fire_info[0], mob.fire_info[1], mob.fire_info[2], mob.fire_info[3], mob.fire_info[4],
                           mob.fire_info[5], mob.fire_info[6], enemy[8])

                # player-enemy collision
                if player.rect.colliderect(enemy[0]) and not i_frames > 0:
                    damage_counter = [20, enemy[8]]
                    i_frames = 120

                # I don't know why, but for some reason after it gets processed, the respective enemy in ememies
                # seems to get updated, too, despite me not doing so. It's helpful, but still anomalous.
                # ... except the counter and "other" value which I have to update here.
                enemy[2] = mob.counter
                enemy[7] = mob.other

                # drawing
                draw_health_bar(mob.bar[0], mob.bar[1], mob.bar[2], mob.bar[3], mob.bar[4])
                pygame.draw.rect(window, enemy[5], enemy[0])

        # all bullet stuff happens here
        for bullet in bullets:
            dead = False  # bullet set to be alive
            bullet[0].x += bullet[1]  # change bullet x pos by x velocity
            bullet[0].y += bullet[2]  # change bullet y pos by y velocity
            bullet[2] = bullet[2] + bullet[4]  # change y velocity by y acceleration

            # collision with walls and also for off-screen
            for platform in platforms:
                if bullet[0].colliderect(platform[0]):
                    dead = True
            if not 0 < bullet[0].y < window_height + 10 or not 0 < bullet[0].x < window_width + 10:
                dead = True

            # if it was shot by the player, collision is done to check to see if it hit the enemy
            if bullet[3] == "player":
                for enemy in enemies:
                    if bullet[0].colliderect(enemy[0]):
                        enemy[4][0] -= bullet[5] + (gold/100)
                        dead = True

            # if it was shot by the enemy, collision sees if it hit the player
            if not dead and bullet[3] == "enemy":
                if bullet[0].colliderect(player.rect) and not i_frames > 0:
                    dead = True
                    damage_counter = [20, bullet[5]]
                    i_frames = 120  # if hit, get invincibility frames

            if dead:
                bullets.remove(bullet)
            else:
                pygame.draw.rect(window, (255, 255, 255), bullet[0])

        # movement
        move_explosions()
        player.move(i_frames)       # i_frames inputted to player to change color

        # reduction of invincibility frames
        if i_frames > 0:
            i_frames -= 1

        # rumble and health decrease
        bar_rumble = 0
        if damage_counter[0] > 0:                              # ticking counter down, taking damage
            damage_counter[0] -= 1
            bar_rumble = random.randint(-3, 3)
        if damage_counter[0] == 1:                             # removes health after rumble
            health -= damage_counter[1]
            damage_counter[1] = 0
        # rumble and health increase
        if damage_counter[1] < 0:                              # ticking counter up, restoring health
            damage_counter[1] += 1
            if health != total_health:
                bar_rumble = random.randint(-2, 2)
        if damage_counter[1] == -1:                            # restores health after rumble
            health = total_health

        # showing UI
        i = 0
        while i < total_health:                                         # health circles
            i += 1
            individual_rumble = bar_rumble * random.randint(-1, 1)      # rumble, off-sets all values
            x_pos = i*25 + 40 + individual_rumble
            y_pos = 585 + individual_rumble
            pygame.draw.circle(window, (100, 50, 50), (x_pos, y_pos), 12)       # background circle

            hearts_losing_life = health - damage_counter[1] + 1

            # inner circle varies.
            if i <= health:                                             # only draws if have equal or more health
                if damage_counter[0] > 0 and i >= hearts_losing_life:   # shrinking animation if taking damage
                    pygame.draw.circle(window, (255, 50, 50), (x_pos, y_pos), 0.5 * damage_counter[0])
                else:
                    pygame.draw.circle(window, (255, 80, 80), (x_pos, y_pos), 10)
            if i > health and damage_counter[0] < 0:                       # growing animation if restoring health
                print("restoring")
                pygame.draw.circle(window, (255, 50, 50), (x_pos, y_pos), 10 - (0.5 * -damage_counter[0]))

        level = (chr(65 + world_x) + str('%02d' % (world_y + 1)))           # getting level value from numbers
        window.blit(small_font.render(level, False, (255, 255, 255)), (1171, 575))          # levels
        window.blit(small_font.render((str(gold)+"g"), False, (255, 255, 50)), (5, 575))    # gold

        # pausing
        key = pygame.key.get_pressed()
        valid_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]      # used for minimap

        # map later
        if key[K_ESCAPE] and not holding_escape:
            holding_escape = True
            fade_counter = 0                        # reusing fade values here
            fade_screen.set_alpha(20)
            while True:
                key = pygame.key.get_pressed()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                # exiting
                if key[K_ESCAPE] and not holding_escape:
                    holding_escape = True
                    fade_counter = 6  # after leaving, fades back in
                    break
                if not key[K_ESCAPE]:
                    holding_escape = False

                # fade
                while fade_counter < 30:
                    fade_screen.set_alpha(fade_counter * 20)
                    fade_counter += 1

                window.blit(fade_screen, (0, 0))
                window.blit(font.render("Paused.", False, (255, 255, 255)), (50, 200))

                # drawing minimap
                load_zones = []
                boss_zones = []
                map_x = 300
                map_y = 100
                # massive for loop like the level creation, but with two more for the whole world.
                for lev_row in world:
                    for lev_value in lev_row:
                        for row in lev_value:
                            for value in row:
                                if value == "W":                                # platforms are drawn
                                    block = pygame.Rect(map_x, map_y, 1, 1)     # on-the-spot
                                    pygame.draw.rect(window, (150, 150, 150), block)
                                if value == "L" or value in valid_numbers:
                                    x_middle = 16 + map_x - ((map_x - 300) % 40)  # loads/bosses added to list
                                    y_middle = 6 + map_y - ((map_y - 100) % 20)
                                    block = pygame.Rect(x_middle, y_middle, 8, 8)
                                    if value == "L":
                                        load_zones.append(block)
                                    else:
                                        if boss_statuses[int(value)]:  # boss only added if alive
                                            boss_zones.append(block)
                                map_x += 1
                            map_x -= 40
                            map_y += 1
                        map_y -= 20
                        map_x += 40
                    map_y += 20
                    map_x = 300

                for load in load_zones:                         # loads/bosses drawn later (after walls) to be on top
                    pygame.draw.rect(window, (255, 100, 0), load)
                for boss in boss_zones:
                    pygame.draw.rect(window, (255, 0, 0), boss)
                player_loc = pygame.Rect(world_x * 40 + 315, world_y * 20 + 105, 10, 10)    # getting player location
                pygame.draw.rect(window, (0, 0, 255), player_loc)                           # player drawn last

                map_x = 10  # showing abilities unlocked
                map_y = 10
                for ability in ability_statuses:
                    ability_rect = pygame.Rect(map_x, map_y, 30, 30)
                    pygame.draw.rect(window, (100, 50, 50), ability_rect)
                    if ability:
                        ability_rect = pygame.Rect(map_x + 5, map_y + 5, 20, 20)
                        pygame.draw.rect(window, (200, 100, 100), ability_rect)
                    map_x += 50

                pygame.display.update()

        if not key[K_ESCAPE]:
            holding_escape = False

        # screen fade
        fade_screen.set_alpha(0)
        if fade_counter > 0:
            fade_screen.set_alpha(fade_counter * 40)
            fade_counter -= 1
        window.blit(fade_screen, (0, 0))

        # grabs values from a ticker in player which get set to 100 upon touching something.
        # used for persistent text boxes, such as after touching a save point.
        if player.show_save == 100:
            damage_counter = [-20, 0]
        if player.show_save > 0:
            player.show_save -= 1
            text = medium_font.render("Your progress has been saved.", False, (255, 255, 100))
            text.set_alpha(player.show_save * 10)
            window.blit(text, (700, 566))
        if player.show_exit > 0:
            player.show_exit -= 1
            text = medium_font.render("Exit is closed until the boss is defeated.", False, (255, 100, 100))
            text.set_alpha(player.show_exit * 10)
            window.blit(text, (700, 566))

        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
