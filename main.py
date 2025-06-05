import pygame
import time
import math


from utils import resize_image,rotate_center

grass            = resize_image(pygame.image.load('Images/imgs/grass.jpg'),  2.5)
track            = resize_image(pygame.image.load('Images/imgs/track.png'),  0.9)

track_border     = resize_image(pygame.image.load('Images/imgs/track-border.png'),  0.9)
track_border_mask = pygame.mask.from_surface(track_border)

red_car          = resize_image(pygame.image.load('Images/imgs/red-car.png'), 0.55)
com_car          = resize_image(pygame.image.load('Images/imgs/purple-car.png'), 0.55)

finish_line      = pygame.image.load('Images/imgs/finish.png')
finish_line_mask = pygame.mask.from_surface(finish_line)

TRACK_WIDTH = track.get_width()
TRACK_HEIGHT = track.get_height()


WIN = pygame.display.set_mode((TRACK_WIDTH,TRACK_HEIGHT))
pygame.display.set_caption("Track Racing Game")

run = True
clock = pygame.time.Clock()  

images = [
    (grass, (0, 0)),
    (track, (0, 0)),
    (finish_line,(130,250)),
    (track_border,(0,0))
]

class Abstract_Car:
    
    def __init__(self,max_velocity,rotating_velocity):
        self.car_img = self.car_img
        self.max_vel = max_velocity
        self.starting_vel = 0
        self.rotating_vel = rotating_velocity
        self.angle = 0
        self.x,self.y = self.start_pos
        self.accelerate = 0.1
    
    def rotating_car(self,rotate_RIGHT = False,rotate_LEFT = False):
        if rotate_RIGHT:
            self.angle -= self.rotating_vel
        elif rotate_LEFT:
            self.angle += self.rotating_vel


    def draw(self,WIN):
        rotate_center(WIN,self.car_img,(self.x,self.y),self.angle)


    def accelerate_car(self, forward=False, backward=False):
        if forward:
            self.starting_vel = min(self.starting_vel + self.accelerate, self.max_vel)
            self.move()
        elif backward:
            self.starting_vel = max(self.starting_vel - self.accelerate, -self.max_vel/2)
            self.move()
        else:
            self.starting_vel *= 0.90  # this if for adding friction before stopping vehicle
            self.move()


    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.starting_vel
        horizontal = math.sin(radians) * self.starting_vel

        self.x -= horizontal
        self.y -= vertical

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.car_img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
        
    def reset(self):
        self.starting_vel = 4
        self.angle = 0
        self.x ,self.y = self.start_pos



class Player_Car(Abstract_Car):
    car_img= red_car
    start_pos = (180,200)


    def move_player_car(self):
            
        keys = pygame.key.get_pressed()


        if keys[pygame.K_a]:
            player_car.rotating_car(rotate_LEFT=True)
        if keys[pygame.K_d]:
            player_car.rotating_car(rotate_RIGHT=True)
        if keys[pygame.K_w]:
            player_car.accelerate_car(forward=True)
        elif keys[pygame.K_s]:
            player_car.accelerate_car(backward=True)
        else:
            player_car.accelerate_car()

    
    def bounce(self):
        if self.starting_vel>=1:
            self.starting_vel = -2.5 # since negative direction means going backward
        elif self.starting_vel<=-1:
            self.starting_vel = 2.5 # since positive direction means going forward

        self.move()  # Reverse the direction and slow down 

PATH = [(161, 105), (117, 68), (67, 100), (61, 351), (70, 477), (177, 595), (309, 723), (405, 706), (429, 501), (514, 462), (605, 536), (613, 708), (731, 717), (747, 426), (650, 365), (414, 353), (428, 258), (709, 254), (748, 160), (704, 73), (331, 75), (277, 143), (281, 330), (240, 411), (172, 360), (171, 280)]

class Computer_Car(Abstract_Car):
    car_img =  com_car
    start_pos = (150,200)

    def __init__(self, max_velocity, rotating_velocity,path=[]):
        super().__init__(max_velocity, rotating_velocity)
        self.path = path
        self.current_point = 0
        self.starting_vel = max_velocity


    def draw_points(self, WIN):
        for point in self.path:
            pygame.draw.circle(WIN, (255, 0, 0), point, 5)

    def draw(self, WIN):
        super().draw(WIN)
        # Computer_Car.draw_points(self,WIN)    # This was done to get the positions for movement of Computer_Car


    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]  # Here we take path co-ordinates
        x_diff = target_x - self.x                          # Finding difference between car and target co-ordinates
        y_diff = target_y - self.y

        if y_diff == 0:     # If Car is Horizantal to Y 
            desired_radian_angle = math.pi / 2  # The angle will be 90 degree
        else:
            desired_radian_angle = math.atan(x_diff / y_diff) 

        if target_y > self.y:       #If target is down side of the car then rotate it by 180 degree
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:      # This helps in rotating vehicle where the angle is minimum
            difference_in_angle -= 360

        if difference_in_angle > 0:         
            self.angle -= min(self.rotating_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotating_vel, abs(difference_in_angle))

    def update_path_point(self):    #After colliding to one point, increment the point count 
    
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.car_img.get_width(), self.car_img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1


    def move_computer_car(self):
        if self.current_point>=len(self.path):
            self.current_point = 0      
    
        self.calculate_angle()
        self.update_path_point()
        super().move()


def collision_of_vehicles(player_car,computer_car):
    pass


def draw(WIN,images,player_car,computer_car):
    for image,pos in images:
        WIN.blit(image,pos)

    player_car.draw(WIN)
    computer_car.draw(WIN)

    pygame.display.update()

player_car = Player_Car(4,4) #Sends velocity and rotating velocity to _init_ of abstract car method (object)
computer_car = Computer_Car(4,5.5,PATH)

while run:

    clock.tick(60)  
    

    draw(WIN,images,player_car,computer_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    computer_car.draw_points(WIN)

    player_car.move_player_car()
    computer_car.move_computer_car()
    
    if player_car.collide(track_border_mask) != None: #Since value is none when object isnt colliding
        player_car.bounce()


    computer_point_of_collision_finish = computer_car.collide(finish_line_mask,130,250)
    if computer_point_of_collision_finish != None:
        computer_car.reset()
        
    

    player_point_of_collision_finish = player_car.collide(finish_line_mask,130,250)
    if player_point_of_collision_finish != None:
        if player_point_of_collision_finish[1] == 0:    #If Player tries to cross finish line from forward (the co-ordinate of y component is 0 at that position) then the player bounces back
            player_car.bounce()
        else:
            player_car.reset()

     
pygame.quit
