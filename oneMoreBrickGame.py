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

class Renderer:
    def __init__(self, screenx, screeny, sim_width, sim_height, environment: PhysicsEnvironment) -> None:
        self.screen_width = screenx
        self.screen_height = screeny
        self.sim_width = sim_width
        self.sim_height = sim_height
                
        self.is_rendering = True
        self.coord1 = None
        self.coord2 = None        
        self.toScreenCoords = None
        self.toSimCoords = None
        
        self.environment = environment
        
        self.screen : pygame.display = pygame.display.set_mode((screenx, screeny), pygame.RESIZABLE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()  
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.time_delta = 1       
    
    def shoot_balls(self) -> None:
        vel = Vector(random.random() * 5.0 - 10, 1.0).unit_vector
        self.environment.objects += [Ball(5, 2, vel.x, vel.y, 1)]
        self.environment.calc_collisions()
    def draw_circle(self, pos: Point, radius: Number, color: Color) -> None:
        pygame.draw.circle(self.screen, color, self.toScreenCoords(pos), radius * self.screen_scaling)
    
    def draw_line(self, p1, p2, color: Color) -> None:
        pygame.draw.line(self.screen, color, self.toScreenCoords(p1), self.toScreenCoords(p2), 2)
    
    def draw_rectangle(self, p1: Point, p2: Point, color: Color) -> None:
        rect = pygame.rect.Rect(min(p1[0], p2[0]), min(p2[1], p1[1]), np.abs(p2[0] - p1[0]), np.abs(p2[1] - p1[1]))
        pygame.draw.rect(self.screen, color, rect)
    
    def get_screen_size(self) -> tuple[int, int]:
        return pygame.display.get_surface().get_size()
    
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
        
        origin_point = self.toScreenCoords((0,0))  
        top_right = self.toScreenCoords((self.sim_width, self.sim_height))

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
                    
  
        for object in self.environment.objects:
            self.draw_circle(object.pos, object.radius, (0, 0, 255))

            for vel_arrow in object.vel_lines:
                self.draw_line(vel_arrow[0], vel_arrow[1], (255, 0, 0))
                
        for line in self.environment.lines:
            self.draw_line(line.p1, line.p2, (0, 0, 0))

        fps = self.font.render(str(round(1 / self.time_delta)), True, (255, 255, 255))
        textRect = fps.get_rect()
        textRect.center = (50, 20)    
        self.screen.blit(fps, textRect)



        pygame.display.flip()
        end_time = time.time()
        self.time_delta = end_time - start_time + 0.001
        
        return events
        

        

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
        self.grid = [[GridCell(0, 0) for _ in range(grid_size[0])] for _ in range(grid_size[1])]
        self.check_point = None
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
        
        self.start_time = time.time()
        
        self.environment = PhysicsEnvironment(self.grid_size.x, self.grid_size.y, step_size=10, game=self)
        self.renderer = Renderer(500, 400, self.grid_size.x, self.grid_size.y, self.environment)
    
    def render_game(self) -> pygame.event.Event:
        return self.renderer.update_screen()
    

    
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
                                print(direction)
                                if (direction.y > 0):
                                    self.shot_balls = 0
                                    self.round_state = 'shooting'
                                    self.shoot_direction = direction.unit_vector
                                    
                                self.click1 = None
                                self.click2 = None

            
            # physics engine handles ball shooting
                    
            
            if keyboard.is_pressed(' '):
                run_tick = True
            else:                                         
                run_tick = False
                
            if keyboard.is_pressed('b'):
                self.environment.step_size = 30
            else:                                         
                self.environment.step_size = 10

            self.time_delta = time.time() - self.start_time
            self.start_time = time.time()

            if run_tick:
                self.environment.run_tick(self.time_delta)
            
            
            self.events = self.render_game()
