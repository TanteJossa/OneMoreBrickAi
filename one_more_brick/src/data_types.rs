use std::ops::{Add, Div, Mul, Sub};
use std::f64::consts::PI;

#[derive(Debug, Clone, Copy)]
struct Point {
    pos: [f64; 2],
}

impl Point {
    fn new(x: f64, y: f64) -> Self {
        Self { pos: [x, y] }
    }

    fn distance(&self, other: &Self) -> f64 {
        ((other.pos[0] - self.pos[0]).powi(2) + (other.pos[1] - self.pos[1]).powi(2)).sqrt()
    }

    fn format_math_other(&self, other: f64) -> [f64; 2] {
        [other, other]
    }
}

impl Add<f64> for &Point {
    type Output = Point;

    fn add(self, other: f64) -> Point {
        let other = self.format_math_other(other);
        Point::new(self.pos[0] + other[0], self.pos[1] + other[1])
    }
}

impl Add<&Point> for &Point {
    type Output = Point;

    fn add(self, other: &Point) -> Point {
        Point::new(self.pos[0] + other.pos[0], self.pos[1] + other.pos[1])
    }
}

impl Sub<f64> for &Point {
    type Output = Point;

    fn sub(self, other: f64) -> Point {
        let other = self.format_math_other(other);
        Point::new(self.pos[0] - other[0], self.pos[1] - other[1])
    }
}

impl Sub<&Point> for &Point {
    type Output = Point;

    fn sub(self, other: &Point) -> Point {
        Point::new(self.pos[0] - other.pos[0], self.pos[1] - other.pos[1])
    }
}

impl Mul<f64> for &Point {
    type Output = Point;

    fn mul(self, other: f64) -> Point {
        let other = self.format_math_other(other);
        Point::new(self.pos[0] * other[0], self.pos[1] * other[1])
    }
}

impl Mul<&Point> for &Point {
    type Output = Point;

    fn mul(self, other: &Point) -> Point {
        Point::new(self.pos[0] * other.pos[0], self.pos[1] * other.pos[1])
    }
}

impl Div<f64> for &Point {
    type Output = Point;

    fn div(self, other: f64) -> Point {
        let other = self.format_math_other(other);
        Point::new(self.pos[0] / other[0], self.pos[1] / other[0])
    }
}

impl Div<&Point> for &Point {
    type Output = Point;

    fn div(self, other: &Point) -> Point {
        Point::new(self.pos[0] / other.pos[0], self.pos[1] / other.pos[1])
    }
}

#[derive(Debug, Clone, Copy)]
struct Vector {
    value: [f64; 2],
}

impl Vector {
    fn new(x: f64, y: f64) -> Self {
        Self { value: [x, y] }
    }

    fn point_in_quadrant(&self, point: &Point) -> bool {
        let Point { x, y } = *point;
        let a = self.x;
        let b = self.y;
        if a >= 0.0 && b >= 0.0 && x >= 0.0 && y >= 0.0 {
            return true;
        }
        if a <= 0.0 && b >= 0.0 && x <= 0.0 && y >= 0.0 {
            return true;
        }
        if a >= 0.0 && b <= 0.0 && x >= 0.0 && y <= 0.0 {
            return true;
        }
        if a <= 0.0 && b <= 0.0 && x <= 0.0 && y <= 0.0 {
            return true;
        }
        false
    }

    fn rotate(&mut self, angle: f64) {
        let angle = PI * angle / 180.0;
        let new_x = self.x * angle.cos() - self.y * angle.sin();
        let new_y = self.x * angle.sin() + self.y * angle.cos();
        self.x = new_x;
        self.y = new_y;
    }

    fn format_math_other(&self, other: impl Into<f64>) -> (f64, f64) {
        let other = other.into();
        if other.is_nan() {
            (0.0, 0.0)
        } else {
            (other, other)
        }
    }

    fn unit_vector(&self) -> Self {
        let length = self.length();
        Self::new(self.x / length, self.y / length)
    }

    fn length(&self) -> f64 {
        f64::abs((self.x * self.x + self.y * self.y).sqrt())
    }
}

impl Add for Vector {
    type Output = Self;

    fn add(self, other: impl Into<Vector>) -> Self::Output {
        let other = other.into();
        Self::new(self.x + other.x, self.y + other.y)
    }
}

impl Sub for Vector {
    type Output = Self;

    fn sub(self, other: impl Into<Vector>) -> Self::Output {
        let other = other.into();
        Self::new(self.x - other.x, self.y - other.y)
    }
}

impl Mul for Vector {
    type Output = Self;

    fn mul(self, other: impl Into<Vector>) -> Self::Output {
        let other = other.into();
        Self::new(self.x * other.x, self.y * other.y)
    }
}

impl Div for Vector {
    type Output = Self;

    fn div(self, other: impl Into<Vector>) -> Self::Output {
        let other = other.into();
        if other.x == 0.0 || other.y == 0.0 {
            return self;
        }
        Self::new(self.x / other.x, self.y / other.y)
