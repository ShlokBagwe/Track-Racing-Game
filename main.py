import pygame
import time
import math
import sys

pygame.init()

from utils import resize_image,rotate_center

grass = resize_image(pygame.image.load('Images/imgs/grass.jpg'),  2.5)
track = resize_image(pygame.image.load('Images/imgs/track.png'),  0.9)

track_border     = resize_image(pygame.image.load('Images/imgs/track-border.png'),  0.9)
track_border_mask = pygame.mask.from_surface(track_border)


red_car = resize_image(pygame.image.load('Images/imgs/red-car.png'), 0.55)
red_car_option = resize_image(pygame.image.load('Images/imgs/red-car.png'), 2)

green_car = resize_image(pygame.image.load('Images/imgs/green-car.png'),0.55)
green_car_option = resize_image(pygame.image.load('Images/imgs/green-car.png'),2)

grey_car = resize_image(pygame.image.load('Images/imgs/grey-car.png'),0.55)
grey_car_option = resize_image(pygame.image.load('Images/imgs/grey-car.png'),2)

com_car = resize_image(pygame.image.load('Images/imgs/purple-car.png'), 0.55)

finish_line      = pygame.image.load('Images/imgs/finish.png')
finish_line_mask = pygame.mask.from_surface(finish_line)

TRACK_WIDTH = track.get_width()
TRACK_HEIGHT = track.get_height()


WIN = pygame.display.set_mode((TRACK_WIDTH,TRACK_HEIGHT))
pygame.display.set_caption("Track Racing Game")

run = True
clock = pygame.time.Clock()  

PLAYER_LAP_COUNT = 0
COMPUTER_LAP_COUNT = 0

WINNING_LAP = 3


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
    

    def collision_of_cars(self,comp_mask,x=0,y=0):
        car_mask = pygame.mask.from_surface(self.car_img)
        offset = (int(self.x - x),int(self.y - y))
        poi = comp_mask.overlap(car_mask,offset)
        return poi

                    
    def reset(self):
        global count_signals
        self.angle = 0
        self.x ,self.y = self.start_pos

    def reset_after_closure(self):
        global count_signals
        self.angle = 0
        self.x ,self.y = self.start_pos
        Computer_Car.reset_current_path(self)
        count_signals = 0



class Player_Car(Abstract_Car):
    car_img= red_car        # after making option menu, This will be the default car if no car is chosen
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

PATH = [(165, 100), (75, 79), (70, 481), (318, 731), (408, 680), (410, 518), (518, 465), (600, 535), (613, 715), (730, 710), (734, 395), (611, 357), (415, 343), (425, 257), (695, 245), (710, 95), (320, 45), (275, 150),(280,380),(176, 388), (178, 280)]

class Computer_Car(Abstract_Car):
    car_img =  com_car
    start_pos = (155,200)

    def __init__(self, max_velocity, rotating_velocity,path=[]):
        super().__init__(max_velocity, rotating_velocity)
        self.path = path
        self.current_point = 0
        self.starting_vel = max_velocity
        self.store_vel = max_velocity

    # def draw_points(self, WIN):
    #     for point in self.path:
    #         pygame.draw.circle(WIN, (255, 0, 0), point, 5)

    # def draw(self, WIN):
    #     super().draw(WIN)
    #     Computer_Car.draw_points(self,WIN)    # This was done to get the positions for movement of Computer_Car
    
    def bounce(self):
        if self.starting_vel>=1:
            self.starting_vel = -self.starting_vel # since negative direction means going backward
        elif self.starting_vel<=-1:
            self.starting_vel = -self.starting_vel      # since positive direction means going forward

        self.move()


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
        
        if self.current_point>=len(self.path):
            self.current_point = 0


    def move_computer_car(self):
        if self.current_point>=len(self.path):
            self.current_point = 0      
    
        self.calculate_angle()
        self.update_path_point()
        super().move()

    def reset_current_path(self):
        self.current_point = 0



def draw(WIN,images,player_car,computer_car):
    for image,pos in images:
        WIN.blit(image,pos)


    player_car.draw(WIN)
    computer_car.draw(WIN)


    player_lap = LAP_FONT.render(f"Player Lap: {PLAYER_LAP_COUNT}", True, (255, 255,255),(0,0,0))  # convert int to string
    computer_lap = LAP_FONT.render(f"Computer Lap: {COMPUTER_LAP_COUNT}", True, (255, 255, 255),(0,0,0)) 
    WIN.blit(player_lap, (10, 700))
    WIN.blit(computer_lap,(10,730))


    pygame.display.update()


def draw_winning_screen(WIN):

    WIN.fill((0,0,0))  


    if PLAYER_LAP_COUNT == WINNING_LAP:
        text = "YOU WON !!!"
    elif COMPUTER_LAP_COUNT == WINNING_LAP:
        text = "YOU LOST"
    else:
        return  # nobody has won yet


    finishing_message = FONTS_NUM.render(text, True, (255, 255, 0))
    x = (TRACK_WIDTH - finishing_message.get_width()) // 2
    y = (TRACK_HEIGHT - finishing_message.get_height()) // 2
    WIN.blit(finishing_message, (x, y))


    pygame.display.update()
    pygame.time.delay(4000)


player_car = Player_Car(4,4) #Sends velocity and rotating velocity to _init_ of abstract car method (object)
computer_car = Computer_Car(3.5,5.5,PATH)


FONTS = pygame.font.SysFont("Comic Sans MS", 48)
FONTS_NUM = pygame.font.SysFont("Impact",80)
LAP_FONT = pygame.font.SysFont("Arial Black", 22)

def draw_menu(WIN):
    WIN.fill((0, 0, 0))  

    label_play = FONTS.render("Press ENTER to Play", True, (255, 255, 255))
    label_options = FONTS.render("Press SPACE for Options", True, (255, 255, 255))
    label_quit = FONTS.render("Press ESC to Quit", True, (255, 255, 255))

    WIN.blit(label_play, ((TRACK_WIDTH - label_play.get_width()) // 2, TRACK_HEIGHT // 2 - 60))
    WIN.blit(label_options, ((TRACK_WIDTH - label_options.get_width()) // 2, TRACK_HEIGHT // 2))
    WIN.blit(label_quit, ((TRACK_WIDTH - label_quit.get_width()) // 2, TRACK_HEIGHT // 2 + 60))

    pygame.display.flip()

def menu_loop():
    clock = pygame.time.Clock()

    while True:
        draw_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
              
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "Play"
                elif event.key == pygame.K_ESCAPE:
                    return "Quit"
                elif event.key == pygame.K_SPACE:
                    return "Options"

        clock.tick(60)


count_signals = 0

def draw_signals(WIN):

    global count_signals

    labels = [
        FONTS_NUM.render("3", True, (255, 255, 255)),
        FONTS_NUM.render("2", True, (255, 255, 255)),
        FONTS_NUM.render("1", True, (255, 255, 255))
    ]

    for label in labels:

        x = (TRACK_WIDTH - label.get_width()) // 2
        y = (TRACK_HEIGHT - label.get_height()) // 2


        center_x = TRACK_WIDTH // 2
        center_y = TRACK_HEIGHT // 2
        pygame.draw.circle(WIN, (255, 0, 0), (center_x, center_y), 90)


        WIN.blit(label, (x, y))

        pygame.display.update()
        pygame.time.delay(1000)

        count_signals+=1

 
def game_loop():
    run = True

    global PLAYER_LAP_COUNT
    global COMPUTER_LAP_COUNT

    while run:
        clock.tick(60)
        
        draw(WIN,images,player_car,computer_car)
        
        if count_signals!=3:
            draw_signals(WIN)        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # computer_car.draw_points(WIN)     ..function call use to draw tracking points

        player_car.move_player_car()
        computer_car.move_computer_car()
        
        if player_car.collide(track_border_mask) != None: #Since value is none when object isnt colliding
            player_car.bounce()

        if computer_car.collide(track_border_mask) != None:
            computer_car.bounce()


        computer_point_of_collision_finish = computer_car.collide(finish_line_mask,130,250)

        if computer_point_of_collision_finish is not None:
            COMPUTER_LAP_COUNT += 1

            computer_car.reset()
            if COMPUTER_LAP_COUNT == WINNING_LAP:
                draw_winning_screen(WIN)
                break

            
        player_point_of_collision_finish = player_car.collide(finish_line_mask,130,250)
        if player_point_of_collision_finish != None:
            if player_point_of_collision_finish[1] == 0:    #If Player tries to cross finish line from forward (the co-ordinate of y component is 0 at that position) then the player bounces back
                player_car.bounce()
            else:
                PLAYER_LAP_COUNT +=1

                player_car.reset()
                

                if PLAYER_LAP_COUNT == WINNING_LAP:
                    draw_winning_screen(WIN)
                    break
        
    
    player_car.reset_after_closure()
    computer_car.reset_after_closure()


def draw_option_menu(WIN):
    WIN.fill((10,10,30))
    vehicles = [
        (red_car_option,(TRACK_WIDTH//2-200,TRACK_HEIGHT//2)),
        (green_car_option,(TRACK_WIDTH//2,TRACK_HEIGHT//2)),
        (grey_car_option,(TRACK_WIDTH//2+200,TRACK_HEIGHT//2))
    ]

    option_font = FONTS.render("Select your Vehicle",1,(255,255,255))
    WIN.blit(option_font,((TRACK_WIDTH - option_font.get_width()) // 2+30, TRACK_HEIGHT // 2 - 100))

    car_rects = []

    for vehicle, pos in vehicles:
        WIN.blit(vehicle, pos)
        rect = pygame.Rect(pos[0], pos[1], vehicle.get_width(), vehicle.get_height())
        car_rects.append((rect, vehicle))  # Here storing both, the rectangle and the vehicle

    pygame.display.update()

    return car_rects

    



def option_loop():
    clock = pygame.time.Clock()
    while True:
        car_rects = draw_option_menu(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, vehicle_img in car_rects:
                    if rect.collidepoint(mouse_pos):
                        player_car.car_img = resize_image(vehicle_img,0.275)  
                        return   
        clock.tick(60)



def main():
    while True:
        choice = menu_loop()
        if choice == "Play":
            game_loop()
        elif choice == "Options":
            option_loop()
        elif choice == "Quit":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
