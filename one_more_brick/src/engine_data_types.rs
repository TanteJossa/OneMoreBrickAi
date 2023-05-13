use either::*;
use is_close::default;
use std::{ops::{Mul, Add, Sub, Div}};
use std::any::type_name;

fn type_of<T>(_: T) -> &'static str {
    type_name::<T>()
}

pub struct Point {
    pub x: f64,
    pub y: f64
}

impl Point {
    pub fn new(x: f64, y: f64) -> Point {
        Point { x: x, y: y }
    }
    pub fn distance(&self, other: Point) -> f64 {
        (other.x - self.x).hypot(other.y - self.y).abs()
    }
    pub fn to_vector(self) -> Vector {
        Vector::new(self.x, self.y)
    }
}


impl Mul<Vector> for Point {
    type Output = Self;

    fn mul(self, rhs: Vector) -> Self::Output {
        Self { x: self.x *  rhs.x, y: self.y * rhs.y }
    }
}
impl Mul<f64> for Point {
    type Output = Self;

    fn mul(self, rhs: f64) -> Self::Output {
        Self { x: self.x * rhs, y: self.y * rhs }
    }
}
impl Mul for Point {
    type Output = Self;

    fn mul(self, rhs: Point) -> Self::Output {
        Self { x: self.x * rhs.x, y: self.y * rhs.y }
    }
}

impl Div<Vector> for Point {
    type Output = Self;

    fn div(self, rhs: Vector) -> Self::Output {
        Self { x: self.x /  rhs.x, y: self.y / rhs.y }
    }
}
impl Div<f64> for Point {
    type Output = Self;

    fn div(self, rhs: f64) -> Self::Output {
        Self { x: self.x / rhs, y: self.y / rhs }
    }
}
impl Div for Point {
    type Output = Self;

    fn div(self, rhs: Point) -> Self::Output {
        Self { x: self.x /  rhs.x, y: self.y / rhs.y }
    }
}

impl Add<Vector> for Point {
    type Output = Self;

    fn add(self, rhs: Vector) -> Self::Output {
        Self { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}
impl Add<f64> for Point {
    type Output = Self;

    fn add(self, rhs: f64) -> Self::Output {
        Self { x: self.x + rhs, y: self.y + rhs }
    }
}
impl Add for Point {
    type Output = Self;

    fn add(self, rhs: Point) -> Self::Output {
        Self { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}

impl Sub<Vector> for Point {
    type Output = Self;

    fn sub(self, rhs: Vector) -> Self::Output {
        Self { x: self.x - rhs.x, y: self.y - rhs.y }
    }
}
impl Sub<f64> for Point {
    type Output = Self;

    fn sub(self, rhs: f64) -> Self::Output {
        Self { x: self.x - rhs, y: self.y - rhs }
    }
}
impl Sub for Point {
    type Output = Self;

    fn sub(self, rhs: Point) -> Self::Output {
        Self { x: self.x - rhs.x, y: self.y - rhs.y }
    }
}

impl Clone for Point {
    fn clone(&self) -> Point {
        Point { x: self.x, y: self.y }
    }
}
    
pub struct Vector {
    pub x: f64,
    pub y: f64
}

impl Vector {
    pub fn new(x: f64, y: f64) -> Vector {
        Vector { x: x, y: y  }
    }
    pub fn length(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
    pub fn unit_vector(&self) -> Vector {
        let length: f64 = self.length();
        Vector { x: self.x / length, y: self.y / length } 
    }

    pub fn rotate(&self, angle: f64) -> Vector {
        let rad_angle = angle * (std::f64::consts::PI / 180.0);
        let new_x = self.x * rad_angle.cos() - self.y * rad_angle.sin();
        let new_y = self.x * rad_angle.sin() + self.y * rad_angle.cos();

        Vector { x: new_x, y: new_y }
    }

    pub fn point_in_quadrant(&self, point: Point) -> bool {
        let (a, b) = (self.x, self.y);
        let (x, y   ) = (point.x, point.x);
        
        if a >= 0.0 && b >= 0.0 && 
            x >= 0.0 && y >= 0.0{
            return true;
        }
        if a <= 0.0 && b >= 0.0 && 
            x <= 0.0 && y >= 0.0{
            return true;
        }   
        if a >= 0.0 && b <= 0.0 && 
            x >= 0.0 && y <= 0.0{
            return true;    
        }
        if a <= 0.0 && b <= 0.0 && 
            x <= 0.0 && y <= 0.0{
            return true;
        }

        false
    }
}   

impl Mul<Point> for Vector {
    type Output = Self;

    fn mul(self, rhs: Point) -> Self::Output {
        Self { x: self.x * rhs.x, y: self.y * rhs.y }
    }
}
impl Mul<f64> for Vector {
    type Output = Self;

    fn mul(self, rhs: f64) -> Self::Output {
        Self { x: self.x * rhs, y: self.y * rhs }
    }
}
impl Mul for Vector {
    type Output = Self;

    fn mul(self, rhs: Vector) -> Self::Output {
        Self { x: self.x * rhs.x, y: self.y * rhs.y }
    }
}


impl Div<Point> for Vector {
    type Output = Self;

    fn div(self, rhs: Point) -> Self::Output {
        Self { x: self.x / rhs.x, y: self.y / rhs.y }
    }
}
impl Div<f64> for Vector {
    type Output = Self;

    fn div(self, rhs: f64) -> Self::Output {
        Self { x: self.x / rhs, y: self.y / rhs }
    }
}
impl Div for Vector {
    type Output = Self;

    fn div(self, rhs: Vector) -> Self::Output {
        Self { x: self.x /  rhs.x, y: self.y / rhs.y }
    }
}

impl Add<Point> for Vector {
    type Output = Self;

    fn add(self, rhs: Point) -> Self::Output {
        Self { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}
impl Add<f64> for Vector {
    type Output = Self;

    fn add(self, rhs: f64) -> Self::Output {
        Self { x: self.x + rhs, y: self.y + rhs }
    }
}
impl Add for Vector {
    type Output = Self;

    fn add(self, rhs: Vector) -> Self::Output {
        Self { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}

impl Sub<Point> for Vector {
    type Output = Self;

    fn sub(self, rhs: Point) -> Self::Output {
        Self { x: self.x - rhs.x, y: self.y - rhs.x }
    }
}
impl Sub<f64> for Vector {
    type Output = Self;

    fn sub(self, rhs: f64) -> Self::Output {
        Self { x: self.x - rhs, y: self.y - rhs }
    }
}
impl Sub for Vector {
    type Output = Self;

    fn sub(self, rhs: Vector) -> Self::Output {
        Self { x: self.x - rhs.x, y: self.y - rhs.y }
    }
}
impl Clone for Vector {
    fn clone(&self) -> Vector {
        Vector { x: self.x, y: self.y }
    }
}


pub struct Line {
    pub p1: Point,
    pub p2: Point,
}

impl Line {
    pub fn new(p1: Point, p2: Point) -> Line {
        Line {p1, p2}
    }
    pub fn length(&self) -> f64 {
        self.p1.distance(self.p2.clone())
    }
    pub fn slope(&self) -> f64 {
        if self.p2.x - self.p1.x == 0.0 {
            return f64::NAN;
        } 
        (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
    }
    pub fn y_intersect(&self) -> f64 {
        self.p1.y -  self.slope() * self.p1.x
    }

    pub fn closest_point(&self, point: Point) -> Point {
        let (x1, y1, x2, y2, x3, y3) = (self.p1.x, self.p1.y, self.p2.x, self.p2.y, point.x, point.y);
        let (dx, dy) = (x2 - x1, y2 - y1);
        let det = dx * dx + dy * dy;
        let num = dy*(y3-y1)+dx*(x3-x1);
        
        
        let a = if det.is_nan() || num.is_nan() || det == 0.0 || num == 0.0{
            0.0
        } else {
            (dy*(y3-y1)+dx*(x3-x1))/det
        };

        Point { x: x1 + a*dx, y: y1 + a*dy }
    }

    pub fn intersection_point(&self, other: Line) -> Either<Point, bool> {
        let (x1, y1, x2, y2, x3, y3, x4, y4) = (self.p1.x, self.p1.y, self.p2.x, self.p2.y, other.p1.x, other.p1.y, other.p2.x, other.p2.y);
        let det = (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4);
        if det != 0.0 {
            let px= ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / det;
            let py= ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / det;
        
            return either::Left(Point {x: px, y: py});
        }
        either::Right(false)
    }
    pub fn point_on_line(&self, point: Point) -> bool {
        let cumulative_dist_to_point = point.distance(self.p1.clone()) + point.distance(self.p2.clone());
        default().is_close(cumulative_dist_to_point, self.length())
    }
    
}
impl Clone for Line {
    fn clone(&self) -> Line {
        Line {p1: self.p1.clone(), p2: self.p2.clone()}
    }
}


pub struct Ball {
    pub pos: Point,
    pub vel: Vector,
    pub radius: f64, 
}
impl Ball {
    pub fn new(pos: Point, vel: Vector, radius: f64) -> Ball {
        Ball {pos, vel, radius}
    }
    pub fn move_forward(&mut self, distance: f64) {
        self.pos = self.pos.clone() + self.vel.unit_vector() * distance;
    }
}
impl Clone for Ball {
    fn clone(&self) -> Ball {
        Ball {pos: self.pos.clone(), vel: self.vel.clone(), radius: self.radius.clone()}
    }
}

