import pygame
import random
#Classes
class Tile:
    def __init__(self,x,y,image,tile_type=None):
        self.tile_coordinates = pygame.Vector2(x,y)
        self.tile_type = tile_type
        self.image = image
        self.rect = pygame.Rect(x,y,40,40)

class UIElement:
    def __init__(self,x,y,width,height,image,ui_type=None):
        self.ui_coordinates = (x,y)
        self.ui_type = ui_type
        self.image = image
        self.rect = pygame.Rect(x,y,width,height)

class Enemy(Tile):
    def __init__(self,x,y,image,enemy_type):
        super().__init__(x,y,image,"enemy")
        self.enemy_type = enemy_type
        self.way_point_number = 0
    def move_down_track(self):
        if(self.way_point_number + 1 == len(waypoint_tiles)):
            self.damage()
            return
        move_vector = pygame.Vector2(((self.tile_coordinates.x - waypoint_tiles[self.way_point_number+1].tile_coordinates.x),(self.tile_coordinates.y-waypoint_tiles[self.way_point_number+1].tile_coordinates.y))).normalize() * tile_scaler
        self.tile_coordinates.x -= move_vector.x
        self.tile_coordinates.y -= move_vector.y
        if(self.tile_coordinates.x == waypoint_tiles[self.way_point_number+1].tile_coordinates.x and self.tile_coordinates.y == waypoint_tiles[self.way_point_number+1].tile_coordinates.y):
            self.way_point_number += 1
    def damage(self):
        #deal damage
        #delete from list
        return
        

class Tower(Tile):
    def __init__(self,x,y,image,tower_type):
        super().__init__(x,y,image,"enemy")
        self.tower_type = tower_type

class Player:
    def __init__(self,health,currency):
        self.health = health
        self.currency = currency

#Setup
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_is_on = True
frame = 0
player = Player(50,150)

#Stage Variables
start_stage = True
stage_1 = False
stage_2 = False
stage_3 = False

#Stage Enemies and Waves
stage_1_wave_counter = 0
stage_1_waves = [["basic_plant"],["basic_plant"]]
stage_1_enemy_list = []


#Background Tile Art Loading
basic_grass_tile = pygame.image.load("basic_grass_tile.png").convert_alpha()
grass_tile = pygame.image.load("grass_tile.png").convert_alpha()
grass_2_tile = pygame.image.load("grass_2_tile.png").convert_alpha()
grass_3_tile = pygame.image.load("grass_3_tile.png").convert_alpha()
grass_4_tile = pygame.image.load("grass_4_tile.png").convert_alpha()
grass_bush_tile = pygame.image.load("grass_bush_tile.png").convert_alpha()

#Track Tile Art Loading
dirt_path_track = pygame.image.load("dirt_path.png").convert_alpha()

#UI Element Art Loading
#Start stage
start_button = pygame.image.load("start_button.png").convert_alpha()
quit_button = pygame.image.load("quit_button.png").convert_alpha()
entropy_name_plate = pygame.image.load("entropy_name_plate.png").convert_alpha()

#Stage menu and UI


#Enemy Art Loading
basic_plant_enemy = pygame.image.load("basic_plant_enemy.png").convert_alpha()


#Tower Art Loading



# Tile Creation - Expect 64x36
tile_scaler = 40
background_tiles = []
grass_ran_num = 0

for column in range(0,screen.get_width(),tile_scaler):
    for row in range(0,screen.get_height(),tile_scaler):
        if(random.randint(1,100) > 90):
            grass_ran_num = random.randint(1,4)
            if(grass_ran_num == 1):
                background_tiles.append(Tile(column,row,grass_tile,"grass_tile"))
            elif(grass_ran_num == 2):
                background_tiles.append(Tile(column,row,grass_2_tile,"grass_2_tile"))
            elif(grass_ran_num == 3):
                background_tiles.append(Tile(column,row,grass_3_tile,"grass_3_tile"))
            else:
                background_tiles.append(Tile(column,row,grass_4_tile,"grass_4_tile"))
        elif(random.randint(1,100) == 90):
            background_tiles.append(Tile(column,row,grass_bush_tile,"grass_bush_tile"))
        else:
            background_tiles.append(Tile(column,row,basic_grass_tile,"basic_grass_tile"))

#Stage 1 Tile Creation
track_tiles = []
waypoint_tiles = []
track_height = (screen.get_height()//2)
track_tile_x = 0
prior_track_option = 0
track_option = 0
while track_tile_x < screen.get_width():
    if(track_tile_x > 0):
        track_option = random.randint(1,10)
    if(track_option == 1 and prior_track_option != 2):
        track_height += tile_scaler
        if(waypoint_tiles[-1].tile_coordinates != track_tiles[-1].tile_coordinates):
            waypoint_tiles.append(track_tiles[-1])
        track_tile_x -= tile_scaler
    if(track_option == 2 and prior_track_option != 1):
        track_height -= tile_scaler
        if(waypoint_tiles[-1].tile_coordinates != track_tiles[-1].tile_coordinates):
            waypoint_tiles.append(track_tiles[-1])
        track_tile_x -= tile_scaler
    prior_track_option = track_option
    track_tile = Tile(track_tile_x,track_height,dirt_path_track,"dirt_path_track")
    track_tiles.append(track_tile)
    track_tile_x += tile_scaler
    if track_tile_x == 0 or track_option <= 2 or track_tile_x == screen.get_width():
        waypoint_tiles.append(track_tile)

#UI Elements
game_start_button = UIElement(screen.get_width()//2-560//2,screen.get_height()//3,560,200,start_button,"start_button")
game_quit_button = UIElement(screen.get_width()//2-560//2,screen.get_height()//1.5,560,200,quit_button,"quit_button")
game_entropy_name_plate = UIElement(screen.get_width()//2-560//2,screen.get_height()//24,560,200,entropy_name_plate,"entropy_name_plate")



#random test region
plantoid = Enemy(0,screen.get_height()//2,basic_plant_enemy,"basic_plant")
stage_1_enemy_list.append(plantoid)






#Game Loop
while game_is_on:
    #Event handling and tab closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #add file saving here
            game_is_on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(start_stage):
                if(game_start_button.rect.collidepoint(pygame.mouse.get_pos())):
                    stage_1 = True
                    start_stage = False
                if(game_quit_button.rect.collidepoint(pygame.mouse.get_pos())):
                    game_is_on = False
    

    #drawing the background
    for tile in background_tiles:
        screen.blit(tile.image,(tile.tile_coordinates))

    #start stage drawing
    if(start_stage):
        screen.blit(game_start_button.image,(game_start_button.ui_coordinates))
        screen.blit(game_quit_button.image,(game_quit_button.ui_coordinates))
        screen.blit(game_entropy_name_plate.image,(game_entropy_name_plate.ui_coordinates))

    #Stage Drawing
    if(stage_1):
        for tile in track_tiles:
            screen.blit(tile.image,(tile.tile_coordinates))
        if(frame % 15 == 0):
            for enemy in stage_1_enemy_list:
                enemy.move_down_track()
        for enemy in stage_1_enemy_list:
            screen.blit(enemy.image,(enemy.tile_coordinates))

    pygame.display.flip()
    frame += 1
    clock.tick(60)