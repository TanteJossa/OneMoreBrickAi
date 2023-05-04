from oneMoreBrickGame import PowerupBall, CollisionBall
from oneMoreBrickEngine import Collision, Line

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

