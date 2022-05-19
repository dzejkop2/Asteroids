import math
import random


import pyglet
import classes.spaceobject as SpaceObject
from classes.spaceship import *
from classes.constants import *
from pyglet import gl
from pyglet.window import key

"---------Globalne konštanty a premenne----------"


"""
Vycentruj ukotvenie obrázka na stred
"""
def set_anchor_of_image_to_center(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    

"""
Pomocna funkcia na zobrazenia kolizneho kolecka
"""
def draw_circle(x, y, radius):
    iterations = 20
    s = math.sin(2 * math.pi / iterations)
    c = math.cos(2 * math.pi / iterations)

    dx, dy = radius, 0

    gl.glBegin(gl.GL_LINE_STRIP)
    gl.glColor3f(1, 1, 1)  # nastav barvu kresleni na bilou
    for i in range(iterations + 1):
        gl.glVertex2f(x + dx, y + dy)
        dx, dy = (dx * c - dy * s), (dy * c + dx * s)
    gl.glEnd()


"----------------VLASTNÉ TRIEDY----------------"

"""
Rodičovská trieda
"""


"""
Trieda Spaceship
Hlavný objekt hry, predstavuje hráča
"""


"""
Trieda Asteroid
"""
class Asteroid(SpaceObject):
    "Metóda ktorá sa vykoná ak dôjde ku kolízii lode a asteroidu"
    def hit_by_spaceship(self, ship):
        global lifes
        if ship.shield == False:
            pressed_keyboards.clear()
            ship.reset()
            ship.get_shield()
            lifes -= 1
        self.delete()

    "Metóda ktorá sa vykoná ak dôjde ku kolíziiwwwww a asteroidu"
    def hit_by_laser(self, laser):
        global score
        self.delete()
        laser.delete()
        score += 10

"""
Trieda Laser
"""
class Laser(SpaceObject):
    def __init__(self, sprite, x ,y):
        super().__init__(sprite,x,y)
        self.laserlifetime = laserlifetime
    def tick(self,dt):
        super().tick(dt)
        self.laserlifetime -= 0.5
        if self.laserlifetime == 0:
            self.delete()

        self.y_speed = laserspeed * math.sin(self.rotation)
        self.x_speed = laserspeed * math.cos(self.rotation)
        
        for obj in [o for o in game_objects if o != self and o != Spaceship]:
            d = self.distance(obj)
            if d < self.radius + obj.radius:
                obj.hit_by_laser(self)
                break
    

class Shield(SpaceObject):
    def __init__(self, sprite, x, y):
        super().__init__(sprite,x, y)
        self.shield_duration = shield_duration        
    def tick(self,dt):
        global pos_x,pos_y
        super().tick(dt)
        
        self.sprite.x = pos_x
        self.sprite.y = pos_y

        self.shield_duration -= dt
        if self.shield_duration <= 0:
            self.delete()

"""
GAME WINDOW CLASS
"""
class Game:
    """
    Konstruktor
    """
    def __init__(self):
        self.window = None
        game_objects = []

    """
    Načítanie všetkých spritov
    """
    def load_resources(self):
        self.playerShip_image = pyglet.image.load('Assetss/PNG/playerShip1_blue.png')
        set_anchor_of_image_to_center(self.playerShip_image)
        self.background_image = pyglet.image.load('Assetss/Backgrounds/black.png')
        self.asteroid_images = ['Assetss/PNG/Meteors/meteorGrey_big1.png',
                           'Assetss/PNG/Meteors/meteorGrey_med1.png',
                           'Assetss/PNG/Meteors/meteorGrey_small1.png',
                           'Assetss/PNG/Meteors/meteorGrey_tiny1.png']

    """
    Vytvorenie objektov pre začiatok hry
    """
    def init_objects(self):
        #Vytvorenie lode
        spaceShip = Spaceship(self.playerShip_image, WIDTH // 2, HEIGHT//2)
        game_objects.append(spaceShip)

        #Nastavenie pozadia a prescalovanie
        self.background = pyglet.sprite.Sprite(self.background_image)
        self.background.scale_x = 6
        self.background.scale_y = 4

        

        #Vytvorenie Meteoritov
        self.create_asteroids(count=7)
        #Pridavanie novych asteroidoch každych 10 sekund
        pyglet.clock.schedule_interval(self.create_asteroids, 6, 1)

    def create_asteroids(self, dt=0, count=1):
        "Vytvorenie X asteroidov"
        for i in range(count):
            # Výber asteroidu náhodne
            img = pyglet.image.load(random.choice(self.asteroid_images))
            set_anchor_of_image_to_center(img)

            # Nastavenie pozície na okraji obrazovky náhodne
            position = [0, 0]
            dimension = [WIDTH, HEIGHT]
            axis = random.choice([0, 1])
            position[axis] = random.uniform(0, dimension[axis])

            # Nastavenie rýchlosti
            tmp_speed_x = random.uniform(-100, 100)
            tmp_speed_y = random.uniform(-100, 100)
            #Temp asteroid object
            asteroid = Asteroid(img, position[0], position[1], tmp_speed_x, tmp_speed_y)
            game_objects.append(asteroid)
    
    def game_lifes(self):
        global lifes
        life = pyglet.image.load("Assetss/PNG/UI/playerLife1_blue.png")
        width = 10
        for i in range(lifes):
            life_asset = pyglet.sprite.Sprite(life,width,HEIGHT - 40)
            life_asset.draw()
            width += 40
    
    def game_end(self):
        if lifes <= 0:
            self.window.clear()
            game_objects.clear()
            lose_text = pyglet.text.Label(text="Game Over!",font_name= "Comic Sans MS", font_size =70,x=WIDTH/2,y=HEIGHT/2,anchor_x='center', anchor_y='center')
            lose_text.draw()
        elif score >= max_score:
            self.window.clear()
            game_objects.clear()
            win_text = pyglet.text.Label(text="Epic Victory Royale!",font_name="Comic Sand MS", font_size =70,x=WIDTH/2,y=HEIGHT/2,anchor_x='center', anchor_y='center')
            win_text.draw()
        
    """
    Event metóda ktorá sa volá na udalosť on_draw stále dookola
    """
    def draw_game(self):
        global score,scoreLabel
        # Vymaže aktualny obsah okna
        self.window.clear()
        # Vykreslenie pozadia
        self.background.draw()
        
        "Vykreslenie koliznych koliečok"
        """
        for o in game_objects:
            draw_circle(o.sprite.x, o.sprite.y, o.radius)
        """
        # Táto časť sa stará o to aby bol prechod cez okraje okna plynulý a nie skokový
        for x_offset in (-self.window.width, 0, self.window.width):
            for y_offset in (-self.window.height, 0, self.window.height):
                # Remember the current state
                gl.glPushMatrix()
                # Move everything drawn from now on by (x_offset, y_offset, 0)
                gl.glTranslatef(x_offset, y_offset, 0)

                # Draw !!! -> Toto vykreslí všetky naše sprites
                batch.draw()

                # Restore remembered state (this cancels the glTranslatef)
                gl.glPopMatrix()
        
        scoreLabel = pyglet.text.Label(text=str(score),font_name="Comic Sans MS", font_size=40,x = 1150, y = 760, anchor_x='right', anchor_y='center')
        scoreLabel.draw()

        self.game_lifes()
        self.game_end()
    """
    Event metóda pre spracovanie klávesových vstupov
    """
    def key_press(self, symbol, modifikatory):
        if symbol == key.W:
            pressed_keyboards.add('W')
        if symbol == key.S:
            pressed_keyboards.add('S')
        if symbol == key.A:
            pressed_keyboards.add('A')
        if symbol == key.D:
            pressed_keyboards.add('D')
        if symbol == key.LSHIFT:
            pressed_keyboards.add('SHIFT')
        if symbol == key.SPACE:
            pressed_keyboards.add("SPACE")

    """
    Event metóda pre spracovanie klávesových výstupov
    """
    def key_release(self, symbol, modifikatory):
        if symbol == key.W:
            pressed_keyboards.discard('W')
        if symbol == key.S:
            pressed_keyboards.discard('S')
        if symbol == key.A:
            pressed_keyboards.discard('A')
        if symbol == key.D:
            pressed_keyboards.discard('D')
        if symbol == key.LSHIFT:
            pressed_keyboards.discard('SHIFT')
        if symbol == key.SPACE:
            pressed_keyboards.discard("SPACE")

    """
    Update metóda
    """
    def update(self, dt):
        for obj in game_objects:
            obj.tick(dt)

    """
    Start game metóda 
    """
    def start(self):
        "Vytvorenie hlavneho okna"
        self.window = pyglet.window.Window(width=WIDTH, height=HEIGHT)

        "Nastavenie udalosti (eventov)"
        self.window.push_handlers(
            on_draw=self.draw_game,
            on_key_press=self.key_press,
            on_key_release=self.key_release
        )

        "Load resources"
        self.load_resources()

        "Inicializacia objektov"
        self.init_objects()

        "Nastavenie timeru pre update metódu v intervale 1./60 = 60FPS"
        pyglet.clock.schedule_interval(self.update, 1. / 60)

        pyglet.app.run()  # all is set, the game can start

"----------- StartGame -----------"
Game().start()