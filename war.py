import random
import time

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.rank = self.get_rank()

    def get_rank(self):
        # Ranking cards: 2 is lowest, Ace is highest
        rank_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
            '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14
        }
        return rank_values[self.value]

    def __str__(self):
        return f"{self.value} of {self.suit}"

    def __repr__(self):
        return self.__str__()

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 
                  'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        # Distribute cards evenly among players
        player_hands = [[] for _ in range(players)]
        for i, card in enumerate(self.cards):
            player_hands[i % players].append(card)
        return player_hands

class WarGame:
    def __init__(self, num_players=2):
        self.num_players = num_players
        self.deck = Deck()
        self.players = self.deck.deal(num_players)
        self.player_names = [f"Player {i+1}" for i in range(num_players)]

    def play_round(self):
        # Collect cards played in this round
        round_cards = []
        round_winners = []

        # Each player plays a card
        for i in range(self.num_players):
            if not self.players[i]:  # Skip if player is out
                continue
            round_cards.append(self.players[i].pop(0))
            round_winners.append(i)

        # If not enough players with cards, end round
        if len(round_winners) < 2:
            return round_winners[0] if round_winners else None

        # Find the highest card
        max_card = max(round_cards, key=lambda x: x.rank)
        winning_indices = [i for i, card in enumerate(round_cards) if card.rank == max_card.rank]

        # Handle war scenario
        if len(winning_indices) > 1:
            print("WAR! Multiple players have the same highest card!")
            return self.handle_war(round_cards, round_winners)

        # Single winner of the round
        winner_index = round_winners[round_cards.index(max_card)]
        
        # Award cards to the winner
        self.players[winner_index].extend(round_cards)
        print(f"{self.player_names[winner_index]} wins the round!")
        
        return winner_index

    def handle_war(self, initial_cards, initial_winners):
        # War mechanic: each player plays 3 face-down cards and one face-up card
        war_participants = initial_winners.copy()
        war_cards = initial_cards.copy()

        # Filter out players with insufficient cards
        war_participants = [
            p for p in war_participants 
            if len(self.players[p]) >= 4
        ]

        # If not enough players for war, distribute cards to original winner
        if len(war_participants) < 2:
            winner_index = initial_winners[0]
            self.players[winner_index].extend(war_cards)
            print(f"{self.player_names[winner_index]} wins by default!")
            return winner_index

        # Conduct war for remaining participants
        for participant in war_participants:
            # Play 3 face-down cards
            for _ in range(3):
                if self.players[participant]:
                    war_cards.append(self.players[participant].pop(0))
                else:
                    break
            
            # Play one face-up card
            if self.players[participant]:
                war_card = self.players[participant].pop(0)
                war_cards.append(war_card)

        # Remove empty lists of war participants
        war_participants = [
            p for p in war_participants 
            if self.players[p]
        ]

        # If no participants left, redistribute to original winner
        if not war_participants:
            winner_index = initial_winners[0]
            self.players[winner_index].extend(war_cards)
            print(f"{self.player_names[winner_index]} wins by default!")
            return winner_index

        # Find the highest card among war cards
        max_war_card = max([card for card in war_cards[-len(war_participants):]], key=lambda x: x.rank)
        
        # Find the winner of the war
        war_winner_index = war_participants[
            [card for card in war_cards[-len(war_participants):]].index(max_war_card)
        ]

        # Award all war cards to the winner
        self.players[war_winner_index].extend(war_cards)
        print(f"{self.player_names[war_winner_index]} wins the WAR!")
        
        return war_winner_index

    def check_game_over(self):
        # Count players with cards
        active_players = [i for i, hand in enumerate(self.players) if hand]
        return len(active_players) == 1

    def get_winner(self):
        active_players = [i for i, hand in enumerate(self.players) if hand]
        return self.player_names[active_players[0]] if active_players else "No winner"

    def play_game(self):
        round_count = 0
        max_rounds = 1000  # Prevent infinite game

        while not self.check_game_over() and round_count < max_rounds:
            print(f"\n--- Round {round_count + 1} ---")
            
            # Print current card counts
            for i, hand in enumerate(self.players):
                print(f"{self.player_names[i]} has {len(hand)} cards")
            
            self.play_round()
            round_count += 1
            time.sleep(0.5)  # Slow down the game for readability

        if round_count >= max_rounds:
            print("Game ended in a draw after 1000 rounds.")
        else:
            print(f"\n{self.get_winner()} wins the game!")

def main():
    print("Welcome to the War Card Game!")
    
    while True:
        try:
            num_players = int(input("How many players? (2-4): "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Please enter a number between 2 and 4.")
        except ValueError:
            print("Please enter a valid number.")

    game = WarGame(num_players)
    game.play_game()

if __name__ == "__main__":
    main()
