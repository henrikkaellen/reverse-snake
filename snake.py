import curses 
from random import randint

def create_snake(n):
    
    snake = []
    y = randint(5, 15)
    x = randint(20, 40)
    #snake.append((y, x))
    while n > 0:
        snake.append((y, x))
        n -= 1
    
    return snake

#constants

WINDOW_WIDTH = 60  # number of columns of window box 
WINDOW_HEIGHT = 20 # number of rows of window box 
'''
Number of blocks in window per line = WINDOW_WIDTH -2. 
Block x index ranges from 1 to WINDOW_WIDTH -2.
Number of blocks in window per column = WINDOW_HEIGHT -2. 
Block y index ranges from 1 to WINDOW_HEIGHT -2.
'''

# prompt for size growth
while True:
    increase = input("Choose size growth per level (insert a number): ")
    try:
        increase = int(increase)
    except ValueError:
        print("Insert a number")
        continue

    break

# setup window
curses.initscr()
win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0) # rows, columns
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1) # -1

# snake and food
#increase = input("By how much shall n increase each round? Insert a number: ")
n = 3
#snake = [(4,11), (4,10), (4,9), (4,8), (4,7), (4,6), (4,5), (4, 4), (4, 3), (4, 2)]
snake = create_snake(n)
food = (6, 6)

win.addch(food[0], food[1], '#')
# game logic
score = 0
level = 1

ESC = 27
key = curses.KEY_RIGHT

while key != ESC:
    win.addstr(0, 2, 'Level ' + str(level) + ' ')
    win.timeout(150 - (len(snake)) // 5 + len(snake)//10 % 120) # increase speed
    #win.timeout(150 - (level*4) // 5 + (level*4)//10 % 120)

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP, curses.KEY_DOWN, ESC]:
        key = prev_key

    # calculate the next coordinates
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    if key == curses.KEY_UP:
        y -= 1
    if key == curses.KEY_LEFT:
        x -= 1
    if key == curses.KEY_RIGHT:
        x += 1

    snake.insert(0, (y, x)) # append O(n)

    # check if we hit the border
    if y == 0: break
    if y == WINDOW_HEIGHT-1: break
    if x == 0: break
    if x == WINDOW_WIDTH -1: break

    # if snake runs over itself
    if snake[0] in snake[1:]: break

    if snake[0] == food:
        # eat the food
        score += level
        food = ()
        while food == ():
            food = (randint(1,WINDOW_HEIGHT-2), randint(1,WINDOW_WIDTH -2))
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '#')
        remove1 = snake.pop()
        win.addch(remove1[0], remove1[1], ' ')
        
        remove2 = snake.pop()
        win.addch(remove2[0], remove2[1], ' ')

    else:
        # move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')
    
    if snake:
        win.addch(snake[0][0], snake[0][1], '*')
    else:
        n += increase
        snake = create_snake(n)
        level += 1
        key = curses.KEY_RIGHT

curses.endwin()
print(f"Your Final score is {score}")
print(f"You reached Level {level}")