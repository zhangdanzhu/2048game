import numpy, sys, random, pygame
from pygame.locals import *

HEIGHT = 400
WIDTH = 400
S_F_SIZE = 10           # 食物和蛇一格的大小
SCREEN_SIZE = (HEIGHT, WIDTH) # 屏幕尺寸
MOVE_PS = 15           # 每秒刷新次数，模拟fps
DIR = 0                 # 蛇移动的方向，0123分别为上右下左
FOOD = [0, 0]           # 食物位置
SNAKE = []              # 蛇
# 屏幕设置，第一个参数分辨率，第二个参数模式(不需要全屏则置0,若需要全屏则为FULLSCREEN)，第三个参数色深
SCREEN = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
SCORE = 0

def run():
    global DIR
    global SCREEN
    global SCORE
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        # 按键
        elif event.type == pygame.KEYDOWN:
            if (event.key == K_ESCAPE):  # 终止程序
                pygame.quit()
                sys.exit(0)
            # 上下左右改变方向,不能去反方向
            elif (event.key == K_LEFT and DIR != 1):
                DIR = 3
            elif (event.key == K_RIGHT and DIR != 3):
                DIR = 1
            elif (event.key == K_UP and DIR != 2):
                DIR = 0
            elif (event.key == K_DOWN and DIR != 0):
                DIR = 2

    # 蛇头接下来的位置
    if (DIR == 0):
        next_head = [SNAKE[0][0], SNAKE[0][1]-1]
    elif (DIR == 1):
        next_head = [SNAKE[0][0]+1, SNAKE[0][1]]
    elif (DIR == 2):
        next_head = [SNAKE[0][0], SNAKE[0][1]+1]
    elif (DIR == 3):
        next_head = [SNAKE[0][0]-1, SNAKE[0][1]]
    # 判断蛇是否会死
    if (next_head[0] >= WIDTH/S_F_SIZE or next_head[0] < 0 or next_head[1] > HEIGHT/S_F_SIZE or next_head[1] < 0) or ((next_head in SNAKE) and (next_head != SNAKE[-1])):
        return 5

    # 更新蛇的位置和形态
    SNAKE.insert(0, next_head)
    if (next_head == FOOD):
        create_food()
        SCORE+=1
        print(SCORE)
    else:
        SNAKE.pop()
    SCREEN.fill((255, 255, 255))
    draw_snake()
    draw_food()

    # 刷新界面
    pygame.display.update()
    # 时钟对象用于控制界面刷新（即蛇移动频率）
    pygame.time.Clock().tick(MOVE_PS)

def draw_snake():
    global SCREEN
    for coord in SNAKE:
        y = coord[1] * S_F_SIZE
        x = coord[0] * S_F_SIZE
        rect = pygame.Rect(x, y, S_F_SIZE, S_F_SIZE)
        pygame.draw.rect(SCREEN, (0, 0, 255), rect)

def draw_food():
    global SCREEN
    rect = pygame.Rect(FOOD[0]*S_F_SIZE, FOOD[1]*S_F_SIZE, S_F_SIZE, S_F_SIZE)
    pygame.draw.rect(SCREEN, (255, 0, 0), rect)

def create_food():
    while True:
        y_food = random.randint(1, HEIGHT/S_F_SIZE - 1)
        x_food = random.randint(1, WIDTH/S_F_SIZE - 1)
        FOOD[1] = y_food
        FOOD[0] = x_food
        if FOOD not in SNAKE:
            break

def init():
    global SCREEN
    # 初始生成蛇和食物
    # 蛇开始位置，不能太靠边
    y_snake = random.randint(10, HEIGHT/S_F_SIZE-10)
    x_snake = random.randint(10, WIDTH/S_F_SIZE-10)
    SNAKE.append([x_snake, y_snake])
    SNAKE.append([x_snake, y_snake+1])
    SNAKE.append([x_snake, y_snake+2])
    print(SNAKE)
    # 食物开始位置
    create_food()

    # 填充白色背景
    SCREEN.fill((255, 255, 255))
    # 画蛇和食物
    draw_snake()
    draw_food()
    print("ss")

    # 显示
    pygame.display.update()

def main():
    global SCREEN
    # pygame初始化
    pygame.init()
    # 初始化
    init()
    # 游戏主体，包括操作、刷新等逻辑控制
    while True:
        if run() == 5:
            break;






if __name__ == '__main__':
    main()