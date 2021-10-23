import os

from blackjack.console import console
from blackjack.game import Game
from blackjack.player import Player


def welcome():
    msg = """
    [green]Welcome to BlackJack!
    This will be a single player game against the computer (dealer).
    We'll be playing from a single 52-cards deck.
    To know the rules and regulations of Blackjack, see https://bicyclecards.com/how-to-play/blackjack/.
    You can exit anytime by pressing CTRL + C.[/green]
    """
    console.print(msg, end="\n\n\n")


def main():
    try:
        welcome()

        player = Player.from_input()

        input("Press ENTER to start playing.")
        os.system("cls||clear")

        game = Game(player)
        game.play()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()
