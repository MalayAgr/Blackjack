from __future__ import annotations

import time
from enum import Enum
from typing import List, Tuple

from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt
from rich.table import Table

from .console import console
from .deck import Card, Deck
from .player import Dealer, Player


def _print_centered(msg):
    console.print(msg, justify="center")


class _StatePanel:
    _tf = "[green]{}\n[/green]"
    _df = "[red]{}[/red]"

    def __init__(self, player: Player, dealer: Dealer) -> None:
        self.player = player
        self.dealer = dealer

    def _row_data(self, title: str, data: str) -> str:
        return f"{self._tf.format(title)}{self._df.format(data)}"

    def _hand(self, player, title, hand: List[str] = None) -> str:
        if hand is None:
            hand = player.hand
        return self._row_data(title=title, data=", ".join(str(card) for card in hand))

    def _player_hand(self) -> str:
        return self._hand(self.player, "Your Hand")

    def _dealer_hand(self) -> str:
        hand = [self.dealer.face_up, "_"] if self.dealer.has_face_down else None
        return self._hand(self.dealer, title="Dealer's Hand", hand=hand)

    def _dealer_count(self) -> str:
        count = "N/A" if self.dealer.has_face_down else self.dealer.count()
        return self._row_data(title="Dealer's Count", data=count)

    def make_state_panel(self, bet) -> Panel:
        grid = Table.grid(expand=True)

        for _ in range(6):
            grid.add_column()

        grid.add_row(
            self._player_hand(),
            self._row_data(title="Count", data=self.player.count()),
            self._row_data(title="Bet", data=f"${bet}"),
            self._row_data(title="Bankroll", data=f"${self.player.bankroll}"),
            self._dealer_hand(),
            self._dealer_count(),
        )
        return Panel(grid)


class _Move(Enum):
    HIT = "Hit"
    STAND = "Stand"
    DOUBLE = "Double"

    @classmethod
    def make_prompt(
        cls, prompt: str = None, double: bool = False
    ) -> Tuple[str, List[str]]:
        moves = list(cls)
        moves = moves[:-1] if double is False else moves
        choices = [str(i) for i in range(1, len(moves) + 1)]

        moves = "\n".join(
            f"{idx}. {move.name}" for idx, move in enumerate(moves, start=1)
        )

        if prompt is None:
            prompt = "Enter your choice"

        return f"{moves}\n{prompt}", choices


class Game:
    def __init__(self, player: Player) -> None:
        self.deck = Deck()

        self.dealer = Dealer()

        self.player = player

        self.current_bet = 0

        self._panel = _StatePanel(player=player, dealer=self.dealer)

    def play(self) -> None:
        """Game loop."""
        playing = True
        n_round = 1

        while playing:
            console.rule(f"[bold blue]Round {n_round}[/bold blue]")

            self._ask_bet()

            if not self.deck:
                self.deck.reset()

            _print_centered("[red]Shuffling deck...[/red]")
            self.deck.shuffle()

            self._deal_initial_cards()

            self._show_state()

            natural = self._natural()

            if not natural:
                self._players_turn()

            self._dealers_turn(natural=natural)

            self._winner(natural=natural)

            next_round = Confirm.ask("Play another round?")
            if not next_round:
                playing = False
                continue

            self.deck.reset()
            self.player.clear_hand()
            self.dealer.clear_hand()
            self.current_bet = 0
            n_round += 1

            console.clear()

    ######################################
    ## UTILITY FUNCTIONS USED BY play() ##
    ######################################

    def _show_state(self):
        panel = self._panel.make_state_panel(bet=self.current_bet)
        console.print(panel)

    def _ask_bet(self) -> None:
        """Ask the bet amount for the current round."""

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
        for _ in range(2):
            card = self.deck.pick_card()
            self.player.add_card_to_hand(card)

            card = self.deck.pick_card()
            self.dealer.add_card_to_hand(card)

    def _natural(self) -> bool:
        if self.player.has_blackjack():
            _print_centered("[blink bold red]BLACKJACK![/blink bold red]")
            return True
        return False

    def _get_move(self, double=False) -> _Move:
        prompt, choices = _Move.make_prompt(double=double)
        choice = IntPrompt.ask(prompt, choices=choices)
        return list(_Move)[choice - 1]

    def _hit(self, player) -> Card:
        card = self.deck.pick_card()
        player.add_card_to_hand(card)
        return card

    def _double(self):
        self.player.bet(amount=self.current_bet)
        self.current_bet *= 2
        self._hit(self.player)

    def _players_turn(self) -> None:
        time.sleep(1)

        _print_centered(f"[red]It's your turn, {self.player.name}.[/red]")

        double = self.player.bankroll > self.current_bet
        move = self._get_move(double=double)

        if move is _Move.DOUBLE:
            self._double()
        else:
            while move is not _Move.STAND:
                time.sleep(1)
                card = self._hit(self.player)
                console.print(f"[red]You've been dealt a [bold]{card}[/bold].[/red]")

                if self.player.count() >= 21:
                    _print_centered("[red]Your count is [bold]>= 21[/bold].")
                    break

                self._show_state()

                move = self._get_move()

        self._show_state()

    def _dealers_turn(self, natural):
        time.sleep(1)

        _print_centered(f"[red]It's the dealer's turn.[/red]")

        time.sleep(1)

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

            _print_centered("[red]Dealer's count is [bold] >= 17[/bold][/red].")

    def _winner(self, natural: bool) -> None:
        _print_centered("[red]Determining winner....[/red]")

        time.sleep(1)

        p_count, d_count = self.player.count(), self.dealer.count()

        if p_count == d_count:
            _print_centered(
                "[red]"
                "This round ended in a push since your count and "
                f"the dealer's counts are the same: [bold]{p_count}[/bold]."
                "[/red]"
            )
            return

        winner = None

        if p_count <= 21 and (d_count < p_count or d_count > 21):
            winner = self.player

        if winner is self.player:
            won = 1.5 * self.current_bet if natural is True else self.current_bet

            _print_centered(
                "[bold green]"
                f"Congratulations! You're the winner, {self.player.name}.\n"
                f"You won [bold]${won}[/bold]. :smiley:"
                "[/bold green]"
            )
            self.player.pay(self.current_bet + won)
            return

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
