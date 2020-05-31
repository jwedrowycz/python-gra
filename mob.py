import pygame
import random
WIDTH = 800
HEIGHT = 600
class Mob:
    def __init__(self, x, y, width, height, color, vely, velx, id, hp):
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.rect = (x,y,width,height)
        self.velx = velx
        self.vely = vely
        self.hp = hp
        self.id = id



    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)



