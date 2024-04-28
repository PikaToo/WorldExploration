from abstract_classes.gameObject import GameObject
from interface_helpers.healthOverlay import HealthOverlay

class HealthManager(GameObject):
    def __init__(self):
        self.max_health = 8 if GameObject.ability_statuses.health_increase else 5
        self.current_health = self.max_health
        self.invincibility_frames = 0
        self.healthOverlay = HealthOverlay()

    def update(self):
        # tick down invincinility frames
        if self.invincibility_frames > 0:
            self.invincibility_frames -= 1
        
        # clamp current health to not exceed max
        self.current_health = min(self.current_health, self.max_health)

        # make sure max health alligns with current ability statuses
        self.max_health = 8 if GameObject.ability_statuses.health_increase else 5

        # update overlay
        self.healthOverlay.update(self.current_health, self.max_health)

    # reduces health by set damage if not invincible
    def take_damage(self, damage):
        if self.invincibility_frames <= 0:
            self.current_health -= damage
            self.invincibility_frames = 120
            self.healthOverlay.take_damage(damage)

    # increases health by set damage    
    def restore_damage(self, damage):
        self.current_health += damage
        self.healthOverlay.restore_damage(damage)

    # brings health back to full    
    def reset_health(self):
        self.restore_damage(self.max_health - self.current_health)

    def set_player_color(self):
        pass
