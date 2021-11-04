from __future__ import annotations

from blackjack.console import console
from blackjack import Game
from blackjack.player import Player


def welcome() -> str:
    """Function which returns the welcome message."""
    return """
    [green]Welcome to BlackJack!
    This will be a single player game against the computer (dealer).
    We'll be playing from a single 52-cards deck.
    To know the rules and regulations of Blackjack, see https://bicyclecards.com/how-to-play/blackjack/.
    You can exit anytime by pressing CTRL + C.[/green]
    \n\n
    """


def main() -> None:
    console.rule("[bold red]Blackjack by Malay Agarwal[/bold red]")
    try:
        console.print(welcome())

        player = Player.from_input()

        input("Press ENTER to start playing.")
        console.clear()

        console.rule("[bold red]Blackjack by Malay Agarwal[/bold red]")

        game = Game(player)
        game.play()
    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()
