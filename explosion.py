from abstract_classes.entity import Entity
from random import randint

# explosion: the enemy death's gold-particle explosion 
class Explosion(Entity):

    # list of all explosions
    explosions = []

    # recursive initialization
    def __init__(self, x_pos, y_pos, size):
    
        # base case: size is zero or negative
        if size <= 0:
            return
        
        # recursive case: make self
        x_velocity = randint(-size, size)
        y_velocity = -8 + size/10
        super().__init__(x_pos, y_pos, size, (255, 255, 0), x_velocity, y_velocity)

        # append to list, make next particle    
        Explosion.explosions.append(self)
        Explosion(x_pos, y_pos, size - 1)

    # moves by velocity; applies gravity; deletes if needed
    def move(self):
        # moving 
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity
        
        # applying gravity 
        self.y_velocity += 0.3
        self.x_velocity *= 0.95

        # deleting if needed
        if self.colliding_with_walls():
            self.delete()


    def delete(self):
        Explosion.explosions.remove(self)