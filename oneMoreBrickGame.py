"""The game class and components
    
    Author: Merc4tor
"""


import numpy as np
from typing import Union, Any
import math
import copy
from data_types import *
from oneMoreBrickEngine import Ball, Collision, PhysicsEnvironment, Line
from data_types import Vector, Point, Line
import pygame
from pygame import Color
import time
import keyboard
import random


Number = Union[int, float]

class BallSpawning:
    def __init__(self, time: Number) -> None:
        self.time_left = time
    
    def __repr__(self) -> str:
        return f'BallSpawning(time_left: {self.time_left})'
    

class Renderer:
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
        
        
        self.screen : pygame.display = pygame.display.set_mode((screenx, screeny), pygame.RESIZABLE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()  
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
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
    
    def draw_text(self, pos=(0,0), text="", color=(255, 255, 255)):
        pos = self.toScreenCoords(pos)
        rendered_text = self.font.render(str(text), True, color)
        text_rect = rendered_text.get_rect()
        text_rect.center = (pos[0], pos[1])
        self.screen.blit(rendered_text, text_rect)

    def update_screen(self) -> None:
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

        fps = self.font.render(str(round(1 / self.time_delta)), True, (255, 255, 255))
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
    def __init__(self, value: Number=0, type: Number=0) -> None:
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
        """
        self.value = value
        self.type = type
    
    def __repr__(self):
        return f'GridCell(value={self.value}, type={self.type})'
    
    @property
    def is_collidable(self) -> bool:
        return self.type >= 1 and self.type <=6
    @property
    def is_upgrade(self) -> bool:
        return self.type <= -1 and self.type >=-10

class Game:
    def __init__(self, level: Number= 1, grid_size: tuple=(7,9)) -> None:
        self.level = level
        self.grid_size = Point(grid_size[0], grid_size[1])
        self.reset_grid()
        self.check_point = 1
        self.ball_amount = level
        
        self.events = []
        
        self.click1: Point = None
        self.click2: Point = None
        
        self.shoot_ball_size = 0.25
        self.ball_speed = 0.5
        
        self.round_state = 'point'
        self.shot_balls = 0
        self.shoot_direction = None
        self.last_shot_ball: Ball = None
        
        self.spawnings = []
        
        self.start_time = time.time()
        
        self.environment = PhysicsEnvironment(self.grid_size.x, self.grid_size.y, step_size=10)
        self.renderer = Renderer(500, 400, self.grid_size.x, self.grid_size.y)
    
    def render_game(self) -> pygame.event.Event:
        events = self.renderer.update_screen()

        rows = int(self.grid_size[1]) - 1

        for row_index, row in enumerate(self.grid):
            for cell_index, cell in enumerate(row):
                if (cell.type == 1):
                    bottom_left = (cell_index+0.01, rows - row_index +0.01)
                    top_right = (cell_index + 1 - 0.01, rows - row_index + 1 - 0.01)
                    color = (0, 255, 255)
                    self.renderer.draw_rectangle(bottom_left, top_right, color)
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), cell.value,(0,0,0))
                
        
        for object in self.environment.objects:
            self.renderer.draw_circle(object.pos, object.radius, (0, 0, 255))

            for vel_arrow in object.vel_lines:
                self.renderer.draw_line(vel_arrow[0], vel_arrow[1], (255, 0, 0))
                
        for line in self.environment.lines:
            self.renderer.draw_line(line.p1, line.p2, (0, 0, 0))

        self.renderer.show_changes()

        return events
    
    def calculate_lines(self) -> None:
        pass
    
    def register_collision(self, collision: Collision) -> None:
        responses = []
        
        if (type(collision.object) == Line):
            collision.object : Line
            if (collision.object.id == 'border-under'):
                responses.append('remove')

            line_grid_cell = collision.object.grid_cell
            if (line_grid_cell):
                grid_cell: GridCell = self.grid[line_grid_cell.y][line_grid_cell.x]
                
                if (grid_cell.is_collidable):
                    if (grid_cell.value > 0):
                        grid_cell.value -= 1
                    
                    if (grid_cell.value == 0):
                        grid_cell.type = 0
                        self.calculate_lines()
                        responses.append('recalculate')

        return responses

    def shoot_ball(self, ball_num: Number=-1) -> Ball:
        ball = Ball(self.grid_size.x / 2, self.shoot_ball_size + 0.1, self.shoot_direction.x, self.shoot_direction.y, self.shoot_ball_size, str(ball_num))
        self.environment.objects.append(ball)
        self.last_shot_ball = ball
        return ball  
    
    def reset_grid(self):
        self.grid = [[GridCell(0, 0) for _ in range(int(self.grid_size[0]))] for _ in range(int(self.grid_size[1]))]

    def spawn_blocks(self):
        # pattern = self.spawn_patterns[random.random() * len(self.spawn_patterns)]
        index_list = [i for i in range(int(self.grid_size[0]))]
        number_of_blocks = int(round(random.random() * (self.grid_size[0] - 1) + 1))
        chosen_indexes = random.sample(index_list, number_of_blocks)
        
        
        new_row = [GridCell((1 if i in chosen_indexes else 0) * int(random.random() * 3 + 1) * self.level, 1 if i in chosen_indexes else 0) for i in range(int(self.grid_size[0]))]
        self.grid[0] = new_row
    
    def move_grid_down(self):
        self.grid.insert(0, [GridCell(0, 0) for _ in range(int(self.grid_size[0]))])
        self.grid.remove(self.grid[-1])
    
    def go_to_last_checkpoint(self):
        self.level = self.check_point
        self.ball_amount = self.check_point
        self.reset_grid()
        self.spawn_blocks()
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
                            elif (self.click2 == None):
                                self.click2 = Point(pos[0], pos[1])
                                
                                direction = Vector(self.click2 - self.click1)
                                # print(direction)
                                if (direction.y > 0):
                                    self.shot_balls = 0
                                    self.round_state = 'start_shooting'
                                    self.shoot_direction = direction.unit_vector
                                    
                                self.click1 = None
                                self.click2 = None
            
            if (self.round_state == 'shooting' and self.last_shot_ball != None and len(self.environment.objects) == 0):
                self.round_state = 'add_bricks'
            
            if (self.round_state == 'add_bricks'):
                if (any(map(lambda cell: cell.value != 0, self.grid[-2]))):
                    print('game over, level: ', str(self.level), ' naar checkpoint: ' + str(self.check_point))
                    self.go_to_last_checkpoint()
                else:
                    self.spawn_blocks()
                    self.level += 1
                    print('level: ', self.level)
                    self.move_grid_down()

                
                self.calculate_lines()
                self.round_state = 'point'
                    
            if (self.round_state == 'start_shooting'):
                self.last_shot_ball = None
                self.spawnings = [BallSpawning(i * 1.5 * (self.shoot_ball_size / self.ball_speed)) for i in range(self.ball_amount)]
                self.round_state = 'shooting'
            
            # physics engine handles ball shooting
                    
            
            if keyboard.is_pressed(' '):
                run_tick = True
            else:                                         
                run_tick = False
                
            if keyboard.is_pressed('b'):
                self.environment.step_size = 80
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
                
                if (type(active_actions[0]) == BallSpawning):
                    ball = self.shoot_ball()
                    collisions_per_ball[ball] = 0
                    
                    collision = self.environment.get_first_collision(ball)
                    self.environment.collisions.append(collision)
                    active_actions = self.calc_active_actions(timestep, travelled_time)
                    
                    if (self.environment.circle_collision):
                        self.environment.calc_collisions()
                
                if (type(active_actions[0]) == Collision):
                    responses = self.register_collision(active_actions[0])
                    
                    resume_collision = True
                    
                    if ( 'recalculate' in responses):
                        print('recalculate')
                        self.environment.calc_collisions()
                        active_actions = self.calc_active_actions(timestep)
                    
                    if ('remove' in responses):
                        if (active_actions[0].ball in self.environment.objects):
                            self.environment.objects.remove(active_actions[0].ball)
                        
                        if (self.environment.circle_collision):
                            self.environment.calc_collisions()
                            active_actions = self.calc_active_actions(timestep, travelled_time)                    
                        resume_collision = False

                    if (resume_collision):
                        ball = active_actions[0].ball
                        ball.vel = active_actions[0].calc_new_vel() * self.environment.collision_efficiency
                        ball.pos = active_actions[0].collision_point
                        
                        # check if the new collision is more urgent
                        collision = self.environment.get_first_collision(ball)

                        if (collision):
                            collisions_per_ball[collision.ball] += 1
                            if (collisions_per_ball[collision.ball] > self.environment.step_size * 10000 * timestep):
                                pass
                            else:
                                self.environment.collisions.append(collision)
                                active_actions = self.calc_active_actions(timestep, travelled_time)
                
                travelled_time += active_actions[0].time_left

                for ball in self.environment.objects:
                    ball.move_forward(active_actions[0].time_left * ball.vel.length)
                
                for spawning in self.spawnings:
                    spawning.time_left -= active_actions[0].time_left
                
                if (len(active_actions) > 0):
                    if (active_actions[0] in self.environment.collisions):
                        self.environment.collisions.remove(active_actions[0])

                    if (active_actions[0] in self.spawnings):
                        self.spawnings.remove(active_actions[0])
                        
                    if (active_actions[0] in active_actions):
                        active_actions.remove(active_actions[0])

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