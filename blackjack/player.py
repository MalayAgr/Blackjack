from __future__ import annotations

from .console import console
from .deck import Card
from .hand import Hand


class _GenericPlayer:
    def __init__(self) -> None:
        self.hand = Hand()

    def player_count(self) -> int:
        return self.hand.count()

    def add_card_to_hand(self, card: Card) -> None:
        self.hand.add_card(card)

    def has_blackjack(self):
        return self.player_count() == 21

    def has_busted(self):
        return self.player_count() > 21

    def clear_hand(self) -> None:
        self.hand.clear()


class Player(_GenericPlayer):
    def __init__(self, name: str, bankroll: float) -> None:
        self.name = name
        self.bankroll = bankroll
        super().__init__()

    @classmethod
    def from_input(cls) -> Player:
        name = console.input("What should we call you? ")

        console.print(f"[green]Hi, {name}![/green]")

        while True:
            print("\n")

            try:
                bankroll = console.input("How much money will you be playing with? $")
                bankroll = float(bankroll)
            except Exception:
                msg = "[bold red]Oops! That's not a valid monetary value. Try again :smiley:[/bold red]"
                console.print(msg)
                continue

            break

        return cls(name=name, bankroll=bankroll)

    def pay(self, amount: float):
        self.bankroll += amount

    def bet(self, amount: float):
        self.bankroll -= amount


class Dealer(_GenericPlayer):
    def __init__(self) -> None:
        self._face_up = 0
        self._face_down = -1
        super().__init__()

    @property
    def face_up(self) -> Card:
        return self.hand[self._face_up]

    @property
    def face_down(self) -> Card:
        return self.hand[self._face_down]
