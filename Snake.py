# import required libraries
from curses import KEY_DOWN
from pickle import NONE
import time
import pygame
import itertools
import random

WIDTH, HEIGHT = int(160), int(160)
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#Some colors that will be used in the game
BLUE = (0, 0, 255)
RED = (0, 255, 0)

#Initialize the available pixels for the food (except those that have the snake on)
available_pixels = list(itertools.product(*[range(0,500,10),range(0,500,10)]))


FPS = 5

def draw_window():
    return

#Where the snake is heading to
direction = NONE

start = 100
PIXEL_SIZE = int(20) #How big one pixel is

class Pixel:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.is_snake = False
        self.is_food = False
        self.color = color

    def draw(self):
        pygame.draw.rect(WIN, self.color,[self.x, self.y, PIXEL_SIZE, PIXEL_SIZE], 0)        

available_pixels = []
for i in range(40):
    for j in range(40):
        available_pixels.append(100 * i + j)

class Food:
    def __init__(self, is_collide, snake_length, grid):
        self.current_pixel = None
        self.spawn_food(is_collide, snake_length, grid)    
    
    def remove_pixel(self, pixel):
        self.available_pixels.remove((pixel.x / PIXEL_SIZE) * 100 + (pixel.y / PIXEL_SIZE))

    def add(self, pixel):
        self.available_pixels.append((pixel.x / PIXEL_SIZE) * 100 + (pixel.y / PIXEL_SIZE))

    def spawn_food(self, is_collide, snake_length, grid):
        # if is_collide or self.current_pixel == None:
        #     food_coordinates = random.choice(self.available_pixels) # Get x and y coordinates for new food pixel
        #     self.current_pixel = Pixel(20 * (food_coordinates // 100), (food_coordinates % 100) * 20, RED)
        # self.current_pixel.draw()
        random_pixel = 0
        counter = 0

        if is_collide or self.current_pixel == None:
            print(grid.cells)
            random_pixel = random.randint(0, (WIDTH // PIXEL_SIZE) * (HEIGHT // PIXEL_SIZE) - snake_length - 1)
            # print(random_pixel)
            for i in range(len(grid.cells)):
                # print(i)
                # print(grid.cells[i])
                if grid.cells[i] == False:
                    if counter == random_pixel:
                        print('spawn')
                        print(random_pixel)
                        print(i)
                        print(grid.cells[i])
                        self.current_pixel = Pixel(PIXEL_SIZE * (i % (WIDTH // 20)),PIXEL_SIZE * (i // (WIDTH // 20)), RED)
                        break
                    counter = counter + 1
        # else:


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
        if not self.is_collide:
            del self.blocks[-1]

    def move_right(self):
        self.blocks.insert(0, Pixel(self.head.x + PIXEL_SIZE, self.head.y, BLUE))
        self.head = self.blocks[0]
        if not self.is_collide:
            del self.blocks[-1]

    def move_up(self):
        self.blocks.insert(0, Pixel(self.head.x, self.head.y - PIXEL_SIZE, BLUE))
        self.head = self.blocks[0]
        if not self.is_collide:
          del self.blocks[-1]

    def move_down(self):
        self.blocks.insert(0, Pixel(self.head.x, self.head.y + PIXEL_SIZE, BLUE))
        self.head = self.blocks[0]
        if not self.is_collide:
            del self.blocks[-1]
    
    def draw(self):
        for block in self.blocks:
            block.draw()
    
    #Grow after eating food:
    # def grow(self, grid):
        # if len(self.blocks) > 1:
        #     if self.blocks[-1].x == self.blocks[-2].x:
        #         #The tail is moving up
        #         if self.blocks[-1].y > self.blocks[-2].y:
        #             if self.blocks[-1].y + PIXEL_SIZE < HEIGHT and grid.cells[int(sel.y * (HEIGHT // 20) // 20 + block.x // 20)] 
        #             self.blocks.append(Pixel(self.blocks[-1].x, self.blocks[-1].y + PIXEL_SIZE, BLUE))
        #         else:
        #             self.blocks.append(Pixel(self.blocks[-1].x, self.blocks[-1].y + PIXEL_SIZE, BLUE))
        #     else:
        #         if self.blocks[-1].x > self.blocks[-2].x:
        #             self.blocks.append(Pixel(self.blocks[-1].x + PIXEL_SIZE, self.blocks[-1].y, BLUE))
        #         else:
        #             self.blocks.append(Pixel(self.blocks[-1].x - PIXEL_SIZE, self.blocks[-1].y, BLUE))
        # else:
        #     if self.direction == 'left':
        #         self.blocks.append(Pixel(self.blocks[-1].x + PIXEL_SIZE, self.blocks[-1].y, BLUE))
        #     if self.direction == 'right':
        #         self.blocks.append(Pixel(self.blocks[-1].x - PIXEL_SIZE, self.blocks[-1].y, BLUE))
        #     if self.direction == 'up':
        #         self.blocks.append(Pixel(self.blocks[-1].x, self.blocks[-1].y + PIXEL_SIZE, BLUE))
        #     if self.direction == 'down':
        #         self.blocks.append(Pixel(self.blocks[-1].x, self.blocks[-1].y - PIXEL_SIZE, BLUE))

class Grid:
    def __init__(self):
        self.cells = [False for i in range((WIDTH // PIXEL_SIZE) * (HEIGHT // PIXEL_SIZE))]

def main():
    clock = pygame.time.Clock()
    run = True
    snake = Snake()
    grid = Grid()
    food = Food(snake.is_collide, snake.length, grid)


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
                else:
                    snake.direction = None



        if snake.direction == 'left':
            snake.move_left()
        elif snake.direction == 'right':
            snake.move_right()
        elif snake.direction == 'up':
            snake.move_up()
        elif snake.direction == 'down':
            snake.move_down()
        
        if abs(snake.head.x - food.current_pixel.x) < 20 and abs(snake.head.y - food.current_pixel.y) < 20:
            snake.is_collide = True
            snake.length = snake.length + 1
            # food.remove_pixel(snake.blocks[-1])
        else:
            snake.is_collide = False

        #Detect collision with itself or wall:

            # print(block.x, block.y)
            # print(int(block.y * (HEIGHT // 20) // 20 + block.x // 20))
        # print('-----')

        #Detect collision with itself (game over)
        if snake.direction != None:
            if snake.head.x < 0 or snake.head.x > WIDTH - PIXEL_SIZE or snake.head.y < 0 or snake.head.y > HEIGHT- PIXEL_SIZE:
                pygame.quit()
            elif grid.cells[int(snake.head.y * (HEIGHT // 20) // 20 + snake.head.x // 20)] == True:
                pygame.quit()

        

        grid = Grid()
        for block in snake.blocks:
            print(block.x, block.y)
            grid.cells[int(block.y * (HEIGHT // 20) // 20 + block.x // 20)] = True
        

        #Dectect collision with wall or itself (game over):


        WIN.fill((100, 100, 23))
        snake.draw()
        food.spawn_food(snake.is_collide, snake.length, grid)
        # print(food.current_pixel.x, food.current_pixel.y)
        food.current_pixel.draw()
        
            
        # print(grid.cells)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

