# import required libraries
from curses import KEY_DOWN
from pickle import NONE
import time
import pygame
import itertools
import random

WIDTH, HEIGHT = 800, 800
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#Some colors that will be used in the game
BLUE = (0, 0, 255)
RED = (0, 0, 255)

#Initialize the available pixels for the food (except those that have the snake on)
available_pixels = list(itertools.product(*[range(0,500,10),range(0,500,10)]))


FPS = 3

def draw_window():
    return

#Where the snake is heading to
direction = NONE

start = 100
PIXEL_SIZE = 20 #How big one pixel is

class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.is_snake = False
        self.is_food = False
        self.color = color

    def draw(self):
        pygame.draw.rect(WIN, self.color,[self.x, self.y, PIXEL_SIZE, PIXEL_SIZE], 0)        


class Snake:
    def __init__(self):
        self.head = Pixel(200, 200, BLUE) #Initial head position of the snake
        self.blocks = [self.head] #Position of all the snake blocks
        self.direction = None
        self.color = BLUE
    def move_left(self):
        self.blocks.insert(0, Pixel(self.blocks.x - PIXEL_SIZE) [self.blocks[0][0] - PIXEL_SIZE, self.blocks[0][1]])
        del self.blocks[-1]
    def move_right(self):
        self.blocks.insert(0, [self.blocks[0][0] + PIXEL_SIZE, self.blocks[0][1]])
        del self.blocks[-1]
    def move_up(self):
        self.blocks.insert(0, [self.blocks[0][0], self.blocks[0][1] - PIXEL_SIZE])
        del self.blocks[-1]
    def move_down(self):
        self.blocks.insert(0, [self.blocks[0][0], self.blocks[0][1] + PIXEL_SIZE])
        del self.blocks[-1]
    def draw(self):
        for block in self.blocks:
            block.draw()
            print(self.direction)
            print('draw')

class Food:
    def __init__(self):
        self.color = RED


def main():
    clock = pygame.time.Clock()
    run = True
    snake = Snake()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'
                elif event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'
                elif event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
                
        if snake.direction == 'left':
            print('left')
            snake.move_left()
        elif snake.direction == 'right':
            print('right')
            snake.move_right()
        elif snake.direction == 'up':
            print('up')
            snake.move_up()
        elif snake.direction == 'down':
            print('down')
            snake.move_down()
        WIN.fill((100, 100, 23))
        snake.draw()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

