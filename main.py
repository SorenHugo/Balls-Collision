import pygame
from random import randint
import sys
import os

class Vector2D:
    def __init__ (self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector2D(self.x + v.x, self.y + v.y)

    def __sub__(self,v):
        return Vector2D(self.x - v.x, self.y - v.y)

    def __mul__(self,k):
        return Vector2D(self.x * k, self.y * k)

    __rmul__ = __mul__

    def __div__(self,k):
        return Vector2D(self.x / k, self.y / k)

    def magnitude(self):
        return (self.x**2 + self.y**2)**0.5

    def normalize(self):
        m = self.magnitude()
        if m == 0 :
            self.x = 1
            m = 1
        self.x /= m
        self.y /= m

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def __iter__(self):
        yield self.x
        yield self.y

class Ball:
    def __init__(self, 
                 center = (0, 0), 
                 radius = 0, 
                 velocity = (0, 0), 
                 screendimension = (1024, 786), 
                 color = (0, 0, 0), 
                 density = 4
                 ):
        self.x, self.y = center
        self.radius = radius
        self.mass = (4/3) * 3.14 * radius**3 * density  
        self.speedx, self.speedy = velocity
        self.color = color
        self.screenwidth, self.screenheight = screendimension
    
    def velocity(self):
        return (self.speedx, self.speedy)
    
    def center(self):
        return (self.x, self.y)
                    
    def move(self):
        if (self.x - self.radius < 0 or self.x + self.radius > self.screenwidth):
            self.speedx *= -1  
        if (self.y - self.radius < 0 or self.y + self.radius > self.screenheight):
            self.speedy *= -1
        self.x += self.speedx
        self.y += self.speedy  
    
    def checkcollision(self,ball):
        dist = ((self.x - ball.x)**2 + (self.y - ball.y)**2)**0.5
        distfuture = (((self.x + self.speedx) - (ball.x + ball.speedx))**2 + 
                      ((self.y + self.speedy) - (ball.y + ball.speedy))**2)**0.5 
        if (distfuture > dist):
            return False
        if (dist < self.radius + ball.radius):
             return True
        return False
       
    def collide(self,b) :
        dirvector = Vector2D(self.x - b.x , self.y - b.y)
        dirvector.normalize()
        u1 = Vector2D(*self.velocity()).dot(dirvector)
        u1normal = Vector2D(*self.velocity()) - u1 * dirvector
        u2 = Vector2D(*b.velocity()).dot(dirvector) 
        u2normal = Vector2D(*b.velocity()) - u2 * dirvector
        v1 = ((self.mass - b.mass) * u1 + 2 * b.mass * u2) / (self.mass + b.mass)
        v2 = ((b.mass - self.mass) * u2 + 2 * self.mass * u1) / (self.mass + b.mass)
        self.speedx, self.speedy = u1normal + v1 * dirvector
        b.speedx, b.speedy = u2normal + v2 * dirvector

def mainloop(screen, balls):
    while True:
        screen.fill((245,245,245))

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
                return
        
        # Move and draw balls
        for i in range(len(balls)):
            balls[i].move()
            pygame.draw.circle(screen, balls[i].color, (int(balls[i].x), int(balls[i].y)), int(balls[i].radius))

        # Check for collisions
        for i in range(len(balls)):
            for j in range(i, len(balls)):
                if (balls[i].checkcollision(balls[j])):
                    balls[i].collide(balls[j])
                    
        pygame.display.flip()

if __name__ == "__main__":
    try:
        num = int(input("请输入小球的数量（建议2-10个）："))
    except ValueError:
        print("输入无效，使用默认值5")
        num = 5
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'  #居中显示窗口
    screen = pygame.display.set_mode(size=(1024,786))
    pygame.display.set_caption("模拟光滑平面内小球的碰撞")
    screen.fill((245,245,245))

    balls = []
    for i in range(num):
        balls.append(Ball(center = (randint(60, 1024 - 60), randint(60, 768 - 60)), 
                          radius = randint(50, 80), 
                          velocity = (randint(0, 2), randint(0, 2))
                         ))
        
    mainloop(screen, balls)
