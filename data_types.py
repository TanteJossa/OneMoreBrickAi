"""
    This file contains the data types used in the project.
    The data types are:
        - Point
        - Line
        - Vector
        
    Author: Merc4tor
"""


import numpy as np
from numbers import Number
from typing import Union, Any
import math
import copy

class Point():
    """
    A point in 2D space.
    
    Properties:
        - pos: np.ndarray, position of the point
        
    Methods:
        - distance(p: Point): float, distance between the point and p
        
    """
    
    def __init__(self, x, y) -> None:
        """
        Initialize a point.
        
        :param x: x-coordinate
        :param y: y-coordinate
        """
        
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
    """
    Vector class
    
    Properties:
        - value: np.ndarray, vector value
        
    Methods:
        - point_in_quadrant(point: Point): bool, check if a point is in a quadrant
    """
    
    def __init__(self, x: Number | Point, y: Number=0) -> None:
        """
        Vector class
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        
        """
        
        
        if type(x) == Point:     
            y = x[1]
            x = x[0]
        if type(x) == Line and type(y) == Line:     
            y = y[1] - x[1]
            x = y[0] - x[0]
        self.value = np.array([x, y])

    def point_in_quadrant(self, point):
        """
        Check if a point is in a quadrant
        :param point: Point to check
        :return: True if point is in a quadrant
        """
        
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
        """Speed of the vector"""
        return np.abs(math.hypot(self.x, self.y))
    
    @property
    def unit_vector(self) -> 'Vector':
        return self / self.length
      
class Line():
    """
    Line is a 2D line defined by two points.
    
    Properties:
        - p1: Point, the first point on the line.
        - p2: Point, the second point on the line.
        - slope: Number, the slope of the line.
        - length: Number, the length of the line.

    Methods:
        - unit_vector: Vector, the unit vector of the line.
        - closest_point_to(point: Point): Point, the closest point to the line.
        - intersection_point(line: Line): Point, the intersection of the two lines.
        - point_on_line(point: Point): bool, check if a point is on the line.
    """
    
    def __init__(self, p1: Point, p2: Point) -> None:
        """
        Creates a line.
        
        :param p1: the first point on the line.
        :type p1: Point
        :param p2: the second point on the line.
        :type p2: Point
        """
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
    
    # don't know why you would ever need this, but it's here
    @property
    def unit_vector(self) -> np.ndarray:
        """
        Returns the unit vector of the line.
        :return: the unit vector of the line.
        :rtype: np.ndarray
        """
        
        return self.vec.value / self.length
    
    @property
    def slope(self):
        if ((self.p2.x - self.p1.x) == 0):
            return math.nan
        return  (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
    
    @property
    def y_intersect(self):
        return self.p1.y - self.slope * self.p1.x
    
    
    def closest_point(self, p: Point):
        """
        Returns the closest point on the line to a given point.
        
        :param p: the point to find the closest point to.
        :type p: Point
        :return: the closest point on the line to the given point.
        :rtype: Point
        """
        (x1, y1), (x2, y2), (x3, y3) = self.p1.pos, self.p2.pos, p.pos
        dx, dy = x2-x1, y2-y1
        det = dx*dx + dy*dy 
        num = (dy*(y3-y1)+dx*(x3-x1))

        if (math.isnan(det) or math.isnan(num) or det == 0 or num == 0):
            a = 0
        else:
            a = (dy*(y3-y1)+dx*(x3-x1))/det

        return Point(x1+a*dx, y1+a*dy)
    
    def intersection_point(self, line: 'Line') -> Point:
        """
        Returns the intersection point of two lines.
        If the lines are parallel, returns False.
        If the lines are coincident, returns the point.
        
        :param line: the line to intersect with.
        :type line: Line
        :return: the intersection point.
        :rtype: Point
        
        >>> line1 = Line((0,0), (1,1))
        >>> line2 = Line((1,1), (2,2))
        >>> line1.intersection_point(line2)
        False
        
        >>> line1 = Line((0,0), (1,1))
        >>> line2 = Line((1,1), (1,2))
        >>> line1.intersection_point(line2)
        False
        
        >>> line1 = Line((0,0), (2,2))
        >>> line2 = Line((0,2), (2,0))
        >>> line1.intersection_point(line2)
        Point(1.0, 1.0)
        """
        
        (x1,y1), (x2,y2), (x3,y3), (x4,y4) = self.p1, self.p2, line.p1, line.p2
        det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
        if det != 0:
            px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / det
            py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / det
        
            return Point(px, py)
        else:
            return False

    
    def point_on_line(self, point: Point) -> bool:
        cumulative_dist_to_point = point.distance(self.p1) + point.distance(self.p2)

        return math.isclose(cumulative_dist_to_point, self.length)
    
    def move_from_point(self, point: Point, length: Number) -> Point:
        return point - self.unit_vector * length        
