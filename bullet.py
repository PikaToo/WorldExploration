from abstract_classes.entity import Entity

# bullet: a bullet shot by either a player or an enemy
class Bullet(Entity):
    bullets = []

    def __init__(self, x_pos, y_pos, x_velocity, y_velocity, owner, size, gravity, damage):
        super().__init__(x_pos, y_pos, size, (255, 255, 255), x_velocity, y_velocity)
        self.owner = owner
        self.size = size
        self.gravity = gravity
        self.damage = damage
        
        Bullet.bullets.append(self)

    # moves bullet by velocity; applies gravity
    def move_self(self):
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        self.y_velocity += self.gravity

    def delete(self):
        Bullet.bullets.remove(self)
