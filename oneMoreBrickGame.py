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
    
    def draw_triangle(self, p1: Point, p2: Point, p3: Point, color: Color) -> None:
        p1 = self.toScreenCoords(p1)
        p2 = self.toScreenCoords(p2)
        p3 = self.toScreenCoords(p3)
        pygame.draw.polygon(self.screen, color, [p1, p2, p3])


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

class CollisionBall(Ball):
    def __init__(self, x: Number = 0, y: Number = 0, radius: Number = 0.4, id="-1", grid_cell:GridCell=None) -> None:
        super().__init__(x, y, 0, 0, radius, id)
        self.grid_cell = grid_cell

