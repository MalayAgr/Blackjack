from __future__ import annotations

import random


class Card:
    face_cards = ("A", "K", "Q", "J")
    ten_cards = ("10", "K", "Q", "J")
    ace_values = (1, 11)

    def __init__(self, pip: int) -> None:
        self._pip = pip

    def __str__(self) -> str:
        return self.pip

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pip={self.pip})"

    @property
    def pip(self) -> str:
        if self._pip > 10:
            return self.face_cards[self._pip - 11]
        return str(self._pip)

    def value(self, current_count=None) -> int:
        pip = self.pip

        if pip == "A":
            if current_count is None:
                raise ValueError("The current count needs to be specified for an ace.")
            return self.ace_values[current_count + 11 < 21]

        return self._pip if pip not in self.face_cards else 10

    def is_ten_card(self) -> bool:
        return self.pip in self.ten_cards

    def is_ace(self) -> bool:
        return self.pip == "A"


class Deck:
    def __init__(self, multiplier=1) -> None:
        self._deck = [Card(card) for card in range(2, 15)] * (4 * multiplier)
        self._deck_state: list[Card] = []

    def __bool__(self) -> bool:
        return bool(self._deck_state)

    def shuffle(self):
        """Shuffle the deck."""
        self._deck_state = list(self._deck)
        random.shuffle(self._deck_state)

    def pick_card(self) -> Card:
        """Pick a card from the deck."""
        deck = self._deck_state or self._deck
        return deck.pop()

    def reset(self) -> None:
        self._deck_state.clear()
