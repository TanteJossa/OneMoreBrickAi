import numpy as np
from numbers import Number
from typing import Union, Any
import math
import copy

class Point():
    def __init__(self, x, y) -> None:
        self.pos = np.array([float(x), float(y)])
    
    def __call__(self) -> np.ndarray:
        return self.pos
    
    def __getitem__(self, index):
        return self.pos[index]
    def __setitem__(self, index, val):
        self.pos[index] = val
    def __len__(self):
        return 2  
    
    def distance(self, p: 'Point'):
        return np.abs(np.hypot(p.x - self.x, p.y - self.y))
    
    @property
    def x(self):
        return self.pos[0]
    @property
    def y(self):
        return self.pos[1]
    
    @x.setter
    def x(self,x):
        self.pos[0] = x
    @y.setter
    def y(self, y):
        self.pos[1] = y
    

    def __repr__(self) :
        return f"Point({self.x}, {self.y})"
    
    def format_math_other(self, other) -> list:
        if not hasattr(other,'__len__'):
            other = [other, other]
        return other   
    def __add__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return Point(self.x + other[0], self.y + other[1])
    def __radd__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return self + other
    
    def __sub__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return Point(self.x - other[0], self.y - other[1])
    def __rsub__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return self - other
    
    def __mul__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return Point(self.x * other[0], self.y * other[1])
    def __rmul__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return self * other
    
    def __truediv__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return Point(self.x / other[0], self.y / other[0])
    def __rdiv__(self, other) -> 'Point':
        other = self.format_math_other(other)
        return self / other

class Vector():
    def __init__(self, x: Number | Point, y: Number=0) -> None:
        if type(x) == Point:     
            y = x[1]
            x = x[0]
        if type(x) == Line and type(y) == Line:     
            y = y[1] - x[1]
            x = y[0] - x[0]
        self.value = np.array([x, y])

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    def __getitem__(self, index):
        return self.value[index]
    def __setitem__(self, index, val):
        self.value[index] = val
    def __len__(self):
        return 2    
    def format_math_other(self, other) -> list:
        if not hasattr(other,'__len__'):
            other = [other, other]
        return other    
    def __add__(self, other) -> 'Vector':
        other = self.format_math_other(other)
        return Vector(self.x + other[0], self.y + other[1])
    def __radd__(self, other) -> 'Vector':
        return self + other
    
    def __sub__(self, other) -> 'Vector':
        other = self.format_math_other(other)
        return Vector(self.x - other[0], self.y - other[1])
    def __rsub__(self, other) -> 'Vector':        
        other = self.format_math_other(other)
        return self - other
    
    def __mul__(self, other) -> 'Vector':
        other = self.format_math_other(other)

        return Vector(self.x * other[0], self.y * other[1])
    def __rmul__(self, other) -> 'Vector':
        other = self.format_math_other(other)
        return self * other
    
    def __truediv__(self, other) -> 'Vector':
        other = self.format_math_other(other)
        if (other[0] == 0 or other[1] == 0):
            return self
        return Vector(self.value[0] / other[0], self.value[1] / other[1])
    def __rdiv__(self, other) -> 'Vector':
        other = self.format_math_other(other)
        return self / other
    

    @property
    def x(self):
        return self.value[0]
    
    @property
    def y(self):
        return self.value[1]
    @x.setter
    def x(self,x):
        self.value[0] = x
    
    @y.setter
    def y(self, y):
        self.value[1] = y

    @property
    def length(self) -> Number:
        return np.abs(math.hypot(self.x, self.y))
    
    @property
    def unit_vector(self) -> 'Vector':
        return self / self.length
    
   
class Line():
    def __init__(self, p1: Point, p2: Point) -> None:
        self.type = 'line'
        if type(p1) != Point:
            p1 = Point(p1[0], p1[1])
        if type(p2) != Point:
            p2 = Point(p2[0], p2[1])
        self.p1, self.p2 = p1, p2
    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"
    
    @property
    def x(self) -> Number:
        return self.p2.x - self.p1.x
        
    @property
    def y(self) -> Number:
        return self.p2.y - self.p1.y
    
    @property
    def vec(self) -> Vector:
        return Vector(self.x, self.y)
        
    @property
    def length(self) -> Number:
        return self.p1.distance(self.p2)
    
    @property
    def unit_vector(self) -> np.ndarray:
        return self.vec.value / self.length
    
    def closest_point(self, p: Point):
        (x1, y1), (x2, y2), (x3, y3) = self.p1.pos, self.p2.pos, p.pos
        dx, dy = x2-x1, y2-y1
        det = dx*dx + dy*dy 
        a = (dy*(y3-y1)+dx*(x3-x1))/det
        return Point(x1+a*dx, y1+a*dy)
    
    def intersection_point(self, line: 'Line'):
        (x1,y1), (x2,y2), (x3,y3), (x4,y4) = self.p1, self.p2, line.p1, line.p2
        det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if det != 0:
            px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / det
            py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / det
        
            return Point(px, py)
        else:
            return False

    def intersection(self, line: 'Line'):
        x1, y1 = self.p1
        x2, y2 = self.p2
        x3, y3 = line.p1
        x4, y4 = line.p2

        # Calculate the slopes and y-intercepts of the two lines
        m1 = (y2 - y1) / (x2 - x1)
        b1 = y1 - m1 * x1
        m2 = (y4 - y3) / (x4 - x3)
        b2 = y3 - m2 * x3

        # Check if the lines are parallel
        if m1 == m2:
            return None

        # Calculate the intersection point
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1

        return x, y

    
    def point_on_line(self, point: Point) -> bool:
        cumulative_dist_to_point = point.distance(self.p1) + point.distance(self.p2)

        return math.isclose(cumulative_dist_to_point, self.length)
    
    def move_from_point(self, point: Point, length: Number) -> Point:
        return point - self.unit_vector * length        



class Circle():
    def __init__(self, x: Number=0, y: Number=0, radius: Number=1, mass: Number=1, vx:Number=0, vy:Number=0, rot:Number=0) -> None:
        self.type = 'circle'
        self.pos = Point(x, y)
        self.radius = radius
        self.mass = mass
        self.vel = Vector(vx, vy)
        self.forces = []
        self.rot = 0
        self.vel_lines = []
    
    def __repr__(self) -> str:
        return f"Circle(pos: {self.pos}, vel: {self.vel})"
    
    @property
    def x(self):
        return self.pos.x
    @property
    def y(self):
        return self.pos.y
    @property
    def vx(self):
        return self.vel[0]
    @property
    def vy(self):
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

    def apply_force(self, force: list[Number],timestep=1):
        self.vel = self.vel + np.array(force) / self.mass * timestep
    
    def apply_forces(self, timestep=1):
        for force in self.forces:
            self.apply_force(force, timestep)
    
    def apply_velocity(self, timestep):
        self.pos = self.next_pos(timestep)
    
    def next_pos(self, timestep: Number) -> Point:
        return self.pos + (self.vel * timestep)
    
    def movement_dir(self, timestep) -> Line:
        return Line(self.pos, self.next_pos(timestep))
    
    def line_collision(self, line: Line, movement_dir: Line):
        # check if collision is possible
        # https://ericleong.me/research/circle-line/

        if movement_dir.length == 0:
            return (False, False, False, False)
        
        # cases where a collision could happen:
        could_collide = False
        # The point of intersection between line and the movement vector of the circle. (a)
        p_a = line.intersection_point(movement_dir)
        if p_a == False:

            return (False, False, False, False)

        if (line.point_on_line(p_a) and movement_dir.point_on_line(p_a)):
            could_collide = True

        # The closest point on the line to the endpoint of the movement vector of the circle. (b)
        p_b = line.closest_point(movement_dir.p2)
        if p_b.distance(movement_dir.p2) < self.radius:
            could_collide = True


        # The closest point on the movement vector to (x1, y1). (c)
        p_c = movement_dir.closest_point(line.p1)
        if p_c.distance(line.p1) < self.radius and movement_dir.point_on_line(p_c):
            could_collide = True


        # The closest point on the movement vector to the other endpoint. (d)
        p_d = movement_dir.closest_point(line.p2)
        if p_c.distance(line.p2) < self.radius and movement_dir.point_on_line(p_d):
            could_collide = True

        if could_collide == False:
            return (False, False, False, False)

        # the circle collided
        p_1 = line.closest_point(self.pos)
        collision_point = p_a - self.radius * (p_a.distance(self.pos) / p_1.distance(self.pos)) * movement_dir.unit_vector

        p_c = line.closest_point(p_a)
        if line.point_on_line(p_c):
            # i use my own method but you can should be able to figure it otut
            offset_x = p_a - p_1
            offset_y = self.pos - p_1
            point_on_new_dir = p_a + offset_x + offset_y
            direction = point_on_new_dir - p_a
            direction_norm = Vector(direction).unit_vector
            new_vel = direction_norm * self.vel.length 

        else:
            # edge intersection
            # calculate what endpoint the circle collided with 
            if p_c.distance(line.p1) < p_c.distance(line.p2):
                endpoint = line.p1
            else:
                endpoint = line.p2
            
            closest_point = movement_dir.closest_point(endpoint)
            distance = closest_point.distance(endpoint)  
            
            move_back_distance = math.sqrt(np.abs(self.radius**2 - distance**2))
            collision_point: Point = movement_dir.move_from_point(collision_point, -move_back_distance)
            
            
            movement_dir_norm = Vector(endpoint, collision_point).unit_vector
            new_vel = movement_dir_norm * movement_dir.vec.value

        # 
        movement_dir_left_over_length = movement_dir.p2.distance(collision_point)
        
        return (True, new_vel, collision_point, movement_dir_left_over_length)
    
                

# can have multiple circles
class PhysicsObject():
    def __init__(self, circles: np.ndarray) -> None:
        self.circles = circles
            
class Collision():
    def __init__(self, circle : Circle, line : Line) -> None:
        self.collision_type = collision_type
        if type(obj2) == Circle:
            self.type = 'circle-circle'
            self.circle1 : Circle = copy.deepcopy(circle1)
            self.circle1_dir_length : Number = circle1_dir_length
            self.circle2 : Circle = copy.deepcopy(obj2)
            self.circle2_dir_length : Number = circle2_dir_length
            self.total_radius = self.circle1.radius + self.circle2.radius
        else:
            self.type = 'circle-line'
            self.circle : Circle = circle1
            self.circle_dir_length : Number = circle1_dir_length
            self.line : Line = obj2
        
        self.calc_collision()

    def calc_collision(self) -> 'Collision':
        if (self.type == 'circle-circle'):
            if (self.collision_type == 'continuous'):
                pos_delta_x = self.circle2.pos.x - self.circle1.pos.x
                vel_delta_x = self.circle2.vel.x - self.circle1.vel.x
                pos_delta_y = self.circle2.pos.y - self.circle1.pos.y
                vel_delta_y = self.circle2.vel.y - self.circle1.vel.y
                                
                # distance from circle1 at time t to circle2 at time t
                # the pos at time t = start_pos + t * vel
                # solving for t (or check for no collision)
                a = vel_delta_x**2 + vel_delta_y**2
                b = 2 * (pos_delta_x * vel_delta_x + pos_delta_y * vel_delta_y)
                c = pos_delta_x**2 + pos_delta_y**2 - self.total_radius**2
                
                if a == 0: 
                    return
                
                determinant = b**2 - 4 * a * c
                
                if determinant < 0: 
                    return
                
                self.collision_time = (-b - math.sqrt(determinant)) / (2 * a) 
                print(self.collision_time)
            else:
                if (self.circle1.pos.distance(self.circle2.pos) < self.total_radius):
                    # collided
                    
                    # assumed collision point
                    midpoint = 0.5 * (self.circle1.pos + self.circle2.pos)
                    
                    circle1_to_circle2 = Line(self.circle1.pos, self.circle2.pos)
                    
                    # radius r away from midpoint
                    c1_new_pos = midpoint - self.circle1.radius * circle1_to_circle2.unit_vector
                    c2_new_pos = midpoint - self.circle2.radius * circle1_to_circle2.unit_vector
                    
                    pos_delta = self.circle2.pos - self.circle1.pos
                    vel_delta = self.circle2.vel - self.circle1.vel
                    
                    pos_vel_dir = np.dot(pos_delta, vel_delta) / Vector(pos_delta).length**2 * (pos_delta)
                    
                    total_mass = self.circle1.mass + self.circle2.mass
                    
                    new_c1 = self.circle2.vel - (2 * self.circle2.mass) / total_mass * - pos_vel_dir
                    new_c2 = self.circle1.vel - (2 * self.circle1.mass) / total_mass * pos_vel_dir
                    
                    
                    
                else:
                    return
            
            
        if (self.type == 'circle-line'):
            # check if collision is possible
            # https://ericleong.me/research/circle-line/
                        
            if self.circle_dir_length == 0:
                self.does_collide = False
                return
            
            
            
            # cases where a collision could happen:
            could_collide = False
            # the vector from start to end in the current "timestep"
            movement_delta = (self.circle.vel.unit_vector * self.circle_dir_length)
            self.movement_dir = Line(self.circle.pos, movement_delta.value + movement_delta)
            
            # The point of intersection between line and the movement vector of the circle. (a)
            self.p_intersection = self.line.intersection_point(self.circle.vel)
            # if there is no intersection point the lines are parallel and there will be no collision
            if self.p_intersection == False:
                self.does_collide = False
                return
            
            #  the intersection point is on both of the line segments 
            if (self.line.point_on_line(self.p_intersection) and self.movement_dir.point_on_line(self.p_intersection)):
                could_collide = True

            # The closest point on the line to the endpoint of the movement vector of the circle. (b)
            p_on_line_to_end = self.line.closest_point(self.movement_dir.p2)
            if p_on_line_to_end.distance(self.movement_dir.p2) < self.circle.radius:
                could_collide = True


            # The closest point on the movement vector to (x1, y1). (c)
            self.p_on_move_to_start = self.movement_dir.closest_point(self.line.p1)
            if self.p_on_move_to_start.distance(self.line.p1) < self.circle.radius and self.movement_dir.point_on_line(self.p_on_move_to_start):
                could_collide = True


            # The closest point on the movement vector to the other endpoint. (d)
            self.p_on_move_to_end = self.movement_dir.closest_point(self.line.p2)
            if self.p_on_move_to_start.distance(self.line.p2) < self.radius and self.movement_dir.point_on_line(self.p_on_move_to_end):
                could_collide = True

            if could_collide == False:
                self.does_collide = False
                return
            
            # the circle collided
            self.p_in_line_to_circle = self.line.closest_point(self.circle.pos)
            self.p_collision = self.p_intersection - self.circle.radius * (self.p_intersection.distance(self.circle.pos) / self.p_in_line_to_circle.distance(self.circle.pos)) * movement_dir.unit_vector

            self.collision_time = Line(self.p_collision, self.circle.pos).length / self.circle_dir_length

        return self
        
    
    def calc_collision_data(self):
        self.p_on_line_to_collision = self.line.closest_point(self.p_collision)
        if self.line.point_on_line(self.p_on_line_to_collision):
            # i use my own method but you can should be able to figure it otut
            offset_x = self.p_intersection - self.p_in_line_to_circle
            offset_y = self.circle.pos - self.p_in_line_to_circle
            point_on_new_dir = self.p_intersection + offset_x + offset_y
            direction = point_on_new_dir - self.p_intersection
            direction_norm = Vector(direction).unit_vector
            new_vel = direction_norm * self.circle.vel.length 

        else:
            # edge intersection
            # calculate what endpoint the circle collided with 
            if self.p_on_move_to_start.distance(self.line.p1) < self.p_on_move_to_start.distance(self.line.p2):
                endpoint = self.line.p1
            else:
                endpoint = self.line.p2
            
            closest_point = self.movement_dir.closest_point(endpoint)
            distance = closest_point.distance(endpoint)  
            
            move_back_distance = math.sqrt(np.abs(self.radius**2 - distance**2))
            collision_point: Point = self.movement_dir.move_from_point(collision_point, -move_back_distance)
            
            
            movement_dir_norm = Vector(endpoint, collision_point).unit_vector
            new_vel = movement_dir_norm * self.movement_dir.vec.value

        # 
        movement_dir_left_over_length = self.movement_dir.p2.distance(collision_point)
        
        return (True, new_vel, collision_point, movement_dir_left_over_length)
    
            
class PhysicsEnvironment():
    def __init__(self, sizex, sizey, objects=[], lines=[]) -> None:
        self.collision_efficiency = 90
        self.size : list = [sizex, sizey]
        self.objects :list[PhysicsObject, Circle, Line] = objects
        self.lines : list[Line] = lines
        self.lines += [Line([0,0], [sizex, 0]), Line([sizex, 0], [sizex, sizey]), Line([sizex, sizey], [0, sizey]), Line([0, sizey], [0, 0]), ]
        self.max_collision_per_tick = 3
        
    def run_tick(self, timestep=1):
        # gravity
        for obj in self.objects:
            obj: Circle
            obj.forces.append([0, -1])
            obj.apply_forces(timestep)
            obj.forces = []
            
        for circle in self.objects:
            circle.vel_lines = []
        
        collision_solver_dict = {}
        for i in range(len(self.objects)):
            collision_solver_dict[self.objects[i]] = self.objects[i+1::]
            
        # filter all the times that can not be in range of the obj
        collisions_dict : dict[Circle: list[Circle]]  = {}
        for circle in list(collision_solver_dict):
            circle: Circle
            collisions_dict[circle] = []
            for circle2 in collision_solver_dict[circle]:
                if circle != circle2:
                    collided, norm, depth = self.circle_circle_collision(circle, circle2)
                    
                    if (collided):
                        collisions_dict[circle].append({'obj': circle2, 'norm': norm, 'depth': depth})         

                        # move them out of eachother
                        circle.move(-norm * depth * 0.51)
                        circle2.move(norm * depth * 0.5)
                        
                        u1, u2 = self.circle_collision(circle, circle2)

                        # add forces
                        circle.forces.append(u1)
                        circle2.forces.append(u2)
            
            # real 
            is_colliding = True
            i=0
            sim_circle = copy.deepcopy(circle)
            has_collided = False
            left_over_dir = sim_circle.movement_dir(timestep)
            while is_colliding and i < self.max_collision_per_tick:
                i =  i + 1
                intersection_lines = []
                for line in self.lines:
                    collided, new_vel, collision_point, left_over_dir_length  = sim_circle.line_collision(line, left_over_dir)
                    if collided:
                        has_collided = True
                        intersection_lines.append({'line': line,'new_vel': new_vel, 'collision_point': collision_point, 'left_over_dir_length': left_over_dir_length})

                if len(intersection_lines) > 0:
                    first_collision = sorted(intersection_lines,key=lambda x: x['left_over_dir_length'], reverse=True)[0]
                    new_pos = first_collision['collision_point'] + first_collision['left_over_dir_length'] * first_collision['new_vel'].unit_vector * timestep

                    left_over_dir = Line(first_collision['collision_point'], new_pos)
                    
                    sim_circle.vel = first_collision['new_vel']
                    # sim_circle.pos = first_collision['collision_point']
                else:
                    is_colliding = False
            
            
            
            if (has_collided):
                # get force to get new vel
                vel_diff = sim_circle.vel - circle.vel
                force_to_get_vel = vel_diff * circle.mass / timestep
                effective_force = force_to_get_vel * (self.collision_efficiency / 100)
                circle.forces.append(effective_force)
                circle.pos = first_collision['collision_point'] + sim_circle.vel.unit_vector * 1e-3

            for obj in self.objects:
                obj: Circle
                print('pre', obj.pos, obj.vel)
                obj.apply_forces(timestep)
                obj.apply_velocity(timestep)
                print('post', obj.pos, obj.vel)
                obj.forces = []

    
    


         