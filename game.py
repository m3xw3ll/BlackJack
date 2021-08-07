import random
import os
import sys
import time

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


class Deck:
    def __init__(self):
        self.cards = [Card(v,s) for v in ['2', '3', '4', '5', '6', '7', '8', '9', '10',
                                         'J', 'Q', 'K', 'A']
                     for s in ['♠', '♥', '♦', '♣']]

    def shuffle(self):
        '''
        Shuffle deck after init
        :return: None
        '''
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self):
        '''
        deal a card
        :return: None
        '''
        if len(self.cards) > 1:
            return self.cards.pop(0)

class Hand():
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        '''
        Add a card to the hand
        :param card: A card
        :return: None
        '''
        self.cards.append(card)

    def get_score(self):
        '''
        Calculate score
        :return: The current score
        '''
        score = 0
        has_ace = False
        for v in self.cards:
            if v.value in ['J', 'Q', 'K']:
                score += 10
            elif v.value == 'A':
                has_ace = True
                score += 11
            else:
                score += int(v.value)

        if has_ace and score > 21:
            score -= 10

        return score





class Game:
    def __init__(self):
        self.hidden = False
        pass

    # Function to print the cards
    def print_cards(self, person, hidden):
        '''
        Pretty print the hand
        :param person: Dealer or player
        :param hidden: If the card is hidden or not
        :return: None
        '''
        s = ""
        for card in person.cards:
            s = s + "┌---------┐\t"

        print(s)

        s = ""
        for card in person.cards:
            if self.hidden:
                s += "|░░░░░░░░░|\t"
            else:
                if card.value == '10':
                    s = s + "| {}      |\t".format(card.value)
                else:
                    s = s + "| {}       |\t".format(card.value)

        print(s)

        s = ""
        for card in person.cards:
            if self.hidden:
                s += "|░░░░░░░░░|\t"
            else:
                s = s + "|         |\t"

        print(s)

        s = ""
        for card in person.cards:
            if self.hidden:
                s += "|░░░░░░░░░|\t"
            else:
                s = s + "|    {}    |\t".format(card.suit)

        print(s)

        s = ""
        for card in person.cards:
            if self.hidden:
                s += "|░░░░░░░░░|\t"
            else:
                s = s + "|         |\t"

        print(s)

        s = ""
        for card in person.cards:
            if self.hidden:
                s += "|░░░░░░░░░|\t"
            else:
                if card.value == '10':
                    s = s + "|      {} |\t".format(card.value)
                else:
                    s = s + "|       {} |\t".format(card.value)

        print(s)

        s = ""
        for card in person.cards:
            s = s + "└---------┘\t"

        print(s)

    def make_board(self):
        '''
        Print the board
        :return: None
        '''
        print("Dealer score: {}".format(self.dealer_hand.get_score()))
        self.print_cards(self.dealer_hand, True)
        "\n"
        "\n"
        self.print_cards(self.player_hand, False)
        print("Player score: {}".format(self.player_hand.get_score()))

    def welcome_screen(self):
        '''
        Print the welcome screen and ask user what he wants to do
        :return: None
        '''
        self.clear()
        print("""
         _     _            _    _            _    
        | |   | |          | |  (_)          | |   
        | |__ | | __ _  ___| | ___  __ _  ___| | __
        | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
        | |_) | | (_| | (__|   <| | (_| | (__|   < 
        |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\ 
                               _/ |                
                              |__/  
        \n
        Welcome to BlackJack!
        What do you want to do?
        [P]LAY
        [R]ULES
        [Q]UIT
        """
        )
        choice = str(input("Choice: \t"))
        while choice.lower() not in ['p', 'play', 'r', 'rules', 'q', 'quit']:
            choice = str(input("What do you want to do?\n"
                               "[P]LAY\n"
                               "[R]ULES\n"
                               "[Q]UIT\n"
                               "Choice: \t"))
        if choice.lower() in ['p', 'play']:
            self.play()
        elif choice.lower() in ['r', 'rules']:
            self.clear()
            self.show_rules()
            choice = str(input("Do you want to [P]LAY or [Q]UIT?\t"))
            while choice.lower() not in ['p', 'play', 'q', 'quit']:
                choice = str(input("Do you want to [P]LAY or [Q]UIT?\t"))
            if choice.lower() in ['p', 'play']:
                self.welcome_screen()
            else:
                print("See you next time")
                sys.exit()
        else:
            print("Okay, maybe next time")
            sys.exit()

    def clear(self):
        '''
        Clear the screen for better readability
        :return: None
        '''
        os.system('cls' if os.name == 'nt' else 'clear')

    def play(self):
        '''
        Play the game
        :return: None
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        playing = True

        while playing:
            self.deck = Deck()
            self.deck.shuffle()

            self.player_hand = Hand()
            self.dealer_hand = Hand()

            self.dealer_hand.hidden = True

            self.dealer_hand.add_card(self.deck.deal())
            for i in range(2):
                self.player_hand.add_card(self.deck.deal())

            game_over = False

            while not game_over:
                self.make_board()
                choice = str(input("Do you want to [H]it or [S]tand?\t"))
                while choice.lower() not in ['h', 's']:
                    choice = str(input("Do you want to [H]it or [S]tand?\t"))

                if choice == 'h':
                    self.clear()
                    self.player_hand.add_card(self.deck.deal())
                    if self.player_busted():
                        self.make_board()
                        print("YOU LOST")
                        game_over = True

                else:
                    while self.dealer_hand.get_score() <= 16:
                        self.clear()
                        self.dealer_hand.add_card(self.deck.deal())
                        self.make_board()
                        time.sleep(1)


                    player_has_blackjack, dealer_has_blackjack = self.check_for_blackjack()
                    if player_has_blackjack or dealer_has_blackjack:
                        game_over = True
                        self.show_blackjack_result(player_has_blackjack, dealer_has_blackjack)
                        continue

                    if self.dealer_busted():
                        print("YOU WIN - Dealer has over 21")
                        game_over = True
                        continue


                    self.get_winner(self.player_hand.get_score(), self.dealer_hand.get_score())
                    game_over = True



            again = str(input("Do you want to play again? [Y/N]\t"))
            while again.lower() not in ['yes', 'y', 'no', 'n']:
                again = str(input("Please enter Y or N\t"))
            if again.lower() == 'n':
                print("Thanks for playing")
                playing = False
            else:
                self.clear()
                game_over = False


    def player_busted(self):
        '''
        Check if player busted
        :return: Boolean value if busted or not
        '''
        return self.player_hand.get_score() > 21

    def dealer_busted(self):
        '''
        Check if dealer busted
        :return: Boolean value if busted or not
        '''
        return self.dealer_hand.get_score() > 21

    def check_for_blackjack(self):
        '''
        Check for blackjack
        :return: Boolean value if blackjack or not
        '''
        player_black_jack = False
        dealer_black_jack = False
        if self.player_hand.get_score() == 21 and len(self.player_hand.cards) == 2:
            player_black_jack = True
        if self.dealer_hand.get_score() == 21 and len(self.dealer_hand.cards) == 2:
            dealer_black_jack = True

        return player_black_jack, dealer_black_jack


    def show_blackjack_result(self, player_has_blackjack, dealer_has_blackjack):
        '''
        Print the blackjack results
        :param player_has_blackjack: Player has blackjack or not
        :param dealer_has_blackjack: Dealer has blackjack or not
        :return:
        '''
        if player_has_blackjack and dealer_has_blackjack:
            print("TIE - Both players have blackjack!")
        elif player_has_blackjack:
            print("YOU WIN - You have Blackjack")
        elif dealer_has_blackjack:
            print("YOU LOOSE - Dealer has Blackjack")


    def get_winner(self, player_score, dealer_score):
        '''
        Compare the scores and get the winner
        :param player_score: The player score
        :param dealer_score: The dealer score
        :return:
        '''
        if player_score == dealer_score:
            print("TIE - Both players have {}".format(player_score))
        elif player_score > dealer_score:
            print("YOU WIN")
        else:
            print("YOU LOSE")

    def show_rules(self):
        '''
        Print rules
        :return: None
        '''
        print("""
        The object of the game is to create card totals higher than those of the dealer's hand 
        but not exceeding 21, or by stopping at a total in the hope that dealer will bust.
        
        Number cards count as their numbers.
        Jack, Queen and King count as 10.
        Aces count as 1 or 11, acording to the players choice.
        
        After the player hits STAND the dealer's hand is resolved by 
        drawing cards until the hand achieves a total of 17 or higher.
        
        A player total of 21 on the first two cards is called Blackjack and the players wins
        immediatelly unless dealer has also one.
        """)


if __name__ == '__main__':
    g = Game()
    g.welcome_screen()





