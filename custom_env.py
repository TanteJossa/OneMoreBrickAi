# dependencies for the environment
import gym
from gym import spaces

# dependencies for the game
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
from oneMoreBrickGame import *


class CustomEnv(gym.Env):
    """
    Custom Environment that follows gym interface

    Everything after the helper functions comment has solely to do with the game itself.
    """

    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(N_CHANNELS, HEIGHT, WIDTH), dtype=np.uint8)

    def step(self, action):
        ...
        info = {}
        return observation, reward, done, info

    # observation needs to be returned
    def reset(self):
        self.level = 1
        self.reset_grid((7, 9))
        self.check_point = 1
        self.ball_amount = 1
        
        self.ai_agent = None
        self.use_agent = False

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
        
        self.powerup_size = 0.2
        self.collision_ball_size = 0.4
        
        self.start_time = time.time()
        self.current_shot_x = self.grid.size[0] / 2
        # actually first shot
        self.next_shot_x = self.grid.size[0] / 2

        # for the AI you should change the step_size to a value as high as possible without your computer crashing 
        self.environment = PhysicsEnvironment(self.grid.size[0], self.grid.size[1], step_size=10)

        if (not self.use_agent):
            self.renderer = Renderer(500, 400, self.grid.size[0], self.grid.size[1])

        self.spawn_new_row(self.level)
        self.move_grid_down()
        self.calculate_lines()


        return observation  # reward, done, info can't be included

    def render(self):
        rows = int(self.grid.size[1]) - 1

        shoot_point = Point(self.current_shot_x, self.shoot_ball_size)

        if (self.click1 != None and self.click2 != None):
            # point lines
            for line in self.shoot_lines:
                self.renderer.draw_line(line.p1, line.p2, (0, 255, 0))
        
        self.renderer.draw_circle(shoot_point, 0.2, (255, 0,0))

        powerup_color = {
            -1: (155, 0, 0),
            -2: (155, 83, 0),
            -3: (155, 165, 0),
            -4: (155, 210, 0),
            -5: (155, 255, 0),
            -6: (128, 192, 0),
            -7: (0, 128, 0),
            -8: (0, 64, 128),
            -9: (0, 0, 255),
            -10: (38, 0, 193),
            -11: (75, 0, 130),
            -11: (75, 0, 130),
        }
        
        powerup_text = {
            -1: 'splt',
            -2: 'del',
            -3: '+',
            -4: 'bnce',
            -5: 'hor',
            -6: 'ver',
            -7: 'cross',
            -8: 'rand',
            -9: 'big',
            -10: 'small',
            -11: 'boost',
            -12: 'shield',
        }
        
        # render cells
        for row_index, row in enumerate(self.grid):
            for cell_index, cell in enumerate(row):
                # block or triangle
                color = (0, 255, 255)

                if (cell.type == 1):
                    bottom_left = (cell_index+0.01, rows - row_index +0.01)
                    top_right = (cell_index + 1 - 0.01, rows - row_index + 1 - 0.01)
                    self.renderer.draw_rectangle(bottom_left, top_right, color)
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), cell.value,(0,0,0))
                
                if (cell.type == 2):
                    p1 = Point(cell_index, rows- row_index)
                    p2 = Point(cell_index, rows- row_index + 1)
                    p3 = Point(cell_index + 1, rows- row_index)
                    self.renderer.draw_triangle(p1, p2, p3, color )
                    self.renderer.draw_text((cell_index + 0.2, rows- row_index + 0.2), cell.value,(0,0,0), 20)
                if (cell.type == 3):
                    p1 = Point(cell_index, rows- row_index)
                    p2 = Point(cell_index, rows- row_index + 1)
                    p3 = Point(cell_index + 1, rows- row_index + 1)
                    self.renderer.draw_triangle(p1, p2, p3, color )
                    self.renderer.draw_text((cell_index + 0.2, rows- row_index + 0.6), cell.value,(0,0,0), 20)
                if (cell.type == 4):
                    p1 = Point(cell_index, rows- row_index)
                    p2 = Point(cell_index + 1, rows- row_index)
                    p3 = Point(cell_index + 1, rows- row_index + 1)
                    self.renderer.draw_triangle(p1, p2, p3, color )
                    self.renderer.draw_text((cell_index + 0.7, rows- row_index + 0.2), cell.value,(0,0,0), 20)
                if (cell.type == 5):
                    p1 = Point(cell_index + 1, rows- row_index + 1)
                    p2 = Point(cell_index + 1, rows- row_index)
                    p3 = Point(cell_index, rows- row_index + 1)
                    self.renderer.draw_triangle(p1, p2, p3, color )
                    self.renderer.draw_text((cell_index + 0.7, rows- row_index + 0.6), cell.value,(0,0,0), 20)

                if (cell.type == 6):
                    self.renderer.draw_circle((cell_index + 0.5, rows- row_index + 0.5), self.collision_ball_size, color)
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), cell.value,(0,0,0), 20)

                # powerup
                if (cell.is_powerup):
                    self.renderer.draw_circle((cell_index + 0.5, rows- row_index + 0.5), self.powerup_size, powerup_color[cell.type])
                    self.renderer.draw_text((cell_index + 0.5, rows- row_index + 0.5), powerup_text[cell.type], (255, 255,255), font_size=13)
                    
        # render shootings balls
        for object in self.environment.objects:
            self.renderer.draw_circle(object.pos, object.radius, (0, 0, 255))

            for vel_arrow in object.vel_lines:
                self.renderer.draw_line(vel_arrow[0], vel_arrow[1], (255, 0, 0))
        
        # render bound lines
        for line in self.environment.lines:
            self.renderer.draw_line(line.p1, line.p2, (0, 0, 0))

        # update screen
        self.renderer.show_changes()

    # HELPER FUNCTIONS FOR THE GAME
    # I'm not gonna rewrite them

    def spawn_new_row(self, level):
        index_list = [i for i in range(int(self.grid.size[0]))]

        # 2 is the number of powerups in a row (including the new ball)
        powerup_indexes = random.sample(index_list, 2)
        bal_powerup_index = powerup_indexes[int(random.random() * len(powerup_indexes) - 1)]

        block_index_list = [x for x in index_list if x not in powerup_indexes]
        
        number_of_blocks = int(round(random.random() * (self.grid.size[0] - 2)))
        chosen_block_indexes = random.sample(block_index_list, number_of_blocks)
        # 
        new_row = [GridCell((1 if i in chosen_block_indexes else 0) * int(random.random() * 3 + 1) * level, int(random.random() * 5 + 1) if i in chosen_block_indexes else 0, Point(i, self.grid.size[1])) for i in range(int(self.grid.size[0]))]
        
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
                    
        powerups = [cell for row in self.grid.grid for cell in row if cell.is_powerup]
        powerups_circles = [PowerupBall(cell.pos[0] + 0.5, cell.pos[1] - 0.5, radius=self.powerup_size, grid_cell= cell) for cell in powerups]
        
        balls_cell = [cell for row in self.grid.grid for cell in row if cell.type == 6]
        collision_balls = [CollisionBall(cell.pos[0] + 0.5, cell.pos[1] - 0.5, radius=self.collision_ball_size, grid_cell=cell) for cell in balls_cell]

        self.environment.collision_objects = []
        self.environment.collision_objects = powerups_circles + collision_balls
        self.environment.lines = lines + self.environment.border_lines

    def horizontal_line(self, y, value=1):
        result = False
        for cell in self.grid[self.grid.size[1] - y]:
            cell:GridCell
            if (cell.is_collidable):
                cell.value -= value
                if (cell.value <= 0):
                    cell.type = 0
                    result = True

        return result
    
    def vertical_line(self, x: int, value: int=1):
        result = False
        for cell in [self.grid[i][x] for i in range(self.grid.size[0])]:
            cell:GridCell
            if (cell.is_collidable):

                cell.value -= value
                if (cell.value <= 0):
                    cell.type = 0
                    result = True
                
        # self.renderer.draw_line(Point(x,0), Point(x, self.renderer.sim_height), (255, 255,255))
        return result
    
    def register_collision(self, collision: Collision) -> None:
        responses = []
        col_grid_cell = None
        if (type(collision.object) == Line):
            collision.object : Line
            if (collision.object.id == 'border-under'):
                if (collision.ball.double_bounce):
                    collision.ball.double_bounce = False
                    collision.ball.has_bounced = True
                else:
                    responses.append('remove')
                    if (self.next_shot_x == -1):
                        self.next_shot_x = collision.collision_point.x

            col_grid_cell = collision.object.grid_cell
        
        if (isinstance(collision.object, CollisionBall)):                    
            col_grid_cell = collision.object.grid_cell

        if (col_grid_cell):
            grid_cell: GridCell = col_grid_cell
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
        ball = GameBall(self.current_shot_x, self.shoot_ball_size + 0.1, self.shoot_direction.x, self.shoot_direction.y, self.shoot_ball_size, str(ball_num))
        self.environment.objects.append(ball)
        self.last_shot_ball = ball
        return ball 
    
    def reset_grid(self, grid_size: tuple[int,int] = (7, 9)):
        self.grid = GameGrid(grid_size[0],grid_size[1])

    # NEEDS TO BE REMOVED THERE ARE NO CHECKPOINTS
    # def go_to_last_checkpoint(self):
        # self.level = self.check_point
        # self.ball_amount = self.check_point
        # self.reset_grid()
        # self.spawn_new_row(self.level)
        # self.move_grid_down()

    def calc_active_actions(self, timestep: Number, travelled_time) -> list[Collision]:
        if (timestep == -1):
            # print(self.environment.collisions)
            active_actions = self.environment.collisions + self.spawnings
        else:
            active_collisions : list[Collision] = list(filter(lambda col: col.time_left + travelled_time < self.environment.step_size * timestep,  self.environment.collisions))

            active_spawnings = list(filter(lambda spawning: spawning.time_left + travelled_time < self.environment.step_size * timestep, self.spawnings))
            active_actions = active_collisions + active_spawnings
        
        active_actions.sort(key=lambda x: x.time_left)
        active_actions = list(filter(lambda x: x, active_actions))
        return active_actions
    
    def run_game_tick(self, timestep) -> None:
        if (self.round_state == 'point'):
            pass
        
        if (self.round_state in ['shooting']):
            if (self.environment.use_gravity):
                self.environment.apply_gravity(timestep)

            # reset the travelled time in this game_tick
            travelled_time = 0
            
            # if a ball is stuck it would collide forever
            # giving a ball a max collision count fixes this
            collisions_per_ball = {}
            collisions_per_ball = {ball: 0 for ball in self.environment.objects}
            
            # a timestep of -1 returns all the events
            
            # gets the collisions and ball spawnings in the current time step
            active_actions = self.calc_active_actions(timestep, travelled_time)

            # execute all collision in the current time step
            while len(active_actions) > 0:

                action = active_actions[0]

                if (type(action) == BallSpawning):
                    ball = self.shoot_ball()
                    collisions_per_ball[ball] = 0
                    

                    if (self.environment.circle_collision):
                        self.environment.calc_collisions()
                    else:
                        collision = self.environment.get_first_collision(ball)

                        if (collision):
                            self.environment.collisions.append(collision)
                    
                    active_actions = self.calc_active_actions(timestep, travelled_time)

                if (type(action) == Collision):
                    collision = action
                    
                    responses = self.register_collision(collision)

                    apply_collision = True
                    # if a it touches a powerup
                    if ('passthrough' in responses):
                        apply_collision = False
                        
                        collision.ball.pos = collision.collision_point + collision.ball.vel * 0.001
                        new_collision = self.environment.get_first_collision(collision.ball)
                        if (new_collision):
                            self.environment.collisions.append(new_collision)
                            active_actions = self.calc_active_actions(timestep, travelled_time)
                    
                    if ('dublicate' in responses):
                        new_bal_vel = copy.deepcopy(collision.ball.vel)
                        new_bal_vel.rotate(30)
                        collision.ball.vel.rotate(-30)

                        new_ball = GameBall(collision.ball.x, collision.ball.y, new_bal_vel.x, new_bal_vel.y, self.shoot_ball_size, is_clone=True)
                        self.environment.objects.append(new_ball)

                        old_ball_collision = self.environment.get_ball_collisions(collision.ball)                        
                        new_ball_collision = self.environment.get_ball_collisions(new_ball)
                        if (len(old_ball_collision) > 0):
                            self.environment.collisions.append(old_ball_collision[0])
                        if (len(new_ball_collision) > 0):
                            self.environment.collisions.append(new_ball_collision[0])

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
                            if (collision.ball not in collisions_per_ball):
                                collisions_per_ball[collision.ball] = 0

                            collisions_per_ball[collision.ball] += 1
                            
                            if (timestep == -1):
                                allowed_collision_num = 1000
                            else:
                                allowed_collision_num = self.environment.step_size * 10000 * timestep
                                                        
                            if (collisions_per_ball[collision.ball] > allowed_collision_num):
                                if (collision.ball in self.environment.objects):
                                    self.environment.objects.remove(collision.ball)
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

                # active_actions = self.calc_active_actions(timestep, travelled_time)

            if (timestep != -1):
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
