import math
import copy
from data_types import *
from oneMoreBrickEngine import Ball, Number, Line
from data_types import Number, Vector, Point, Line
import pygame
import time
import keyboard
from oneMoreBrickGame import *

class Game:
    def start_game(self) -> Number:

        # input from the AI
        # for the ai: Hier moet de AI komen die de shoot_direction (Vector(x, y)) bepaalt en de round_state op 'start_shooting' zet
        # al deze pygame dingen zijn voor de mouse dingen en het klikken enz
        # the ai can you the self.grid.grid = GridCell.value and GridCell.type, the ball amount, the level and the (self.current_shot_x, self.shoot_ball_size) as shoot coordinates

        angle = action * 180 # action is a value ranging from 0 to 1
        radians = math.radians(angle)
        y = math.sin(radians)
        x = math.cos(radians)
        direction = Vector(x, y)
        self.round_state = 'start_shooting'
        self.shoot_direction = direction.unit_vector
        

        # the balls are shooting
        ALL_BALLS_RETURNED = self.last_shot_ball != None and len(self.environment.objects) == 0

        while not ALL_BALLS_RETURNED:
            ALL_BALLS_RETURNED = self.last_shot_ball != None and len(self.environment.objects) == 0
            for ball in self.environment.objects:
                is_outside_game = ball.pos.x < 0.0 + ball.radius or ball.pos.x > self.grid.size[0] - ball.radius or ball.pos.y < 0 + ball.radius or ball.pos.y > self.grid.size[1] - ball.radius
                no_speed = ball.vel.length == 0
                if (is_outside_game or no_speed):
                    self.environment.objects.remove(ball)

            # if any problem would occur it's prolly with the run_game_tick method - srry
            self.time_delta = time.time() - self.start_time
            self.start_time = time.time()    
                
            # for the AI you can make this always be 1 and control the speed with the self.environment.step_size (they both do the same, but timestep is for the changes in frame time and step_size is for the speed of the simulation)
            self.run_game_tick(self.time_delta)
                      
        self.environment.objects = []
            
        
        # adding the new bricks
        for row in self.grid:
            for cell in row:
                if (cell.is_used):
                    cell.type = 0
                        
        if (any(map(lambda cell: cell.value != 0, self.grid[-2]))):
            if (self.use_agent):
                return self.level
            print('game over, level: ', str(self.level), ' naar checkpoint: ' + str(self.check_point))
            self.go_to_last_checkpoint()
        else:
            self.spawn_new_row(self.level)
            self.level += 1
            if (not self.use_agent):
                print('level: ', self.level)
            self.move_grid_down()


        
        self.calculate_lines()
        self.environment.calc_collisions()
        if (self.next_shot_x != -1):
            self.current_shot_x = self.next_shot_x
        
        self.next_shot_x = -1

        # prepare for shooting
        self.last_shot_ball = None
        self.shot_balls = 0
        self.spawnings = [BallSpawning(i * 1.5 * (self.shoot_ball_size / self.ball_speed)) for i in range(self.ball_amount)]

        
        
    def get_observation(self):
        data = []
        for row in self.grid:
            for cell in row:
                data += [cell.type, cell.value]
        
        data.append(self.ball_amount)
        data.append(self.current_shot_x)
        return data