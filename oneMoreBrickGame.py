"""The game class and components
    
    Author: Merc4tor
"""


import numpy as np
from typing import Union, Any
import math
import copy
from data_types import *
from oneMoreBrickEngine import Ball, Collision, Number, PhysicsEnvironment, Line
from data_types import Number, Vector, Point, Line
import pygame
from pygame import Color
import time
import keyboard
import random
from grid_utils import get_lines

Number = Union[int, float]

class BallSpawning:
    def __init__(self, time: Number) -> None:
        self.time_left = time
    
    def __repr__(self) -> str:
        return f'BallSpawning(time_left: {self.time_left})'
    

class Renderer:
    """The renderer class.
    
    Properties:
        screen_width: The width of the screen in pixels.
        screen_height: The height of the screen in pixels.
        sim_width: The width of the simulation.
        sim_height: The height of the simulation.
        screen_scaling: The scaling factor for the screen.
        is_rendering: Whether the game is currently rendering.
        toScreenCoords: A function that converts a point from the simulation to the screen.
        toSimCoords: A function that converts a point from the screen to the simulation.
        screen: The pygame screen.
        clock: The pygame clock.
        font: The pygame font.
        time_delta: The time delta.
    
    
    Methods:
        draw_circle: Draws a circle.
        draw_line: Draws a line.
        draw_rectangle: Draws a rectangle.
        draw_text: Draws text.
        reset_screen: Resets the screen.
        show_changes: renders/updates the screen.
    """
    
    def __init__(self, screenx, screeny, sim_width, sim_height) -> None:
        self.screen_width = screenx
        self.screen_height = screeny
        self.sim_width = sim_width
        self.sim_height = sim_height
                
        self.is_rendering = True
        self.coord1 = None
        self.coord2 = None        
        self.toScreenCoords = None
        self.toSimCoords = None
        
        
        self.screen : pygame.surface.Surface = pygame.display.set_mode((screenx, screeny), pygame.RESIZABLE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()  
        pygame.font.init()
        self.fonts = {32:pygame.font.Font('freesansbold.ttf', 32)}
        self.time_delta = 1       
    
    def draw_circle(self, pos: Point, radius: Number, color: Color) -> None:
        pygame.draw.circle(self.screen, color, self.toScreenCoords(pos), radius * self.screen_scaling)
    
    def draw_line(self, p1, p2, color: Color) -> None:
        pygame.draw.line(self.screen, color, self.toScreenCoords(p1), self.toScreenCoords(p2), 2)
    
    def draw_rectangle(self, p1: Point, p2: Point, color: Color) -> None:
        p1 = self.toScreenCoords(p1)
        p2 = self.toScreenCoords(p2)
        rect = pygame.rect.Rect(min(p1[0], p2[0]), min(p2[1], p1[1]), np.abs(p2[0] - p1[0]), np.abs(p2[1] - p1[1]))
        pygame.draw.rect(self.screen, color, rect)
    
    def get_screen_size(self) -> tuple[int, int]:
        return pygame.display.get_surface().get_size()
    
    def draw_text(self, pos=(0,0), text="", color=(255, 255, 255), font_size = 32):
        pos = self.toScreenCoords(pos)
        if (font_size in self.fonts):
            font = self.fonts[font_size]
        else:
            self.fonts[font_size] = pygame.font.Font('freesansbold.ttf', font_size)
            font = self.fonts[font_size]
            
        rendered_text = font.render(str(text), True, color)
        text_rect = rendered_text.get_rect()
        text_rect.center = (pos[0], pos[1])
        self.screen.blit(rendered_text, text_rect)

    def reset_screen(self) -> pygame.event.Event:
        """
        Manages the size of the sim field and the events
        """
        
        start_time = time.time()     
            
        self.screen_width, self.screen_height = self.get_screen_size()
        
        screen_scaling_x = self.screen_width / self.sim_width
        screen_scaling_y = self.screen_height / self.sim_height
        
        if screen_scaling_x <  screen_scaling_y:
            # pixel per sim unit
            self.screen_scaling =   screen_scaling_x
            
            sim_field_x_offset = 0
            sim_field_height = self.sim_height * self.screen_scaling
            sim_field_y_offset = self.screen_height - (self.screen_height - sim_field_height)  / 2      
        else:
            # pixel per sim unit
            self.screen_scaling =   screen_scaling_y
            
            sim_field_y_offset = self.screen_height
            sim_field_width = self.sim_width * self.screen_scaling
            sim_field_x_offset = (self.screen_width - sim_field_width)  / 2
        
        self.toScreenCoords = lambda pos: [(pos[0]) * self.screen_scaling + sim_field_x_offset, (-pos[1]) * self.screen_scaling + sim_field_y_offset]
        self.toSimCoords = lambda pos: [(pos[0] - sim_field_x_offset) * (1/self.screen_scaling), (-pos[1] + sim_field_y_offset) * (1/self.screen_scaling)]
        
        # rendering
        self.screen.fill((0, 0, 0))
        
        origin_point = (0,0)  
        top_right = (self.sim_width, self.sim_height)

        self.draw_rectangle(origin_point, top_right, (100, 100, 100))

        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = self.toSimCoords(event.pos)
                # print(pos)
                # if (self.coord1 == None):
                #     self.coord1 = pos
                # elif (self.coord2 == None):
                    # self.coord2 == pos
                    # self.shoot_balls()
                    
                    # self.coord1 = None
                    # self.coord2 = None

        fps = self.fonts[32].render(str(round(1 / self.time_delta)), True, (255, 255, 255))
        textRect = fps.get_rect()
        textRect.center = (50, 20)    
        self.screen.blit(fps, textRect)


        # pygame.display.flip()

        end_time = time.time()
        self.time_delta = end_time - start_time + 0.001
        
        return events
    
    def show_changes(self):
        pygame.display.flip()
  
class GridCell:
    """
    Value is if the grid item is a collision type
    
    type:
    0=niks
    
    1=blokje
    2=opening rechts boven
    3=opening rechts onder
    4=opening links boven
    5=opening links onder
    6=cirkel (nu niks mee doen maar wel positie kunnen herkennen (altijd midden in een blokje met een radius 0.45))
    
    -1=Dublicate
    -2=death
    -3=Extra ball
    -4=floor bounce
    -5=Horizontal line
    -6=Vertical line
    -7=Horizontal line and Vertical line
    -8=random direction up
    -9=bigger
    -10=smaller
    -11=Boost
    -12=Shield

    """
    def __init__(self, value: Number=0, type: Number=0, pos: Point=(0,0)) -> None:
        self.pos = pos
        self.value = value
        self.type = type
        self.is_used = False

    def __repr__(self):
        return f'GridCell(value={self.value}, type={self.type}, pos={self.pos})'
    
    def move(self, x: Number, y: Number):
        self.pos.x += x
        self.pos.y += y
    
    @property
    def is_collidable(self) -> bool:
        return self.type >= 1 and self.type <=6
    @property
    def is_powerup(self) -> bool:
        return self.type <= -1 and self.type >=-11

class GameGrid():
    def __init__(self,sizex: int = 7, sizey: int = 9) -> None:
        self.grid: list[list[GridCell]] = [[GridCell(0, 0, Point(col, row)) for col in range(int(sizex))] for row in range(int(sizey))]
    
    @property
    def size(self) -> list[int, int]:
        y = len(self.grid)
        if (y > 0):
            x = len(self.grid[0])
        else:
            x = 0
        return [x, y]
    
    @property
    def flipped_grid(self) -> list[list[GridCell]]:
        return [self.grid[self.size[1] - i] for i in range(self.size[1])]
    
    def __getitem__(self, index):        
        return self.grid[index]

    # def __setitem__(self, index, value):
    #     self.grid[self.size[1] - index] = value



class GameBall(Ball):
    def __init__(self, x: Number = 0, y: Number = 0, vx: Number = 0, vy: Number = 0, radius: Number = 1, id="-1", is_clone:bool = False) -> None:
        super().__init__(x, y, vx, vy, radius, id)
        self.double_bounce = False
        self.has_bounced = False
        self.is_clone = is_clone
        self.size = 1
        self.is_boosted = False
        self.is_shielded = False

class PowerupBall(Ball):
    def __init__(self, x: Number = 0, y: Number = 0, radius: Number = 0.4, id="-1", grid_cell:GridCell=None) -> None:
        super().__init__(x, y, 0, 0, radius, id)
        self.grid_cell = grid_cell

class Game:

    def __init__(self, level: Number= 1, grid_size: tuple=(7,9)) -> None:
        self.level = level
        self.reset_grid(grid_size)
        self.check_point = 1
        self.ball_amount = level
        
        self.events = []
        
        self.click1: Point = None
        self.click2: Point = None
        
        self.shoot_ball_size = 0.15
        self.ball_speed = 0.5
        
        self.round_state = 'point'
        self.shot_balls = 0
        self.shoot_direction = None
        self.last_shot_ball: GameBall = None
        self.shoot_lines = []
        self.spawnings = []
        
        self.start_time = time.time()
        
        self.environment = PhysicsEnvironment(self.grid.size[0], self.grid.size[1], step_size=10)
        self.renderer = Renderer(500, 400, self.grid.size[0], self.grid.size[1])
        
        self.calculate_lines()

    
    def render_game(self) -> pygame.event.Event:
        events = self.renderer.reset_screen()

        rows = int(self.grid.size[1]) - 1

        shoot_point = Point(self.grid.size[0] / 2, self.shoot_ball_size)

        if (self.click1 != None and self.click2 != None):
            
            for line in self.shoot_lines:
                self.renderer.draw_line(line.p1, line.p2, (0, 255, 0))

            
            # direction = Vector(self.click2 - self.click1)
            # direction_point = direction.unit_vector * 100
            # self.renderer.draw_line(shoot_point, direction_point, (0, 255, 0))
        
        self.renderer.draw_circle(shoot_point, 0.2, (255, 0,0))

        powerup_color = {
            -1: (255, 0, 0),
            -2: (255, 83, 0),
            -3: (255, 165, 0),
            -4: (255, 210, 0),
            -5: (255, 255, 0),
            -6: (128, 192, 0),
            -7: (0, 128, 0),
            -8: (0, 64, 128),
            -9: (0, 0, 255),
            -10: (38, 0, 193),
            -11: (75, 0, 130),
        }
        
        for row_index, row in enumerate(self.grid):
            for cell_index, cell in enumerate(row):
                if (cell.type == 1):
                    bottom_left = (cell_index+0.01, rows - row_index +0.01)
                    top_right = (cell_index + 1 - 0.01, rows - row_index + 1 - 0.01)
                    color = (0, 255, 255)
                    self.renderer.draw_rectangle(bottom_left, top_right, color)
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), cell.value,(0,0,0))
                if (cell.is_powerup):
                    self.renderer.draw_circle((cell_index + 0.5, rows- row_index + 0.5), 0.4, powerup_color[cell.type])
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), cell.type, (255, 255,255), font_size=13)
                    
        
        for object in self.environment.objects:
            self.renderer.draw_circle(object.pos, object.radius, (0, 0, 255))

            for vel_arrow in object.vel_lines:
                self.renderer.draw_line(vel_arrow[0], vel_arrow[1], (255, 0, 0))
                
        for line in self.environment.lines:
            self.renderer.draw_line(line.p1, line.p2, (0, 0, 0))

        self.renderer.show_changes()

        return events
    
    def spawn_blocks(self, level):
        index_list = [i for i in range(int(self.grid.size[0]))]
        
        
        powerup_indexes = random.sample(index_list, 2)
        bal_powerup_index = powerup_indexes[int(random.random() * len(powerup_indexes) - 1)]

        # pattern = self.spawn_patterns[random.random() * len(self.spawn_patterns)]
        block_index_list = [x for x in index_list if x not in powerup_indexes]
        
        number_of_blocks = int(round(random.random() * (self.grid.size[0] - 2)))
        chosen_block_indexes = random.sample(block_index_list, number_of_blocks)
        
        new_row = [GridCell((1 if i in chosen_block_indexes else 0) * int(random.random() * 3 + 1) * level, 1 if i in chosen_block_indexes else 0, Point(i, self.grid.size[1])) for i in range(int(self.grid.size[0]))]
        
        for index in powerup_indexes:
            new_row[index].type = -1 * int(random.random() * 10 + 1)
            new_row[index].value = 0
        
        new_row[bal_powerup_index].type = -3
        new_row[bal_powerup_index].value = 0
        
        self.grid.grid[0] = new_row
    
    def move_grid_down(self):
        for row in self.grid:
            for cell in row:
                cell.move(0, -1)
        
        for ball in self.environment.collision_objects:
            ball.pos.y -= 1
            
        self.grid.grid.insert(0, [GridCell(0, 0, Point(col, self.grid.size[1])) for col in range(int(self.grid.size[0]))])
        self.grid.grid.remove(self.grid[-1])    
    
    def calculate_lines(self):
        grid = [[cell.type if cell.is_collidable else 0 for cell in row] for row in self.grid[1:]]
        result = get_lines(grid)        
        
        # 
        lines = [Line(line[0], line[1], grid_cell=self.grid[self.grid.size[1] - data['point'][1]][data['point'][0]])  for data in result for line in data['lines']]

        for ball in self.environment.collision_objects:
            if (ball.grid_cell.is_used):
                self.environment.collision_objects.remove(ball)
                ball.grid_cell.type = 0
                ball.grid_cell.value = 0
                
        for row in self.grid:
            for cell in row:
                if (cell.is_used):
                    cell.type = 0 
                    
        powerups = [cell for row in self.grid.grid for cell in row if cell.is_powerup]
        powerups_circles = [PowerupBall(cell.pos[0] + 0.5, cell.pos[1] + 0.5, radius=0.5, grid_cell= cell) for cell in powerups]
        
        
        
        self.environment.collision_objects = []
        self.environment.collision_objects = powerups_circles
        self.environment.lines = lines + self.environment.border_lines


    
    def horizontal_line(self, y, value=1):
        result = False
        for cell in self.grid[self.grid.size[1] - y]:
            cell:GridCell
            cell.value -= value
            if (cell.value <= 0 and cell.is_collidable):
                cell.type = 0
                result = True

        return result
    
    def vertical_line(self, x: int, value: int=1):
        result = False
        for cell in [self.grid[i][x] for i in range(self.grid.size[0])]:
            cell:GridCell
            cell.value -= value
            if (cell.value <= 0 and cell.is_collidable):
                cell.type = 0
                result = True
        self.renderer.draw_line(Point(x,0), Point(x, self.renderer.sim_height), (255, 255,255))
        return result
        
    def register_collision(self, collision: Collision) -> None:
        responses = []
        
        if (type(collision.object) == Line):
            collision.object : Line
            if (collision.object.id == 'border-under'):
                if (collision.ball.double_bounce):
                    collision.ball.double_bounce = False
                    collision.ball.has_bounced = True
                else:
                    responses.append('remove')

                    
                    
            line_grid_cell = collision.object.grid_cell
            if (line_grid_cell):
                grid_cell: GridCell = line_grid_cell
                if (grid_cell.is_collidable):
                    if (grid_cell.value > 0):
                        grid_cell.value -= 1
                    
                    if (grid_cell.value == 0):
                        grid_cell.type = 0
                        self.calculate_lines()
                        responses.append('recalculate')
                        
        if (isinstance(collision.object, PowerupBall)):
            collision.object : PowerupBall
            collision.ball : GameBall
            grid_cell = collision.object.grid_cell
            responses.append('passthrough')
            match grid_cell.type:
                case -1:
                    if (not collision.ball.is_clone):
                        responses.append('dublicate')
                        grid_cell.is_used = True

                case -2:
                    responses.append('remove')
                    grid_cell.is_used = True

                case -3:
                    grid_cell.type = 0
                    self.environment.collision_objects.remove(collision.object)
                    self.ball_amount += 1
                    grid_cell.is_used = True
                    responses.append('recalculate')
                case -4:
                    if (not collision.ball.has_bounced and not collision.ball.double_bounce):
                        grid_cell.is_used = True
                        collision.ball.double_bounce = True


                case -5:
                    horizontal_result = self.horizontal_line(int(grid_cell.pos[1]))
                    if (horizontal_result):
                        responses.append('recalculate')
                        self.calculate_lines()
                    grid_cell.is_used = True

                case -6:
                    vertical_result = self.vertical_line(int(grid_cell.pos[0]))
                    if (vertical_result):
                        responses.append('recalculate')
                        self.calculate_lines()
                    grid_cell.is_used = True

                case -7:
                    horizontal_result = self.horizontal_line(int(grid_cell.pos[1]))
                    vertical_result = self.vertical_line(int(grid_cell.pos[0]))
                    if (horizontal_result or vertical_result):
                        responses.append('recalculate')
                        self.calculate_lines()
                    grid_cell.is_used = True

                case -8:
                    responses.append('randomdirup')
                    responses.append('recalculate')
                    grid_cell.is_used = True


                case -9:
                    if (collision.ball.size != 2):
                        collision.ball.size *= 2
                        collision.ball.radius *= 2
                        grid_cell.is_used = True

                case -10:
                    if (collision.ball.size != 0.5):
                        collision.ball.size /= 2
                        collision.ball.radius /= 2
                        grid_cell.is_used = True
                case -11:
                    if (not collision.ball.is_boosted):
                        grid_cell.is_used = True
                        collision.ball.is_boosted = True
                case -12:
                    if (not collision.ball.is_shielded):
                        grid_cell.is_used = True
                        collision.ball.is_shielded = True
        return responses

    def shoot_ball(self, ball_num: Number=-1) -> GameBall:
        ball = GameBall(self.grid.size[0] / 2, self.shoot_ball_size + 0.1, self.shoot_direction.x, self.shoot_direction.y, self.shoot_ball_size, str(ball_num))
        self.environment.objects.append(ball)
        self.last_shot_ball = ball
        return ball  
    
    def reset_grid(self, grid_size: tuple[int,int] = (7, 9)):
        self.grid = GameGrid(grid_size[0],grid_size[1])
        


    
    def go_to_last_checkpoint(self):
        self.level = self.check_point
        self.ball_amount = self.check_point
        self.reset_grid()
        self.spawn_blocks(self.level)
        self.move_grid_down()
    
    def start_game(self) -> None:
        while True:
            if (self.round_state == 'point'):

                if (len(self.events) > 0):
                    for event in self.events:
                        
                        if (event.type == pygame.MOUSEBUTTONDOWN):
                            pos = self.renderer.toSimCoords(event.pos)
                            if (self.click1 == None):
                                self.click1 = Point(pos[0], pos[1])
                            # elif (self.click2 == None):
                                self.click2 = Point(pos[0], pos[1])
                                
                        
                        if (event.type == pygame.MOUSEMOTION):
                            pos = self.renderer.toSimCoords(event.pos)
                            if (not self.click1 == None):
                                self.click2 = Point(pos[0], pos[1])
                                direction = Vector(self.click2 - self.click1)

                                touched_bottom = False
                                lines = []
                                ball = Ball(self.grid.size[0] / 2, self.shoot_ball_size + 0.1, direction.x, direction.y, self.shoot_ball_size)
                                for i in range(10):
                                    if (not touched_bottom):
                                        previous_pos = copy.deepcopy(ball.pos)
                                        collisions = self.environment.get_ball_collisions(ball)


                                        
                                        collisions = list(filter(lambda x: not isinstance(x.object, PowerupBall), collisions))
                                        
                                        if (len(collisions) == 0):
                                            touched_bottom = True
                                            continue
                                        
                                        if (collisions[0].object.id == 'border-under'):
                                            touched_bottom = True
                                            continue
                                        
                                        ball.vel = collisions[0].calc_new_vel()
                                        ball.pos = collisions[0].collision_point
                                        lines.append(Line(previous_pos, ball.pos))
                                
                                self.shoot_lines = lines


                        if (event.type == pygame.MOUSEBUTTONUP):
                            if (self.click1 != None and self.click2 != None):
                                direction = Vector(self.click2 - self.click1)

                                if (direction.y > 0):
                                    self.round_state = 'start_shooting'
                                    self.shoot_direction = direction.unit_vector

                                
                            self.click1 = None
                            self.click2 = None
            if (self.round_state == 'shooting'):
                if keyboard.is_pressed('m'):
                    self.environment.objects = []
            
            
            if (self.round_state == 'shooting' and self.last_shot_ball != None and len(self.environment.objects) == 0):
                self.round_state = 'add_bricks'
            
            if (self.round_state == 'add_bricks'):
                if (any(map(lambda cell: cell.value != 0, self.grid[-2]))):
                    print('game over, level: ', str(self.level), ' naar checkpoint: ' + str(self.check_point))
                    self.go_to_last_checkpoint()
                else:
                    self.spawn_blocks(self.level)
                    self.level += 1
                    print('level: ', self.level)
                    self.move_grid_down()


                
                self.calculate_lines()
                self.environment.calc_collisions()
                self.round_state = 'point'
                    
            if (self.round_state == 'start_shooting'):
                self.last_shot_ball = None
                self.shot_balls = 0
                self.spawnings = [BallSpawning(i * 1.5 * (self.shoot_ball_size / self.ball_speed)) for i in range(self.ball_amount)]
                self.round_state = 'shooting'
            
                                
            
            if keyboard.is_pressed(' '):
                run_tick = True
            else:                                         
                run_tick = False
            run_tick = True

            if keyboard.is_pressed('b'):
                self.environment.step_size = 30
            else:                                         
                self.environment.step_size = 10

            self.time_delta = time.time() - self.start_time
            self.start_time = time.time()

            if run_tick:
                self.run_game_tick(self.time_delta)
            
            self.events = self.render_game()

    def calc_active_actions(self, timestep: Number, travelled_time) -> list[Collision]:
        active_collisions : list[Collision] = list(filter(lambda col: col.time_left + travelled_time < self.environment.step_size * timestep,  self.environment.collisions))

        active_spawnings = list(filter(lambda spawning: spawning.time_left + travelled_time < self.environment.step_size * timestep, self.spawnings))
        active_actions = active_collisions + active_spawnings

        active_actions.sort(key=lambda x: x.time_left)
        return active_actions

    def run_game_tick(self, timestep) -> None:
        if (self.round_state == 'point'):
            pass
        
        if (self.round_state in ['shooting']):
            if (self.environment.use_gravity):
                self.environment.apply_gravity(timestep)

            travelled_time = 0
            collisions_per_ball = {}
            collisions_per_ball = {ball: 0 for ball in self.environment.objects}
            
            active_actions = self.calc_active_actions(timestep, travelled_time)

            active_spawnings = list(filter(lambda x: x.time_left < self.environment.step_size * timestep, self.spawnings))

            active_actions += active_spawnings
            
            while len(active_actions) > 0:
                action = active_actions[0]

                if (type(action) == BallSpawning):
                    ball = self.shoot_ball()
                    collisions_per_ball[ball] = 0
                    
                    collision = self.environment.get_first_collision(ball)
                    self.environment.collisions.append(collision)
                    active_actions = self.calc_active_actions(timestep, travelled_time)
                    
                    if (self.environment.circle_collision):
                        self.environment.calc_collisions()
                
                if (type(action) == Collision):
                    collision = action
                    
                    responses = self.register_collision(collision)
                    
                    apply_collision = True
                    # if a it touches a powerup
                    if ('passthrough' in responses):
                        apply_collision = False
                        
                        collision.ball.pos = collision.collision_point + collision.ball.vel * 0.001
                        collision = self.environment.get_first_collision(collision.ball)
                        self.environment.collisions.append(collision)
                        active_actions = self.calc_active_actions(timestep, travelled_time)
                    
                    if ('dublicate' in responses):
                        new_bal_vel = copy.deepcopy(collision.ball.vel)
                        new_bal_vel.rotate(30)
                        collision.ball.vel.rotate(-30)

                        new_ball = GameBall(collision.ball.x, collision.ball.y, new_bal_vel.x, new_bal_vel.y, self.shoot_ball_size, is_clone=True)
                        self.environment.objects.append(new_ball)

                        old_ball_collision = self.environment.get_ball_collisions(collision.ball)                        
                        new_ball_collision = self.environment.get_ball_collisions(new_ball)
                        self.environment.collisions += [old_ball_collision[0], new_ball_collision[0]]

                        active_actions = self.calc_active_actions(timestep, travelled_time)  
                        
                    if ('randomdirup' in responses):
                        # tan 60 = 1.73
                        random_dir = Vector(random.random() * (2 * 1.73) - 1.73, 1).unit_vector * collision.ball.vel.length
                        collision.ball.vel = random_dir
                    
                    
                                          

                    if ('remove' in responses):
                        if (collision.ball in self.environment.objects):
                            self.environment.objects.remove(collision.ball)
                        
                        if (self.environment.circle_collision):
                            self.environment.calc_collisions()
                            active_actions = self.calc_active_actions(timestep, travelled_time)                    
                        apply_collision = False
                    
                    if (apply_collision):
                        ball = collision.ball
                        ball.vel = collision.calc_new_vel() * self.environment.collision_efficiency
                        ball.pos = collision.collision_point
                        
                        # check if the new collision is more urgent
                        collision = self.environment.get_first_collision(ball)

                        if (collision):
                            collisions_per_ball[collision.ball] += 1
                            if (collisions_per_ball[collision.ball] > self.environment.step_size * 10000 * timestep):
                                pass
                            else:
                                self.environment.collisions.append(collision)
                                active_actions = self.calc_active_actions(timestep, travelled_time)
                    
                    if ( 'recalculate' in responses):
                        self.environment.calc_collisions()
                        active_actions = self.calc_active_actions(timestep, travelled_time)
                        
                    
                travelled_time += action.time_left
                
                for ball in self.environment.objects:
                    ball.move_forward(action.time_left * ball.vel.length)
                
                for spawning in self.spawnings:
                    spawning.time_left -= action.time_left
                
                if (action in self.environment.collisions):
                    self.environment.collisions.remove(action)

                if (action in self.spawnings):
                    self.spawnings.remove(action)
                    
                if (action in active_actions):
                    active_actions.remove(action)

            if (travelled_time < self.environment.step_size * timestep):
                movement_time_left = (self.environment.step_size * timestep - travelled_time)
                
                for ball in self.environment.objects:
                    ball.move_forward(movement_time_left * ball.vel.length)

                for spawning in self.spawnings:
                    spawning.time_left -= movement_time_left


            if (self.environment.use_gravity or (self.environment.circle_collision)):
                fix_clipping = self.environment.fix_clipping()   
                if (fix_clipping):     
                    self.environment.calc_collisions()

