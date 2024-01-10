import random
import os
import time 
from colorama import Fore, Back, Style, init

suits = ['♠︎', '♣', '♦', '♥']

faces = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']

blitz_count = 0 

init()

def main_game():
    global blitz_count
    blitz_count = 0 
    play_again = True
    
    while play_again:
        while True: 
            winning_player = single_round()
            if blitz_count > 1:
                print(f"{Fore.BLUE}It's a tie!{Fore.RESET}")
            elif blitz_count == 1:
                print(f"{Fore.BLUE}{winning_player} wins! {Fore.RESET}")
            else: 
                print(f"\n{Fore.BLUE}{winning_player} wins! {Fore.RESET}")
            
            play_again_input = ''
            while play_again_input not in ('y', 'n'):
                print('')
                play_again_input = input("Would you like to play again? (y/n): ")
            
            if play_again_input == 'n':
                play_again = False
                break
    print()
    print(f"{Fore.RED}Thanks for playing!{Fore.RESET}")

def determine_winner(player_hands, running_totals):
    winning_suit, max_points = '', 0 
    winning_player = ''
    
    for current_player in player_hands:
        player_running_totals = running_totals[current_player]
        for suit in player_running_totals:
            points = player_running_totals[suit]
            if points > max_points:
                max_points = points 
                winning_suit = suit 
                winning_player = current_player 
    return winning_player

def improve_hand(deck, disc_cards, running_totals, player, hand):
    print(f"\n{Fore.BLUE}{player}'s {Fore.RESET} turn to improve hand: ")
    print_points(running_totals, player)
    display_hand(hand)
    time.sleep(5)
    os.system('clear')

    hand, drawn_card = draw_card(deck, hand, disc_cards) # draws a card from the deck
    add_running_totals(running_totals, player, drawn_card)
    print_points(running_totals, player)
    display_hand(hand)
    time.sleep(2)

    hand, disc_cards, discarded_card = remove_card(hand, disc_cards) # allows user to remove a card from their hand 
    subtract_running_totals(running_totals,player, discarded_card)
    print_points(running_totals, player)
    display_hand(hand)
    
    return hand 

def call_game():
    call_options = ('y', 'n')
    player_call = ''
    while player_call not in call_options:
        print('') # for consistent format 
        player_call = input("Think you have a winning hand? Would you like to call the game? (y or n) ")

    if player_call == 'y':
        return True 
    else: 
        return False 

def scan_blitz(running_totals, player):
    for suit in running_totals[player]:
        points = running_totals[player][suit]
        if points == 31:
            print(f"\n{Fore.BLUE}You have a blitz!{Fore.RESET}")
            return True
    
    return False

def scan_three_of_a_kind(hand, running_totals, player):
    face_counts = {face: 0 for face in faces}

    for face, suit in hand:
        if face in face_counts:
            face_counts[face] += 1

    for face, count in face_counts.items():
        if count == 3:
            running_totals[player]['♠︎'] = 30
            running_totals[player]['♣'] = 0
            running_totals[player]['♦'] = 0
            running_totals[player]['♥'] = 0

    return running_totals
         
    
def startings_totals(running_totals, player, player_hand):
    for card in player_hand:
        face, suit = card
        if suit in suits:
            if face == 'A':
                running_totals[player][suit] += 11 
            elif face in ('J','K','Q'):
                running_totals[player][suit] += 10
            else:
                running_totals[player][suit] += face
    return running_totals

def add_running_totals(running_totals, player, drawn_card):
    face, suit = drawn_card 
    if face == 'A':
        running_totals[player][suit] += 11 
    elif face in ('J','K','Q'):
        running_totals[player][suit] += 10
    else:
        running_totals[player][suit] += face
    return running_totals

def subtract_running_totals(running_totals,player, discarded_card):
    face, suit = discarded_card 
    if face == 'A':
        running_totals[player][suit] -= 11 
    elif face in ('J','K','Q'):
        running_totals[player][suit] -= 10
    else:
        running_totals[player][suit] -= face
    return running_totals

def print_points(running_totals, player):
    for suit in suits:
        points = running_totals[player][suit]
        print(f"{suit}: {points} points")
        
def get_num_players():
    player_options = ('2','3','4','5','6')
    num_players = ""
    while num_players not in player_options:
        num_players = input("Enter number of players: ") 
    return num_players

def player_hands_dict(num_players):
    player_hands_dict = {f"Player {i + 1}": [] for i in range(int(num_players))} # initializes dict of lists 
    return player_hands_dict # returns players and their hands 

def single_round():
    num_players = get_num_players() # asks user for number of players
    player_hands = player_hands_dict(num_players) # creates dict of list for each player's hand
    running_totals = {player: {'♠︎': 0, '♣': 0,'♦': 0, '♥': 0} for player in player_hands}
    deck = take_pile() # initializes deck 
    disc_cards = disc_pile() # initializes discarded cards from deck
    
    for player in player_hands:
        player_hands[player], deck = deal_cards(deck, 3)
        startings_totals(running_totals, player, player_hands[player])
        running_totals = scan_three_of_a_kind(player_hands[player], running_totals, player) # checks for three of a kind
    
    all_player_hands = player_hands
    
    game_called = False
    while not game_called:
        for player in all_player_hands: # each player will draw a card and discard a card 
            player_hand = all_player_hands[player]
            print(f"\n{Fore.BLUE}{player}'s{Fore.RESET} turn: ")
            winning_player, game_called = single_turn(deck, disc_cards, running_totals, player, player_hands)
            time.sleep(1)

            if winning_player:
                return winning_player
    
    return None
        
def single_turn(deck, disc_cards, running_totals, player, all_player_hands):     
    hand = all_player_hands[player]
    print_points(running_totals, player)
    display_hand(hand) # displays player their current hand

    game_call = call_game()
    if game_call:
        os.system('clear')
        print(f"\n{Fore.BLUE}{player} {Fore.RESET}{Fore.RED}calls the game! Other players have one final turn to improve their hand. {Fore.RESET}")
        for other_player in all_player_hands:
            if other_player != player:
                mutable_hand = list(all_player_hands[other_player])
                all_player_hands[other_player] = improve_hand(deck, disc_cards, running_totals, other_player, mutable_hand)
                

        time.sleep(1)
        winning_player = determine_winner(all_player_hands, running_totals)
        return winning_player, True # sets game_called to True
    

    blitz_win = scan_blitz(running_totals, player)
    running_totals = scan_three_of_a_kind(hand, running_totals, player)
    if blitz_win:
        global blitz_count
        print(f"\n{Fore.BLUE}{player}{Fore.RESET} has a blitz! Each player will have one more chance to get 31 points.")
        blitz_count += 1
        return player, False # sets game_called to False 

     
    time.sleep(2)
    os.system('clear')
    hand, drawn_card = draw_card(deck, hand, disc_cards) # draws a card from the deck
    add_running_totals(running_totals, player, drawn_card)
    print_points(running_totals, player)
    display_hand(hand)

    time.sleep(2)
    hand, disc_cards, discarded_card = remove_card(hand, disc_cards) # allows user to remove a card from their hand 
    subtract_running_totals(running_totals,player, discarded_card)
    print_points(running_totals, player)
    display_hand(hand)
    time.sleep(5)
    os.system('clear')

    all_player_hands[player] = hand 

    return None, False

    
    
def draw_card(deck, hand, disc_cards):
    print("\nDrawing a card...")
    if not deck:
        print("Shuffling the discarded cards to create a new deck.")
        deck = disc_cards 
    drawn_card = deck.pop() # takes last card of the deck (card on top)
    hand.append(drawn_card)
    return hand, drawn_card

def remove_card(hand, disc_cards):
    disc_options = ('1','2','3','4')
    chosen_card = ''
    while chosen_card not in disc_options:
        chosen_card = input("\nChoose a card to remove (1-4): ")
    print(f"\nRemoving card {chosen_card}...")
    chosen_card_index = int(chosen_card) - 1
    discarded_card = hand.pop(chosen_card_index)
    disc_cards.append(discarded_card)
    return hand, disc_cards, discarded_card

def take_pile():
    deck = [] # deck is a list of tuples 
    for suit in suits:
        for face in faces:
            deck.append((face, suit))
    if deck:
        print(f' ____________ ')
        print(f'|            |')
        print(f'|            |')
        print(f'|            |')
        print(f'|    {Fore.BLUE}deck    {Fore.RESET}|')
        print(f'|            |')
        print(f'|            |')
        print(f'|____________|')
    return deck

def disc_pile():
    disc_cards = []
    print(f' ____________ ')
    print(f'|            |')
    print(f'|            |')
    print(f'|    {Fore.RED}disc    {Fore.RESET}|')
    print(f'|    {Fore.RED}pile    {Fore.RESET}|')
    print(f'|            |')
    print(f'|            |')
    print(f'|____________|')
    return disc_cards
   
def deal_cards(deck, cards): 
    random.shuffle(deck)
    hand = deck[:cards]
    deck = deck[cards:]
    return hand, deck

def display_hand(hand):
    lines = [""] * 8
    for card in hand:
        face, suit = card
        if suit in ['♦', '♥']:
            suit_color = Fore.RED
        else: 
            suit_color = Fore.BLACK
        
        if face == 10: # treat 10 differently because of spacing issues
            face_str = str(face)
            lines[0] += f' ____________ '
            lines[1] += f'|            |'
            lines[2] += f'|{suit_color} {face_str}         {Style.RESET_ALL}|' # adjusted spacing
            lines[3] += f'|            |'
            lines[4] += f'|{suit_color}     {suit}      {Style.RESET_ALL}|'
            lines[5] += f'|            |'
            lines[6] += f'|{suit_color}         {face} {Style.RESET_ALL}|' # adjusted spacing 
            lines[7] += f'|____________|'
        else:
            face_str = str(face)
            lines[0] += f' ____________ '
            lines[1] += f'|            |'
            lines[2] += f'|{suit_color} {face}          {Style.RESET_ALL}|'
            lines[3] += f'|            |'
            lines[4] += f'|{suit_color}     {suit}      {Style.RESET_ALL}|'
            lines[5] += f'|            |'
            lines[6] += f'|{suit_color}          {face} {Style.RESET_ALL}|'
            lines[7] += f'|____________|'
    for line in lines:
        print(line + Style.RESET_ALL)    

main_game()