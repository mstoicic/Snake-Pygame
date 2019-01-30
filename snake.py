"""
File Name     :: snake.py
Description   :: Classic Snake game created using Pygame module
Dependencies  :: pygame
"""

import math
import os
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# PYGAME SOUND INIT AND SOUND VARIABLES
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

pickup_sound = pygame.mixer.Sound(os.path.join("sound", "Pickup_00.wav"))
end_sound = pygame.mixer.Sound(os.path.join("sound", "Lose_00.wav"))

class cube(object):
    rows = 20
    width = 500

    def __init__(self, start, dirnx = 1, dirny = 0, color = (0, 255, 0)):
        self.pos = start
        # With dirnx = 1 snake starts moving on game start / no need to press any key
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        """Direction in snake object is changed so it needs to be changed here also to stay within object"""
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        """Figures values for snakes cubes to be drawn"""
        dis = self.width // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis + 1, j*dis + 1, dis - 2, dis - 2))  # -2 for creating lines inside cube space
        
        # Creates eyes on starting snakes cube
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius*2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)
        

class snake(object):
    """Snake object containes cube object"""
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        """Movement function"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # Gives list of all keyboard keys
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # Checkes if turn is available
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                # If we are at last turn removes the last position to prevent automatic movements
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # Checks for edge of screen / enables transition from on side to another
                if c.dirnx == -1 and c.pos[0] <= 0: 
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1: 
                    c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0],c.rows - 1)
                # If not on screens edge continue moving
                else: c.move(c.dirnx,c.dirny)


    def reset(self, pos):
        """Resets body, cubes and direction"""
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        """Adds 'snack' cube to end of snake """
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # Logic to sort out direction snake is moving and append cube on end
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # Gives direction of movement to appended cube
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

        # Plays the cube pickup sound sound
        pygame.mixer.Sound.play(pickup_sound)
        

    def draw(self, surface):
        """Checks if snakes body cube is first on the list / If true -> draws eyes on it"""
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    """Grid lines drawing"""
	# Gap between lines needs to be whole number
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        # Draws lines -> horizontal / vertical
        pygame.draw.line(surface, (201, 201, 201), (x, 0),(x, w))
        pygame.draw.line(surface, (201, 201, 201), (0, y),(w, y))
        

def redrawWindow(surface):
    """Creates geme window and all elements"""
    global rows, width, s, snack
    # Sets the surface color
    surface.fill((128, 128, 128))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    """Creates cube 'snack' that snake can eat on random location"""
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        # Checks if created coordinates are inside snakes body to prevent creating snacks in that position
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    """Creates message box above Pygame screen"""
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    """Main function / sets initial parameters"""
    global width, rows, s, snack
    width = 500
    rows = 20

    win = pygame.display.set_mode((width, width))
    s = snake((0, 255, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(255, 0, 0))
    clock = pygame.time.Clock()
    flag = True
    
    while flag:
        # Sets the games speed
        pygame.time.delay(50)   # Higher value -> Slower
        clock.tick(8)           # Lower value -> Slower
        s.move()
        # Check if the head od snake hits a snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        # Check end condition / snake hitting itself
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x + 1:])):
                # Plays the game over sound sound
                pygame.mixer.Sound.play(end_sound)
                print('Score: ', len(s.body))
                message_box('Game Over', 'Play again')
                s.reset((10, 10))
                break

        redrawWindow(win)
    pass

main()