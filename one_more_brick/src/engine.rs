use std::vec;

use either::Either;

use super::engine_data_types::{Point, Vector, Line, Ball};

pub struct Collision {
    ball: Ball,
    collision_point: Point,
    touch_point: Point,
    col_type: String,
    new_vel:  Vector,
    object: Either<Ball, Line>
}

impl Collision {
    pub fn new(ball: Ball, collision_point: Point, touch_point: Point, col_type: String, new_vel: Vector, object: Either<Ball, Line>) -> Collision {
        Collision {
            ball : ball,
            collision_point : collision_point,
            touch_point : touch_point,
            col_type : col_type,
            new_vel : new_vel,
            object : object,
        }
    }

    pub fn is_valid(self) -> bool {
        let relative_collision_point = self.collision_point - self.ball.pos;

        !(self.ball.vel * -1.0).point_in_quadrant(relative_collision_point)
    }

    pub fn calc_new_vel(&self) -> Vector {
        let new_vel = 
            if self.col_type == "point" {
                let vel = self.collision_point - self.touch_point;
                Vector::new(vel.x, vel.y)
            } else if  self.col_type == "line" {

                let intersect_vec = (self.touch_point - self.collision_point).to_vector();
                intersect_vec.rotate(90.0);
                let collision_vec = intersect_vec;
                let collision_line = Line::new(self.touch_point, self.touch_point - collision_vec);
                
                let p_1 = collision_line.closest_point(self.ball.pos);

                let touch_to_p1 = (p_1 - self.touch_point).to_vector();
                let direction_point = self.ball.pos - touch_to_p1 * 2.0;
                
                (direction_point - self.collision_point).to_vector()
            } else if self.col_type == "ball" {
                self.new_vel
            } else {
                self.new_vel
            };

        new_vel.unit_vector() * self.ball.vel.length()
    }

    pub fn distance(self) -> f64 {
        self.ball.pos.distance(self.collision_point)
    }
    pub fn time_left(self) -> f64 {
        if self.ball.vel.length() == 0.0 {
            return 0.0;
        }
        self.distance() / self.ball.vel.length()
    }

}

impl Clone for Collision {
    fn clone(&self) -> Collision {
        Collision {
            ball : self.ball.clone(),
            collision_point : self.collision_point.clone(),
            touch_point : self.touch_point.clone(),
            col_type : self.col_type.clone(),
            new_vel : self.new_vel.clone(),
            object : self.object.clone(),
        }
    }
}

struct Interaction {
    ball: Ball,
    object: Either<Ball, Line>,
    is_static: bool,
    collisions: Vec<Collision>,
    interaction_type: String,
}

impl Interaction {
    pub fn new(ball: Ball, object: Either<Ball, Line>, is_static: bool, interaction_type: String) -> Interaction {
        if interaction_type == "ball" {
            let collisions = Interaction::calc_ball_collision(ball, Either::left(object).unwrap(), is_static);
            
            return Interaction {
                ball: ball,
                object: object,
                is_static: is_static,
                collisions: collisions,
                interaction_type: interaction_type,
            };
        } else if interaction_type == "line" {
            let collisions = Interaction::calc_line_collision(ball, Either::right(object).unwrap());
            
            return Interaction {
                ball: ball,
                object: object,
                is_static: is_static,
                collisions: collisions,
                interaction_type: interaction_type,
            };
        }
        Interaction {
            ball: ball,
            object: object,
            is_static: is_static,
            collisions: vec![],
            interaction_type: interaction_type,
        }
    }

    fn calc_ball_collision(ball: Ball, ball2: Ball, is_static: bool) -> Vec<Collision> {
        let pos_delta_x = ball2.pos.x - ball.pos.x;
        let vel_delta_x = ball2.vel.x - ball.vel.x;
        let pos_delta_y = ball2.pos.y - ball.pos.y;
        let vel_delta_y = ball2.vel.y - ball.vel.y;

        let total_radius = ball.radius + ball2.radius;

        let a = vel_delta_x*vel_delta_x + vel_delta_y*vel_delta_y;
        let b = (pos_delta_x * vel_delta_x + pos_delta_y * vel_delta_y) * 2.0;
        let c = pos_delta_x*pos_delta_x + pos_delta_y*pos_delta_y - total_radius*total_radius;

        if a == 0.0 {
            return vec![];
        }
        let discriminant = b*b - 4.0*a*c;

        if discriminant < 0.0 {
            return vec![];
        }

        let collision_time = (-b - discriminant.sqrt()) / (2.0 * a);
        let collision_point = ball.pos + ball.vel * collision_time;
        let collision_point2 = ball2.pos + ball2.vel * collision_time;

        let touch_point = collision_point + (collision_point2 - collision_point).to_vector().unit_vector() * ball.radius * 0.5;

        let collisions = if is_static {
            let collision = Collision::new(ball, collision_point, touch_point, "line".to_string(), Vector::new(0.0, 0.0), Either::Left(ball2));
            vec![collision]
        } else {
            let n = (collision_point - collision_point2).to_vector().unit_vector();
            n.rotate(90.0);
            let p = (n * ball.vel) - (n * ball2.vel);

            let ball1_new_vel = ball.vel + n * p.length();
            let ball2_new_vel = ball2.vel - n * p.length();

            let collision = Collision::new(ball, collision_point, touch_point, "ball".to_string(), ball1_new_vel, Either::Left(ball2));
            let collision2 = Collision::new(ball2, collision_point2, touch_point, "ball".to_string(), ball2_new_vel, Either::Left(ball));
            vec![collision, collision2]
        };
        
        let mut collisions: Vec<Collision> = collisions
            .into_iter()
            .filter(|collision| collision.is_valid())
            .collect::<Vec<Collision>>();
        
        collisions.sort_by(|a, b| a.time_left().partial_cmp(&b.time_left()).unwrap());
 
        collisions

    }
    fn calc_line_collision(ball: Ball, line: Line) -> Vec<Collision> {
        let ball_movement_line = Line::new(ball.pos, ball.pos + ball.vel);

        let line_p1_closest = ball_movement_line.closest_point(line.p1);
        let line_p1_distance = line_p1_closest.distance(line.p1);
        let line_p2_closest = ball_movement_line.closest_point(line.p2);
        let line_p2_distance = line_p2_closest.distance(line.p2);

        let mut collisions = vec![];

        if line_p1_distance < ball.radius {
            let collision1_point_offset = (ball.radius*ball.radius - line_p1_distance*line_p1_distance).sqrt();
            let collision1_point = line_p1_closest - ball.vel.unit_vector() * collision1_point_offset;
            collisions.push(Collision::new(ball, collision1_point, line.p1, "line".to_string(), Vector::new(0.0, 0.0), Either::Right(line)));
        }
        if line_p2_distance < ball.radius {
            let collision2_point_offset = (ball.radius*ball.radius - line_p2_distance*line_p2_distance).sqrt();
            let collision2_point = line_p2_closest - ball.vel.unit_vector() * collision2_point_offset;
            collisions.push(Collision::new(ball, collision2_point, line.p2, "line".to_string(), Vector::new(0.0, 0.0), Either::Right(line)));
        }

        match line.intersection_point(ball_movement_line) {
            Either::Left(p_intersection) => {
                let ball_closest_on_line = ball_movement_line.closest_point(p_intersection);
                let ball_distance = ball_closest_on_line.distance(p_intersection);

                let closest_to_intersection = (p_intersection - ball_closest_on_line).to_vector();

                let col_ratio = if ball_distance == 0.0 {1.0} else {ball.radius / ball_distance};

                let touch_point = p_intersection - closest_to_intersection * col_ratio;

                if line.point_on_line(touch_point) {
                    let distance_touch_to_intersection = touch_point.distance(p_intersection);
                    let distance_intersection_to_collision = (ball.radius*ball.radius + distance_touch_to_intersection*distance_touch_to_intersection).sqrt();

                    let collision_point = p_intersection - closest_to_intersection * distance_intersection_to_collision;

                    collisions.push(Collision::new(ball, collision_point, touch_point, "line".to_string(), Vector::new(0.0, 0.0), Either::Right(line)));

                }
            }
            Either::Right(p_intersection) => {}
        }

        let mut collisions: Vec<Collision> = collisions
            .into_iter()
            .filter(|collision| collision.is_valid())
            .collect::<Vec<Collision>>();
        
        collisions.sort_by(|a, b| a.time_left().partial_cmp(&b.time_left()).unwrap());
 
        collisions


    }
}

struct PhysicsEnvironment {
    balls: Vec<Ball>,
    lines: Vec<Line>,
    border_lines: Vec<Line>,
    collision_balls: Vec<Ball>,
    ball_collision: bool,
    size: Vec<f64>,
    step_size: f64,
}

impl  PhysicsEnvironment {
    pub fn new(size: Vec<f64>, step_size: f64) -> PhysicsEnvironment {
        let border_lines = vec![
            Line::new(Point::new(0.0, 0.0), Point::new(0.0, size[1])),
            Line::new(Point::new(0.0, size[1]), Point::new(size[0], size[1])),
            Line::new(Point::new(size[0], size[1]), Point::new(size[0], 0.0)),
            Line::new(Point::new(size[0], 0.0), Point::new(0.0, 0.0))
        ];
        
        PhysicsEnvironment {
            balls: vec![],
            lines: vec![],
            border_lines: border_lines,
            collision_balls: vec![],
            ball_collision:  false,
            size: size,
            step_size: step_size,
        }
    }

    pub fn get_ball_collisions(self, ball: Ball) -> Vec<Collision> {
        let mut collisions = vec![];

        if self.ball_collision {
            for ball2 in self.balls {
                if ball.pos !=  ball2.pos {
                    let interaction = Interaction::new(ball, Either::Left(ball2), false, "ball".to_string());
                    if interaction.collisions.len() > 0 {
                        collisions.push(interaction.collisions[0].clone());
                    }
                }
            }
        }

        for ball2 in self.collision_balls {
            let interaction = Interaction::new(ball, Either::Left(ball2), true, "ball".to_string());
            let ball_interactions: Vec<Collision> = interaction.collisions.iter().filter(|collision| collision.ball.pos == ball.pos).collect();
            if ball_interactions.len() > 0 {
                collisions.push(ball_interactions[0].clone());
            }
        }

        for line in self.lines {
            let interaction = Interaction::new(ball, Either::Right(line), false, "line".to_string());
            if interaction.collisions.len() > 0 {
                collisions.push(interaction.collisions[0].clone());
            }
        }


        collisions.sort_by(|a, b| a.time_left().partial_cmp(&b.time_left()).unwrap());
        collisions
    }

    pub fn get_first_collision(&self, ball: Ball) -> Either<Collision, bool> {
        let collisions = self.get_ball_collisions(ball);
        if collisions.len() != 0 {
            return Either::Left(collisions[0].clone());
        }
        Either::Right(false)
    }
}
