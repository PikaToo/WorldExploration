import pygame
import sys
import level
from pygame.locals import *

# importing objects
from abilityStatusList import AbilityStatusList
from persistentTextBox import PersistentTextBox
from gameObject import GameObject
from enemy import Enemy
from explosion import Explosion
from bullet import Bullet
from platformManager import Platform
from player import Player
from fadeManager import FadeManager
from healthManager import HealthManager
from pauseManager import PauseManager
from worldManager import WorldManager
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

save_point = (0, boss_statuses, ability_statuses, 0)   # point, bosses, abilities, gold, minimap

# TODO:
# fix rest of OOP
#
# save point(s) near tutorial area
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

def save_game(point):
    global save_point
    save_point = (point, boss_statuses, ability_statuses, gold)

def load_game(save_data, player):
    # sets the load data and configures the world x/y and player abilities based on that.
    global boss_statuses, ability_statuses, gold
    if save_data[0] == 0:
        GameObject.world_x = 0
        GameObject.world_y = 0
    if save_data[0] == 1:
        GameObject.world_x = 0
        GameObject.world_y = 8
    if save_data[0] == 2:
        GameObject.world_x = 2
        GameObject.world_y = 7
    if save_data[0] == 97:
        GameObject.world_x = 5
        GameObject.world_y = 3
    if save_data[0] == 98:
        GameObject.world_x = 0
        GameObject.world_y = 8
    if save_data[0] == 99:
        GameObject.world_x = 4
        GameObject.world_y = 11
    boss_statuses = save_data[1]
    ability_statuses = save_data[2]
    gold = save_data[3]
    player.player_pos_change(save_data[0])

def main():
    # initializing single objects
    fadeManager = FadeManager()
    pauseManager = PauseManager()
    healthManager = HealthManager()
    worldManager = WorldManager()
    fpsDisplay = FpsDisplay()
    player = Player()
    menuManager = MenuManager()

    save_text = PersistentTextBox("Your progress has been saved.", medium_font, (255, 255, 100))
    exit_text = PersistentTextBox("Exit is closed until the boss is defeated.", medium_font, (255, 100, 100)) 

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


    global boss_statuses, gold
    # setting theme colors based on location, using a list where 1st two values are y-value range and 3rd is color
    background_color_palette = [
        [0, 5,  (0, 0, 0),     0, 4,   (100, 100, 100)],    # tutorial colors
        [6, 8,  (0, 10, 0),    5, 9,   (50, 60, 50)],       # grass colors
        [9, 12, (0, 0, 10),    10, 12, (50, 50, 60)]]       # ice colors
    # color values (pink) incase none was assigned.
    background_color = (255, 100, 100)

    # update after loading
    GameObject.set_ability_statuses(ability_statuses)
    GameObject.set_boss_statuses(boss_statuses)
    
    # initial values
    worldManager.create_level(world)
    
    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # iterating through the color list defined earlier.
        for potential_value in background_color_palette:
            if potential_value[0] <= GameObject.world_y <= potential_value[1]:     # first half is background color
                background_color = potential_value[2]
            if potential_value[3] <= GameObject.world_y <= potential_value[4]:     # second half is wall color
                Platform.wall_color = potential_value[5]
        window.fill(background_color)

        # pause screen / pausing
        key = pygame.key.get_pressed()  # exit through escape
        pauseManager.check_for_pause(key[K_ESCAPE], Platform.platforms, player)
        if pauseManager.manually_paused or pauseManager.upgrader_paused:
            
            # fading in
            fadeManager.darken_fade()
            fadeManager.display()

            # displaying pause screen
            pauseManager.display(world, font, medium_font, small_font)

            # don't do anything else- we're done here (continue causes the pause effect)
            fpsClock.tick(FPS)
            pygame.display.update()
            continue
    
        # if player alive, check if need to swap stages
        if healthManager.current_health > 0:
            worldManager.update_world_coordinates(player)

        # if the player is dead, reloads
        else:
            healthManager.reset_health()
            load_game(save_point, player)

        # building the stage
        if worldManager.world_changed:

            # fade to black
            fadeManager.set_darkest_fade()
            
            # first delete all entities in current stage, then make new stage
            worldManager.empty_level()
            worldManager.create_level(world)

        # enemy stuff
        player.exit_status = True
        for enemy in Enemy.enemies:
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
                if player.rect.colliderect(enemy.rect):
                    healthManager.take_damage(enemy.damage)

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
                for enemy in Enemy.enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.current_health -= bullet.damage + (gold/100)
                        will_die = True

            # if bullet shot by an enemy, checks collision against player
            if bullet.owner == "enemy":
                if bullet.rect.colliderect(player.rect):
                    healthManager.take_damage(bullet.damage)
                    will_die = True

            if will_die:
                bullet.delete()

        # movement and updating
        for explosion in Explosion.explosions:
            explosion.move()
        player.update()
        healthManager.update()

        # if exits are closed, shows text and prevents movement if player tries to leave bounds
        if not player.exit_status:
            if not player.in_bounds():
                exit_text.enable()
            player.stop_escape()

        # bad that player save like this TODO: fix
        if player.save != 0:
            save_game(player.save)
            player.save = 0
            save_text.enable()
            healthManager.reset_health()
        player.save_point = save_point
        
        # drawing entities
        for platform in Platform.platforms:
            platform.draw()
        for bullet in Bullet.bullets:
            bullet.draw()
        for explosion in Explosion.explosions:
            explosion.draw()
        for enemy in Enemy.enemies:
            enemy.draw()
        player.draw()
        healthManager.display_overlay()
        save_text.display()
        exit_text.display()
        
        level = (chr(65 + GameObject.world_x) + str('%02d' % (GameObject.world_y + 1)))           # getting level value from numbers
        GameObject.window.blit(small_font.render(level, False, (255, 255, 255)), (1171, 575))          # levels
        GameObject.window.blit(small_font.render((str(gold)+"g"), False, (255, 255, 50)), (5, 575))    # gold


        # DEBUG: shows  FPS if backspace is pressed
        fpsDisplay.display(fpsClock, font)

        # default screen fade: try to clear up the screen
        fadeManager.lighten_fade()
        fadeManager.display()
 
        # every frame, update static variables (temp)
        GameObject.set_ability_statuses(ability_statuses)
        GameObject.set_boss_statuses(boss_statuses)

        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
