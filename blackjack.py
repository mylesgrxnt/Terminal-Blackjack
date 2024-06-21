from random import choice
from time import sleep
from colorama import Fore, Back
import os

SLEEP_TIME = 1.0
card_count = 0

class Player():
    player_list = []

    def __init__(self, name, is_dealer=False, games_won=0, games_played=0, ace_checked=False):
        self.name = name
        self.hand = {} 
        self.hand_val = 0
        self.is_dealer = is_dealer
        self.busted = False
        self.games_won = games_won
        self.games_played = games_played
        self.ace_checked = ace_checked
        Player.player_list.append(self)

    def check_bust(self):
        has_ace = False
        for each in self.hand:
            if each[0:3] == "Ace":
                has_ace = True
        if self.hand_val > 21:
            if has_ace and not self.ace_checked:
                self.hand_val -= 10
                self.ace_checked = True
            else:
                self.busted = True
                clear()
                self.print_hand()
                print(f"{self.name} Busts!\n")
                sleep(SLEEP_TIME)
                if self.is_dealer:
                    clear()

    def add_card_to_hand(self, card_dict, discard):
        global card_count
        try:
            rand_card = choice(list(card_dict))
        except:
            card_dict = discard
            discard = {}
        rand_card = choice(list(card_dict))
        if int(card_dict[rand_card]) < 7:
            card_count += 1
        elif int(card_dict[rand_card]) > 9:
            card_count -= 1
        self.hand[rand_card] = card_dict[rand_card]
        card_dict.pop(rand_card, None)
        self.hand_val = sum(self.hand.values())
        if self.ace_checked:
            self.hand_val -= 10
        self.check_bust()
            
    def get_dealt(self, discard, card_dict):
        print(f"Dealing {self.name}")
        sleep(SLEEP_TIME)
        self.busted = False
        self.ace_checked = False
        for card in list(self.hand):
            discard[card] = self.hand[card]
            self.hand.pop(card, None)
        try:
            for _ in range(2):
                self.add_card_to_hand(card_dict, discard)
        except:
            if not card_dict:
                card_dict = discard
                discard = {}
                print("Shuffling ...")
            self.get_dealt(discard, card_dict)
        return discard, card_dict

    def hit(self, card_dict):
        self.add_card_to_hand(card_dict, discard)

    def print_hand(self, wait=True, dealer_show_cards=False):
        self.print_ascii_hand(dealer_show_cards, wait)
        if not self.is_dealer or dealer_show_cards:
            print(f"Hand Value is: {self.hand_val}")
            print()
            sleep(SLEEP_TIME)
        # else:
        #     print(f"Dealer Value Showing: {next(iter(dealer.hand.values()))} + ?")
        
    def card_print(self, result, card_list, rank, suit):
        HEARTS   = chr(9829) # Character 9829 is '♥'.
        DIAMONDS = chr(9830) # Character 9830 is '♦'.
        SPADES   = chr(9824) # Character 9824 is '♠'.
        CLUBS    = chr(9827) # Character 9827 is '♣'.

        suit_dict = {
            "Hearts": HEARTS,
            "Diamonds": DIAMONDS,
            "Spades": SPADES,
            "Clubs": CLUBS,
        }

        dealer_card = ['┌─────────┐', '│░░░░░░░░░│', '│░░░░░░░░░│', '│░░░░░░░░░│', '│░░░░░░░░░│', '│░░░░░░░░░│', '│░░░░░░░░░│', '│░░░░░░░░░│', '└─────────┘']

        space = ' '
        if rank == "10":
            space = ''

        fore_color = Fore.BLACK
        if suit == "Hearts" or suit == "Diamonds":
            fore_color = Fore.RED

        card_list[0].append('┌─────────┐')
        card_list[1].append('│{}{}{}       {}│'.format(Back.WHITE + fore_color, rank, space, Back.BLACK + Fore.WHITE))
        card_list[2].append(f'│{Back.WHITE + fore_color}         {Back.BLACK + Fore.WHITE}│')
        card_list[3].append(f'│{Back.WHITE + fore_color}         {Back.BLACK + Fore.WHITE}│')
        card_list[4].append('│{}    {}    {}│'.format(Back.WHITE + fore_color, suit_dict[suit], Back.BLACK + Fore.WHITE))
        card_list[5].append(f'│{Back.WHITE + fore_color}         {Back.BLACK + Fore.WHITE}│')
        card_list[6].append(f'│{Back.WHITE + fore_color}         {Back.BLACK + Fore.WHITE}│')
        card_list[7].append('│{}       {}{}{}│'.format(Back.WHITE + fore_color, space, rank, Back.BLACK + Fore.WHITE))
        card_list[8].append('└─────────┘')
            
        for index, line in enumerate(card_list):
            result.append(''.join(card_list[index]))

        
        # card_list[0] = ['┌─────────┐']
        # card_list[1] = ['│░░░░░░░░░│']
        # card_list[2] = ['│░░░░░░░░░│']
        # card_list[3] = ['│░░░░░░░░░│']
        # card_list[4] = ['│░░░░░░░░░│']
        # card_list[5] = ['│░░░░░░░░░│']
        # card_list[6] = ['│░░░░░░░░░│']
        # card_list[7] = ['│░░░░░░░░░│']
        # card_list[8] = ['└─────────┘']

        return result

    def print_ascii_hand(self, dealer_show_cards, wait):
        result = []
        card_list = [[],[],[],[],[],[],[],[],[]]
        for card in self.hand:
            if card.split(' ')[0][0] == "1":
                rank = card.split(' ')[0][0:2]
            else:
                rank = card.split(' ')[0][0]
            result = self.card_print(result,card_list,rank,card.split(' ')[2])

        if self.is_dealer and len(self.hand) == 2 and not dealer_show_cards:
            dealer_card = []
            dealer_card.append('┌─────────┐')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append(f'│{Back.WHITE + Fore.BLACK}░░░░░░░░░{Back.BLACK + Fore.WHITE}│')
            dealer_card.append('└─────────┘')
            count = 0
            for each in result:
                if not (result.index(each) > len(result) - 10):
                    print(each + dealer_card[count])
                    count += 1
            print()
            if wait:
                sleep(SLEEP_TIME)
        else:
            for each in result:
                if result.index(each) > len(result) - 10:
                    print(each)

if __name__ == "__main__":
    p1 = Player(Fore.CYAN + "Player 1" + Fore.WHITE)
    p2 = Player(Fore.YELLOW + "Player 2" + Fore.WHITE)

    dealer = Player(Fore.RED + "Dealer" + Fore.WHITE, is_dealer=True)

    def clear():
        os.system("cls")

    def print_dealer_hand_during_play():
        print("Dealer Hand:")
        dealer.print_hand(wait=False)

    discard = {}
    card_dict = {
        "Ace of Hearts":11,
        "King of Hearts":10,
        "Queen of Hearts":10,
        "Jack of Hearts":10,
        "10 of Hearts":10,
        "9 of Hearts":9,
        "8 of Hearts":8,
        "7 of Hearts":7,
        "6 of Hearts":6,
        "5 of Hearts":5,
        "4 of Hearts":4,
        "3 of Hearts":3,
        "2 of Hearts":2,
        "Ace of Diamonds":11,
        "King of Diamonds":10,
        "Queen of Diamonds":10,
        "Jack of Diamonds":10,
        "10 of Diamonds":10,
        "9 of Diamonds":9,
        "8 of Diamonds":8,
        "7 of Diamonds":7,
        "6 of Diamonds":6,
        "5 of Diamonds":5,
        "4 of Diamonds":4,
        "3 of Diamonds":3,
        "2 of Diamonds":2,
        "Ace of Clubs":11,
        "King of Clubs":10,
        "Queen of Clubs":10,
        "Jack of Clubs":10,
        "10 of Clubs":10,
        "9 of Clubs":9,
        "8 of Clubs":8,
        "7 of Clubs":7,
        "6 of Clubs":6,
        "5 of Clubs":5,
        "4 of Clubs":4,
        "3 of Clubs":3,
        "2 of Clubs":2,
        "Ace of Spades":11,
        "King of Spades":10,
        "Queen of Spades":10,
        "Jack of Spades":10,
        "10 of Spades":10,
        "9 of Spades":9,
        "8 of Spades":8,
        "7 of Spades":7,
        "6 of Spades":6,
        "5 of Spades":5,
        "4 of Spades":4,
        "3 of Spades":3,
        "2 of Spades":2,
    }

    clear()
    show_card_count = input("Show Card Count?\nYes(1) or No(2): ")

    while True:
        clear()
        dealer_play = False
        dealer_won = True
        victorious_list = []
        # max_player_score = 0

        for player in Player.player_list:
            discard, card_dict = player.get_dealt(discard, card_dict)
            player.print_hand()
            clear()
        
        if dealer.hand_val == 21:
            print("Blackjack!")

        else:
            for player in Player.player_list:
                if player.is_dealer:
                    print("Dealer Hand:")
                    player.print_hand(dealer_show_cards = True)
                    for non_dealer in Player.player_list[:-1]:
                        if not non_dealer.busted:
                            dealer_play = True
                            # if non_dealer.hand_val > max_player_score:
                            #     max_player_score = non_dealer.hand_val
                    if dealer_play:
                        while player.hand_val < 17: # or (player.hand_val < 21 and player.hand_val < max_player_score)
                            clear()
                            print("Dealer Hit")
                            player.hit(card_dict)
                            player.print_hand()
                            print(f"Dealer Hand Value is: {player.hand_val}\n")
                            sleep(SLEEP_TIME)

                else:
                    decision = "1"
                    while decision == "1" and not player.busted:
                        print_dealer_hand_during_play()
                        print("Current Player Hand:")
                        player.print_hand()
                        if show_card_count == "1":
                            print(f"Card Count is {'+' if card_count>0 else ''}{card_count}")
                        decision = input(f"{player.name} Hit(1) or Stand(2): ")
                        print()
                        if decision == "1":
                            clear()
                            player.hit(card_dict)
                    clear()
        
        for player in Player.player_list:
            player.games_played += 1
            if not player.is_dealer:
                if (player.hand_val > dealer.hand_val or dealer.busted) and not player.busted:
                    victorious_list.append(player.name)
                    player.games_won += 1
                    dealer_won = False
        
        if dealer_won:
            dealer.games_won += 1
            print(f"Dealer Won!")
        else:
            print(", ".join(victorious_list) + " Won!")

        for player in Player.player_list:
            back_color = Back.RED
            win_percent = round(100*player.games_won/player.games_played, 1)
            if win_percent >= 50.0:
                back_color = Back.GREEN
            print(f"{player.name}'s Hand Value: {player.hand_val}. \t Win Percentage: {Fore.WHITE + back_color + (7-len(str(win_percent)))*" " + str(win_percent) + " " + Fore.WHITE + Back.BLACK}")

        play_again = input("\n'Q' to quit, any other key to continue: ")
        print()
        if play_again == "Q":
            break