from __future__ import annotations

from typing import Optional

from rich.prompt import FloatPrompt

from .console import console
from .deck import Card, Hand


class _GenericPlayer:
    def __init__(self) -> None:
        self.hand = Hand()

    def count(self) -> int:
        return self.hand.get_count()

    def add_card_to_hand(self, card: Card) -> None:
        self.hand.append(card)

    def has_blackjack(self) -> bool:
        return self.count() == 21

    def has_busted(self) -> bool:
        return self.count() > 21

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

        bankroll = FloatPrompt.ask("How much money will you be playing with? ($)")

        return cls(name=name, bankroll=bankroll)

    def pay(self, amount: float) -> None:
        self.bankroll += amount

    def bet(self, amount: float) -> None:
        self.bankroll -= amount


class Dealer(_GenericPlayer):
    def __init__(self) -> None:
        self._face_up = 0
        self.has_face_down = True
        self._face_down = -1
        super().__init__()

    @property
    def face_up(self) -> Card:
        return self.hand[self._face_up]

    @property
    def face_down(self) -> Optional[Card]:
        if self.has_face_down:
            return self.hand[self._face_down]

    def clear_hand(self) -> None:
        self.has_face_down = True
        return super().clear_hand()
