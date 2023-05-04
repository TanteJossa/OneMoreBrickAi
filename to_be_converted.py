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
        while True:
            if (self.round_state == 'point'):
                # for the ai: Hier moet de AI komen die de shoot_direction (Vector(x, y)) bepaalt en de round_state op 'start_shooting' zet
                # al deze pygame dingen zijn voor de mouse dingen en het klikken enz
                # the ai can you the self.grid.grid = GridCell.value and GridCell.type, the ball amount, the level and the (self.current_shot_x, self.shoot_ball_size) as shoot coordinates

                
                if (self.use_agent):
                    data = []
                    for row in self.grid:
                        for cell in row:
                            data += [cell.type, cell.value]
                    
                    data.append(self.ball_amount)
                    data.append(self.current_shot_x)
                    
                    output = self.ai_agent.activate(data)
                    angle = output[0] * 150 + 15
                    radians = math.radians(angle)
                    y = math.sin(radians)
                    x = math.cos(radians)
                    direction = Vector(x, y)
                    self.round_state = 'start_shooting'
                    self.shoot_direction = direction.unit_vector
                
                else:
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
                                    ball = Ball(self.current_shot_x, self.shoot_ball_size + 0.1, direction.x, direction.y, self.shoot_ball_size)
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
                for ball in self.environment.objects:
                    is_outside_game = ball.pos.x < 0.0 + ball.radius or ball.pos.x > self.grid.size[0] - ball.radius or ball.pos.y < 0 + ball.radius or ball.pos.y > self.grid.size[1] - ball.radius
                    no_speed = ball.vel.length == 0
                    if (is_outside_game or no_speed):
                        self.environment.objects.remove(ball)
                    

            
            ALL_BALLS_RETURNED = self.last_shot_ball != None and len(self.environment.objects) == 0
            ALL_CELLS_SHOT = all([cell.value == 0 for row in self.grid.grid for cell in row])
            
            if (self.round_state == 'shooting' and (ALL_BALLS_RETURNED or ALL_CELLS_SHOT)):
                if (ALL_CELLS_SHOT):
                    print('checkpoint at ' + str(self.level))
                    self.check_point = self.level
                self.environment.objects = []
                
                self.round_state = 'add_bricks'
            
            if (self.round_state == 'add_bricks'):
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
                self.round_state = 'point'
                    
            if (self.round_state == 'start_shooting'):
                self.last_shot_ball = None
                self.shot_balls = 0
                self.spawnings = [BallSpawning(i * 1.5 * (self.shoot_ball_size / self.ball_speed)) for i in range(self.ball_amount)]
                self.round_state = 'shooting'

            self.time_delta = time.time() - self.start_time
            self.start_time = time.time()    
                
            # for the AI you can make this always be 1 and control the speed with the self.environment.step_size (they both do the same, but timestep is for the changes in frame time and step_size is for the speed of the simulation)
            self.run_game_tick(self.time_delta)
            
            
            self.events = self.render_game()
