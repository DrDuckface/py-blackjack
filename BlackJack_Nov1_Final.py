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

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600

# initialize some useful global variables
deck = None
in_play = False
outcome = ""
score = 0
player_hand = None
dealer_hand = None

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

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):        
        if self.suit == None:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        hand_string = "Hand contains " 
        
        for card in self.cards:
            hand_string += (card.get_suit() + card.get_rank() + " ")
            
        return hand_string

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
        return value
            
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.cards.append(card)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop(0)
    
    def __str__(self):
        # return a string representing the deck
        deck_string = "Deck contains " 
        
        for card in self.cards:
            deck_string += (card.get_suit() + card.get_rank() + " ")
            
        return deck_string


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand
    
    outcome = "Welcome to BlackJack! Hit or stand?"
    
    #Create and shuffle deck
    deck = Deck()
    deck.shuffle()
    
   #Create player hand
    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    
    #Create dealer hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Print hands
    print "Player hand: " + str(player_hand)
    print "Dealer hand: " + str(dealer_hand)
    
    in_play = True


def hit():
    global player_hand, outcome, score, in_play
    
    # Check that hand is in play
    if in_play == False:
        outcome = "Game is over. Deal new game."
        return
    
    # if player hand value is less than 21
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        print "Player hits. Hand value: " + str(player_hand.get_value())
        outcome = "Hit or stand?"    
    
    # if player busts
    if player_hand.get_value() > 21:  
        outcome = "Player has busted!"
        in_play = False
        score -= 1
        print outcome
    
       
def stand():
    global dealer_hand, outcome, in_play, score
   
    # Check if player has busted
    if in_play == False:
        outcome = "Game is over. Deal new game."
        return
    
    while dealer_hand.get_value() <= 17:
        dealer_hand.add_card(deck.deal_card())
    
    # Dealer value
    print "Dealer hand value: " + str(dealer_hand.get_value())
    print "Player hand value: " + str(player_hand.get_value())
        
    # Check if dealer has busted
    if dealer_hand.get_value() > 21:
        outcome = "Dealer has busted!"
        score += 1
        print outcome
    
    elif dealer_hand.get_value() < player_hand.get_value():
        outcome = "Player wins!"
        score += 1
        print outcome
        
    else:
        outcome = "Dealer wins!"
        score -= 1
        print outcome
        
    in_play = False
        

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    # draw title and labels
    canvas.draw_text("BlackJack", [5, CANVAS_HEIGHT/2], 20, "white")
    canvas.draw_text("Player", [5, 116], 16, "white")
    canvas.draw_text("Dealer", [5, CANVAS_HEIGHT - CARD_SIZE[1] - 9], 16, "white")
    
    # draw score
    canvas.draw_text("Score: " + str(score), [5, CANVAS_HEIGHT/2 + 20], 16, "white")
    
    # draw dialog
    canvas.draw_text(outcome, [CANVAS_WIDTH/3, CANVAS_HEIGHT/2], 16, "white")
    
    # draw hands
    player_hand.draw(canvas, [0, 0])
    dealer_hand.draw(canvas, [ 0, CANVAS_HEIGHT - CARD_SIZE[1] ])
    
    # conditionally hide `hole` card until game is over
    if in_play == True:
        card = Card("X", "X") # intentially invalid card
        card.draw(canvas, [ 0, CANVAS_HEIGHT - CARD_SIZE[1] ])
        

# initialization frame
frame = simplegui.create_frame("Blackjack", CANVAS_WIDTH, CANVAS_HEIGHT)
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