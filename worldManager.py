from gameObject import GameObject
from platforms import Platform
from enemy import Enemy
from bullet import Bullet
from explosion import Explosion

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

    # delete all entities
    def empty_level(self):
        Platform.platforms = []
        Enemy.enemies = []
        Bullet.bullets = []
        Explosion.explosions = []

    def create_level(self, world):
        stage = world[GameObject.world_y][GameObject.world_x]
        wall_x = wall_y = 0
        for row in stage:
            for value in row:
                if value == "W":
                    Platform(wall_x, wall_y, 30, "platform")
                if value == "U":
                    Platform(wall_x + 5, wall_y + 5, 15, "upgrade")
                if value == "L":
                    Platform(wall_x + 5, wall_y + 5, 15, "load")
                # Enemy(x_pos, y_pos, color, size, counter, enemy_AI, enemy_health, boss, other, damage)
                if value == "0" and GameObject.boss_statuses.target:
                    Enemy(wall_x, wall_y, (255, 0, 0), 20, -60, "Target", 8, 0, False, 1)
                if value == "1" and GameObject.boss_statuses.harmer:
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

        # processed world change, can discard
        self.world_changed = False