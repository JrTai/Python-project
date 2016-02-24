# Minesweeper game

import random
import simplegui

# Global size, width and heigh must be same number, for instance 500 x 500 or 600 x 600
screen = (600, 600)
flag_state = False
game_on = True
N = 10
bomb_number = N + 1
win = False
bomb_win = bomb_number
flag_count = 0

# import image
Flag_size= (120, 150)
Flag_image = simplegui.load_image("http://ext.pimg.tw/mozaiyang/4b703de1793d5.jpg")
Bomb_size = (781, 800)
Bomb_image = simplegui.load_image("http://www.clipartlord.com/wp-content/uploads/2013/09/bomb2.png")
White_size = (313, 313)
White_image = simplegui.load_image("http://www.champion.com.tw/upload/Tile/i000002/PA88000.jpg")
Block_size = (1600, 1600)
Block_image = simplegui.load_image("http://www.queensu.ca/connect/grad/files/2014/01/question-mark-block.jpg")

# N x N Minesweeper
def new_game():
    global N, bomb_list, flag_list, open_list, grid_center, grid_size, number_list
    global number_map, bomb_number
    #N = 10
    #bomb_number = N * 3
    print bomb_number
    grid_size = (screen[0] / N, screen[1] / N)
    grid_center = (grid_size[0] / 2, grid_size[1] / 2)
    
    # Creat bomb_list and shuffle the list
    bomb_list = []
    for i in range(N * N):
        if bomb_number != 0:
            bomb_list.append(1)
            bomb_number -= 1
        else:
            bomb_list.append(0)
    random.shuffle(bomb_list)
    
    # Creat open list, decise which grid is open
    open_list = []
    for i in range(N * N):
        open_list.append(False)
    
    # Flag list    
    flag_list = []
    for i in range(N * N):
        flag_list.append(False)
    
    print "Bomb_MAP"
    # Bomb map for view
    for number in range(N):
        temp = list(bomb_list[number * N: N * (number + 1)])
        print temp
    
    print "Number_MAP"
    # Creat corresponding number map
    number_map = []
    for i in range(N * N):
        number_map.append(0)
        
    # Caculate bomb around
    for number in range(N * N):
        bomb_count = 0
        # left up corner
        if number == 0:
            if bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # right up corner
        elif number == N - 1:
            if bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # left down corner
        elif number == N*N - N:
            if bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N+1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N+1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N+1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # right down corner
        elif number == N*N - 1:
            if bomb_list[number - 1] + bomb_list[number - N] + bomb_list[number - N-1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number - N] + bomb_list[number - N-1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number - N] + bomb_list[number - N-1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count 
                bomb_count = 0
        # up line 
        elif 0 < number < N -1:
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number + N-1] + bomb_list[number + N] + bomb_list[number + N+1] == 5:
                bomb_count += 5
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number + N-1] + bomb_list[number + N] + bomb_list[number + N+1] == 4:
                bomb_count += 4
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number + N-1] + bomb_list[number + N] + bomb_list[number + N+1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number + N-1] + bomb_list[number + N] + bomb_list[number + N+1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number + N-1] + bomb_list[number + N] + bomb_list[number + N+1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # down line 
        elif N*N - N < number < N*N - 1:
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N-1] + bomb_list[number - N] + bomb_list[number - N+1] == 5:
                bomb_count += 5
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N-1] + bomb_list[number - N] + bomb_list[number - N+1] == 4:
                bomb_count += 4
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N-1] + bomb_list[number - N] + bomb_list[number - N+1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N-1] + bomb_list[number - N] + bomb_list[number - N+1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N-1] + bomb_list[number - N] + bomb_list[number - N+1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # left line
        elif number % N == 0 and number != 0 and number != N*N - N: 
            if bomb_list[number - N] + bomb_list[number - N+1] + bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 5:
                bomb_count += 5
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N+1] + bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 4:
                bomb_count += 4
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N+1] + bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N+1] + bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N+1] + bomb_list[number + 1] + bomb_list[number + N] + bomb_list[number + N+1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        # right line
        elif number % N == N-1 and number != N-1  and number != N*N - 1: 
            if bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 5:
                bomb_count += 5
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 4:
                bomb_count += 4
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 3:
                bomb_count += 3
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 2:
                bomb_count += 2
                number_map[number] = bomb_count
                bomb_count = 0
            if bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - 1] + bomb_list[number + N] + bomb_list[number + N-1] == 1:
                bomb_count += 1
                number_map[number] = bomb_count
                bomb_count = 0
        else:
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 8:
                    bomb_count += 8
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 7:
                    bomb_count += 7
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 6:
                    bomb_count += 6
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 5:
                    bomb_count += 5
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 4:
                    bomb_count += 4
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 3:
                    bomb_count += 3
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 2:
                    bomb_count += 2
                    number_map[number] = bomb_count
                    bomb_count = 0
            if bomb_list[number - 1] + bomb_list[number + 1] + bomb_list[number - N] + bomb_list[number - N-1] + bomb_list[number - N+1] + bomb_list[number + N] + bomb_list[number + N-1] + bomb_list[number + N+1] == 1:
                    bomb_count += 1
                    number_map[number] = bomb_count
                    bomb_count = 0                
                
    # Test number map
    for number in range(N):
        temp = list(number_map[number * N: N * (number + 1)])
        print temp

# Drawing in Canvas
def draw_handler(canvas):
    for row in range(N):
        temp = list(bomb_list[row * N: N * (row + 1)])
        for col in range(N):
            if flag_list[row * N + col] == False and open_list[row * N + col] == False:
                canvas.draw_image(Block_image, (Block_size[0] / 2, Block_size[1] / 2), Block_size, 
                                  (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                  grid_size * 0.9)
            elif open_list[row * N + col] == False:
                canvas.draw_image(Flag_image, (Flag_size[0] / 2, Flag_size[1] / 2), Flag_size, 
                                  (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                  grid_size * 0.9)                
            if open_list[row * N + col]:
                if temp[col] == 1:
                    canvas.draw_image(White_image, (White_size[0] / 2, White_size[1] / 2), White_size, 
                                      (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                      grid_size * 0.9)
                    canvas.draw_image(Bomb_image, (Bomb_size[0] / 2, Bomb_size[1] / 2), Bomb_size, 
                                      (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                      grid_size)
                else:
                    canvas.draw_image(White_image, (White_size[0] / 2, White_size[1] / 2), White_size, 
                                      (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                      grid_size )
                    canvas.draw_text(str(number_map[row * N + col]), 
                                      (grid_center[0] * 0.8 + (grid_size[0] * col), grid_center[1] * 1.3 + (grid_size[1] * row)), 
                                      grid_size[0] * 0.5, "Blue")
                    if number_map[row * N + col] == 0:
                        canvas.draw_image(White_image, (White_size[0] / 2, White_size[1] / 2), White_size, 
                                          (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                          grid_size)                                                          
            if not game_on:
                if temp[col] == 1:
                    canvas.draw_image(White_image, (White_size[0] / 2, White_size[1] / 2), White_size, 
                                      (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                      grid_size * 0.9)
                    canvas.draw_image(Bomb_image, (Bomb_size[0] / 2, Bomb_size[1] / 2), Bomb_size, 
                                      (grid_center[0] + (grid_size[0] * col), grid_center[1] + (grid_size[0] * row)), 
                                      grid_size)
                canvas.draw_text('You lose!', (screen[0] / 2 * 0.5, screen[1] / 2 ), 80, 'Blue', 'serif')
                
            if win:
                canvas.draw_text('You win!', (screen[0] / 2 * 0.5, screen[1] / 2 ), 80, 'Black', 'serif')
                    
# helper function for open number around
def open_around(grid):
    #print "open number ", point
    if bomb_list[grid] != 1:
        if number_map[grid] != 0 and open_list[grid] == False and flag_list[grid] == False:
            open_list[grid] = True
   

# helper function for open grid
def open_grid(grid):
    global point
    #print "open ", point
    if bomb_list[grid] != 1:
        if number_map[grid] == 0 and open_list[grid] == False and flag_list[grid] == False:
            open_list[grid] = True
            point += grid - point
            #print "move to ", point
            open_detect(point)
    

# helper turning open function
def open_detect(index):
    global open_list, point
    point = index
    #print "start ", point
    around = [point + 1, point - 1, 
              point + N, point + N+1, point + N-1, 
              point - N, point - N+1, point - N-1]
    left_up_cornor = [point + 1,point + N, point + N+1]
    right_up_cornor = [point - 1,point + N, point + N-1]
    left_down_cornor = [point + 1,point - N, point - N+1]
    right_down_cornor = [point - 1,point - N, point - N-1]    
    up_line = [point + 1, point - 1, point + N, point + N+1, point + N-1]
    left_line = [point + 1, point + N, point + N+1, point - N, point - N+1]
    right_line = [point - 1, point + N, point + N-1, point - N, point - N-1]
    down_line = [point + 1, point - 1, point - N, point - N+1, point - N-1]
    
    #if 0 <= grid <= N*N - 1:
    # left up corner
    if point == 0:
        for grid in left_up_cornor:
            open_around(grid)
            open_grid(grid)
    # right up corner
    elif point == N-1:
        for grid in right_up_cornor:
            open_around(grid)
            open_grid(grid)
    # left down corner
    elif point == N*N - N:
        for grid in left_down_cornor:
            open_around(grid)
            open_grid(grid)
    # right down corner
    elif point == N*N - 1:
        for grid in right_down_cornor:
            open_around(grid)
            open_grid(grid)
            
    # up line
    elif 0 < point < N-1:
        for grid in up_line:
            open_around(grid)
            open_grid(grid)
    # left line
    elif point % N == 0:
         for grid in left_line:
            open_around(grid)
            open_grid(grid)
    # right line
    elif point % N == N-1:
        for grid in right_line:
            open_around(grid)
            open_grid(grid)

    # down line
    elif N*N - N < point < N*N - 1:
        for grid in down_line:
            open_around(grid)
            open_grid(grid)

    # center region
    else:
        for grid in around:
            open_around(grid)
            open_grid(grid)
           

# Mouse handler
def mouse_handler(position):
    global game_on, count, bomb_number, win, N, flag_count
    count = 0
    x = position[0] // grid_size[0] + 1
    y = position[1] // grid_size[1] + 1
    index_mouse = (y - 1) * N + (x - 1)
    #print "mouse ", index_mouse
    if game_on and not win:
        if flag_state:
            if flag_list[index_mouse] == True:
                flag_list[index_mouse] = False
                flag_count -= 1
            elif flag_list[index_mouse] == False:
                flag_list[index_mouse] = True
                flag_count += 1
                for i in range(N * N):
                    if open_list[i] == True:
                        count += 1
                        if count == N * N - bomb_win and flag_count == bomb_win:
                            win = True
                            print "You Win!!"
            return
        else:
            if bomb_list[index_mouse] == 1 and flag_list[index_mouse] == False:
                open_list[index_mouse] = True
                game_on = False
                return
            elif flag_list[index_mouse] == False:
                open_list[index_mouse] = True
                if number_map[index_mouse] == 0 and bomb_list[index_mouse] != 1:
                    open_detect(index_mouse)
                    
        for i in range(N * N):
            if open_list[i] == True:
                count += 1
                if count == N * N - bomb_win and flag_count == bomb_win:
                    win = True
                    print "You Win!!"

# key handler
def keydown(key):
    global flag_state
    if key == simplegui.KEY_MAP["space"]:
        flag_state = True  
    
  
def keyup(key):
    global flag_state
    if key == simplegui.KEY_MAP["space"]:
        flag_state = False

# New game handler
def button_handler():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    N = 5
    bomb_number = N + 1
    flag_count = 0
    bomb_win = bomb_number
    game_on = True
    win = False
    new_game()

def button_handler2():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    game_on = True
    win = False
    N = 10
    bomb_number = N + 1
    flag_count = 0
    bomb_win = bomb_number
    new_game()
    

def button_handler3():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    N =15
    bomb_number = N * 2
    flag_count = 0
    bomb_win = bomb_number
    game_on = True
    win = False
    new_game()
    
    
def button_handler4():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    N = 20
    bomb_number = N * 3
    flag_count = 0
    bomb_win = bomb_number
    game_on = True
    win = False
    new_game()
    
    
def button_handler5():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    N = 25
    bomb_number = N * 4
    flag_count = 0
    bomb_win = bomb_number
    game_on = True
    win = False
    new_game()
    
    
def button_handler6():
    global game_on, N, bomb_number, bomb_win, win, flag_count
    N = 30
    bomb_number = N * 5
    flag_count = 0
    bomb_win = bomb_number
    game_on = True
    win = False
    new_game()
    
    
#def input_handler(number):
#    global game_on, bomb_number
#    game_on = True
#    bomb_number = int(number)
#    new_game()
        
        
# simplegui frame
frame = simplegui.create_frame('Minesweeper', screen[0], screen[1])
frame.add_label('Hold space key to mark a mine while clicking!')
button1 = frame.add_button('New Game (5 x 5)', button_handler)
button2 = frame.add_button('New Game (10 x 10)', button_handler2)
button3 = frame.add_button('New Game (15 x 15)', button_handler3)
button4 = frame.add_button('New Game (20 x 20)', button_handler4)
button5 = frame.add_button('New Game (25 x 25)', button_handler5)
button6 = frame.add_button('New Game (30 x 30)', button_handler6)
#inp = frame.add_input('Change bomb number!', input_handler, 50)
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(mouse_handler)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.start()
new_game()

    
    
    

