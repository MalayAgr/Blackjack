from __future__ import annotations

import random

FACE_CARDS = ("A", "K", "Q", "J")


class Deck:
    def __init__(self) -> None:
        self._deck = list(range(2, 15)) * 4
        self._deck_state: list[int] = []

    def shuffle(self):
        """Shuffle the deck."""
        self._deck_state = list(self._deck)
        random.shuffle(self._deck_state)

    def _resolve_card(self, card: int) -> str:
        """Take an int card value and return its actual value."""
        if card > 10:
            return FACE_CARDS[card - 11]
        return str(card)

    def pick_card(self) -> str:
        """Pick a card from the deck."""
        deck = self._deck_state or self._deck
        card = deck.pop()
        return self._resolve_card(card)
