from __future__ import annotations

from rich import print

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


class Player(_GenericPlayer):
    def __init__(self, name: str, bankroll: float) -> None:
        self.name = name
        self.bankroll = bankroll
        super().__init__()

    @classmethod
    def from_input(cls) -> Player:
        name = input("What should we call you? ")

        print(f"[green]Hi, {name}![/green]")

        while True:
            print("\n")

            try:
                bankroll = input("How much money will you be playing with? $")
                bankroll = float(bankroll)
            except Exception:
                msg = "[bold red]Oops! That's not a valid monetary value. Try again :smiley:[/bold red]"
                print(msg)
                continue

            break

        return cls(name=name, bankroll=bankroll)

    def pay(self, amount: float, multiplier=1):
        self.bankroll += amount * multiplier

    def bet(self, amount: float):
        self.bankroll -= amount


class Dealer(_GenericPlayer):
    def __init__(self) -> None:
        self.face_up = 0
        self.face_down = -1
        super().__init__()

    def face_up_card(self) -> str:
        return self.hand[self.face_up]

    def face_down_card(self) -> str:
        return self.hand[self.face_down]
