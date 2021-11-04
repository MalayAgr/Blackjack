from __future__ import annotations

import time
from enum import Enum
from typing import Dict, List, Optional, Tuple

from rich.panel import Panel
from rich.prompt import FloatPrompt, Prompt
from rich.table import Table

from .console import console
from .deck import Card, Deck
from .player import Dealer, Player, PlayerType


def _print_centered(msg: str) -> None:
    """Prints a message to the console with center justification.

    Arguments
    ----------
    msg: Message to be printed.
    """
    console.print(msg, justify="center")


class _StatePanel:
    """Class to represent the current state of the game.

    It uses rich.panel.Panel to create a pretty-looking state panel.
    See: https://rich.readthedocs.io/en/latest/panel.html.

    The Panel is made up of a table with 6 header-less columns.
    There is a single row, where the entries in each column are (in this order):
    - Player's hand
    - Player's count
    - Bet amount
    - Bankroll amount
    - Dealer's hand
    - Dealer's count

    Each row has a title part and a data part.
    See https://github.com/MalayAgr/Blackjack/blob/main/sample/sample_panel.gif.

    Attributes
    ---------
    player: Player instance
        Player of the game.

    dealer: Dealer instance
        Dealer of the game.

    tf: str
        Formatting string that should be used for the title part of the row.

    df: str
        Formatting string that should be used for the data part of the row.

    Methods
    ---------
    make_state_panel(bet: float) -> Panel:
        Creates and returns the Panel object representing the
        current state of the game.
    """

    tf = "[green]{}[/green]"
    df = "[red]{}[/red]"

    def __init__(self, player: Player, dealer: Dealer) -> None:
        """
        Arguments
        ----------
        player: Player playing the game.

        dealer: Dealer for the game.
        """
        self.player = player
        self.dealer = dealer

    def _row_data(self, title: str, data: str) -> str:
        """Method to format and obtain a row in the table.

        Arguments
        ---------
        title: Title for the row.

        data: Data for the row.

        Returns
        ----------
        str, the row data.
        """
        return f"{self.tf.format(title)}\n{self.df.format(data)}"

    def _hand(self, player: PlayerType, title: str, hand: List[str] = None) -> str:
        """Method to obtain the row entry for the current hand of a player.

        The title part for the hand is title and the data part
        is a comma-separated string of cards.

        Arguments
        ----------
        player: Player whose hand's row entry needs to be created.

        title: Title part for the entry.

        hand: Optional hand that should be used as the data part. Provide this when the
        current hand of the player needs to be overridden with some other value. When
        None, the hand attribute of player is used. Defaults to None.

        Returns
        ----------
        str, the hand rendered as a row.
        """
        if hand is None:
            hand = (str(card) for card in player.hand)
        return self._row_data(title=title, data=", ".join(hand))

    def make_state_panel(self, bet: float) -> Panel:
        """Method to create the Panel object.

        Arguments
        ----------
        bet: Data part of the bet amount entry.

        Returns
        ----------
        Panel, the created Panel object.
        """
        grid = Table.grid(expand=True)

        for _ in range(6):
            grid.add_column()

        dealer_hand = (
            [str(self.dealer.face_up), "_"] if self.dealer.has_face_down else None
        )
        dealer_count = "N/A" if self.dealer.has_face_down else self.dealer.count()

        grid.add_row(
            self._hand(player=self.player, title="Your Hand"),
            self._row_data(title="Count", data=self.player.count()),
            self._row_data(title="Bet", data=f"${bet}"),
            self._row_data(title="Bankroll", data=f"${self.player.bankroll}"),
            self._hand(player=self.dealer, title="Dealer's Hand", hand=dealer_hand),
            self._row_data(title="Dealer's Count", data=dealer_count),
        )
        return Panel(grid)


class _Move(Enum):
    """Enumeration to represent moves that a player can make.

    Members
    ----------
    - HIT
    - STAND
    - DOUBLE

    Methods
    --------
    make_prompt(prompt: str = None, double: bool = False) -> Tuple[str, Dict[str, _Move]]
        Returns a prompt that can be used to ask users to select a move
        and a mapping between the choice numbers and moves.
    """

    HIT = "Hit"
    STAND = "Stand"
    DOUBLE = "Double"

    @classmethod
    def make_prompt(
        cls, prompt: str = None, double: bool = False
    ) -> Tuple[str, Dict[str, _Move]]:
        """Method which creates a prompt that can be used to ask a user
        their move.

        Arguments
        ----------
        prompt: Line of text which should be printed after listing all choices.
        When None, it defaults to "Enter your choice". Defaults to None.

        double: Indicates whether the DOUBLE move should be included or not.
        Defaults to False.

        Returns
        ----------
        A two-tuple with:
        - str, the prompt.
        - dict, a mapping between choice numbers as strings and the moves.
        """
        moves = (move for move in cls if move is not cls.DOUBLE or double is True)
        choices = {str(idx): move for idx, move in enumerate(moves, start=1)}

        moves = "\n".join(f"{idx}. {move.name}" for idx, move in choices.items())

        if prompt is None:
            prompt = "Enter your choice"

        return f"{moves}\n{prompt}", choices


def _get_move(double: bool = False) -> _Move:
    """Function which asks the user to select a move.

    Arguments
    ----------
        double: Indicates whether the "Double" move should be included or not.
        Defaults to False.

    Returns
    ----------
    _Move, the selected move.
    """
    prompt, choices = _Move.make_prompt(double=double)
    choice = Prompt.ask(prompt, choices=choices.keys())
    return choices[choice]


class Game:
    """Class which represents a game of BlackJack, having all the
    capabilities to run one round of the game.

    Attributes
    ----------
    deck: Deck
        Deck used in the game.

    dealer: Dealer
        Dealer for the game.

    player: Player
        Player playing the game.

    current_bet: float
        Amount of money currently bet. Defaults to 0.

    Methods
    ----------
    play() -> None
        Runs one round of BlackJack.

    reset() -> None
        Resets the state of the game by clearing the player's
        and the dealer's hands and setting the bet back to 0.
    """

    def __init__(self, player: Player) -> None:
        self.deck = Deck()

        self.dealer = Dealer()

        self.player = player

        self.current_bet = 0.0

        self._panel = _StatePanel(player=player, dealer=self.dealer)

    def play(self) -> None:
        """Run one round of BlackJack."""
        self._ask_bet()

        if not self.deck:
            self.deck.reset()

        _print_centered("[red]Shuffling deck...[/red]")
        self.deck.shuffle()

        _print_centered("[red]Dealing initial cards...[/red]")
        self._deal_initial_cards()

        time.sleep(1)
        self._show_state()

        # Check if player has 21 on first two cards
        if (natural := self.player.has_blackjack()) is True:
            _print_centered("[blink bold red]BLACKJACK![/blink bold red]")
        else:
            time.sleep(1)
            _print_centered(f"[red]It's your turn, {self.player.name}.[/red]")

            self._players_turn()

        time.sleep(1)

        _print_centered("[red]It's the dealer's turn.[/red]")

        time.sleep(1)

        self._dealers_turn(natural=natural)

        time.sleep(1)

        _print_centered("[red]Determining winner....[/red]")

        time.sleep(1)

        self._winner(natural=natural)

    def reset(self) -> None:
        self.player.clear_hand()
        self.dealer.clear_hand()
        self.current_bet = 0

    ####################################
    ## UTILITY METHODS USED BY play() ##
    ####################################

    def _show_state(self) -> None:
        """Method which displays the current state of the game."""
        panel = self._panel.make_state_panel(bet=self.current_bet)
        console.print(panel)

    def _ask_bet(self) -> None:
        """Method which asks the bet amount for the current round."""
        while True:
            bet = FloatPrompt.ask(
                "How much money will you be betting for this round? ($)"
            )

            if bet > self.player.bankroll:
                msg = "[bold red]Oops! You're betting more money than you have. Try again :smiley:[/bold red]"
                console.print(msg, end="\n")
                continue

            self.player.bet(amount=bet)
            self.current_bet = bet
            break

    def _deal_initial_cards(self) -> None:
        """Method which deals the first two cards to the player and the dealer."""
        for _ in range(2):
            card = self.deck.pick_card()
            self.player.add_card_to_hand(card)

            card = self.deck.pick_card()
            self.dealer.add_card_to_hand(card)

    def _hit(self, player: PlayerType) -> Card:
        """Method which implements the Hit move.

        Hit is a move where the player draws a card from the deck.

        Arguments
        -----------
        player: Player who is making this move.

        Returns
        ----------
        Card, the card drawn from the deck.
        """
        card = self.deck.pick_card()
        player.add_card_to_hand(card)
        return card

    def _double(self) -> None:
        """Method which implements the Double move.

        Double is a move where the player doubles their bet and
        is dealt a single card from the deck.
        """
        self.player.bet(amount=self.current_bet)
        self.current_bet *= 2

        _print_centered(
            f"You've doubled the bet to [bold green]{self.current_bet}[/bold green].\n"
            "The dealer will deal a card to you..."
        )

        time.sleep(1)

        card = self._hit(self.player)

        console.print(f"[red]You've been dealt a [bold]{card}[/bold].[/red]")

        self._show_state()

    def _players_turn(self) -> None:
        """Method which implements the player's play.

        In any round, in the beginning, the player has at least two options:
        - Hit (take a card)
        - Stand (do nothing)

        A third move, Double, is available if their bankroll permits it.

        If the player chooses to double, they double their bet, take a
        card and their play ends.

        If the player chooses to hit, they can keep choosing to hit until they
        finally choose to stand or their count becomes >=21, whichever happens first.

        If the player stands, their play ends and no action needs to be taken.
        """
        double = self.player.bankroll > self.current_bet
        move = _get_move(double=double)

        if move is _Move.DOUBLE:
            self._double()
            return

        while move is not _Move.STAND:
            time.sleep(1)
            card = self._hit(self.player)
            console.print(f"[red]You've been dealt a [bold]{card}[/bold].[/red]")

            if self.player.count() >= 21:
                _print_centered("[red]Your count is [bold]>= 21[/bold].")
                break

            self._show_state()

            move = _get_move()

        self._show_state()

    def _dealers_turn(self, natural: bool) -> None:
        """Method which implements the dealer's play.

        All decisions for the dealer are predetermined.

        The dealer must keep hitting until their count is >= 17, except
        when there is a natural (player has 21 on first two cards).

        In case of a natural, the dealer just reveals their face-down card and
        their play ends.

        Arguments
        -----------
        natural: Indicates whether or not the player has a natural.
        """
        _print_centered("[red]Dealer is revealing their face-down card...[/red]")

        time.sleep(1)

        dealer = self.dealer

        face_down = self.dealer.face_down

        msg = f"[red]Dealer's face-down card is [bold]{face_down}[/bold].[/red]"
        console.print(msg)

        dealer.has_face_down = False
        self._show_state()

        if not natural:
            while dealer.count() < 17:
                time.sleep(1)
                card = self._hit(dealer)
                msg = f"[red]The dealer has been dealt a [bold]{card}[/bold].[/red]"
                console.print(msg)
                self._show_state()

            _print_centered("[red]Dealer's count is [bold]>= 17[/bold].[/red]")

    def _winner(self, natural: bool) -> Optional[Player]:
        """Method which determines the winner and handles the payout.

        If the player is the winner, they get to keep their bet and if:
        - There is a natural, the player is paid 1.5 times their bet amount.
        - There is no natural, the player is paid an amount equal to their bet amount.

        The player loses their bet amount if they cross 21 or the dealer wins.

        Arguments
        ----------
        natural: Indicates whether or not the player has a natural.

        Returns
        -----------
        Player, when the player is the winner. None otherwise.
        """
        p_count, d_count = self.player.count(), self.dealer.count()

        if p_count == d_count:
            _print_centered(
                "[red]"
                "This round ended in a push since your count and "
                f"the dealer's counts are the same: [bold]{p_count}[/bold]."
                "[/red]"
            )
            return

        if p_count <= 21 and (d_count < p_count or d_count > 21):
            won = 1.5 * self.current_bet if natural is True else self.current_bet

            _print_centered(
                "[bold green]"
                f"Congratulations! You're the winner, {self.player.name}.\n"
                f"You won [bold]${won}[/bold]. :smiley:"
                "[/bold green]"
            )
            # Refund the bet + pay the won amount
            self.player.pay(self.current_bet + won)
            return self.player

        if p_count > 21:
            _print_centered(
                "[bold red]"
                "D'oh! You have busted.\n"
                "You didn't win anything. :frowning:"
                "[/bold red]"
            )
            return

        _print_centered(
            "[red]"
            "The dealer won.\n"
            f"You lost [bold]${self.current_bet}[/bold]. :frowning:"
            "[red]"
        )
