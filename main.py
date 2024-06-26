import pygame
import sys
import level
from pygame.locals import *

# importing objects
from abstract_classes.gameObject import GameObject
from abstract_classes.enemy import Enemy
from explosion import Explosion
from bullet import Bullet
from abstract_classes.platforms import Platform
from player import Player
from managers.fadeManager import FadeManager
from managers.healthManager import HealthManager
from managers.pauseManager import PauseManager
from managers.worldManager import WorldManager
from managers.menuManager import MenuManager
from managers.goldManager import GoldManager
from managers.uiManager import UiManager
from managers.saveManager import SaveManager

# SAVE_FILE = "save_data/save_data.txt"

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

world = level.level()

# TODO: little circle particles once no longer invincible 
# TODO: make it so player loads to desired load code position 
# TODO: bosses unique health bars 
# TODO: fix enemies being able to jump you immediately 
# TODO: better saving system
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

def main():
    # initializing single objects
    fadeManager = FadeManager()
    pauseManager = PauseManager()
    healthManager = HealthManager()
    worldManager = WorldManager()
    menuManager = MenuManager()
    goldManager = GoldManager()
    saveManager = SaveManager()
    uiManager = UiManager(healthManager, goldManager)
    player = Player()

    # menu loop
    while True:
        events = pygame.event.get()     # we need to pass events to the menu so we store
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        menuManager.display(events)

        if menuManager.load_code() != None:
            saveManager.load_from_code(menuManager.load_code(), player) 
            Platform.update_color()
            worldManager.create_stage(player, world)
            break
        
        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()
    
    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
         
        # pause screen / pausing
        key = pygame.key.get_pressed()  # exit through escape
        pauseManager.check_for_pause(key[K_ESCAPE], player)
        if pauseManager.manually_paused or pauseManager.upgrader_paused:
            
            # fading in
            fadeManager.darken_fade()
            fadeManager.display()

            # displaying pause screen
            pauseManager.display(world)

            # don't do anything else- we're done here (continue causes the pause effect)
            fpsClock.tick(FPS)
            pygame.display.update()
            continue
        
        # if player alive, check if need to swap stages
        if healthManager.current_health > 0:
            worldManager.update_world_coordinates(player)

        # if the player is dead, reloads
        else:
            fadeManager.set_darkest_fade()
            healthManager.reset_health()
            saveManager.load_data(player)
            worldManager.build_new_stage(player, world)

        # building the stage
        if worldManager.world_changed:
            fadeManager.set_darkest_fade()
            worldManager.build_new_stage(player, world)

        # enemy stuff
        for enemy in Enemy.enemies:
            if enemy.current_health <= 0:                            # if death is true, does some things
                goldManager.gain_gold(enemy.gold)
                Explosion(enemy.rect.x + (enemy.rect.width / 2), enemy.rect.y + (enemy.rect.height / 2), enemy.gold + 1)
                enemy.delete()

            else:                               # if death isn't true, does everything else
                enemy.move()                    # moves enemies, gives them player location

                # player-enemy collision
                if player.rect.colliderect(enemy.rect):
                    healthManager.take_damage(enemy.damage)

        # all bullet stuff happens here
        for bullet in Bullet.bullets:
            will_die = False
            bullet.move_self()
            
            # checking collision with walls and also for off-screen to see if bullet should live
            if (bullet.colliding_with_walls() or not bullet.in_bounds()):
                will_die = True

            # if bullet shot by the player, checks collision againt enemies
            if bullet.owner == "player":
                for enemy in Enemy.enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemy.current_health -= bullet.damage + (goldManager.current_gold()/100)
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
        healthManager.update(player)

        # if exits are closed, shows text and prevents movement if player tries to leave bounds
        if not player.exit_status:
            if not player.in_bounds():
                uiManager.enable_exit_text()
            player.stop_escape()

        # saving
        if saveManager.check_for_save(player):
            saveManager.save_data(player)
            uiManager.enable_save_text()
            healthManager.reset_health()
        
        # setting background color and updating platform wall color
        window.fill(Platform.update_color())
        
        # drawing entities in order of increasing visbility priority
        for platform in Platform.platforms:
            platform.draw()
        for explosion in Explosion.explosions:
            explosion.draw()
        for bullet in Bullet.bullets:
            bullet.draw()
        for enemy in Enemy.enemies:
            enemy.draw()
            enemy.draw_health_bar()
        player.draw()

        # drawing ui elements
        uiManager.display()

        # DEBUG: shows FPS if backspace is pressed
        uiManager.display_fps(fpsClock)

        # default screen fade: try to clear up the screen
        fadeManager.lighten_fade()
        fadeManager.display()
 
        # ticks at FPS, updates screen to show new drawings
        fpsClock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
