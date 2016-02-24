# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
hide_card = True
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.hand)):
            ans += " " + str(self.hand[i])
        return "Hand contains" + ans


    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        number = []
        a_count = 0
        hand_value = 0
        for i in range(len(self.hand)):
            ans = ""
            ans += str(self.hand[i])           
            number.append(ans[1])
        for rank in number:
            if rank == 'A':
                a_count += 1
        if a_count == 0:
            for rank in number:
                hand_value += VALUES[rank]
            return hand_value
        else:
            for rank in number:
                hand_value += VALUES[rank]
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value         
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand)):
            suit_rank = str(self.hand[i])
            suit = suit_rank[0]
            rank = suit_rank[1]
            card = Card(suit, rank)
            card.draw(canvas, [pos[0] + i * 100, pos[1]])
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(suit + rank)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        suit_rank = self.deck.pop(-1)
        suit = suit_rank[0]
        rank = suit_rank[1]  
        return Card(suit, rank)
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.deck)):
            ans += " " + str(self.deck[i])
        return "Deck contains" + ans



#define event handlers for buttons
def deal():
    global outcome, in_play, new_deck, player, dealer, information, score, hide_card

    # your code goes here
    new_deck = Deck()
    new_deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(new_deck.deal_card())
    player.add_card(new_deck.deal_card())
    dealer.add_card(new_deck.deal_card())
    dealer.add_card(new_deck.deal_card())
    information = "Hit or stand?"
    outcome = ""
    
    if in_play:
        score -= 1
        outcome = "You lose..."
    
    in_play = True
    hide_card = True

def hit():
    # replace with your code below
    global outcome, in_play, new_deck, player, dealer, information, score, hide_card
    if in_play:
        outcome = ""
    
    if in_play:
        if player.get_value() <= 21:
            player.add_card(new_deck.deal_card())
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    if in_play:
        if player.get_value() > 21:
            outcome = "You went bust and lose."
            information = "New deal?"
            in_play = False
            hide_card = False
            score -= 1
    
def stand():
    global outcome, in_play, new_deck, player, dealer, information, score, hide_card
    information = "New deal?"
    hide_card = False
    # replace with your code below
    if in_play:
        if player.get_value() > 21:
            outcome = "You went bust and lose."
            in_play = False
            score -= 1
            
    if in_play:
        if dealer.get_value() >= player.get_value():
            outcome = "You lose!!"
            in_play = False
            score -= 1
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < player.get_value():
            dealer.add_card(new_deck.deal_card())
            if dealer.get_value() >= player.get_value() and dealer.get_value() <= 21:
                outcome = "You lose!"
                in_play = False
                score -= 1
    
    # assign a message to outcome, update in_play and score
    if in_play:
        if dealer.get_value() > 21:
            outcome = "Dealer went bust and you win."
            in_play = False
            score += 1
        elif player.get_value() > dealer.get_value():
            outcome = "You win."
            in_play = False
            score += 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BlackJack', (150, 100), 40, 'Aqua')
    canvas.draw_text('Score', (400, 100), 30, 'Black')
    canvas.draw_text(str(score), (480, 100), 30, 'Black')
    canvas.draw_text('Dealer', (20, 175), 30, 'Black')
    canvas.draw_text('Player', (20, 375), 30, 'Black')
    canvas.draw_text(outcome, (120, 175), 30, 'Black')
    canvas.draw_text(information, (120, 375), 30, 'Black')
    
    dealer.draw(canvas, [20, 200])
    player.draw(canvas, [20, 400])
    
    if hide_card:
        canvas.draw_image(card_back, CARD_CENTER, CARD_SIZE, [20 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)
    


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

# remember to review the gradic rubric