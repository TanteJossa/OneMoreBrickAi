"""
    This is the main engine of the game.
    It is responsible for the following:
    - Collision detection
    - Moving objects
    
    Classes
    - Ball
    - MovingObject
    - PhyisicsEnvoironment
    
    Author: Merc4tor
"""

import numpy as np
from numbers import Number
from typing import Union, Any
import math
import copy
from data_types import *

class MovingObject():
    """
        MovingObject class
        Properties:
        - pos: Point
        - vel: Vector
        
        Methods:
            - move_forward
    """
    def __init__(self,x: Number=0, y: Number=0, vx: Number=0, vy: Number=0) -> None:
        """
            Constructor
            - pos: Point
            - vel: Vector
        """
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
    """ 
        Ball class
        Properties:
        - pos: Point
        - vel: Vector
        - radius: Number
        - id: String
        
        Methods:
            - move_forward
    """
    
    def __init__(self, x: Number=0, y: Number=0, vx: Number=0, vy: Number=0, radius: Number=1, id="-1") -> None:
        """
        Constructor
        - x: x position
        - y: y position
        - vx: x velocity
        - vy: y velocity
        - radius: radius of the ball
        - id: id of the ball
        """
        super().__init__(x, y, vx, vy)
        self.radius = radius
        self.vel_lines = []
        self.id = id
        pass
    
    def move_forward(self, distance: Number=0):
        """
            Move the ball forward
            - distance: distance to move along velocity
        """
        self.pos += self.vel.unit_vector * distance

        pass
    
    def __repr__(self) -> str:
        return f"Ball(id: {self.id}, pos: {self.pos}, vel: {self.vel.unit_vector})"

class Collision():
    """
    Collision class
    Properties:
        - ball: Ball
        - line: Line
        - collision_point: Point
        - touch_point: Point
        - touch_point: Point
        - type: str
        - distance: Number
        
    Methods:
        - is_valid
        - calc_new_vel
    """
    
    def __init__(self, ball: Ball, collision_point: Point, touch_point: Point, type: str='line', new_vel:Vector=None) -> None:
        self.ball = ball
        self.collision_point = collision_point
        self.touch_point = touch_point
        self.type = type
        self.new_vel = new_vel


    def is_valid(self):
        relative_collision_point = self.collision_point - self.ball.pos
        # check if the collision point not in the opposite quadrant
        return not (-1 * self.ball.vel).point_in_quadrant(relative_collision_point)
    
    def calc_new_vel(self):
        """
            Calculate the new velocity of the ball after the collision
            - return: Vector of the new velocity of the ball after the collision.
            - The new velocity is calculated by the following formula:
            - if the collision is with a point:
                - the new velocity is the point between the touch point and the collision point
            - if the collision is with a line:
                - look at the function
        """
        
        
        # the line between the touch point and the collision point flipped by 90 degrees
        
        if (self.type == 'point'):
            new_vel = Vector(self.collision_point - self.touch_point)
        if (self.type == 'line'):
            collision_vec = Vector(self.touch_point.y - self.collision_point.y, self.touch_point.x - self.collision_point.x)
            collision_line = Line(self.touch_point, self.touch_point + collision_vec)
            
            p_1 = collision_line.closest_point(self.ball.pos)
            touch_to_p1 = Vector(self.touch_point.x - p_1.x, self.touch_point.y - p_1.y)

            direction_point = self.ball.pos + 2 * touch_to_p1
            
            new_vel = Vector(direction_point.x - self.collision_point.x, direction_point.y - self.collision_point.y)
        if (self.type == 'circle'):
            # the calculation happens in the intersection
            new_vel = self.new_vel
            
        return new_vel.unit_vector * self.ball.vel.length
        
        
    def __repr__(self):
        return f'Collision(ball={self.ball.id}, collision_point: {self.collision_point} touch_point: {self.touch_point}, distance: {self.distance}, type: {self.type})'
    
    @property
    def distance(self):
        return self.ball.pos.distance(self.collision_point)
    @property
    def time_left(self):
        if (self.ball.vel.length == 0):
            return 0
        return self.distance / self.ball.vel.length


class BallLineInteraction():
    """
    Interaction between a line a a ball
    Properties:
        - ball: Ball
        - line: Line
        - collisions: Collision
            - Sorted by the distance
            - The first collision is the closest one
    
    Methods:
        - calc_collisions
    """
    def __init__(self, ball: Ball, line: Line) -> None:
        """
        Constructor
        - ball: Ball
        - line: Line
        
        The constructor automatically calculates the collisions
        """
        self.ball = ball
        self.line = line
        self.collisions: list[Collision] = []
        self.calc_collisions()

    
    def __repr__(self):
        return 'Interaction(ball: '+self.ball.id+', line: '+str(id(Line))+', collisions: '+ str(self.collisions)+')'
        
    def calc_collisions(self):
        """
            Calculate the collisions between a line and a ball
            The collision is calculated by the following formula:
            - if the ball touches an edge point on his way:
                - the collision point is the point on the movement line that has the distance of the radius to the edge point
                - the touch point is the edge point
            - if the ball touches a line on his way:
                - the collision point is the point between the ball and the line
                - the touch point is the line 
        """        
        
        # a vector line
        ball_movement_line = Line(self.ball.pos, self.ball.pos + self.ball.vel)
                        
        

        # 1. the bal touches an edge point on his way
        # check this first because the lines can be parralel, then there will be no intersection point
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
                self.collisions.append(Collision(ball=self.ball, collision_point=collision1_point, touch_point=self.line.p1, type='point'))

            if (line_p2_distance < self.ball.radius):
                collision2_point_offset = math.sqrt(self.ball.radius**2 - line_p2_distance**2)
                collision2_point = line_p2_closest - collision2_point_offset * self.ball.vel.unit_vector
                # collision2_distance = collision2_point.distance(self.ball.pos)
                self.collisions.append(Collision(ball=self.ball, collision_point=collision2_point, touch_point=self.line.p2, type='point'))



        p_intersection: Point = self.line.intersection_point(ball_movement_line)
        if p_intersection != False:
            # both lines arent parralel, so a line collision van occur
        
            # 2. the center of the Ball crosses the line
            ball_closest_on_line = self.line.closest_point(self.ball.pos)
            ball_distance = ball_closest_on_line.distance(self.ball.pos)
            
            clostest_to_intersection_vec = Vector(p_intersection - ball_closest_on_line)
            if (ball_distance == 0):
                col_ratio = 1
            else:
                col_ratio = self.ball.radius / ball_distance
            
            touch_point = p_intersection - clostest_to_intersection_vec * col_ratio

            if (self.line.point_on_line(touch_point)):
                # line collision
                distance_touch_to_intersection = touch_point.distance(p_intersection)
                distance_intersection_to_collision = math.sqrt(self.ball.radius**2 + distance_touch_to_intersection**2)
        
                collision_point = p_intersection - self.ball.vel.unit_vector * distance_intersection_to_collision

                self.collisions.append(Collision(ball=self.ball, collision_point=collision_point, touch_point=touch_point, type='line'))

        self.collisions = list(filter(lambda x: x.is_valid(), self.collisions))
        if (len(self.collisions) > 0):
            #because there is only 1 ball, it can be sorted on distance in stead of time left 
            self.collisions.sort(key=lambda x: x.distance)
           
class BallBallInteraction():
    """
    Interaction between a Ball and a ball
    Properties:
        - ball: Ball
        - ball: Ball
        - collisions: Collision
            - Sorted by the distance
            - The first collision is the closest one
    
    Methods:
        - calc_collisions
    """
    def __init__(self, ball: Ball, ball2: Ball) -> None:
        """
        Constructor
        - ball: Ball
        - ball2: Ball
        
        The constructor automatically calculates the collisions
        """
        self.ball = ball
        self.ball2 = ball2
        self.collisions: list[Collision] = []
        self.collision_point : Point= None
        self.ball2_collision_point : Point= None
        self.calc_collisions()

    
    def __repr__(self):
        return 'Interaction(ball: '+self.ball.id+', ball2: '+self.ball2.id+', collisions: '+ str(self.collisions)+')'
        
    def calc_collisions(self):
        """
            Using my own calculations
            https://www.desmos.com/calculator/lorrhfmnyr 
        """        
                        
        pos_delta_x = self.ball2.pos.x - self.ball.pos.x
        vel_delta_x = self.ball2.vel.x - self.ball.vel.x
        pos_delta_y = self.ball2.pos.y - self.ball.pos.y
        vel_delta_y = self.ball2.vel.y - self.ball.vel.y

        total_radius = self.ball.radius + self.ball2.radius
        
        # distance from circle1 at time t to circle2 at time t
        # the pos at time t = start_pos + t * vel
        # solving for t (or check for no collision)
        a = vel_delta_x**2 + vel_delta_y**2
        b = 2 * (pos_delta_x * vel_delta_x + pos_delta_y * vel_delta_y)
        c = pos_delta_x**2 + pos_delta_y**2 - total_radius**2
        
        if a == 0: 
            # distance betweeen balls is 0
            return
        
        determinant = b**2 - 4 * a * c
        
        if determinant < 0: 
            return
        
        collision_time = (-b - math.sqrt(determinant)) / (2 * a) 
        self.collision_point = self.ball.pos + self.ball.vel * collision_time
        self.ball2_collision_point = self.ball2.pos + self.ball2.vel * collision_time
        
        touch_point = self.collision_point + Vector(self.ball2_collision_point - self.collision_point).unit_vector * self.ball.radius

        ball_vel, ball2_vel = self.calc_new_vels()
        
        # line, because the other ball acts as a line
        collision = Collision(ball=self.ball, collision_point=self.collision_point, touch_point=touch_point, type='circle', new_vel=ball_vel)
        collision2 = Collision(ball=self.ball2, collision_point=self.ball2_collision_point, touch_point=touch_point, type='circle', new_vel=ball2_vel)
        
        if (collision.is_valid()):
            self.collisions.append(collision)
        if (collision2.is_valid()):
            self.collisions.append(collision2)
    
    def calc_new_vels(self) -> tuple[Vector, Vector]:
        """
        Calculate the new velocity for the two balls
        """
        
        # https://ericleong.me/research/circle-circle/
        n = Vector(self.ball2_collision_point - self.collision_point).unit_vector
        p = (n * self.ball.vel) - (n * self.ball2.vel)
        # print((n * self.ball.vel.length))
        ball1_new_vel = self.ball.vel - n * p
        ball2_new_vel = self.ball2.vel + n * p
        
        return (ball1_new_vel, ball2_new_vel)
        
        
            
class PhysicsEnvironment():
    """
    The physics environment
    Properties:
        - size: list[int]
        - objects: list[Ball]
        - lines: list[Line]
        - collisions: list[Collision]
        - step_size: float
    
    Methods:
        - calc_collisions
        - get_first_collision
        - run_tick
    
    """
    
    def __init__(self, sizex, sizey, objects=[], lines=[], step_size=0.005, use_gravity:bool=False, circle_collision: bool=False, collision_efficiency: Number= 1) -> None:
        """
        Constructor
        - sizex: int
        - sizey: int
        - objects: list[Ball]
        - lines: list[Line]
        - step_size: float
        
        The constructor automatically calculates the collisions
        """        
        self.step_size = step_size
        self.size : list = [sizex, sizey]
        self.objects :list[Ball] = objects
        self.lines : list[Line] = lines
        self.lines += [Line([0,0], [sizex, 0]), Line([sizex, 0], [sizex, sizey]), Line([sizex, sizey], [0, sizey]), Line([0, sizey], [0, 0]), ]
        self.collisions: list[Collision] = []
        self.use_gravity = use_gravity
        self.circle_collision = circle_collision
        self.collision_efficiency = collision_efficiency
        self.calc_collisions()
    
    def calc_collisions(self):
        # # ball interactions
        # if self.circle_collision:
        #     # every pair exists once
        #     collision_solver_dict = {}
        #     for i in range(len(self.objects)):
        #         collision_solver_dict[self.objects[i]] = self.objects[i+1::]
                
        #     for ball in collision_solver_dict:
        #         for ball2 in collision_solver_dict[ball]:
        #             interaction = BallBallInteraction(ball,ball2)
        #             if (len(interaction.collisions) > 0):
        #                 self.collisions += interaction.collisions
        
        # get the collisions for each ball
        for ball in self.objects:
            collision = self.get_first_collision(ball)
            if (collision):
                self.collisions.append(collision)



                                
        # sort the collsions
        if (len(self.collisions) != 0):            
            self.collisions.sort(key=lambda x: x.time_left)
    
    def get_first_collision(self, ball: Ball) -> Collision:
        collisions = []
        
        for ball2 in self.objects:
            if (ball != ball2):
                interaction = BallBallInteraction(ball,ball2)
                if (len(interaction.collisions) > 0):
                    collisions.append(interaction.collisions[0])
        
        # line interactions
        for line in self.lines:
            interaction = BallLineInteraction(ball,line)
            if (len(interaction.collisions) > 0):
                collisions.append(interaction.collisions[0])

        if (len(collisions) != 0):    
            #because there is only 1 ball, it can be sorted on distance in stead of time left 
            collisions.sort(key=lambda x: x.distance)
            ball.vel_lines = []
            ball.vel_lines.append([ball.pos, collisions[0].collision_point] ) 
            return collisions[0]
        else: 
            return False
    
    def fix_ball_clipping(self):
        for ball in self.objects:
            for ball2 in self.objects:
                distance = ball.pos.distance(ball2.pos)
                if (distance < (ball.radius + ball2.radius)):
                    diff = distance - (ball.radius + ball2.radius)
                    half_diff = diff / 2
                    n = Vector(ball2.pos - ball.pos).unit_vector
                    ball.pos += n * half_diff
                    ball2.pos -= n * half_diff
    
    def fix_clipping(self):
        for i in range(4):
            self.fix_ball_clipping()
        
            for ball in self.objects:
                for line in self.lines:
                    closest_point = line.closest_point(ball.pos)
                    distance = ball.pos.distance(closest_point)
                    if(distance < ball.radius):
                        diff = distance - ball.radius
                        n = Vector(closest_point - ball.pos).unit_vector
                        ball.pos += n * diff
            
    def run_tick(self, timestep=1):
        # self.collisions = []

        # clear the lines
        # for ball in self.objects:
        #     ball.vel_lines = []
        
        if (self.use_gravity):
            for ball in self.objects:
                ball.vel += (0, -1 * self.step_size)
            
        if (self.use_gravity or (self.circle_collision and len(active_collisions_old) > 0)):
            self.collisions = []
            self.calc_collisions()
                
        travelled_time = 0
        collisions_per_ball = {}
        collisions_per_ball = {ball: 0 for ball in self.objects}
        # change the balls movements and positions
        active_collisions : list[Collision] = list(filter(lambda col: col.time_left < self.step_size, self.collisions))
        active_collisions_old = copy.deepcopy(active_collisions)
        while len(active_collisions) > 0:
            ball = active_collisions[0].ball
            ball.vel = active_collisions[0].calc_new_vel() * self.collision_efficiency
            ball.pos = active_collisions[0].collision_point
            
            # check if the new collision is more urgent
            collision = self.get_first_collision(ball)

            if (collision):
                collisions_per_ball[collision.ball] += 1
                if (collisions_per_ball[collision.ball] > self.step_size * 5000):
                    ball.vel.y = 0
                    ball.vel.x = 0
                else:
                    if (collision.time_left < self.step_size):
                        # the collision takes place in the current time step
                        active_collisions.append(collision)
                        active_collisions.sort(key=lambda x: x.time_left)
                    else:
                        # the collision takes place outside this timestep
                        self.collisions.append(collision)
                        self.collisions.sort(key=lambda x: x.time_left)
                        
            for ball in self.objects:
                ball.move_forward(active_collisions[0].time_left * ball.vel.length)
            travelled_time += active_collisions[0].time_left
            if (active_collisions[0] in self.collisions):
                self.collisions.remove(active_collisions[0])
            if (active_collisions[0] in active_collisions):
                active_collisions.remove(active_collisions[0])

        if (travelled_time < self.step_size):
            for ball in self.objects:
                ball.move_forward((self.step_size - travelled_time) * ball.vel.length)

        self.fix_clipping()

        
