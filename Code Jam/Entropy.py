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

class SlidingPanel:
    def __init__(self,x,y,width,height,image,direction):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.image = image
        self.direction = direction

        self.open = False

        self.rect = pygame.Rect(x,y,width,height)

        if(direction == "vertical"):
            self.closed_y = y
            self.open_y = y - height + 20
            self.target_y = y

            self.arrow_rect = pygame.Rect(
                x + width//2 - 20,
                y,
                40,
                20
            )

        elif(direction == "horizontal"):
            self.closed_x = x
            self.open_x = x - width + 20
            self.target_x = x

            self.arrow_rect = pygame.Rect(
                x,
                y + height//2 - 20,
                20,
                40
            )

    def toggle(self):
        self.open = not self.open

        if(self.direction == "vertical"):
            if(self.open):
                self.target_y = self.open_y
            else:
                self.target_y = self.closed_y

        elif(self.direction == "horizontal"):
            if(self.open):
                self.target_x = self.open_x
            else:
                self.target_x = self.closed_x

    def update(self):

        if(self.direction == "vertical"):

            if(self.y < self.target_y):
                self.y += 10
            elif(self.y > self.target_y):
                self.y -= 10

            self.rect.y = self.y
            self.arrow_rect.y = self.y

        elif(self.direction == "horizontal"):

            if(self.x < self.target_x):
                self.x += 10
            elif(self.x > self.target_x):
                self.x -= 10

            self.rect.x = self.x
            self.arrow_rect.x = self.x

class Enemy(Tile):
    def __init__(self,x,y,image,enemy_type,track):
        super().__init__(x,y,image,"enemy")
        self.enemy_type = enemy_type
        self.way_point_number = 0
        if(self.enemy_type == "basic_plant_enemy"):
            self.health = 2
        if(self.enemy_type == "basic_tree_enemy"):
            self.health = 5
        if(self.enemy_type == "basic_fly_enemy"):
            self.health = 1
        self.waypoint_track = track
    def move_down_track(self):
        if(self.way_point_number + 1 == len(self.waypoint_track)):
            self.damage(player)
            return
        while((self.tile_coordinates.x - self.waypoint_track[self.way_point_number+1].tile_coordinates.x) == 0 and (self.tile_coordinates.y-self.waypoint_track[self.way_point_number+1].tile_coordinates.y) == 0):
            self.way_point_number += 1
            if(self.way_point_number + 1 == len(self.waypoint_track)):
                self.damage(player)
                return
        move_vector = pygame.Vector2(((self.tile_coordinates.x - self.waypoint_track[self.way_point_number+1].tile_coordinates.x),(self.tile_coordinates.y-self.waypoint_track[self.way_point_number+1].tile_coordinates.y))).normalize() * tile_scaler
        self.tile_coordinates.x -= move_vector.x
        self.tile_coordinates.y -= move_vector.y
        if(self.tile_coordinates.x == self.waypoint_track[self.way_point_number+1].tile_coordinates.x and self.tile_coordinates.y == self.waypoint_track[self.way_point_number+1].tile_coordinates.y):
            self.way_point_number += 1
        self.rect = pygame.Rect(self.tile_coordinates.x,self.tile_coordinates.y,40,40)
    def damage(self,player):
        player.health -= self.health
        if(stage_1):
            stage_1_enemy_list.remove(self)
            self.health = -1
        if(stage_2):
            stage_2_enemy_list.remove(self)
            self.health = -1
        if(stage_3):
            stage_3_enemy_list.remove(self)
            self.health = -1
    def take_damage(self,amount):
        self.health -= amount
        if(self.health <= 0):
            if(stage_1):
                stage_1_enemy_list.remove(self)
            if(stage_2):
                stage_2_enemy_list.remove(self)
            if(stage_3):
                stage_3_enemy_list.remove(self)
        

class Tower(Tile):
    def __init__(self,x,y,image,tower_type):
        super().__init__(x,y,image,"tower")
        self.tower_type = tower_type
    def attack(self,target:Enemy):
        if(self.tower_type == "small_wizard_tower"):
            projectile_list.append(Projectile(self.tile_coordinates.x,self.tile_coordinates.y,wizard_projectile,"wizard",target))
        if(self.tower_type == "small_mage_tower"):
            projectile_list.append(Projectile(self.tile_coordinates.x,self.tile_coordinates.y,mage_projectile,"mage",target))

class Player:
    def __init__(self,health,currency):
        self.health = health
        self.currency = currency

class Projectile:
    def __init__(self,x,y,image,projectile_type,target):
        self.pos = pygame.Vector2(x,y)
        self.projectile_type = projectile_type
        self.image = image
        self.target = target
        self.projectile_stage = 0
        self.velocity = None
    def advance_projectile_stage(self):
        if(self.projectile_type == "wizard"):
            self.projectile_stage += 1
            self.velocity = (self.pos-self.target.tile_coordinates).normalize()*15
            self.pos -= self.velocity
            self.collision_check()
        elif(self.projectile_type == "mage"):
            if self.velocity is None:
                self.velocity = (self.pos-self.target.tile_coordinates)//4
            self.pos -= self.velocity
            self.projectile_stage += 1
            if(self.projectile_stage == 4):
                if(stage_1):
                    for enemy in stage_1_enemy_list:
                        if(enemy.rect.colliderect(pygame.Rect(self.pos.x-100,self.pos.y-100,240,240))):
                            enemy.take_damage(4)
                if(stage_2):
                    for enemy in stage_2_enemy_list:
                        if(enemy.rect.colliderect(pygame.Rect(self.pos.x-100,self.pos.y-100,240,240))):
                            enemy.take_damage(4)
                if(stage_3):
                    for enemy in stage_3_enemy_list:
                        if(enemy.rect.colliderect(pygame.Rect(self.pos.x-100,self.pos.y-100,240,240))):
                            enemy.take_damage(4)
                projectile_list.remove(self)
                explosion = Projectile(self.pos.x - 100, self.pos.y - 100, mage_explosion,"mage_explosion",None)
                projectile_list.append(explosion)
        elif(self.projectile_type == "mage_explosion"):
            self.projectile_stage += 1
            if self.projectile_stage == 5:
                projectile_list.remove(self)

    def collision_check(self):
        if(self.target.rect.collidepoint((self.pos.x+20,self.pos.y+20)) and self.projectile_type == "wizard" and self.target.health > 0):
            projectile_list.remove(self)
            self.target.take_damage(1)
            player.currency += 1
        elif(self.target.health <= 0):
            projectile_list.remove(self)

#Setup
pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_is_on = True
frame = 0
player = Player(health=50,currency=350)
font = pygame.font.SysFont("helvetica", 32)

#Background Tile Art Loading
basic_grass_tile = pygame.image.load("Code Jam/basic_grass_tile.png").convert_alpha()
grass_tile = pygame.image.load("Code Jam/grass_tile.png").convert_alpha()
grass_2_tile = pygame.image.load("Code Jam/grass_2_tile.png").convert_alpha()
grass_3_tile = pygame.image.load("Code Jam/grass_3_tile.png").convert_alpha()
grass_4_tile = pygame.image.load("Code Jam/grass_4_tile.png").convert_alpha()
grass_bush_tile = pygame.image.load("Code Jam/grass_bush_tile.png").convert_alpha()

#Track Tile Art Loading
dirt_path_track = pygame.image.load("Code Jam/dirt_path.png").convert_alpha()

#UI Element Art Loading
#Start stage
start_button = pygame.image.load("Code Jam/start_button.png").convert_alpha()
quit_button = pygame.image.load("Code Jam/quit_button.png").convert_alpha()
entropy_name_plate = pygame.image.load("Code Jam/entropy_name_plate.png").convert_alpha()
#Select_screen
select_1 = pygame.image.load("Code Jam/select_1.png").convert_alpha()
select_2 = pygame.image.load("Code Jam/select_2.png").convert_alpha()
select_3 = pygame.image.load("Code Jam/select_3.png").convert_alpha()

#Stage menu and UI
bottom_bar_image = pygame.image.load("Code Jam/bottom_bar.png").convert_alpha()
upgrade_panel_image = pygame.image.load("Code Jam/upgrade_panel.png").convert_alpha()

#Enemy Art Loading
basic_plant_enemy = pygame.image.load("Code Jam/basic_plant_enemy.png").convert_alpha()
basic_tree_enemy = pygame.image.load("Code Jam/basic_tree_enemy.png").convert_alpha()
basic_fly_enemy = pygame.image.load("Code Jam/basic_fly_enemy.png").convert_alpha()

#Tower Art Loading
small_wizard_tower = pygame.image.load("Code Jam/small_wizard_tower.png").convert_alpha()
small_mage_tower = pygame.image.load("Code Jam/small_mage_tower.png").convert_alpha()

#Projectile Art Loading
wizard_projectile = pygame.image.load("Code Jam/wizard_projectile.png").convert_alpha()
mage_projectile = pygame.image.load("Code Jam/mage_projectile.png").convert_alpha()
mage_explosion = pygame.image.load("Code Jam/mage_explosion.png").convert_alpha()

#Heart and Star Flowers
heart = pygame.transform.scale(pygame.image.load("Code Jam/heart.png").convert_alpha(),(40,40))
star_flower = pygame.transform.scale(pygame.image.load("Code Jam/star_flower.png").convert_alpha(),(50,50))

#Stage Variables
start_stage = True
select_screen = False
stage_1 = False
stage_2 = False
stage_3 = False

stage_1_complete = False
stage_2_complete = False
stage_3_complete = False

placed_towers = []
placing_tower = False
selected_tower = None

projectile_list = []

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
stage_1_track_tiles = []
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
        if(waypoint_tiles[-1].tile_coordinates != stage_1_track_tiles[-1].tile_coordinates):
            waypoint_tiles.append(stage_1_track_tiles[-1])
        track_tile_x -= tile_scaler
    if(track_option == 2 and prior_track_option != 1):
        track_height -= tile_scaler
        if(waypoint_tiles[-1].tile_coordinates != stage_1_track_tiles[-1].tile_coordinates):
            waypoint_tiles.append(stage_1_track_tiles[-1])
        track_tile_x -= tile_scaler
    prior_track_option = track_option
    track_tile = Tile(track_tile_x,track_height,dirt_path_track,"dirt_path_track")
    stage_1_track_tiles.append(track_tile)
    track_tile_x += tile_scaler
    if track_tile_x == 0 or track_option <= 2 or track_tile_x == screen.get_width():
        waypoint_tiles.append(track_tile)
#Stage 2 Tile Creation
stage_2_track_tiles_1 = [Tile(0,screen.get_height()//2,dirt_path_track,"dirt_path_track")]
stage_2_track_tiles_2 = [Tile(screen.get_width()//2,screen.get_height()-tile_scaler,dirt_path_track,"dirt_path_track")]
stage_2_waypoint_tiles_1 = [stage_2_track_tiles_1[-1]]
stage_2_waypoint_tiles_2 = [stage_2_track_tiles_2[-1]]
prior_track_option = 0

while stage_2_track_tiles_1[-1].tile_coordinates.x < screen.get_width():
    track_option = random.randint(1,10)
    if((track_option == 1 or track_option == 2) and (prior_track_option != 3 and prior_track_option != 4)):
        track_tile = Tile(stage_2_track_tiles_1[-1].tile_coordinates.x,stage_2_track_tiles_1[-1].tile_coordinates.y + tile_scaler,dirt_path_track,"dirt_path_track")
        prior_track_option = track_option
        if(stage_2_waypoint_tiles_1[-1].tile_coordinates != stage_2_track_tiles_1[-1].tile_coordinates):
            stage_2_waypoint_tiles_1.append(stage_2_track_tiles_1[-1])
    elif((track_option == 3 or track_option == 4) and (prior_track_option != 1 and prior_track_option != 2)):
        track_tile = Tile(stage_2_track_tiles_1[-1].tile_coordinates.x,stage_2_track_tiles_1[-1].tile_coordinates.y - tile_scaler,dirt_path_track,"dirt_path_track")
        prior_track_option = track_option
        if(stage_2_waypoint_tiles_1[-1].tile_coordinates != stage_2_track_tiles_1[-1].tile_coordinates):
            stage_2_waypoint_tiles_1.append(stage_2_track_tiles_1[-1])
    else:
        track_tile = Tile(stage_2_track_tiles_1[-1].tile_coordinates.x + tile_scaler,stage_2_track_tiles_1[-1].tile_coordinates.y,dirt_path_track,"dirt_path_track")
        prior_track_option = 0
    
    stage_2_track_tiles_1.append(track_tile)
    if(track_option <= 4):
            stage_2_waypoint_tiles_1.append(stage_2_track_tiles_1[-1])
stage_2_waypoint_tiles_1.append(track_tile)

while stage_2_track_tiles_2[-1].tile_coordinates.y > 0:
    track_option = random.randint(1,10)
    if((track_option == 1 or track_option == 2) and (prior_track_option != 3 and prior_track_option != 4)):
        track_tile = Tile(stage_2_track_tiles_2[-1].tile_coordinates.x + tile_scaler,stage_2_track_tiles_2[-1].tile_coordinates.y,dirt_path_track,"dirt_path_track")
        prior_track_option = track_option
        if(stage_2_waypoint_tiles_2[-1].tile_coordinates != stage_2_track_tiles_2[-1].tile_coordinates):
            stage_2_waypoint_tiles_2.append(stage_2_track_tiles_2[-1])
    elif((track_option == 3 or track_option == 4) and (prior_track_option != 1 and prior_track_option != 2)):
        track_tile = Tile(stage_2_track_tiles_2[-1].tile_coordinates.x - tile_scaler,stage_2_track_tiles_2[-1].tile_coordinates.y,dirt_path_track,"dirt_path_track")
        prior_track_option = track_option
        if(stage_2_waypoint_tiles_2[-1].tile_coordinates != stage_2_track_tiles_2[-1].tile_coordinates):
            stage_2_waypoint_tiles_2.append(stage_2_track_tiles_2[-1])
    else:
        track_tile = Tile(stage_2_track_tiles_2[-1].tile_coordinates.x,stage_2_track_tiles_2[-1].tile_coordinates.y - tile_scaler,dirt_path_track,"dirt_path_track")
        prior_track_option = 0
    
    stage_2_track_tiles_2.append(track_tile)
    if(track_option <= 4):
        stage_2_waypoint_tiles_2.append(stage_2_track_tiles_2[-1])
stage_2_waypoint_tiles_2.append(track_tile)

#Stage 3 Tile Creation
stage_3_track_tiles_1 = []
stage_3_track_tiles_2 = []
stage_3_track_tiles_3 = []
stage_3_waypoint_tiles_1 = []
stage_3_waypoint_tiles_2 = []
stage_3_waypoint_tiles_3 = []

columns_selected = []

while len(columns_selected < 3):
    column_selected = random.randrange(0,screen.get_width(),tile_scaler)
    if(column_selected in columns_selected):
        pass
    else:
        columns_selected.append(column_selected)

#First Column
for y in range(0,screen.get_height(),tile_scaler):
    stage_3_track_tiles_1.append(Tile(columns_selected[0],y,dirt_path_track,"dirt_path_track"))
stage_3_waypoint_tiles_1.append(stage_3_track_tiles_1[0])
stage_3_waypoint_tiles_1.append(stage_3_track_tiles_1[-1])
#Second Column
for y in range(0,screen.get_height(),tile_scaler):
    stage_3_track_tiles_1.append(Tile(columns_selected[1],y,dirt_path_track,"dirt_path_track"))
stage_3_waypoint_tiles_2.append(stage_3_track_tiles_2[0])
stage_3_waypoint_tiles_2.append(stage_3_track_tiles_2[-1])
#Third Column
for y in range(0,screen.get_height(),tile_scaler):
    stage_3_track_tiles_3.append(Tile(columns_selected[2],y,dirt_path_track,"dirt_path_track"))
stage_3_waypoint_tiles_3.append(stage_3_track_tiles_3[0])
stage_3_waypoint_tiles_3.append(stage_3_track_tiles_3[-1])


#Stage Enemies and Waves
stage_1_wave_counter = 0
stage_1_wave_spawning = True
stage_1_spawn_taken = False
stage_1_wave_template = [
    ["basic_plant_enemy" for i in range(5)],
    ["basic_plant_enemy" for i in range(5)],
    ["basic_tree_enemy" for i in range(5)],
    ["basic_fly_enemy" for i in range(5)],
    ["basic_tree_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_fly_enemy","basic_fly_enemy"],
    ["basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_fly_enemy"],
    ["basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_fly_enemy"],
    ["basic_fly_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_tree_enemy"],
    ["basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_fly_enemy","basic_fly_enemy","basic_fly_enemy"],
    ["basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy","basic_fly_enemy","basic_fly_enemy","basic_fly_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_tree_enemy","basic_plant_enemy","basic_plant_enemy","basic_plant_enemy"],
    ["basic_fly_enemy" for i in range(20)],
    ["basic_tree_enemy"] #Consider adding stage 1 boss, like mastuh pumpking
]
stage_1_enemy_list = []


stage_2_wave_counter = 0
stage_2_wave_spawning = True
stage_2_spawn_taken = False
stage_2_wave_template = [
    ["basic_plant_enemy" for i in range(5)]
]
stage_2_enemy_list = []

stage_3_wave_counter = 0
stage_3_wave_spawning = True
stage_3_spawn_taken = False
stage_3_wave_template = []
stage_3_waves = []
stage_3_enemy_list = []




#UI Elements
game_start_button = UIElement(screen.get_width()//2-560//2,screen.get_height()//3,560,200,start_button,"start_button")
game_quit_button = UIElement(screen.get_width()//2-560//2,screen.get_height()//1.5,560,200,quit_button,"quit_button")
game_entropy_name_plate = UIElement(screen.get_width()//2-560//2,screen.get_height()//24,560,200,entropy_name_plate,"entropy_name_plate")
game_select_1 = UIElement(screen.get_width()//2-400,screen.get_height()//2-100,200,200,select_1,"select_1")
game_select_2 = UIElement(screen.get_width()//2-100,screen.get_height()//2-100,200,200,select_2,"select_2")
game_select_3 = UIElement(screen.get_width()//2+200,screen.get_height()//2-100,200,200,select_3,"select_3")

game_bottom_bar = SlidingPanel(
    screen.get_width()//2 - bottom_bar_image.get_width()//2,
    screen.get_height()-20,
    bottom_bar_image.get_width(),
    bottom_bar_image.get_height(),
    bottom_bar_image,
    "vertical"
)
upgrade_panel = SlidingPanel(
    screen.get_width()-20,
    screen.get_height()//2-upgrade_panel_image.get_height()//2,
    upgrade_panel_image.get_width(),
    upgrade_panel_image.get_height(),
    upgrade_panel_image,
    "horizontal"
)
wizard_tower_rect = pygame.Rect(
    0,
    0,
    small_wizard_tower.get_width(),
    small_wizard_tower.get_height()
)
mage_tower_rect = pygame.Rect(
    0,
    0,
    small_wizard_tower.get_width(),
    small_wizard_tower.get_height()
)

#random test region


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
                    select_screen = True
                    start_stage = False
                if(game_quit_button.rect.collidepoint(pygame.mouse.get_pos())):
                    game_is_on = False
            elif select_screen:
                if(game_select_1.rect.collidepoint(pygame.mouse.get_pos())):
                    select_screen = False
                    stage_1 = True

                    stage_1_waves = [
                        wave.copy()
                        for wave in stage_1_wave_template
                    ]
                if(game_select_2.rect.collidepoint(pygame.mouse.get_pos()) and stage_1_complete):
                    select_screen = False
                    stage_2 = True
                    stage_2_waves = [
                        wave.copy()
                        for wave in stage_2_wave_template
                    ]
                if(game_select_3.rect.collidepoint(pygame.mouse.get_pos()) and stage_2_complete):
                    select_screen = False
                    stage_3 = True
                    stage_3_waves = [
                        wave.copy()
                        for wave in stage_3_wave_template
                    ]
            if(stage_1 or stage_2 or stage_3):
                if(game_bottom_bar.arrow_rect.collidepoint(pygame.mouse.get_pos())):
                    game_bottom_bar.toggle()
            if(game_bottom_bar.open):
                if(wizard_tower_rect.collidepoint(pygame.mouse.get_pos())):
                    if(selected_tower == None and player.currency >= 100):
                        selected_tower = Tower(
                            0,
                            0,
                            small_wizard_tower,
                            "small_wizard_tower"
                        )
                if(mage_tower_rect.collidepoint(pygame.mouse.get_pos())):
                    if(selected_tower == None and player.currency >= 200):
                        selected_tower = Tower(
                            0,
                            0,
                            small_mage_tower,
                            "small_mage_tower"
                        )
                elif(selected_tower != None):
                    track_check_list = []
                    if(stage_1):
                        track_check_list = stage_1_track_tiles
                    elif(stage_2):
                        track_check_list = stage_2_track_tiles_1 + stage_2_track_tiles_2
                    valid = True
                    for tile in track_check_list:
                        if tile.rect.colliderect(selected_tower.rect):
                            valid = False
                    if(valid and selected_tower.tower_type == "small_wizard_tower" and player.currency >= 100):
                        placed_towers.append(selected_tower)
                        selected_tower = None
                        player.currency -= 100
                    elif(valid and selected_tower.tower_type == "small_mage_tower" and player.currency >= 200):
                        placed_towers.append(selected_tower)
                        selected_tower = None
                        player.currency -= 200
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(stage_1 or stage_2 or stage_3):
                    game_bottom_bar.toggle()
            if event.key == pygame.K_u:
                if(stage_1 or stage_2 or stage_3):
                    upgrade_panel.toggle()

    

    #drawing the background
    for tile in background_tiles:
        screen.blit(tile.image,(tile.tile_coordinates))

    #start stage drawing
    if(start_stage):
        screen.blit(game_start_button.image,(game_start_button.ui_coordinates))
        screen.blit(game_quit_button.image,(game_quit_button.ui_coordinates))
        screen.blit(game_entropy_name_plate.image,(game_entropy_name_plate.ui_coordinates))

    if select_screen:
        screen.blit(game_select_1.image,(game_select_1.ui_coordinates))
        if not(stage_1_complete):
            screen.blit(pygame.transform.grayscale(game_select_2.image),(game_select_2.ui_coordinates))
        else:
            screen.blit((game_select_2.image),(game_select_2.ui_coordinates))
        if not(stage_2_complete):
            screen.blit(pygame.transform.grayscale(game_select_3.image),(game_select_3.ui_coordinates))
        else:
            screen.blit(game_select_3.image,(game_select_3.ui_coordinates))


    #Stage Drawing
    if(stage_1):
        for tile in stage_1_track_tiles:
            screen.blit(tile.image,(tile.tile_coordinates))

        if(stage_1_wave_spawning):
            if(len(stage_1_waves) > stage_1_wave_counter):
                for enemy in stage_1_waves[stage_1_wave_counter]:
                    if not(stage_1_spawn_taken):
                        if enemy == "basic_plant_enemy":
                            stage_1_enemy_list.append(
                                Enemy(
                                    0,
                                    screen.get_height()//2,
                                    basic_plant_enemy,
                                    "basic_plant_enemy",
                                    waypoint_tiles
                                )
                            )

                        if enemy == "basic_tree_enemy":
                            stage_1_enemy_list.append(
                                Enemy(
                                    0,
                                    screen.get_height()//2,
                                    basic_tree_enemy,
                                    "basic_tree_enemy",
                                    waypoint_tiles
                                )
                            )

                        if enemy == "basic_fly_enemy":
                            stage_1_enemy_list.append(
                                Enemy(
                                    0,
                                    screen.get_height()//2,
                                    basic_fly_enemy,
                                    "basic_fly_enemy",
                                    waypoint_tiles
                                )
                            )
                        stage_1_waves[stage_1_wave_counter].remove(enemy)
                        stage_1_spawn_taken = True
        if(len(stage_1_enemy_list) == 0):
            stage_1_wave_spawning = True
            if(len(stage_1_waves) > stage_1_wave_counter):
                stage_1_wave_counter += 1
                player.currency += 25 + (stage_1_wave_counter//5)*25
            else:
                stage_1_complete = True
                stage_1 = False
                select_screen = True
                stage_1_wave_spawning = False
                stage_1_enemy_list.clear()
                placed_towers.clear()
                selected_tower = None
                player.health = 50
                player.currency = 250
                stage_1_wave_counter = 0
                stage_1_spawn_taken = False
                projectile_list.clear()

        if(selected_tower != None):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            grid_x = (mouse_x // tile_scaler) * tile_scaler
            grid_y = (mouse_y // tile_scaler) * tile_scaler

            selected_tower.tile_coordinates.x = grid_x
            selected_tower.tile_coordinates.y = grid_y
            selected_tower.rect.x = grid_x
            selected_tower.rect.y = grid_y


            screen.blit(
                selected_tower.image,
                selected_tower.tile_coordinates
            )
            
        screen.blit(heart,(20,20))
        screen.blit(font.render(f"{player.health}",True,(255,255,255)),(70,20))
        screen.blit(star_flower,(100,15))
        screen.blit(font.render(f"{player.currency}",True,(255,255,255)),(150,20))

        if(frame % 20 == 0):
            for enemy in stage_1_enemy_list:
                if(enemy.enemy_type == "basic_plant_enemy"):
                    enemy.move_down_track()
                    
        if(frame % 30 == 0):
            for enemy in stage_1_enemy_list:
                if(enemy.enemy_type == "basic_tree_enemy"):
                    enemy.move_down_track()
        if(frame % 15 == 0):
            for enemy in stage_1_enemy_list:
                if(enemy.enemy_type == "basic_fly_enemy"):
                    enemy.move_down_track()
        
        if(all(stage_1_enemy_list[i].tile_coordinates.x > 0 for i in range(0,len(stage_1_enemy_list)))):
            stage_1_spawn_taken = False

        for enemy in stage_1_enemy_list:
            screen.blit(enemy.image,(enemy.tile_coordinates))
        for tower in placed_towers:
            screen.blit(
                tower.image,
                tower.tile_coordinates
            )
            if(frame % 60 == 0 and tower.tower_type == "small_wizard_tower" and len(stage_1_enemy_list) > 0):
                tower.attack(stage_1_enemy_list[0])
            if(frame % 260 == 0 and tower.tower_type == "small_mage_tower" and len(stage_1_enemy_list) > 0):
                tower.attack(stage_1_enemy_list[0])

        for projectile in projectile_list:
            if(frame % 3 == 0 and projectile.projectile_type == "wizard"):
                projectile.advance_projectile_stage()
            elif(frame % 6 == 0 and projectile.projectile_type == "mage"):
                projectile.advance_projectile_stage()
            elif(frame % 10 == 0 and projectile.projectile_type == "mage_explosion"):
                projectile.advance_projectile_stage()
            screen.blit(projectile.image,projectile.pos)

        game_bottom_bar.update()
        screen.blit(
            game_bottom_bar.image,
            (game_bottom_bar.x,game_bottom_bar.y)
        )
        if(game_bottom_bar.open):
            wizard_tower_rect.x = game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler//2
            wizard_tower_rect.y = game_bottom_bar.y+game_bottom_bar.height//2
            screen.blit(small_wizard_tower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler//2,game_bottom_bar.y+game_bottom_bar.height//2))
            screen.blit(star_flower,(game_bottom_bar.x+game_bottom_bar.width//2-60,game_bottom_bar.y+game_bottom_bar.height//2+35))
            screen.blit(font.render("100",True,(255,255,255)),(game_bottom_bar.x+game_bottom_bar.width//2-8,game_bottom_bar.y+game_bottom_bar.height//2+43))

            mage_tower_rect.x = game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4
            mage_tower_rect.y = game_bottom_bar.y+game_bottom_bar.height//2
            screen.blit(small_mage_tower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4,game_bottom_bar.y+game_bottom_bar.height//2))
            screen.blit(star_flower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*5.5,game_bottom_bar.y+game_bottom_bar.height//2+35))
            screen.blit(font.render("200",True,(255,255,255)),(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4,game_bottom_bar.y+game_bottom_bar.height//2+43))
        
        upgrade_panel.update()

        screen.blit(
            upgrade_panel.image,
            (upgrade_panel.x,upgrade_panel.y)
        )

    if(stage_2):
            for tile in stage_2_track_tiles_1:
                screen.blit(tile.image,(tile.tile_coordinates))
            for tile in stage_2_track_tiles_2:
                screen.blit(tile.image,(tile.tile_coordinates))
    
            if(stage_2_wave_spawning):
                if(len(stage_2_waves) > stage_2_wave_counter):
                    for enemy in stage_2_waves[stage_2_wave_counter]:
                        if not(stage_2_spawn_taken):
                            if enemy == "basic_plant_enemy":
                                if random.randint(0,1) == 1:
                                    stage_2_enemy_list.append(
                                        Enemy(
                                            0,
                                            screen.get_height()//2,
                                            basic_plant_enemy,
                                            "basic_plant_enemy",
                                            stage_2_waypoint_tiles_1
                                        )
                                    )
                                else:
                                    stage_2_enemy_list.append(
                                        Enemy(
                                            screen.get_width()//2,
                                            screen.get_height()-tile_scaler,
                                            basic_plant_enemy,
                                            "basic_plant_enemy",
                                            stage_2_waypoint_tiles_2
                                        )
                                    )
                            stage_2_waves[stage_2_wave_counter].remove(enemy)
                            stage_2_spawn_taken = True
            if(len(stage_2_enemy_list) == 0):
                stage_2_wave_spawning = True
                if(len(stage_2_waves) > stage_2_wave_counter):
                    stage_2_wave_counter += 1
                    player.currency += 25
                else:
                    stage_2_complete = True
                    stage_2 = False
                    select_screen = True
                    player.health = 50
                    player.currency = 250
                    stage_2_wave_counter = 0
                    stage_2_spawn_taken = False
                    stage_2_wave_spawning = False
                    placed_towers.clear()
                    selected_tower = None
                    projectile_list.clear()
    
            if(selected_tower != None):
                mouse_x, mouse_y = pygame.mouse.get_pos()
    
                grid_x = (mouse_x // tile_scaler) * tile_scaler
                grid_y = (mouse_y // tile_scaler) * tile_scaler
    
                selected_tower.tile_coordinates.x = grid_x
                selected_tower.tile_coordinates.y = grid_y
                selected_tower.rect.x = grid_x
                selected_tower.rect.y = grid_y
    
    
                screen.blit(
                    selected_tower.image,
                    selected_tower.tile_coordinates
                )
                
            screen.blit(heart,(20,20))
            screen.blit(font.render(f"{player.health}",True,(255,255,255)),(70,20))
            screen.blit(star_flower,(100,15))
            screen.blit(font.render(f"{player.currency}",True,(255,255,255)),(150,20))
    
            if(frame % 20 == 0):
                for enemy in stage_2_enemy_list:
                    if(enemy.enemy_type == "basic_plant_enemy"):
                        enemy.move_down_track()
                        
            if(frame % 30 == 0):
                for enemy in stage_2_enemy_list:
                    if(enemy.enemy_type == "basic_tree_enemy"):
                        enemy.move_down_track()
            if(frame % 15 == 0):
                for enemy in stage_2_enemy_list:
                    if(enemy.enemy_type == "basic_fly_enemy"):
                        enemy.move_down_track()
            
            if(all(stage_2_enemy_list[i].tile_coordinates.x > 0 for i in range(0,len(stage_2_enemy_list)))):
                stage_2_spawn_taken = False
    
            for enemy in stage_2_enemy_list:
                screen.blit(enemy.image,(enemy.tile_coordinates))
            for tower in placed_towers:
                screen.blit(
                    tower.image,
                    tower.tile_coordinates
                )
                if(frame % 60 == 0 and tower.tower_type == "small_wizard_tower" and len(stage_2_enemy_list) > 0):
                    tower.attack(stage_2_enemy_list[0])
                if(frame % 260 == 0 and tower.tower_type == "small_mage_tower" and len(stage_2_enemy_list) > 0):
                    tower.attack(stage_2_enemy_list[0])
    
            for projectile in projectile_list:
                if(frame % 3 == 0 and projectile.projectile_type == "wizard"):
                    projectile.advance_projectile_stage()
                elif(frame % 6 == 0 and projectile.projectile_type == "mage"):
                    projectile.advance_projectile_stage()
                elif(frame % 10 == 0 and projectile.projectile_type == "mage_explosion"):
                    projectile.advance_projectile_stage()
                
                screen.blit(projectile.image,projectile.pos)
    
            game_bottom_bar.update()
            screen.blit(
                game_bottom_bar.image,
                (game_bottom_bar.x,game_bottom_bar.y)
            )
            if(game_bottom_bar.open):
                wizard_tower_rect.x = game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler//2
                wizard_tower_rect.y = game_bottom_bar.y+game_bottom_bar.height//2
                screen.blit(small_wizard_tower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler//2,game_bottom_bar.y+game_bottom_bar.height//2))
                screen.blit(star_flower,(game_bottom_bar.x+game_bottom_bar.width//2-60,game_bottom_bar.y+game_bottom_bar.height//2+35))
                screen.blit(font.render("100",True,(255,255,255)),(game_bottom_bar.x+game_bottom_bar.width//2-8,game_bottom_bar.y+game_bottom_bar.height//2+43))

                mage_tower_rect.x = game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4
                mage_tower_rect.y = game_bottom_bar.y+game_bottom_bar.height//2
                screen.blit(small_mage_tower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4,game_bottom_bar.y+game_bottom_bar.height//2))
                screen.blit(star_flower,(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*5.5,game_bottom_bar.y+game_bottom_bar.height//2+35))
                screen.blit(font.render("200",True,(255,255,255)),(game_bottom_bar.x+game_bottom_bar.width//2-tile_scaler*4,game_bottom_bar.y+game_bottom_bar.height//2+43))
            
            upgrade_panel.update()
    
            screen.blit(
                upgrade_panel.image,
                (upgrade_panel.x,upgrade_panel.y)
            )


    pygame.display.flip()
    frame += 1
    clock.tick(60)