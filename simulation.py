import math
import pygame
from oneMoreBrickEngine import Ball, PhysicsEnvironment, Line
import time
import keyboard
import random
scaling = 1

pygame.init()

(width, height) = (500, 400)
sim_width, sim_height = 20, 20
sim_scaling = 10
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.flip()
clock = pygame.time.Clock()  
font = pygame.font.Font('freesansbold.ttf', 32)
                                            
         
circle1 = Ball(4, 3,  1, -1, 2, '1')
circle2 = Ball(6, 6, -1, 0, 1, '2')      
circle3 = Ball(4, 6)    
line1 = Line([4,0], [4,1.5])
ball_num = 3
random_circles = [Ball(random.random() * sim_scaling, random.random() * sim_scaling, random.random() * 2 -1, random.random() * 2 - 1, random.random() * 1 + 0.5, str(i)) for i in range(ball_num)]
# line1 = Line([2,5], [6,7])
print(id(line1))
environment = PhysicsEnvironment(sim_scaling, sim_scaling, [circle1], [line1], 0.1, True)
         
                                                       
                                          


                              

         

time_delta = 1       
running = True                 
while running:                   
    start_time = time.time()     
    
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    if screen_width / screen_height > 1:
        screen_scaling = screen_height / sim_scaling
        sim_field_x_offset = (screen_width - screen_height) / 2
        sim_field_y_offset = screen_height

           
    else:
        screen_scaling = screen_width / sim_scaling
        sim_field_x_offset = 0
        sim_field_y_offset = screen_height - ((screen_height - screen_width) / 2)
    
    toScreenCoords = lambda pos: [(pos[0]) * screen_scaling + sim_field_x_offset, (-pos[1]) * screen_scaling + sim_field_y_offset]
    toSimCoords = lambda pos: [(pos[0] - sim_field_x_offset) * (1/screen_scaling), (-pos[1] + sim_field_y_offset) * (1/screen_scaling)]
    screen.fill((0, 0, 0))
    
    origin_point = toScreenCoords((0,0))  
    top_right = toScreenCoords((10, 10))

    sim_area = pygame.rect.Rect(origin_point[0], top_right[1], top_right[0] - origin_point[0], origin_point[1] - top_right[1])
    pygame.draw.rect(screen, (100, 100, 100), sim_area)
     
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = toSimCoords(event.pos)
            circle1.x = pos[0]
            circle1.y = pos[1]
            environment.calc_collisions()
            
    if keyboard.is_pressed(' '):
        run_tick = True
    else:                                         
        run_tick = False
                                                     
    if run_tick:
        environment.run_tick(time_delta)
     
        
    for object in environment.objects:
        centre_on_screen = toScreenCoords((object.x, object.y))
        pygame.draw.circle(screen, (0, 0, 255), centre_on_screen, radius=object.radius * screen_scaling)
        # point_on_circle = (math.cos(object.rot) * object.radius + object.x, math.sin(object.rot) * object.radius + object.y,)
        # point_on_circle_on_screen = toScreenCoords(point_on_circle)
        
        # pygame.draw.line(screen, (0, 255, 0),centre_on_screen,  point_on_circle_on_screen)

        for vel_arrow in object.vel_lines:
            
            p1_on_screen = toScreenCoords(vel_arrow[0])
            p2_on_screen = toScreenCoords(vel_arrow[1])
            pygame.draw.line(screen, (211, 255, 0), p1_on_screen,  p2_on_screen)
        

            
    for line in environment.lines:
        p1_on_screen = toScreenCoords(line.p1)
        p2_on_screen = toScreenCoords(line.p2)
        pygame.draw.line(screen, (0, 0, 0), p1_on_screen,  p2_on_screen)
         
    fps = font.render(str     (round(1 / time_delta)), True, (255, 255, 255))
    textRect = fps.get_rect()
    textRect.center = (50, 20)    
    screen.blit(fps, textRect)



    pygame.display.flip()
    end_time = time.time()
    time_delta = end_time - start_time + 0.001
       
