# template for "Stopwatch: The Game"
import simplegui

# define global variables
integer = 0
count_stop = 0
count_spot = 0
target_C = 5
timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global A, B, C, D
    A = t / 600
    B = (((t % 600) - ((t % 600) % 100) ) / 100 ) % 10
    C = ((t - ( t % 10) ) / 10 ) % 10
    D = t % 10
    return str(A) + ":" + str(B) + str(C) + "." + str(D)  
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global timer_running
    timer.start()
    timer_running = True
    
def stop():
    global count_stop, count_spot, timer_running
    timer.stop()
    if timer_running:
        count_stop += 1
        timer_running = False
        if C == target_C and D == 0 and integer != 0:
            count_spot += 1
    

def reset():
    global integer, count_stop, count_spot, target_C
    timer.stop()
    integer = 0
    count_stop = 0
    count_spot = 0
    target_C = 5

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global integer
    integer += 1
    
def input_handler(number):
    global target_C
    try:
        target_C = int(number)
    except:
        return
    

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(integer), (95, 130), 50, "White")
    canvas.draw_text("Hit/Stop", (185, 35), 30, "Red")
    canvas.draw_text("Target", (35, 35), 30, "Red")
    canvas.draw_text(str(count_spot) + "/" + str(count_stop), (205, 70), 30, "Red")
    canvas.draw_text(str(target_C) + ".0", (60, 70), 30, "Red")
    
# create frame
frame = simplegui.create_frame('Stopwatch', 300, 200)
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
button1 = frame.add_button('Start', start, 50)
button2 = frame.add_button('Stop', stop, 50)
button3 = frame.add_button('Reset', reset, 50)
inp = frame.add_input('Enter target seconds (0~9):', input_handler, 50)

# register event handlers


# start frame
frame.start()


# Please remember to review the grading rubric
