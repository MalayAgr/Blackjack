from __future__ import annotations

import functools
from collections import UserList
from typing import List

from .deck import Card


class Hand:
    def __init__(self) -> None:
        self.cards: List[Card] = []

    def __getitem__(self, key: int) -> Card:
        return self.cards[key]

    def __contains__(self, item: Card) -> bool:
        return item in self.cards

    def count(self) -> int:
        if not self.cards:
            return 0

        count = 0

        for card in self.cards:
            count += card.value(current_count=count)

    def add_card(self, card: str) -> None:
        self.cards.append(card)

    def clear(self) -> None:
        self.cards.clear()
