import math
import pygame

class Sprite:
    def __init__(self, x, y, speed, img):
        self.image = pygame.image.load(img)
        self.speed = speed
        self.speedY = 0
        self.x = x
        self.y = y
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

class Button(Sprite):
    def __init__(self,x,y,imgOnHover,imgOffHover):
        Sprite.__init__(self, x, y,0, imgOnHover)
        self.imgOnHover = imgOnHover
        self.imgOffHover = imgOffHover

    def update(self):
        if (self.x < pygame.mouse.get_pos()[0]<self.x+self.width
                and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
            self.image = self.imgOnHover
        else:
            self.image = self.imgOffHover

    def isPressed(self):
        if (self.x < pygame.mouse.get_pos()[0]<self.x+self.width
                and self.y < pygame.mouse.get_pos()[1] < self.y + self.height):
            return pygame.mouse.get_pressed()[0]
        else:
            return False

class Camera():
    def __init__(self, world_width,world_height,screen_width,screen_height):
        self.x = 0
        self.y =-800
        self.world_width = world_width
        self.world_height =  world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
    def update(self, sprite):
        if (sprite.x < self.world_width - self.screen_width/2
                and sprite.x > self.screen_width/2):
            self.x = int(self.screen_width/2)-sprite.x

        if (sprite.y < self.world_height - self.screen_height/2
                and sprite.y > self.screen_height/2):
            self.y = int(self.screen_height/2)-sprite.y

class Player(Sprite):
    def __init__(self,x,y,speed,img):
        Sprite.__init__(self, x, y,speed, img)
        self.imgR = self.image
        self.imgL = pygame.transform.flip(self.image, True, False)
        self.dir = 'right'


    def update(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x+=self.speed
            self.dir = 'right'
        if keys[pygame.K_LEFT]:
            self.x-=self.speed
            self.dir = 'left'
        if keys[pygame.K_UP]:
            self.y-=self.speed
        if keys[pygame.K_DOWN]:
            self.y+=self.speed
        if self.dir == 'right':
            self.image = self.imgR
        else:
            self.image = self.imgL

class Bullet(Sprite):
    def __init__(self,x,y,x_mouse,y_mouse,img):
        Sprite.__init__(self, x, y,0, img)
        self.begin_rasst = math.sqrt(math.pow(x_mouse - x, 2) + math.pow(y_mouse - y, 2))
        self.x_prirost = (x_mouse - x) / (self.begin_rasst) * 10
        self.y_prirost = (y_mouse - y) / (self.begin_rasst) * 10
        self.x_nachala = x
        self.y_nachala = y
    def rasst(self,x0,y0,x1,y1):
        return  math.sqrt(math.pow(x1 - x0, 2) + math.pow(y1 - y0, 2))

class Portal(Sprite):
    def __init__(self, x, y,list_images):
        Sprite.__init__(self, x, y, 0, list_images[0])
        self.cooldown = 0
        self.list_images = []
        for i in range(len(list_images)):
            image = pygame.image.load(list_images[0])
            image = pygame.transform.scale(image, [
                int(image.get_width()*0.3),
                int(image.get_height()*0.3),
            ])
            self.list_images.append(image)
        self.nomer = 0

    def update(self):
        self.cooldown+=1
        if self.cooldown == 50:
            self.cooldown = 0
            if self.nomer==len(self.list_images)-1:
                self.nomer = 0
            else:
                self.nomer += 1
            self.image =self.list_images[self.nomer]


class Zombi(Sprite):
    def __init__(self,x,y,sprite,img):
        Sprite.__init__(self, x, y, 0, img)
        self.cel = sprite
        self.begin_rasst = math.sqrt(math.pow(sprite.x - x, 2) + math.pow(sprite.y - y, 2))
        self.x_prirost = (sprite.x - x) / (self.begin_rasst) * 5
        self.y_prirost = (sprite.y - y) / (self.begin_rasst) * 5

    def update(self):
        self.begin_rasst = math.sqrt(math.pow(self.cel.x - self.x, 2) + math.pow(self.cel.y - self.y, 2))
        self.x_prirost = (self.cel.x - self.x) / (self.begin_rasst) * 5
        self.y_prirost = (self.cel.y - self.y) / (self.begin_rasst) * 5
        self.x+=self.x_prirost
        self.y+=self.y_prirost

