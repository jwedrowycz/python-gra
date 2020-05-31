import pygame
import random
WIDTH = 800
HEIGHT = 600

class Projectile:
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 7

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
