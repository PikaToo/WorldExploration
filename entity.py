import pygame


class Entity(object):
    window = None

    def __init__(self, x_pos, y_pos, size, color, x_velocity, y_velocity):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color

    # checks for collision against a list of other entities
    def colliding_with(self, entity_list):
        for entity in entity_list:
            if self.rect.colliderect(entity.rect):
                return True
        return False

    def draw(self):
        pygame.draw.rect(Entity.window, self.color, self.rect)