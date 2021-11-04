from __future__ import annotations

import random
from typing import List


class Card:
    """Class to represent a single card.

    Attributes
    ----------
    pip: str
        String pip of the card like '2' and 'A'.

    Methods
    ----------
    value(current_count: int = None) -> int:
        Returns the value of the card for counting.

    is_ace() -> bool:
        Returns True if the card has a pip of A.
    """

    _face_cards = ("A", "K", "Q", "J")

    def __init__(self, pip: int) -> None:
        """
        Arguments
        ---------
        pip: Integer position of the card.
        Cards 2 through 10 are at the same position as their pip.
        Cards A, K, Q and J have positions 11, 12, 13 and 14 respectively.
        Using this allows for easier generation of cards since users
        do not have handle A, K, Q and J separately.

        Raises
        ----------
        ValueError, when pip is less than 2 or greater than 14.
        """
        if not 2 <= pip <= 14:
            raise ValueError("pip can only be between 2 and 14.")
        self._pip = pip

    def __str__(self) -> str:
        return self.pip

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(pip={self.pip})"

    @property
    def pip(self) -> str:
        """String pip of the card."""
        if self._pip > 10:
            return self._face_cards[self._pip - 11]
        return str(self._pip)

    def value(self, ace: int = 11) -> int:
        """Method to compute the value of a card.

        Cards 2 through 10 have the same value as their pip.
        Cards K, Q and J have a value of 10.
        Ace can have a value of 1 or 11.

        Arguments
        ----------
        ace: Value that should be assigned to an ace. Defaults to 11.
        """
        pip = self.pip

        if pip == "A":
            return ace

        return self._pip if pip not in self._face_cards else 10

    def is_ace(self) -> bool:
        """Method to check if a card is an ace."""
        return self.pip == "A"


class Deck:
    """Class to represent a deck of cards.

    Attributes
    ----------
    multipliers: tuple
        Sizes of the deck supported in terms of a 52-card deck.

    Methods
    ----------
    shuffle() -> None:
        Randomly shuffles the deck.

    pick_card() -> Card:
        Picks a card from the top of the deck and returns it.

    reset() -> None:
        Clears the deck.

    __bool__() -> bool:
        Returns True if the deck is not empty.

    __len__() -> int:
        Current size of the deck.
    """

    multipliers = (1, 2, 4, 6, 8)

    def __init__(self, multiplier: int = 1) -> None:
        """
        Arguments
        ----------
        multiplier: Size of the deck in terms of a 52-card deck.
        Defaults to 1.

        Raises
        ----------
        ValueError, when multiplier is not a supported value.
        """
        if multiplier not in self.multipliers:
            msg = f"multiplier can only be one of {self.multipliers}"
            raise ValueError(msg)

        self._deck = [Card(card) for card in range(2, 15)] * (4 * multiplier)
        self._deck_state: List[Card] = []

    def __bool__(self) -> bool:
        """Returns True if the deck is not empty."""
        return bool(self._deck_state)

    def __len__(self) -> int:
        """Returns the current length of the deck."""
        return len(self._deck_state)

    def shuffle(self) -> None:
        """Method to shuffle the deck."""
        if not self._deck_state:
            self._deck_state = list(self._deck)
        random.shuffle(self._deck_state)

    def pick_card(self) -> Card:
        """Method to pick a card from the top of the deck."""
        deck = self._deck_state or self._deck
        return deck.pop()

    def reset(self) -> None:
        """Method to clear the deck.

        Call this method first if, in a reshuffle, you want a full
        deck instead of just the current cards in it.
        """
        self._deck_state.clear()
