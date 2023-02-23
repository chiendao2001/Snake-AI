# import required libraries
from curses import KEY_DOWN
from pickle import NONE
import pygame
import itertools
import random
import sys
sys.path.append("/Users/chiendao/Desktop/Snake AI/button")


WIDTH, HEIGHT = int(600), int(600)
ROWS = 20
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#Some colors that will be used in the game
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN  = (0, 255, 0)
GREY = (128,128,128)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# button.Button()
#Initialize the available pixels for the food (except those that have the snake on)
available_pixels = list(itertools.product(*[range(0,500,10),range(0,500,10)]))


fps = 5

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

def get_distance(grid, snake_pixel, current_food_pixel):
    distance = -1 
    #Only check if the pixel is inside the grid
    # print(snake_pixel.x, snake_pixel.y)
    if snake_pixel.x >= 0 and snake_pixel.x < WIDTH and snake_pixel.y >= 0 and snake_pixel.y < HEIGHT:
        snake_cell = grid.cells[int((snake_pixel.y // PIXEL_SIZE) * (WIDTH // PIXEL_SIZE) + (snake_pixel.x // PIXEL_SIZE))]
        if not snake_cell:
            distance = abs(snake_pixel.x - current_food_pixel.x) + abs(snake_pixel.y - current_food_pixel.y)
    return distance

def choose_next_move(grid, snake, current_food_pixel):
    # Compute the distance of the 4 cells next to the snake's head to the food
    left_dist = get_distance(grid, Pixel(snake.head.x - PIXEL_SIZE, snake.head.y, BLUE), current_food_pixel) # Left pixel
    right_dist = get_distance(grid, Pixel(snake.head.x + PIXEL_SIZE, snake.head.y, BLUE), current_food_pixel) # Right pixel
    up_dist = get_distance(grid, Pixel(snake.head.x, snake.head.y - PIXEL_SIZE, BLUE), current_food_pixel) #Top pixel
    down_dist = get_distance(grid, Pixel(snake.head.x, snake.head.y + PIXEL_SIZE, BLUE), current_food_pixel) # Up pixel
    
    # print(left_dist, right_dist, up_dist, down_dist)
    # print('------')
    possible_distances = [dist for dist in [left_dist, right_dist, up_dist, down_dist] if dist >= 0]
    if len(possible_distances) > 0:
        next_move = min(possible_distances)
        if left_dist == next_move and snake.direction != 'right':
            snake.direction = 'left'
        elif right_dist == next_move and snake.direction != 'left':
            snake.direction = 'right'
        elif up_dist == next_move and snake.direction != 'down':
            snake.direction = 'up'
        elif down_dist == next_move and snake.direction != 'up':
            snake.direction = 'down'

class Button:
    def __init__(self, x, y , width, height, color, message, message_x, message_y):
        self.x = x
        self.y = y
        self.message_x = message_x
        self.message_y = message_y
        self.width = width
        self.height = height
        self.color = color
        self.message = message

    def draw(self):
        pygame.draw.rect(WIN, self.color, [self.x, self.y, self.width, self.height], 0)
        smallfont = pygame.font.SysFont('Corbel',35)
        text = smallfont.render(self.message , True , BLACK)
        WIN.blit(text, (self.message_x, self.message_y))

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
            # print(grid.cells)
            random_pixel = random.randint(0, (WIDTH // PIXEL_SIZE) * (HEIGHT // PIXEL_SIZE) - snake_length - 1)
            # print(random_pixel)
            for i in range(len(grid.cells)):
                # print(i)
                # print(grid.cells[i])
                if grid.cells[i] == False:
                    if counter == random_pixel:
                        self.current_pixel = Pixel(PIXEL_SIZE * (i % (WIDTH // 20)),PIXEL_SIZE * (i // (WIDTH // 20)), RED)
                        break
                    counter = counter + 1
        # else:


class Snake:
    def __init__(self):
        self.head = Pixel(WIDTH / 2, HEIGHT / 2, GREEN) #Initial head position of the snake
        self.blocks = [self.head] #Position of all the snake blocks
        self.direction = 'left'
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
   
class Grid:
    def __init__(self):
        self.cells = [False for i in range((WIDTH // PIXEL_SIZE) * (HEIGHT // PIXEL_SIZE))]


def draw_text(text, font, text_col, x ,y):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))

def display_menu():
    play_button = Button(WIDTH / 3, HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'PLAY', 3 * WIDTH / 8, 3 * HEIGHT / 16)
    option_button = Button(WIDTH / 3, 3 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'OPTIONS', 3 * WIDTH / 8, 7 * HEIGHT / 16)
    quit_button = Button(WIDTH / 3, 5 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'QUIT', 3 * WIDTH / 8, 11 * HEIGHT / 16)
        
    play_button.draw()
    option_button.draw()
    quit_button.draw()    

def main():
    temp = None # ONly for testing for NOW!!!
    is_main_menu = True #Variable to know if we are in the main menu
    is_playing = False # Indicate whether the player has started the game
    is_manual = False # Indicate the game mode
    is_option = False
    is_level = False
    is_mode = False
    difficulty = 'hard'
    clock = pygame.time.Clock()
    run = True
    pygame.init()
    snake = Snake()
    grid = Grid()
    food = Food(snake.is_collide, snake.length, grid)
    play_button = Button(WIDTH / 3, HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'PLAY', 3 * WIDTH / 8, 3 * HEIGHT / 16)
    option_button = Button(WIDTH / 3, 3 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'OPTIONS', 3 * WIDTH / 8, 7 * HEIGHT / 16)
    quit_button = Button(WIDTH / 3, 5 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'QUIT', 3 * WIDTH / 8, 11 * HEIGHT / 16)
    level_button = Button(WIDTH / 3, HEIGHT / 3, WIDTH / 3, HEIGHT / 8, GREY, 'LEVEL', 2 * WIDTH / 5, 2*HEIGHT/5)
    mode_button = Button(WIDTH / 3, 2 * HEIGHT / 3, WIDTH / 3, HEIGHT / 8, GREY, 'MODE', 2 * WIDTH / 5, 7*HEIGHT/10)
    manual_button = Button(WIDTH / 3, HEIGHT / 3, WIDTH / 3, HEIGHT / 8, GREY, 'MANUAL', 2 * WIDTH / 5, 2*HEIGHT/5)
    ai_button = Button(WIDTH / 3, 2 * HEIGHT / 3, WIDTH / 3, HEIGHT / 8, GREY, 'AI', 2 * WIDTH / 5, 7*HEIGHT/10)
    easy_button = Button(WIDTH / 3, HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'EASY', 3 * WIDTH / 8, 3 * HEIGHT / 16)
    medium_button = Button(WIDTH / 3, 3 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'MEDIUM', 3 * WIDTH / 8, 7 * HEIGHT / 16)
    hard_button = Button(WIDTH / 3, 5 * HEIGHT / 8, WIDTH / 3, HEIGHT / 8, GREY, 'HARD', 3 * WIDTH / 8, 11 * HEIGHT / 16)
    back_button = Button(20, 20, 100, 50, GREY, 'BACK', 30, 30)

    while run:
        WIN.fill((100, 100, 23))
            

        if is_main_menu:
              
            play_button.draw()
            option_button.draw()
            quit_button.draw()

        pygame.time.delay(20)

        if difficulty == 'easy':
            clock.tick(fps)
        elif difficulty == 'medium':
            clock.tick(fps * 2)
        elif difficulty == 'hard':
            clock.tick(fps * 10)

        event = pygame.event.poll()
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
                run = False
        elif event.type == pygame.KEYDOWN: #Only allow interaction if the mode is manual
            if is_manual:    
                if event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                    # print('press left')
                elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'
                    # print('press right')
                elif event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'
                    # print('press up')
                elif event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
                    # print('press down')
            elif event.key == pygame.K_SPACE:
                    if temp == None:
                        temp = snake.direction
                        snake.direction = None
                    else:
                        snake.direction = temp
                        temp = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(mouse)
            if is_main_menu:
                if mouse[0] >= play_button.x and mouse[0] <= play_button.x + play_button.width and mouse[1] >= play_button.y and mouse[1] <= play_button.y + play_button.height:
                    is_playing = True
                    is_main_menu = False
                    print('success')
                elif mouse[0] >= quit_button.x and mouse[0] <= quit_button.x + quit_button.width and mouse[1] >= quit_button.y and mouse[1] <= quit_button.y + quit_button.height:
                    pygame.quit()
                    run = False
                elif mouse[0] >= option_button.x and mouse[0] <= option_button.x + option_button.width and mouse[1] >= option_button.y and mouse[1] <= option_button.y + option_button.height:
                    is_main_menu = False
                    is_option = True
            elif is_option:
                if is_level:
                    if mouse[0] >= easy_button.x and mouse[0] <= easy_button.x + easy_button.width and mouse[1] >= easy_button.y and mouse[1] <= easy_button.y + easy_button.height:
                        difficulty = 'easy'
                    elif mouse[0] >= medium_button.x and mouse[0] <= medium_button.x + medium_button.width and mouse[1] >= medium_button.y and mouse[1] <= medium_button.y + medium_button.height:
                        difficulty = 'medium'
                    elif mouse[0] >= hard_button.x and mouse[0] <= hard_button.x + hard_button.width and mouse[1] >= hard_button.y and mouse[1] <= hard_button.y + hard_button.height:
                        difficulty = 'hard'
                    elif mouse[0] >= back_button.x and mouse[0] <= back_button.x + back_button.width and mouse[1] >= back_button.y and mouse[1] <= back_button.y + back_button.height:
                        is_level = False
                
                elif is_mode:
                    if mouse[0] >= manual_button.x and mouse[0] <= manual_button.x + manual_button.width and mouse[1] >= manual_button.y and mouse[1] <= manual_button.y + manual_button.height:
                        is_manual = True
                    elif mouse[0] >= ai_button.x and mouse[0] <= ai_button.x + ai_button.width and mouse[1] >= ai_button.y and mouse[1] <= ai_button.y + ai_button.height:
                        is_manual = False
                    elif mouse[0] >= back_button.x and mouse[0] <= back_button.x + back_button.width and mouse[1] >= back_button.y and mouse[1] <= back_button.y + back_button.height:
                        is_mode = False

                elif mouse[0] >= level_button.x and mouse[0] <= level_button.x + level_button.width and mouse[1] >= level_button.y and mouse[1] <= level_button.y + level_button.height:
                    is_level = True
                elif mouse[0] >= mode_button.x and mouse[0] <= mode_button.x + mode_button.width and mouse[1] >= mode_button.y and mouse[1] <= mode_button.y + mode_button.height:
                    print('mode')
                    is_mode = True
                elif mouse[0] >= back_button.x and mouse[0] <= back_button.x + back_button.width and mouse[1] >= back_button.y and mouse[1] <= back_button.y + back_button.height:
                    is_option = False
                    is_level = False
                    is_mode = False
                    is_main_menu = True

        if is_playing:
            #Display score
                smallfont = pygame.font.SysFont('Corbel', 30)
                score = smallfont.render('Score: ' + str(snake.length) , True , BLACK)  
                WIN.blit(score, (20, 20))          
            # if is_manual:
                if not is_manual and snake.direction != None:
                    choose_next_move(grid, snake, food.current_pixel)

                if snake.direction == 'left':
                    snake.move_left()
                    # print('left')
                elif snake.direction == 'right':
                    snake.move_right()
                    # print('right')
                elif snake.direction == 'up':
                    snake.move_up()
                    # print('up')
                elif snake.direction == 'down':
                    snake.move_down()
                    # print('down')
                
                if abs(snake.head.x - food.current_pixel.x) < 20 and abs(snake.head.y - food.current_pixel.y) < 20:
                    snake.is_collide = True
                    snake.length = snake.length + 1
                    print(snake.length)
                    # food.remove_pixel(snake.blocks[-1])
                else:
                    snake.is_collide = False

                #Detect collision with itself (game over)
                if snake.direction != None:
                    if snake.head.x < 0 or snake.head.x > WIDTH - PIXEL_SIZE or snake.head.y < 0 or snake.head.y > HEIGHT- PIXEL_SIZE or grid.cells[int(snake.head.y * (HEIGHT // 20) // 20 + snake.head.x // 20)]:
                        if is_manual:
                            is_playing = False
                            is_main_menu = True
                        snake = Snake()
                        grid = Grid()
                        food = Food(snake.is_collide, snake.length, grid)
                        print('-----')

                #Reset the status of each cell on the grid (whethere it is a snake block)
                grid = Grid()
                for block in snake.blocks:
                    grid.cells[int(block.y * (HEIGHT // 20) // 20 + block.x // 20)] = True
            

                snake.draw()
                food.spawn_food(snake.is_collide, snake.length, grid)
                # print(food.current_pixel.x, food.current_pixel.y)
                food.current_pixel.draw()
                
            # else:
            #     pass    
        # pygame.quit()

        if is_option:
            back_button.draw()
            if is_level:
                if difficulty == 'easy':
                    easy_button.color = YELLOW
                    medium_button.color = GREY
                    hard_button.color = GREY
                elif difficulty == 'medium':
                    easy_button.color = GREY
                    medium_button.color = YELLOW
                    hard_button.color = GREY
                else:
                    easy_button.color = GREY
                    medium_button.color = GREY
                    hard_button.color = YELLOW
                easy_button.draw()
                medium_button.draw()
                hard_button.draw()
            elif is_mode:
                if is_manual:
                    manual_button.color = YELLOW
                    ai_button.color = GREY
                else:
                    manual_button.color = GREY
                    ai_button.color = YELLOW
                ai_button.draw()
                manual_button.draw()
            else:
                level_button.draw()
                mode_button.draw()

        if run:
          pygame.display.update()

if __name__ == "__main__":
    main()

