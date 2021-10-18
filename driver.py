from blackjack.game import Game
from blackjack.player import Player

import os

from rich import print


def welcome():
    msg = """
    [green]Welcome to BlackJack!
    This will be a single player game against the computer (dealer).
    We'll be playing from a single 52-cards deck.
    To know the rules and regulations of Blackjack, see https://bicyclecards.com/how-to-play/blackjack/.
    You can exit anytime by pressing CTRL + C.[/green]
    """
    print(msg, end="\n\n\n")


def add_player():
    name = input("What should we call you? ")

    print(f"[green]Hi, {name}![/green]")

    correct = False

    while not correct:
        print("\n")

        try:
            bankroll = input("How much money will you be playing with? $")
            bankroll = float(bankroll)
        except Exception:
            msg = "[bold red]Oops! That's not a valid monetary value. Try again :smiley:[/bold red]"
            print(msg)
            continue

        correct = True

    return Player(name=name, bankroll=bankroll)


def main():
    try:
        welcome()

        player = add_player()

        input("Press ENTER to start playing.")
        os.system("cls||clear")

        game = Game(player)
        game.play()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()
