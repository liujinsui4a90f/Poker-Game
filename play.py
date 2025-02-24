import random
from queue import Queue
from matplotlib import pyplot as plt
import itertools
import logging

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

class Record:
    def __init__(self, playerNum):
        self.pNum = playerNum  # Set the number of players
        self.records = [[] for i in range(self.pNum)]  # Initialize the records list with empty lists for each player
    
    def addRecord(self, players : list):
        for i, p in enumerate(players):
            self.records[i].append(p.cards.qsize())  # Add the number of cards each player has to the corresponding record list

    def draw(self):
        plt.figure(figsize=(10, 6))  # Set the size of the graph
        for i in range(self.pNum):
            plt.plot(self.records[i], label=f"Player {i}")
        plt.xlabel("Step")
        plt.legend()
        plt.show()  # Draw the graph
        plt.savefig("records.png")  # Save the graph as a PNG file
        
class Game:
    def __init__(self, num=4):
        self.playerNum = num  # Set the number of players to 4
        self.players = [Player() for i in range(self.playerNum)]  # Create the specified number of player objects
        self.recorder = Record(self.playerNum)  # Create a record object for the game
        self.currentPlayer = 0  # Initialize the current player to player 0
        self.pile = []  # Initialize the pile as an empty list
        self.step = 1  # Initialize the step count to 1

        logging.basicConfig(filename='game.log', level=logging.INFO, format='%(asctime)s %(message)s')  # Set up logging

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
            #print(self.pile)  # Print the current state of the pile
            pos = self.TakeCardPos()  # Find the position of the card that can be taken
            tmpNum = len(self.pile)

            logging.info(f"In step {self.step}")
            for i in self.players:
                logging.info(f"Player {self.players.index(i)} has {i.cards.qsize()} cards")  # Print the number of cards each player has

            if pos != -1:
                print(f"In step {self.step}, player {self.currentPlayer} takes {tmpNum-pos} cards")
            else:
                print(f"In step {self.step}, no player takes any cards")

            
            if pos != -1:
                for i in range(pos, len(self.pile)):
                    temp = self.pile.pop()  # Remove a card from the pile
                    self.players[self.currentPlayer].getCard(temp)  # Add the removed card to the current player's queue
            else:
                self.currentPlayer += 1  # If no card can be taken, switch to the next player

            self.recorder.addRecord(self.players)  # Add the current state of the game to the record object
            self.step += 1  # Increment the step count
            self.currentPlayer %= self.playerNum  # Ensure the current player is within the range of 0 to playerNum-1
        for p in self.players:
            if p.cards.qsize() != 0:  # If a player has cards left
                logging.info(f"Player {self.players.index(p)} wins!")  # Print the winner
                print(f"Player {self.players.index(p)} wins!")  # Print the winner
        self.recorder.draw()  # Draw the graph of the game



if __name__ == "__main__":
    while True:
        g = Game(6)  # Create a game object
        g.run()  # Run the game
        ans = input("Do you want to play again? (y/n): ")  # Ask the user if they want to play again
        if ans.lower() != "y":  # If the user does not want to play again
            break  # Exit the loop
