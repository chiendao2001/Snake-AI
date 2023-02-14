# import required libraries
from curses import KEY_DOWN
from pickle import NONE
import time
import pygame
import itertools
import random

WIDTH, HEIGHT = 600, 600
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#Some colors that will be used in the game
BLUE = (0, 0, 255)
RED = (0, 255, 0)

#Initialize the available pixels for the food (except those that have the snake on)
available_pixels = list(itertools.product(*[range(0,500,10),range(0,500,10)]))


FPS = 10

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
        print(self.color)

available_pixels = []
for i in range(40):
    for j in range(40):
        available_pixels.append(100 * i + j)

class Food:
    def __init__(self):
        available_pixels = []
        for i in range(WIDTH // 20):
            for j in range(HEIGHT // 20):
                available_pixels.append(100 * i + j)
        self.available_pixels = available_pixels
        food_coordinates = random.choice(self.available_pixels) # Get x and y coordinates for new food pixel
        self.current_pixel = Pixel(20 * (food_coordinates // 100), (food_coordinates % 100) * 20, RED)    
    
    def remove_pixel(self, pixel):
        self.available_pixels.remove((pixel.x / PIXEL_SIZE) * 100 + (pixel.y / PIXEL_SIZE))

    def spawn_food(self, is_collide):
        if is_collide or self.current_pixel == None:
            food_coordinates = random.choice(self.available_pixels) # Get x and y coordinates for new food pixel
            self.current_pixel = Pixel(20 * (food_coordinates // 100), (food_coordinates % 100) * 20, RED)
        print(self.current_pixel.x)
        print(self.current_pixel.y)
        print(self.current_pixel.color)
        self.current_pixel.draw()

class Snake:
    def __init__(self):
        self.head = Pixel(WIDTH / 2, HEIGHT / 2, BLUE) #Initial head position of the snake
        self.blocks = [self.head] #Position of all the snake blocks
        self.direction = None
        self.color = BLUE
        self.is_collide = False
        self.length = 1
    def move_left(self):
        self.blocks.insert(0, Pixel(self.head.x - PIXEL_SIZE, self.head.y, BLUE))
        self.head = self.blocks[0]
        del self.blocks[-1]
    def move_right(self):
        self.blocks.insert(0, Pixel(self.head.x + PIXEL_SIZE, self.head.y, BLUE))
        self.head = self.blocks[0]
        del self.blocks[-1]
    def move_up(self):
        self.blocks.insert(0, Pixel(self.head.x, self.head.y - PIXEL_SIZE, BLUE))
        self.head = self.blocks[0]
        del self.blocks[-1]
    def move_down(self):
        self.blocks.insert(0, Pixel(self.head.x, self.head.y + PIXEL_SIZE, BLUE))
        self.head = self.blocks[0]
        del self.blocks[-1]
    def draw(self):
        for block in self.blocks:
            block.draw()

def main():
    clock = pygame.time.Clock()
    run = True
    snake = Snake()
    food = Food()
    food.remove_pixel(snake.head)
    
    while run:
        pygame.time.delay(50)
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
            snake.move_left()
        elif snake.direction == 'right':
            snake.move_right()
        elif snake.direction == 'up':
            snake.move_up()
        elif snake.direction == 'down':
            snake.move_down()


        #Detect collision
        if abs(snake.head.x - food.current_pixel.x) < 20 and abs(snake.head.y - food.current_pixel.y) < 20:
            snake.is_collide = True
        else:
            snake.is_collide = False
        WIN.fill((100, 100, 23))
        snake.draw()
        food.spawn_food(snake.is_collide)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

