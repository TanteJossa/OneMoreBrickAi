"""The game class and components
    
    Author: Merc4tor
"""


import numpy as np
from typing import Union, Any
import math
import copy
from data_types import *
from oneMoreBrickEngine import Ball, PhysicsEnvironment, Line
from data_types import Vector, Point, Line
import pygame
from pygame import Color
import time
import keyboard
import random


Number = Union[int, float]

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
        
        self.environment = PhysicsEnvironment(sim_width, sim_height, step_size=0.01)
        
        self.screen : pygame.display = pygame.display.set_mode((screenx, screeny), pygame.RESIZABLE)
        pygame.display.flip()
        self.clock = pygame.time.Clock()  
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.time_delta = 1       

        self.loop()
    
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
    
    def loop(self) -> None:
        while self.is_rendering == True:
            start_time = time.time()     
                
            self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
            
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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_rendering = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = self.toSimCoords(event.pos)
                    if (self.coord1 == None):
                        self.coord1 = pos
                    elif (self.coord2 == None):
                        self.coord2 == pos
                        self.shoot_balls()
                        
                        self.coord1 = None
                        self.coord2 = None
                        
            if keyboard.is_pressed(' '):
                run_tick = True
            else:                                         
                run_tick = False
                                                            
            if run_tick:
                self.environment.run_tick(self.time_delta)
            
                
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

class Game:
    def __init__(self, level: Number= 1, grid_size: tuple=(7,9)) -> None:
        self.level = level
        self.grid = [[GridCell(0, 0) for _ in range(grid_size[0])] for _ in range(grid_size[1])]
        self.check_point = None
        self.ball_amount = level
        self.start_game()
    
    def render_game(self) -> None:
        self.renderer = Renderer(500, 400, 10, 10)
    
    def start_game(self) -> None:
        self.render_game()