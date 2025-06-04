import pygame
import time
import math


from utils import resize_image,rotate_center

grass = resize_image(pygame.image.load('C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\grass.jpg'),2.5)

finish = pygame.image.load(r'C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\finish.png')

track_border = resize_image(pygame.image.load(r'C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\track-border.png'),0.9)

track_border_mask = pygame.mask.from_surface(track_border)

track = resize_image(pygame.image.load(r'C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\track.png'),0.9)

red_car = resize_image(pygame.image.load(r'C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\red-car.png'),0.55)

finish_line = pygame.image.load(r'C:\Windows (D)\Languages\PYTHON 2.0\Project\Track_Racing\Images\imgs\finish.png')

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
        self.red_car_img = self.RED_CAR_IMG
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
        rotate_center(WIN,self.red_car_img,(self.x,self.y),self.angle)


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
        car_mask = pygame.mask.from_surface(self.red_car_img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
        
    def reset(self):
        self.starting_vel = 0
        self.angle = 0
        self.x ,self.y = self.start_pos



class Player_Car(Abstract_Car):
    RED_CAR_IMG= red_car
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


def draw(WIN,images,player_car):
    for image,pos in images:
        WIN.blit(image,pos)

    player_car.draw(WIN)
    pygame.display.update()

player_car = Player_Car(3,3) #Sends velocity and rotating velocity to _init_ of abstract car method

while run:

    clock.tick(60)  
    

    draw(WIN,images,player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    

    player_car.move_player_car()
    
    if player_car.collide(track_border_mask) != None: #Since value is none when object isnt colliding
        player_car.bounce()

    point_of_collision_finish = player_car.collide(finish_line_mask,130,250)
    if point_of_collision_finish != None:
        if point_of_collision_finish[1] == 0:
            player_car.bounce()
            print(point_of_collision_finish)
        else:
            player_car.reset()

        
    

pygame.quit
