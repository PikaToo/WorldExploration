from gameObject import GameObject

class WorldMover(GameObject):
    def __init__(self):
        pass

    def update_world_coordinates(self, player):
        if player.exit_status:  # only can change level if exits are open (i.e. bosses are dead)
            
            # moving world by x
            if player.rect.x < 10:
                player.rect.x = GameObject.window_width - 30
                GameObject.set_world_coordinates(GameObject.world_x - 1, GameObject.world_y)
            
            if player.rect.x + 10 > GameObject.window_width:
                player.rect.x = 10
                GameObject.set_world_coordinates(GameObject.world_x + 1, GameObject.world_y)
            
            # moving world by y
            if player.rect.y < 10:
                player.rect.y = GameObject.window_height - 30
                GameObject.set_world_coordinates(GameObject.world_x, GameObject.world_y - 1)
            
            if player.rect.y + 10 > GameObject.window_height:
                player.rect.y = 30
                player.cap_upward_speed()  # to stop entering a room at really high jump speed
                GameObject.set_world_coordinates(GameObject.world_x, GameObject.world_y + 1)