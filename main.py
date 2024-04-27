import pygame
import sys
import random
import level
from pygame.locals import *

# importing objects
from abilityStatusList import AbilityStatusList
from gameObject import GameObject
from entity import Entity
from enemy import Enemy
from explosion import Explosion
from bullet import Bullet
from platform import Platform
from player import Player
from fader import Fader
from pauser import Pauser
from upgrader import Upgrader
from worldMover import WorldMover
from fpsDisplay import FpsDisplay
from menuManager import MenuManager

SAVE_FILE = "save_data/save_data.txt"

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

# lists of whether each boss is dead or alive.
boss_statuses = [True, True, True, True, True, True, True, True, True, True]
ability_statuses = AbilityStatusList()

world = level.level()
gold = 0

# current position on the map. starts at 0, 0, the top left.
world_y = 0
world_x = 0

save_point = (0, boss_statuses, ability_statuses, 0)   # point, bosses, abilities, gold, minimap

# TODO:
# fix rest of OOP
#  fix fade-in from upgrade
#
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

# passing information to entity
GameObject.set_window(window)
GameObject.set_window_size(window_width, window_height)
GameObject.set_world_coordinates(world_x, world_y)

def save_game(point):
    global save_point
    save_point = (point, boss_statuses, ability_statuses, gold)

def load_game(save_data, player):
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
    if save_data[0] == 98:
        world_x = 0
        world_y = 8
    if save_data[0] == 99:
        world_x = 4
        world_y = 11
    boss_statuses = save_data[1]
    ability_statuses = save_data[2]
    gold = save_data[3]
    player.player_pos_change(save_data[0])

def main():
    # initializing single objects
    fader = Fader()
    pauser = Pauser()
    upgrader = Upgrader()
    worldMover = WorldMover()
    fpsDisplay = FpsDisplay()
    player = Player()
    menuManager = MenuManager()

    # menu loop
    while True:
        events = pygame.event.get()     # we need to pass events to the menu so we store
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        menuManager.display(events, font)

        if menuManager.load_data() != None:
            load_game(menuManager.load_data(), player)
            break
        
        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()

    global boss_statuses, gold, world_x, world_y
    # setting theme colors based on location, using a list where 1st two values are y-value range and 3rd is color
    background_color_palette = [
        [0, 5,  (0, 0, 0),     0, 4,   (100, 100, 100)],    # tutorial colors
        [6, 8,  (0, 10, 0),    5, 9,   (50, 60, 50)],       # grass colors
        [9, 12, (0, 0, 10),    10, 12, (50, 50, 60)]]       # ice colors
    # color values (pink) incase none was assigned.
    background_color = (255, 100, 100)

    # initial values
    previous_stage = 0
    damage_counter = [0, 0]
    
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
                Platform.wall_color = potential_value[5]
        window.fill(background_color)

        key = pygame.key.get_pressed()  # exit through escape
        # pause screen / pausing
        pauser.check_for_pause(key[K_ESCAPE])
        if pauser.paused:
            # fading in
            fader.darken_fade()
            fader.display()

            # displaying pause screen with its world minimap
            pauser.display(world, font)

            # don't do anything else- we're done here (paused)
            fpsClock.tick(FPS)
            pygame.display.update()
            continue
        
        # player upgrade collision
        for platform in Platform.platforms:
            if platform.type == "upgrade" and player.rect.colliderect(platform.rect):  # if the platform was an upgrade token, calls another function
                upgrader.enable_menu()
        
        if upgrader.showing_menu():
            fader.darken_fade()
            upgrader.display(font, medium_font, small_font)

            # exit by pressing p
            if key[K_p]:
                upgrader.disable_menu()

            else:
                # don't do anything else- we're done here (paused)
                fpsClock.tick(FPS)
                pygame.display.update()
                continue
    
        # setting total health player based on abilities
        player.set_max_health()

        # if player alive, check if need to swap stages
        if player.current_health > 0:
            worldMover.update_world_coordinates(player)

        # if the player is dead, reloads
        else:
            player.reset_health()
            load_game(save_point)

        # building the stage
        if not (world_y + 1) > len(world) and not (world_x + 1) > len(world[0]):    # making sure level exists
            stage = world[world_y][world_x]
        if stage != previous_stage:
            # TODO: convert these to static methods
            Platform.platforms = []
            Entity.enemies = []
            Bullet.bullets = []
            Explosion.explosions = []
            wall_x = wall_y = 0

            fader.set_darkest_fade()

            for row in stage:
                for value in row:
                    if value == "W":
                        Platform(wall_x, wall_y, 30, "platform")
                    if value == "U":
                        Platform(wall_x + 5, wall_y + 5, 15, "upgrade")
                    if value == "L":
                        Platform(wall_x + 5, wall_y + 5, 15, "load")
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

        # every frame, update static variables (temp)
        GameObject.set_world_coordinates(world_x, world_y)
        GameObject.set_ability_statuses(ability_statuses)
        GameObject.set_boss_statuses(boss_statuses)

        previous_stage = stage  # setting this for the next frame to use
        
        # enemy stuff
        player.exit_status = True
        for enemy in Entity.enemies:
            if enemy.current_health <= 0:                            # if death is true, does some things
                gold += enemy.gold
                Explosion(enemy.rect.x + (enemy.rect.width / 2), enemy.rect.y + (enemy.rect.height / 2), enemy.gold + 1)
                if enemy.boss != -1:
                    boss_statuses[enemy.boss] = False
                enemy.delete()

            else:                               # if death isn't true, does everything else
                if enemy.boss != -1:
                    if boss_statuses[enemy.boss]:   # checks to see if the boss status of the enemy is true
                        player.exit_status = False

                enemy.move(player.rect, Platform.platforms)  # moves enemies, gives them player location

                # player-enemy collision
                if player.rect.colliderect(enemy.rect) and player.has_no_i_frames():
                    damage_counter = [20, enemy.damage]
                    player.give_i_frames()

                # drawing
                enemy.draw_health_bar()

        # all bullet stuff happens here
        for bullet in Bullet.bullets:
            will_die = False
            bullet.move_self()
            
            # checking collision with walls and also for off-screen to see if bullet should live
            if (bullet.colliding_with_platforms() or not bullet.in_bounds()):
                will_die = True

            # if bullet shot by the player, checks collision againt enemies
            if bullet.owner == "player":
                for enemy in Entity.enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.current_health -= bullet.damage + (gold/100)
                        will_die = True

            # if bullet shot by an enemy, checks collision against player
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(player.rect) and player.has_no_i_frames():
                    damage_counter = [20, bullet.damage]
                    player.give_i_frames()
                    will_die = True

            if will_die:
                bullet.delete()

        # movement
        for explosion in Explosion.explosions:
            explosion.move()
        player.move()  

        # if exits are closed, shows text and prevents movement if player tries to leave bounds
        if not player.exit_status:              
            if not player.in_bounds():
                player.show_exit_warning()
            player.stop_escape()

        # bad that player save like this TODO: fix
        if player.save != 0:
            save_game(player.save)
            player.save = 0
        player.save_point = save_point
        
        # drawing entities
        for platform in Platform.platforms:
            platform.draw()
        for bullet in Bullet.bullets:
            bullet.draw()
        for explosion in Explosion.explosions:
            explosion.draw()
        for enemy in Entity.enemies:
            enemy.draw()
        player.draw()

        # rumble and health decrease
        bar_rumble = 0
        if damage_counter[1] > 0:                              # ticking counter down, taking damage
            damage_counter[0] -= 1
            bar_rumble = random.randint(-3, 3)
            if damage_counter[0] == 0:                             # removes health after rumble
                player.current_health -= damage_counter[1]
                damage_counter[1] = 0
        # rumble and health increase
        if damage_counter[1] < 0:                              # ticking counter up, restoring health
            damage_counter[0] -= 1
            bar_rumble = random.randint(-2, 2)
            if damage_counter[0] == 0:                            # restores health after rumble
                player.current_health = player.max_health
                damage_counter[1] = 0

        # showing UI
        i = 0
        while i < player.max_health:                                         # health circles
            i += 1
            individual_rumble = bar_rumble * random.randint(-1, 1)      # rumble, off-sets all values
            x_pos = i*25 + 40
            y_pos = 585
            x_pos_rumble = x_pos + individual_rumble
            y_pos_rumble = y_pos + individual_rumble
            pygame.draw.circle(window, (100, 50, 50), (x_pos, y_pos), 12)       # background circle

            hearts_losing_life = player.current_health - damage_counter[1] + 1
            
            # inner circle varies.
            if i <= player.current_health:                                             # only draws if have equal or more health
                if damage_counter[0] > 0 and i >= hearts_losing_life:   # shrinking animation if taking damage
                    pygame.draw.circle(window, (255, 50, 50), (x_pos_rumble, y_pos_rumble), 0.5 * damage_counter[0])
                else:
                    pygame.draw.circle(window, (255, 80, 80), (x_pos_rumble, y_pos_rumble), 10)
            if i > player.current_health and damage_counter[1] < 0:                       # growing animation if restoring health
                pygame.draw.circle(window, (255, 50, 50), (x_pos, y_pos), 10 - (0.5 * damage_counter[0]))

        level = (chr(65 + world_x) + str('%02d' % (world_y + 1)))           # getting level value from numbers
        window.blit(small_font.render(level, False, (255, 255, 255)), (1171, 575))          # levels
        window.blit(small_font.render((str(gold)+"g"), False, (255, 255, 50)), (5, 575))    # gold

        # DEBUG: shows  FPS if backspace is pressed
        fpsDisplay.display(fpsClock, font)

        # default screen fade: try to clear up the screen
        fader.lighten_fade()
        fader.display()

        # grabs values from a ticker in player which get set to 100 upon touching something.
        # used for persistent text boxes, such as after touching a save point.
        if player.just_saved():
            damage_counter = [20, -1]  # healing player by dealing negative damage
        if player.showing_saved_text():
            player.reduce_save_timer()
            text = medium_font.render("Your progress has been saved.", False, (255, 255, 100))
            text.set_alpha(player.show_save * 10)
            window.blit(text, (700, 566))
        if player.showing_exit_warning():
            player.reduce_exit_warning_timer()
            text = medium_font.render("Exit is closed until the boss is defeated.", False, (255, 100, 100))
            text.set_alpha(player.show_exit * 10)
            window.blit(text, (700, 566))

        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
