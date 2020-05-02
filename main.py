#Snake Tutorial Python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class Cube(object):
    """Klasa dla kostki, która jest cześcią snake oraz snack"""
    rows = 20
    w = 500
    def __init__(self,start,direction_for_x =1,direction_for_y=0,color=(255,0,0)):
        self.position = start
        self.direction_for_x = 1
        self.direction_for_y = 0
        self.color = color

    def move(self, direction_for_x , direction_for_y):
        self.direction_for_x = direction_for_x
        self.direction_for_y = direction_for_y
        self.position = (self.position[0] + self.direction_for_x, self.position[1] + self.direction_for_y)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i*distance+1, j*distance+1, distance-2, distance-2))
        if eyes:
            centre = distance//2
            radius =3
            circleMiddle1 = (i*distance+centre-radius, j*distance+8)
            circleMiddle2 = (i*distance + distance - radius*2, j*distance+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle1, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



        # zostało dodane 1 do i oraz j by kostka nie rusowała się na liniach siatki, -2 dwa tak samo

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.direction_for_x = 0
        self.direction_for_y = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # run = False
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_for_x = -1
                    self.direction_for_y = 0
                    self.turns[self.head.position[:]] = [self.direction_for_x, self.direction_for_y]
                elif keys[pygame.K_RIGHT]:
                    self.direction_for_x = 1
                    self.direction_for_y = 0
                    self.turns[self.head.position[:]] = [self.direction_for_x, self.direction_for_y]
                elif keys[pygame.K_DOWN]:
                    self.direction_for_x = 0
                    self.direction_for_y = 1
                    self.turns[self.head.position[:]] = [self.direction_for_x, self.direction_for_y]
                elif keys[pygame.K_UP]:
                    self.direction_for_x = 0
                    self.direction_for_y = -1
                    self.turns[self.head.position[:]] = [self.direction_for_x, self.direction_for_y]

        for index, element in enumerate(self.body):
            p = element.position[:]
            if p in self.turns:
                turn = self.turns[p]
                element.move(turn[0], turn[1])
                if index == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if element.direction_for_x == -1 and element.position[0] <= 0:
                    element.position = (element.rows - 1, element.position[1])
                elif element.direction_for_x == 1 and element.position[0] >= element.rows - 1:
                    element.position = (0, element.position[1])
                elif element.direction_for_y == 1 and element.position[1] >= element.rows - 1:
                    element.position = (element.position[0], 0)
                elif element.direction_for_y == -1 and element.position[1] <= 0:
                    element.position = (element.position[0], element.rows - 1)
                else:
                    element.move(element.direction_for_x, element.direction_for_y)

    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_for_x = 0
        self.direction_for_y = 1

    def addCube(self):
        tail = self.body[-1]
        dx = tail.direction_for_x
        dy = tail.direction_for_y
        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0]-1,tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0]+1,tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0],tail.position[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0],tail.position[1]+1)))

        self.body[-1].direction_for_x = dx
        self.body[-1].direction_for_y = dy

    def draw(self, surface):
        for i, element in enumerate(self.body):
            if i == 0:
                element.draw(surface, True)
            else:
                element.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    
    x = 0 
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y= y + sizeBtwn
        # rysowanie linii
        pygame.draw.line(surface, (255,255,255), (x,0), (x, w))
        pygame.draw.line(surface, (255,255,255), (0,y), (w, y))



def redrawWindow(surface):
    global rows, width, snake, snack
    surface.fill((120,120,160))
    snake.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.position == (x,y), positions))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass



def main():
    global width, rows, snake, snack
    width = 500
    # height = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake((255,100,0), (10, 10))
    snack = Cube(randomSnack(rows, snake), color=(0, 255, 0))
    run = True

    clock = pygame.time.Clock()

    while run:

        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.addCube()
            snack = Cube(randomSnack(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x+1:])):
                print('Score: ', len(snake.body))
                message_box('Game Over', 'Play again')
                snake.reset((10, 10))
                break

        redrawWindow(win)




main()