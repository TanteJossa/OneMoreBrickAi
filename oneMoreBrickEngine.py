import numpy as np
from numbers import Number
from typing import Union, Any
import math
import copy
from data_types import *

class MovingObject():
    def __init__(self,x: Number=0, y: Number=0, vx: Number=0, vy: Number=0) -> None:
        self.pos = Point(x, y)
        self.vel = Vector(vx, vy)
        pass
    
    @property
    def x(self) -> Number:
        return self.pos.x
    @property
    def y(self) -> Number:
        return self.pos.y
    @property
    def vx(self) -> Number:
        return self.vel[0]
    @property
    def vy(self) -> Number:
        return self.vel[1]
    
    @x.setter
    def x(self,x):
        self.pos[0] = x
    @y.setter
    def y(self, y):
        self.pos[1] = y
    @vx.setter
    def vx(self,vx):
        self.vel[0] = vx
    @vy.setter
    def vy(self, vy):
        self.vel[1] = vy
        
class Ball(MovingObject):
    def __init__(self, x: Number=0, y: Number=0, vx: Number=0, vy: Number=0, radius: Number=1, id="-1") -> None:
        super().__init__(x, y, vx, vy)
        self.radius = radius
        self.vel_lines = []
        self.id = id
        pass
    
    def move_forward(self, distance: Number=0):
        self.pos += self.vel.unit_vector * distance

        pass
    
    def __repr__(self) -> str:
        return f"Ball(pos: {self.pos}, vel: {self.vel.unit_vector})"

class Collision():
    def __init__(self, ball: Ball, line: Line, collision_point: Point, touch_point: Point, type: str='line') -> None:
        self.ball = ball
        self.line = line
        self.collision_point = collision_point
        self.touch_point = touch_point
        self.type = type

    def is_valid(self):
        relative_collision_point = self.collision_point - self.ball.pos
        # print(relative_collision_point, self.ball.vel)
        # check if the collision point not in the opposite quadrant
        return not (-1 * self.ball.vel).point_in_quadrant(relative_collision_point)
    
    def calc_new_vel(self):
        # the line between the touch point and the collision point flipped by 90 degrees
        
        if (self.type == 'point'):
            new_vel = Vector(self.collision_point.x - self.touch_point.x, self.collision_point.y - self.touch_point.y)
        if (self.type == 'line'):
            collision_vec = Vector(self.touch_point.y - self.collision_point.y, self.touch_point.x - self.collision_point.x)
            collision_line = Line(self.touch_point, self.touch_point + collision_vec)
            
            p_1 = collision_line.closest_point(self.ball.pos)
            p_c = collision_line.closest_point(self.collision_point)
            p1_to_pc = Vector(p_1.x - p_c.x, p_1.y - p_c.y)

            direction_point = self.ball.pos - 2 * p1_to_pc
            
            new_vel = Vector(direction_point.x - self.collision_point.x, direction_point.y - self.collision_point.y)
        return new_vel.unit_vector
        
        
    def __repr__(self):
        return 'Collision(ball='+str(self.ball.id)+', line: '+str(id(self.line))+', collision_point: '+str(self.collision_point)+', touch_point: '+str(self.touch_point)+', distance: '+str(self.distance)+')'
    
    @property
    def distance(self):
        return self.ball.pos.distance(self.collision_point)
    

class Interaction():
    def __init__(self, ball: Ball, line: Line) -> None:
        self.ball = ball
        self.line = line
        self.is_colliding = False
        self.collision: Collision
        self.collisions: list[Collision] = []
        self.calc_collision()

    
    def __repr__(self):
        return 'Interaction(ball: '+self.ball.id+', line: '+str(id(Line))+' , collided: '+str(self.is_colliding)+', collisions: '+ str(self.collisions)+')'
        
    def calc_collision(self):
        # a vector line
        ball_movement_line = Line(self.ball.pos, self.ball.pos + self.ball.vel)
        # print(ball_movement_line)
                        
        p_intersection: Point = self.line.intersection_point(ball_movement_line)
        # two lines are the same
        slope_are_the_same = self.line.slope == ball_movement_line.slope or (math.isnan(self.line.slope) and math.isnan(ball_movement_line.slope))
        yintersect_the_same = self.line.y_intersect == ball_movement_line.y_intersect or (math.isnan(self.line.y_intersect) and math.isnan(ball_movement_line.y_intersect))

        lines_are_the_same = slope_are_the_same and yintersect_the_same

        # is vertical
        if ((math.isnan(self.line.slope) and math.isnan(ball_movement_line.slope))):
            if (self.line.p1.x != ball_movement_line.p1.x):
                lines_are_the_same = False

        if (lines_are_the_same):
            if (self.line.p1.distance(self.ball.pos) < self.line.p2.distance(self.ball.pos)):
                # p_intersection = self.line.p1
                collision_point = self.line.p1 - self.ball.vel.unit_vector * self.ball.radius
                self.collisions.append(Collision(ball=self.ball, line=self.line, collision_point=collision_point, touch_point=self.line.p1, type='point'))
            else:
                # p_intersection = self.line.p2
                collision_point = self.line.p2 - self.ball.vel.unit_vector * self.ball.radius
                self.collisions.append(Collision(ball=self.ball, line=self.line, collision_point=collision_point, touch_point=self.line.p2, type='point'))
            self.collisions = list(filter(lambda x: x.is_valid(), self.collisions))
            self.is_colliding = True
            return 
        
        if p_intersection == False:
            # movement vector and line are paralel and can never collide
            return
        
        # 1. the bal touches an edge point on his way
        line_p1_closest = ball_movement_line.closest_point(self.line.p1)
        line_p1_distance = line_p1_closest.distance(self.line.p1)
        line_p2_closest = ball_movement_line.closest_point(self.line.p2)
        line_p2_distance = line_p2_closest.distance(self.line.p2)

        if (line_p1_distance < self.ball.radius or line_p2_distance < self.ball.radius):
            self.collision_type = 'edge'
            
            if (line_p1_distance < self.ball.radius):
                collision1_point_offset = math.sqrt(self.ball.radius**2 - line_p1_distance**2)
                collision1_point = line_p1_closest - collision1_point_offset * self.ball.vel.unit_vector
                # collision1_distance = collision1_point.distance(self.ball.pos)
                self.collisions.append(Collision(ball=self.ball, line=self.line, collision_point=collision1_point, touch_point=self.line.p1, type='point'))

            if (line_p2_distance < self.ball.radius):
                collision2_point_offset = math.sqrt(self.ball.radius**2 - line_p2_distance**2)
                collision2_point = line_p2_closest - collision2_point_offset * self.ball.vel.unit_vector
                # collision2_distance = collision2_point.distance(self.ball.pos)
                self.collisions.append(Collision(ball=self.ball, line=self.line, collision_point=collision2_point, touch_point=self.line.p2, type='point'))
            
        # 2. the center of the Ball crosses the line
        ball_closest_on_line = self.line.closest_point(self.ball.pos)
        ball_distance = ball_closest_on_line.distance(self.ball.pos)
        
        clostest_to_intersection_vec = Vector(p_intersection.x - ball_closest_on_line.x, p_intersection.y - ball_closest_on_line.y)
        
        
        col_ratio = self.ball.radius / ball_distance
        
        touch_point = p_intersection - clostest_to_intersection_vec * col_ratio
        
   
        
        
        if (self.line.point_on_line(touch_point)):
            # line collision
            distance_touch_to_intersection = touch_point.distance(p_intersection)
            distance_intersection_to_collision = math.sqrt(self.ball.radius**2 + distance_touch_to_intersection**2)
     
            collision_point = p_intersection - self.ball.vel.unit_vector * distance_intersection_to_collision

            self.collisions.append(Collision(ball=self.ball, line=self.line, collision_point=collision_point, touch_point=touch_point, type='line'))

        self.collisions = list(filter(lambda x: x.is_valid(), self.collisions))
        if (len(self.collisions) > 0):
            self.collisions.sort(key=lambda x: x.distance)
            self.is_colliding = True
           
            # print(self.collisions)

class PhysicsEnvironment():
    def __init__(self, sizex, sizey, objects=[], lines=[], step_size=0.005) -> None:
        self.step_size = step_size
        self.size : list = [sizex, sizey]
        self.objects :list[Ball] = objects
        self.lines : list[Line] = lines
        self.lines += [Line([0,0], [sizex, 0]), Line([sizex, 0], [sizex, sizey]), Line([sizex, sizey], [0, sizey]), Line([0, sizey], [0, 0]), ]
        self.collisions: list[Collision] = []
        self.max_collision_per_tick = 3
        self.calc_collisions()
    
    def calc_collisions(self):
        # get the collisions for each ball
        for ball in self.objects:
            collision = self.get_first_collision(ball)
            if (collision):
                self.collisions.append(collision)

        # sort the collsions
        if (len(self.collisions) != 0):            
            self.collisions.sort(key=lambda x: x.distance)
    
    def get_first_collision(self, ball: Ball) -> Collision:
        collisions = []
        for line in self.lines:
            interaction = Interaction(ball,line)
            if (len(interaction.collisions) > 0):
                collisions.append(interaction.collisions[0])

        if (len(collisions) != 0):            
            collisions.sort(key=lambda x: x.distance)
            ball.vel_lines = []
            ball.vel_lines.append([ball.pos, collisions[0].collision_point] ) 
            return collisions[0]
        else: 
            return False

            
    def run_tick(self, timestep=1):
        # self.collisions = []

        # clear the lines
        # for ball in self.objects:
        #     ball.vel_lines = []
        

                
        

        # change the balls movements and positions
        active_collisions : list[Collision] = list(filter(lambda col: col.distance < self.step_size, self.collisions))
        while len(active_collisions) > 0:
            ball = active_collisions[0].ball
            left_over_distance = ball.pos.distance(active_collisions[0].collision_point)
            ball.vel = active_collisions[0].calc_new_vel()
            ball.pos = active_collisions[0].collision_point
            
            # check if the new collision is more urgent
            collision = self.get_first_collision(ball)
            
            if (collision):
                if (collision.distance < self.step_size):
                    # the collision takes place in the current time step

                    active_collisions.append(collision)
                    active_collisions.sort(key=lambda x: x.distance)
                else:
                    # the collision takes place outside this timestep
                    self.collisions.append(collision)
                    self.collisions.sort(key=lambda x: x.distance)
                
            for ball in self.objects:
                ball.move_forward(active_collisions[0].distance)
            
            if (active_collisions[0] in self.collisions):
                self.collisions.remove(active_collisions[0])
            if (active_collisions[0] in active_collisions):
                active_collisions.remove(active_collisions[0])


            
        for ball in self.objects:
            if (len(active_collisions) > 0):
                if (ball in [col.ball for col in active_collisions]):
                    # print(self.collisions[0].distance, ball.vel.unit_vector * self.step_size)
                    if (self.collisions[0].distance < (ball.vel.unit_vector * self.step_size).length):
                        left_over_distance = ball.pos.distance(self.collisions[0].collision_point)
                        ball.vel = self.collisions[0].calc_new_vel()
                        ball.pos = self.collisions[0].collision_point - (ball.vel.unit_vector *  left_over_distance)
                
            ball.pos += ball.vel.unit_vector * self.step_size
            

            
            
            



     
    
        