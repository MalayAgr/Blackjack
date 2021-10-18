from __future__ import annotations


from .deck import Deck
from .hand import Hand


class _GenericPlayer:
    def __init__(self) -> None:
        self.hand = Hand()

    def player_count(self, aces=None) -> int:
        return self.hand.count(aces=aces)

    def draw_card(self, deck: Deck):
        card = deck.pick_card()
        self.hand.add_card(card)

    def has_blackjack(self, aces=None):
        return self.player_count(aces=aces) == 21

    def has_busted(self, aces=None):
        return self.player_count(aces=aces) > 21


class Player(_GenericPlayer):
    def __init__(self, name: str, bankroll: float) -> None:
        self.name = name
        self.bankroll = bankroll
        super().__init__()

    def pay(self, amount: float, multiplier=1):
        self.bankroll += amount * multiplier

    def bet(self, amount: float):
        self.bankroll -= amount


class Dealer(_GenericPlayer):
    def __init__(self) -> None:
        self.face_up = ""
        self.face_down = ""
        super().__init__()
