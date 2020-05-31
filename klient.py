import pygame
import socket
import time
from player import Player
from mob import Mob
from settings import *
import pickle
import sys
from pygame.locals import *
import threading

pygame.init()


class Socket:
    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect(("127.0.0.1", 4444))
    def recieve_data(self):
        self.data = self.clientsocket.recv(1024 * 4)
        self.data = pickle.loads(self.data)

        return self.data



class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('arial.ttf', 45)
        self.clock = pygame.time.Clock()



    def print_text(self, gracz, t):
        if gracz == 1:
            self.text_to_screen(self.win, t, 0, 0)
        if gracz == 2:
            self.text_to_screen(self.win, t, WIDTH - 150, 0)

    def text_objects(self, text, font):

        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()

    def text_to_screen(self, screen, text, x, y, color):
        size = 35
        color = color
        font_type = 'arial.ttf'
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    def redraw_window(self, win, gracz, p1, p2, mobs, projectiles1, projectiles2):

        for m in mobs:
            mob = Mob(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8])
            mob.draw(win)
        if gracz == 1:
            p1.draw(win)
            for p in projectiles1:
                p.draw(win)

        if gracz == 2:
            p2.draw(win)
            for p in projectiles2:
                p.draw(win)

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.win, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.win, ic, (x, y, w, h))

        smallText = pygame.font.SysFont("arial", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.win.blit(textSurf, textRect)

    def game_intro(self):
        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.win.fill(WHITE)
            largeText = pygame.font.SysFont("arial", 115)
            TextSurf, TextRect = self.text_objects("SUPER GRA", largeText)
            TextRect.center = ((WIDTH / 2), (HEIGHT / 2))
            self.win.blit(TextSurf, TextRect)

            self.button("Wejdź do gry", 150, 450, 100, 50, GREEN, (128, 255, 0), self.display)
            self.button("Wyjdź", 550, 450, 100, 50, RED, (255, 128, 0), self.quit_game)

            pygame.display.update()
            self.clock.tick(15)
            # text_to_screen(win, "Oczekiwanie na drugiego gracza...", 140, HEIGHT // 2)

    def game_wait(self):

        intro = True

        while intro:
            for event in pygame.event.get():
                # print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.win.fill(WHITE)
            self.text_to_screen(self.win, "Oczekiwanie na drugiego gracza...", 140, HEIGHT // 2, BLACK)


            pygame.display.update()
            # win.blit(TextSurf, TextRect)

    def quit_game(self):
        print('qweqwe')

    def display(self):
        socket = Socket()
        pygame.init()


        bg = pygame.image.load("bg1.png").convert()

        game_finished = False
        data = []
        key_left = False
        key_right = False
        is_shooting = False
        onGround = True
        isHit1 = False
        isHit2 = False
        sprite_hit = False
        countdown = 1000
        bt = 1
        s_id = None

        while game_finished == False:

            self.win.blit(bg, (0, 0))
            dt = self.clock.tick(60) / 1000

            bt -= dt

            tab = socket.recieve_data()

            game_score = tab[5][0]
            mobs_left = tab[5][1]

            self.text_to_screen(self.win, game_score, WIDTH // 2, 0, WHITE)
            self.text_to_screen(self.win, mobs_left, WIDTH // 3, 0, WHITE)

            p1 = Player(tab[0][0], tab[0][1], tab[0][2], tab[0][3], tab[0][4], tab[0][5])
            p2 = Player(tab[1][0], tab[1][1], tab[1][2], tab[1][3], tab[1][4], tab[1][5])
            mobs = []
            for m in tab[2]:
                mobs.append(m)

            self.redraw_window(self.win, 1, p1, p2, mobs, tab[3], tab[4])
            self.redraw_window(self.win, 2, p1, p2, mobs, tab[3], tab[4])
            pygame.display.update()
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        key_left = True
                    if event.key == pygame.K_d:
                        key_right = True

                    if event.key == pygame.K_SPACE:
                        is_shooting = True



                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        key_left = False
                    if event.key == pygame.K_d:
                        key_right = False
                    if event.key == pygame.K_SPACE:
                        is_shooting = False
                    if event.key == pygame.K_SPACE:
                        is_shooting = False

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            socket = Socket()
            arr = [key_left, key_right, is_shooting, onGround, isHit1, isHit2, sprite_hit, s_id, dt, dt]

            data_arr = pickle.dumps(arr)
            socket.clientsocket.send(data_arr)

# def koniecgry(msg,kolor):
#     screen_text = font.render(msg, True, kolor)
#     win.blit(screen_text, [300, 200])
#

game = Game()
game.game_intro()


