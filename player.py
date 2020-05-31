import pygame


class Player:
    def __init__(self, x, y, width, height, color, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        self.hp = hp


    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
