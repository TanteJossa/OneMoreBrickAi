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

    def point_in_quadrant(self, point):
        a, b = self.value
        x, y = point
        
        if (a >= 0 and b >= 0 and 
            x >= 0 and y >= 0):
            return True
        if (a <= 0 and b >= 0 and 
            x <= 0 and y >= 0):
            return True
        if (a >= 0 and b <= 0 and 
            x >= 0 and y <= 0):
            return True
        if (a <= 0 and b <= 0 and 
            x <= 0 and y <= 0):
            return True

        return False


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
        num = (dy*(y3-y1)+dx*(x3-x1))
        # print(det, num)
        if (math.isnan(det) or math.isnan(num) or det == 0 or num == 0):
            a = 0.000001
        else:
            a = (dy*(y3-y1)+dx*(x3-x1))/det

        return Point(x1+a*dx, y1+a*dy)
    
    def intersection_point(self, line: 'Line') -> Point:
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
