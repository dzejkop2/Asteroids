import math


import pyglet
import spaceobject as SpaceObject
from constants import *
from pyglet import gl
from pyglet.window import key

class Spaceship(SpaceObject):

    "Konśtruktor"
    def __init__(self, sprite, x ,y):
        super().__init__(sprite,x,y)
        self.laser_ready = True
        self.shield = False

        #flame sprity
        flame_sprite = pyglet.image.load("Assetss/PNG/Effects/fire05.png")
        set_anchor_of_image_to_center(flame_sprite)
        self.flame = pyglet.sprite.Sprite(flame_sprite,batch=batch)
        self.flame.visible = False
    
    """
    Metóda zodpovedná za vystrelenie laseru
    """
    def shoot(self):
        img = pyglet.image.load("Assetss/PNG/Lasers/laserBlue04.png")
        set_anchor_of_image_to_center(img)

        laser_x = self.sprite.x + math.cos(self.rotation) * self.radius
        laser_y = self.sprite.y + math.sin(self.rotation) * self.radius

        laser = Laser(img,laser_x,laser_y)
        laser.rotation = self.rotation

        game_objects.append(laser)

    def get_shield(self):
        self.shield = True
        img = pyglet.image.load('Assetss/PNG/Effects/shield1.png')
        set_anchor_of_image_to_center(img)
        shield = Shield(img, self.sprite.x, self.sprite.y)
        
        game_objects.append(shield)
        pyglet.clock.schedule_once(self.shield_lose, shield_duration)

    def shield_lose(self,dt):
        self.shield = False
        
    def get_position(self):
        global pos_x,pos_y,rotation
        pos_x = self.sprite.x
        pos_y = self.sprite.y
        rotation = self.rotation

    """
    Každý frame sa vykoná táto metóda to znamená v našom prípade:
    60 simkov * za sekundu
    Mechanic of spaceship - rotation, movement, controls
    """
    def tick(self, dt):
        super().tick(dt)

        "Zrýchlenie po kliknutí klávesy W. Výpočet novej rýchlosti"
        if 'W' in pressed_keyboards:
            self.x_speed = self.x_speed + dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed + dt * ACCELERATION * math.sin(self.rotation)

            #flame pozicie a zobrazenie
            self.flame.x = self.sprite.x - math.cos(self.rotation) * self.radius
            self.flame.y = self.sprite.y - math.sin(self.rotation) * self.radius
            self.flame.rotation = self.sprite.rotation
            self.flame.visible = True
        #ak nie je W tak flame neni vidno
        else:
            self.flame.visible = False
        
        "Spomalenie/spätný chod po kliknutí klávesy S"
        if 'S' in pressed_keyboards:
            self.x_speed = self.x_speed - dt * ACCELERATION * math.cos(self.rotation)
            self.y_speed = self.y_speed - dt * ACCELERATION * math.sin(self.rotation)

        "Otočenie doľava - A"
        if 'A' in pressed_keyboards:
            self.rotation += ROTATION_SPEED

        "Otočenie doprava - D"
        if 'D' in pressed_keyboards:
            self.rotation -= ROTATION_SPEED

        "Ručná brzda - SHIFT"
        if 'SHIFT' in pressed_keyboards:
            self.x_speed = 0
            self.y_speed = 0

        if "SPACE" in pressed_keyboards and self.laser_ready:
            self.shoot()
            self.laser_ready = False
            pyglet.clock.schedule_once(self.reload, delay_shooting)
        
        if self.shield == True:
            self.get_position()

        "VYBERIE VŠETKY OSTATNE OBJEKTY OKREM SEBA SAMA"
        for obj in [o for o in game_objects if o != self]:
            # d = distance medzi objektami
            d = self.distance(obj)
            if d < self.radius + obj.radius:
                obj.hit_by_spaceship(self)
                break

    "Metóda zodpovedná za reset pozície rakety"
    def reset(self):
        self.sprite.x = WIDTH // 2
        self.sprite.y = HEIGHT // 2
        self.rotation = 1.57  # radiany -> smeruje hore
        self.x_speed = 0
        self.y_speed = 0
    
    def reload(self,dt):
        self.laser_ready = True
        