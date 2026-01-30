from settings import *
from meshes.chicken_mesh import ChickenMesh

function = type(vars)

class entity:
    def __init__(self, app, type, x, y, z, name, ):
        self._app = app
    
        self.type = type
        if name != None:
            self.name = name
        else: 
            self.name = type(self).__name__


        self.can_fly = 0
        self.x = x
        self.y = y
        self.z = z

 
        
    def __setitem__(self, key, value):
    
        for k, v in vars(self).items():
            if not k.startswith("_") and not isinstance(v, function):
                if k == key:
                    setattr(self, k, value)

    

    def __getitem__(self, key):
        for k, v in vars(self).items():
            if not k.startswith("_") and not isinstance(v, function):
                if k == key:
                    return v
                
        return None
    
    def render(self):
        pass

    def update(self):
        pass

    def kill(self):
        pass

    def __repr__(self):
        return type(self).__name__

class player_entity(entity):
    def __init__(self, app, name, player):

        self._player = player
        self._app = app
        assert hasattr(player, "position"), "player object needs position attribute"
        assert hasattr(player, "yaw"), "player object needs yaw attribute"
        assert hasattr(player, "pitch"), "player object needs pitch attribute"
        assert hasattr(player, "health"), "player object needs health attribute"


        super().__init__(app, "player ",*player.position , name)

        self.x,  self.y, self.z = tuple(player.position)
        self.yaw, self.pitch = player.yaw,player.pitch
        self.health = player.health
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._player.position = glm.vec3(self.x, self.y, self.z)
        self._player.yaw = self.yaw
        self._player.pitch = self.pitch
        self._player.name = str(self.name)
        self._player.can_fly = bool(int(self.can_fly))
        self._player.health = self.health
        
        
    def kill(self):
        self._app.sound.playsound("minecraft.entities.player_die_sound")
        self._player.health = 0
        self._player.at_death()
    
    def update(self):
        super().update()
        self.health = self._player.health

class block_entity:
    def __init__(self, voxel_handler, position, type):
        self.voxel_hander = voxel_handler
        self.position = position
        self.type = type

        self.data = {
            "position": glm.vec3(position),
            "x":glm.ivec3(position).x,
            "y":glm.ivec3(position).y,
            "z":glm.ivec3(position).z,
            

        }
    def as_dict(self):
        return entity(self)
    def get(self, key):
        return self.data.get(key, None)
    def set(self, key, value):
        self.data[key] = value
    def has(self, key):
        return True if key in self.data.keys() else False
    

    def destroy(self):
        self.voxel_hander.set_block(*self.position, 0)
        del self

    def change(self, block):
        self.voxel_hander.set_block(*self.position, block)
        del self  
    def update(self): pass

class Torch(block_entity):
    TO_UP = 1
    TO_LEFT = 2
    TO_RIGHT = 3
    TO_FRONT = 4
    TO_BACK = 5
    def __init__(self, voxel_handler, position, data:dict):
        super().__init__(voxel_handler, position, "torch")

        for i in data.items():
            key, item = i
            if not self.has(key): self.set(key, item)

        if not self.has("angled"): self.set("angled", self.TO_UP)
    def kill(self):
        self.voxel_hander.app.sound.playsound("minecraft.torch.fizz")
        self.destroy()



class Chicken(entity):
    def __init__(self, app, x, y, z, name=""):
        super().__init__(app, "chicken", x, y, z, name)
        self._app = app
        self._entity_index = len(self._app.entity_handler.entities) - 1
        self._mesh = ChickenMesh(app)
        self._timer_to_duck = 0
        self.ducking_time = random.randint(2000, 9500)
        self.weight = 2.3
        self._fall_velocity = 0
        self._gravity = 0.1
        self._velocity_on_fall = self.weight * 0.1
        self._kill_countdown = -1
        self._is_garbage = False
        self.health = CHINKEN_DEFAULT_HEALTH
        self.yaw = 0
        self.pitch = 0

       


    def render(self):
        self._mesh.position = glm.vec3(self.x, self.y, self.z)
        self._mesh.set_uniform()
        self._mesh.render()

    def kill(self):
        if self._kill_countdown != -1:
            return
        self._app.sound.playsound_localy("minecraft.entities.chicken_die_sound", glm.vec3(self.x, self.y, self.z))
        self._kill_countdown = 15

    def walk(self, position):
        pos = glm.vec3(self.x, self.y, self.z)
        position *= self._app.delta_time * 0.002
        if position.y > 0:
            self.y += 0.91 if not self._app.collisions.chicken_collided_top(glm.vec3(self.x, self.y, self.z)) else 0
        self.x += position.x if not (self._app.collisions.chicken_collided_right if position.x > 0 else self._app.collisions.chicken_collided_left)(pos) else 0
        self.z += position.z if not (self._app.collisions.chicken_collided_back if position.z > 0 else self._app.collisions.chicken_collided_front)(pos) else 0

        if position.z == 0 and position.x > 0:
            self.yaw = 0

        if position.z == 0 and position.x < 0:
            self.yaw = 180

        if position.x == 0 and position.z >= 0:
            self.yaw = 90

        if position.x == 0 and position.z >= 0:
            self.yaw = 270

        
    
    def damage(self, hp):
        if self._kill_countdown > 0:
            return
        if self.health - hp < 0:
            self.kill()

        else:
            self.health -= hp
            if hp > 0: self._app.sound.playsound_localy("minecraft.entities.chicken_hurt", glm.vec3(self.x, self.y, self.z))
        
    def update(self):
        self._mesh.yaw = self.yaw
        self._mesh.pitch = self.pitch
        
        if self.health == 0:
            self.kill()
        if self._kill_countdown > 0:
            self.pitch = (1 - (self._kill_countdown / 15) ) * 90
            self._kill_countdown -= 1
      
        if self._kill_countdown == 0:
            self._is_garbage = True
            return
        if self._kill_countdown > 0:
            return
   
        self._timer_to_duck += 1
    
        self._velocity_on_fall = self.weight * 0.1

        if self._app.collisions.chicken_collided_bottom(glm.vec3(self.x, self.y, self.z)):
            if self._fall_velocity != 0: self.damage(self._fall_velocity // VELOCITY_PER_HP)
            self._fall_velocity = 0
        if not self._app.collisions.chicken_collided_bottom(glm.vec3(self.x, self.y, self.z)) and self._fall_velocity == 0:
            self._fall_velocity = self._velocity_on_fall
      
    
        self.y += -self._fall_velocity
        if self._fall_velocity != 0:
            self._fall_velocity += self._gravity





        if self.y < -9:
            self.kill()

    


            
        
        if random.random() < 0.5:
            walk_directions = [
                glm.vec3(0, 0, 1), glm.vec3(0, 0, -1), 
                glm.vec3(-1, 0, 0), glm.vec3(1, 0, 0), 
                
            ]
            
            block_front = self._app.voxel_handler.getblock(*glm.ivec3(self.x, self.y - 1, self.z - 1))
            block_back = self._app.voxel_handler.getblock(*glm.ivec3(self.x, self.y - 1, self.z + 1))
            block_left = self._app.voxel_handler.getblock(*glm.ivec3(self.x + 1, self.y - 1, self.z ))
            block_right = self._app.voxel_handler.getblock(*glm.ivec3(self.x - 1, self.y - 1, self.z ))
            available_blocks_to_walk = [block_back, block_front, block_left, block_right]
            if available_blocks_to_walk.count(GRASS) == 4:
                self.walk(random.choice(walk_directions))
            
            elif available_blocks_to_walk.count(GRASS) != 0:
                self.walk(walk_directions[available_blocks_to_walk.index(GRASS)])

            elif available_blocks_to_walk.count(DIRT) != 0:
                self.walk(walk_directions[available_blocks_to_walk.index(DIRT)])
            else:
                block_front = self._app.voxel_handler.getblock(*glm.ivec3(self.x, self.y, self.z - 1))
                block_back = self._app.voxel_handler.getblock(*glm.ivec3(self.x, self.y, self.z + 1))
                block_left = self._app.voxel_handler.getblock(*glm.ivec3(self.x + 1, self.y, self.z ))
                block_right = self._app.voxel_handler.getblock(*glm.ivec3(self.x - 1, self.y, self.z ))
                available_blocks_to_walk = [block_back, block_front, block_left, block_right]
                if available_blocks_to_walk.count(GRASS) == 4:
                    self.walk(random.choice(walk_directions) + glm.vec3(1))
                
                elif available_blocks_to_walk.count(GRASS) != 0:
                    self.walk(walk_directions[available_blocks_to_walk.index(GRASS)] + glm.vec3(1))

                elif available_blocks_to_walk.count(DIRT) != 0:
                    self.walk(walk_directions[available_blocks_to_walk.index(DIRT)] + glm.vec3(1))

        #chicken ai 


        if random.random() < 0.35:
            self._app.sound.playsound_localy(f"minecraft.entities.chicken_ducks{random.randint(1, 3)}", glm.vec3(self.x, self.y, self.z))
    def choice(self):
        blocks = self._app.voxel_handler.grab(self.x - 5, self.x + 5, self.y + 4, self.y - 4, self.z - 5, self.z + 5)
    

def get_from_type(type):
    if type == "chicken":
        return Chicken
    
    else:
        return None