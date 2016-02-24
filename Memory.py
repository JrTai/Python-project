# implementation of card game - Memory

import simplegui
import random

ls1 = range(8)
ls2 = range(8)
ls_card = ls1 + ls2
random.shuffle(ls_card)
exposed=[]
for i in range(16):
    exposed.append(False)
state = 0
count = 0

print ls_card
print exposed


# helper function to initialize globals
def new_game():
    global state, count
    random.shuffle(ls_card)
    for i in range(16):
        exposed[i] = False
    state = 0
    count = 0
    label.set_text("Turns = " + str(count))


     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, index1, index2, count
    click_pos = [pos[0], pos[1]]
    
    if state == 0:
        for i in range(16):
            if exposed[i] != True:
                if 50 + 50 * (i - 1) < click_pos[0] < 50 + 50 * i:
                    exposed[i] = True
                    index1 = i
                    state = 1
                    count += 1
    elif state == 1:
        for i in range(16):
            if exposed[i] != True:
                if 50 + 50 * (i - 1) < click_pos[0] < 50 + 50 * i:
                    exposed[i] = True
                    index2 = i
                    state = 2
                    #count += 1
    elif state == 2:
        if ls_card[index1] == ls_card[index2]:
            for i in range(16):
                if exposed[i] != True:
                    if 50 + 50 * (i - 1) < click_pos[0] < 50 + 50 * i:
                        exposed[index1] = True
                        exposed[index2] = True
                        exposed[i] = True
                        index1 = i
                        state = 1
                        count += 1
        else:
            for i in range(16):
                if exposed[i] != True:
                    if 50 + 50 * (i - 1) < click_pos[0] < 50 + 50 * i:
                        exposed[index1] = False
                        exposed[index2] = False
                        exposed[i] = True
                        index1 = i
                        state = 1
                        count += 1
    
    # Test of program
    #print count
    #print ls_card
    #print exposed
    
    # Output and update the Turns
    label.set_text("Turns = " + str(count))
                    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    i = 0
    space = 50
    number_size = 60
    for number in ls_card:
        if exposed[i] == True:
            canvas.draw_text(str(number), (14 + i * space, 75), number_size, 'White')
            i += 1
        else:
            canvas.draw_line([24.5 + (i * space ), 3], [25 + (i * space ), 98], 44, 'Green')
            i += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric