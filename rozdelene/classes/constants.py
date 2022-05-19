import pyglet

"Window constants"
WIDTH = 1200
HEIGHT = 800

"Game constants"
ACCELERATION = 120              #Zrýchlenie rakety
ROTATION_SPEED = 0.05           #Rýchlosť otáčania rakety

game_objects = []
batch = pyglet.graphics.Batch() #ZOZNAM SPRITOV PRE ZJEDNODUŠENÉ VYKRESLENIE
pressed_keyboards = set()       #MNOŽINA ZMAČKNUTÝCH KLÁVES

delay_shooting = 0.4
laserlifetime = 45
laserspeed = 250

shield_duration = 3

"Score"
score = 0

lifes = 3
max_score = 150

pos_x = 0
pos_y = 0
rotation = 0
