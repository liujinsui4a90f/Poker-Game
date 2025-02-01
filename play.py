import random
from queue import Queue
import itertools

class Player:
    def __init__(self):
        self.cards = Queue()  # Initialize the player's card queue

    def getCards(self, c):
        for card in c:
            self.cards.put(card)  # Add cards to the player's queue

    def getCard(self, c):
        self.cards.put(c)  # Add a single card to the player's queue
    
    def dropCard(self):
        return self.cards.get()  # Remove a card from the player's queue

class Game:
    def __init__(self):
        self.playerNum = 4  # Set the number of players to 4
        self.players = [Player() for i in range(self.playerNum)]  # Create the specified number of player objects
        self.currentPlayer = 0  # Initialize the current player to player 0
        self.pile = []  # Initialize the pile as an empty list
        self.step = 1  # Initialize the step count to 1

        cards = [i % 13 + 1 for i in range(52)]  # Create a deck of 52 cards with values ranging from 1 to 13
        random.shuffle(cards)  # Shuffle the deck
        for i, player in enumerate(itertools.cycle(self.players)):  # Cycle through the player objects and loop them to the end of the list
            player.getCard(cards[i])  # Add a card to each player's queue
            if i == 51:  # If all 52 cards have been added to the players' queues
                break  # Exit the loop

    def notFinished(self) -> bool:
        counter = 0  # Initialize a temporary variable to 0
        for p in self.players:
            if p.cards.qsize() == 0:  # If a player has 0 cards
                counter += 1  # Increment the temporary variable
        if counter < self.playerNum - 1:  # If not all players have 0 cards
            return True  # The game continues
        return False  # The game ends

    def TakeCardPos(self):
        currentCard = self.pile[-1]  # Get the top card of the pile
        for i, c in enumerate(self.pile[:-1]):
            if c % 13 == currentCard % 13:  # Check if there is a card in the pile with the same value as the top card (considering the cycle of 13 cards)
                return i  # Return the position of the card with the same value
        return -1  # If no card with the same value is found, return -1

    def run(self):
        while self.notFinished():  # While the game is not finished
            if self.players[self.currentPlayer].cards.qsize() == 0:  # If the current player has 0 cards
                self.currentPlayer += 1  # Switch to the next player
                self.currentPlayer %= self.playerNum  # Ensure the current player is within the range of 0 to playerNum-1
                continue  # Skip the current player and switch to the next player

            self.pile.append(self.players[self.currentPlayer].dropCard())  # The current player drops a card into the pile
            print(self.pile)  # Print the current state of the pile
            pos = self.TakeCardPos()  # Find the position of the card that can be taken

            print(f"In step {self.step}")
            for i in self.players:
                print(f"Player {self.players.index(i)} has {i.cards.qsize()} cards")  # Print the number of cards each player has

            if pos != -1:
                for i in range(pos, len(self.pile)):
                    temp = self.pile.pop()  # Remove a card from the pile
                    self.players[self.currentPlayer].getCard(temp)  # Add the removed card to the current player's queue
            else:
                self.currentPlayer += 1  # If no card can be taken, switch to the next player

            self.step += 1  # Increment the step count
            self.currentPlayer %= self.playerNum  # Ensure the current player is within the range of 0 to playerNum-1
        for p in self.players:
            if p.cards.qsize() != 0:  # If a player has cards left
                print(f"Player {self.players.index(p)} wins!")  # Print the winner



if __name__ == "__main__":
    g = Game()  # Create a game object
    g.run()  # Run the game
