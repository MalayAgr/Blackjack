from __future__ import annotations

from rich.prompt import Confirm

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

        game = Game(player)

        n_round = 1

        while True:
            console.rule("[bold red]Blackjack by Malay Agarwal[/bold red]")
            console.rule(f"[bold blue]Round {n_round}[/bold blue]")
            game.play()

            next_round = Confirm.ask("Play another round?")
            if not next_round:
                break

            game.reset()
            console.clear()
            n_round += 1

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()


if __name__ == "__main__":
    main()
