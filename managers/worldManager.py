from abstract_classes.gameObject import GameObject
from abstract_classes.platforms import Platform
from abstract_classes.enemy import Enemy
from bullet import Bullet
from explosion import Explosion

from platform_classes.savepoint import Savepoint
from platform_classes.upgradepoint import Upgradepoint
from platform_classes.wall import Wall

from enemy_classes.bird import Bird
from enemy_classes.coldBird import ColdBird
from enemy_classes.follower import Follower
from enemy_classes.harmer import Harmer
from enemy_classes.iceyFollower import IceyFollower
from enemy_classes.pewer import Pewer
from enemy_classes.shooter import Shooter
from enemy_classes.target import Target

class WorldManager(GameObject):
    def __init__(self):
        # to process world changes (i.e., to know to build them)
        self.world_changed = False

    def update_world_coordinates(self, player):
        if player.exit_status:  # only can change level if exits are open (i.e. bosses are dead)
            # moving world by x
            if player.rect.x < 10:
                player.rect.x = GameObject.window_width - 30
                GameObject.set_world_coordinates(GameObject.world_x - 1, GameObject.world_y)
                self.world_changed = True

            if player.rect.x + 10 > GameObject.window_width:
                player.rect.x = 10
                GameObject.set_world_coordinates(GameObject.world_x + 1, GameObject.world_y)
                self.world_changed = True
            
            # moving world by y
            if player.rect.y < 10:
                player.rect.y = GameObject.window_height - 30
                GameObject.set_world_coordinates(GameObject.world_x, GameObject.world_y - 1)
                self.world_changed = True
            
            if player.rect.y + 10 > GameObject.window_height:
                player.rect.y = 30
                player.cap_upward_speed()  # to stop entering a room at really high jump speed
                GameObject.set_world_coordinates(GameObject.world_x, GameObject.world_y + 1)
                self.world_changed = True

    # empties stage then creates new one from the world given
    def build_new_stage(self, player, world):
        self.empty_stage()
        self.create_stage(player, world)

    # delete all entities
    def empty_stage(self):
        Platform.platforms = []
        Wall.walls = []
        Upgradepoint.upgradepoints = []
        Savepoint.savepoints = []
        Enemy.enemies = []
        Bullet.bullets = []
        Explosion.explosions = []

    # creates stage
    def create_stage(self, player, world):
        stage = world[GameObject.world_y][GameObject.world_x]

        # first adding all platforms        
        wall_x = wall_y = 0
        for row in stage:
            for value in row:
                if value == "W":
                    Wall(wall_x, wall_y, 30)
                elif value == "U":
                    Upgradepoint(wall_x + 5, wall_y + 5, 15)
                elif value == "L":
                    Savepoint(wall_x + 5, wall_y + 5, 15)
                wall_x += 30
            wall_y += 30
            wall_x = 0

        # then adding all enemies 
        wall_x = wall_y = 0
        for row in stage:
            for value in row:
                if value == "0" and GameObject.boss_statuses.target:
                    Target(wall_x, wall_y, player, Platform.platforms)
                if value == "1" and GameObject.boss_statuses.harmer:
                    Harmer(wall_x, wall_y, player, Platform.platforms)
                if value == "F":
                    Follower(wall_x, wall_y, player, Platform.platforms)
                if value == "S":
                    Shooter(wall_x, wall_y, player, Platform.platforms)
                if value == "B":
                    Bird(wall_x, wall_y, player, Platform.platforms)
                if value == "I":
                    IceyFollower(wall_x, wall_y, player, Platform.platforms)
                if value == "C":
                    ColdBird(wall_x, wall_y, player, Platform.platforms)
                if value == "P":
                    Pewer(wall_x, wall_y, player, Platform.platforms)
                wall_x += 30
            wall_y += 30
            wall_x = 0

        # processed world change, can discard
        self.world_changed = False