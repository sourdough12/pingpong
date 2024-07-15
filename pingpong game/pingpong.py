from pygame import *
x = 100
y = 100
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from random import randint, choice
import time as timer
window_width = 1500
window_height = 900
window = display.set_mode((window_width, window_height))

init()

from random import randint, choice

bg = transform.scale( image.load('football field.png'), (window_width, window_height))

class Character(sprite.Sprite):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y,speed):
        super().__init__()
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.image = transform.scale(image.load(self.filename),(self.size_x,self.size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def draw(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
class Player(Character):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y,speed,score):
        self.score = score
        super().__init__(filename,size_x,size_y,pos_x,pos_y,speed)
class Ball(Character):
    def __init__(self,filename,size_x,size_y,pos_x,pos_y,speed_x,speed_y):
        super().__init__(filename,size_x,size_y,pos_x,pos_y,0)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.angle = 0
        self.rotate_speed = 3
        self.rotate_image = self.image
        self.rotate_rect = self.rotate_image.get_rect(center = (self.rect.x, self.rect.y))
    def update(self):
        if self.rect.y < 0:
            self.speed_y *= -1
        if self.rect.x < 0:
            self.speed_x *= -1
        if self.rect.y > window_height-self.size_y:
            self.speed_y *= -1
        if self.rect.x > window_width-self.size_x:
            self.speed_x *= -1
        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x 
    def rotate(self):
        self.angle += self.rotate_speed
        self.rotate_image = transform.rotate(self.image,self.angle)
        self.rotate_rect = self.rotate_image.get_rect(center = (self.rect.x, self.rect.y))
    def draw(self):
        window.blit(self.rotate_image,(self.rotate_rect.x, self.rotate_rect.y))
        draw.rect(window,(255,0,0),self.rotate_rect,2)  

player_left =  Player('bar.png',100,300,100,300,10,0)
player_right = Player('bar.png',100,300,1300,300,10,0)
ball = Ball("football.png",100,100,700,400,8,8)


clock = time.Clock()
fps = 60
font.init()
style = font.SysFont(None,70)
game = True
finish = False
score = 3
isResetBallPosition = False 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(fps)
    window.blit(bg, (0,0))
    player_left.draw()
    player_right.draw() 
    ball.draw()
    ball.rotate()

    text = style.render(str(player_left.score)+ "-"+ str(player_right.score),True,(255,255,255))
    window.blit(text,(500,20))



    


    if finish == False:
        ball.update()
        key_pressed = key.get_pressed()
        if key_pressed[K_w] and player_left.rect.y > 0:
            player_left.rect.y -= player_left.speed   
        if key_pressed[K_s] and player_left.rect.y < window_height-player_left.size_y:
            player_left.rect.y += player_left.speed   
        if key_pressed[K_UP] and player_right.rect.y > 0:
            player_right.rect.y -= player_right.speed 
        if key_pressed[K_DOWN] and player_right.rect.y < window_height-player_right.size_y:
            player_right.rect.y += player_right.speed 

        collide_left = sprite.collide_rect(ball,player_left)
        if collide_left == 1:
            ball.speed_x *= -1
        collide_right = sprite.collide_rect(ball,player_right)
        if collide_right == 1:
            ball.speed_x *= -1

        if ball.rect.x > window_width-ball.size_x:
            player_left.score += 1
            isResetBallPosition = True
        if ball.rect.x < 0:
            player_right.score += 1 
            isResetBallPosition = True
        if isResetBallPosition:
            ball.rect.x = 700
            ball.rect.y = 400
            isResetBallPosition = False


        if player_left.score == score or player_right.score == score:
            finish = True
    else:
        if player_left.score == score:
            text_win_left = style.render('LEFT WINS!',True,(255,255,255))
            window.blit(text_win_left,(500,100))
        if player_right.score == score:
            text_win_right = style.render('RIGHT WINS!',True,(255,255,255))
            window.blit(text_win_right,(500,100))



#         isCollide = sprite.collide_rect(player1,player2)
#         if isCollide:
#             hp -= 1
#             player1.rect.x = 600
#             player1.rect.y = 200
#             if hp <= 0:
#                 print('YOU LOSE')
#                 finish = True
#         isCollide_Treasure = sprite.collide_rect(player1,treasure)
#         if isCollide_Treasure:
#             print('YOU WIN')
#             finish = True