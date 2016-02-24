# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_vel = [0, 0]
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_pos = [PAD_WIDTH / 2, HEIGHT / 2]
paddle2_pos = [WIDTH - (PAD_WIDTH / 2), HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4) + (abs(ball_vel[0]) * 0.5)
        ball_vel[1] = -random.randrange(2, 6) + (-abs(ball_vel[1]) * 0.5)
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(2, 4) + (-abs(ball_vel[0]) * 0.5)
        ball_vel[1] = -random.randrange(2, 6) + (-abs(ball_vel[1]) * 0.5)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_vel
    score1 = 0
    score2 = 0
    ball_vel = [0, 0]
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")    
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]            
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[0] > WIDTH / 2:
        if ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT / 2 and ball_pos[1] >= paddle2_pos[1] - PAD_HEIGHT / 2 and ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
            ball_vel[0] = - ball_vel[0]
        elif ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
            spawn_ball(LEFT)
            score1 += 1
    if ball_pos[0] < WIDTH / 2:
        if ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT / 2 and ball_pos[1] >= paddle1_pos[1] - PAD_HEIGHT / 2 and ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
            ball_vel[0] = - ball_vel[0]
        elif ball_pos[0] < PAD_WIDTH + BALL_RADIUS:
            spawn_ball(RIGHT)
            score2 += 1

    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] >= PAD_HEIGHT / 2 and paddle1_pos[1] <= HEIGHT - PAD_HEIGHT / 2:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] < PAD_HEIGHT:
        paddle1_pos[1] += 1
    else:
        paddle1_pos[1] -= 1
    if paddle2_pos[1] >= PAD_HEIGHT / 2 and paddle2_pos[1] <= HEIGHT - PAD_HEIGHT / 2:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] < PAD_HEIGHT:
        paddle2_pos[1] += 1
    else:
        paddle2_pos[1] -= 1
        
    
    # draw paddles
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1]- PAD_HEIGHT / 2],[paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT / 2], PAD_WIDTH, "Blue")
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1]- PAD_HEIGHT / 2],[paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT / 2], PAD_WIDTH, "Blue")    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4, 40), 36, 'Red')
    canvas.draw_text(str(score2), (WIDTH * 3 / 4, 40), 36, 'Red')
        
def keydown(key):
    global paddle1_vel, paddle2_vel 
    paddle_move_speed = 8
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_move_speed
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_move_speed
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_move_speed
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_move_speed       
    
  
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle_move_speed = 8
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += paddle_move_speed
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= paddle_move_speed
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel += paddle_move_speed
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= paddle_move_speed
    


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', new_game, 100)


# start frame
new_game()
frame.start()
