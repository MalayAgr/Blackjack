from __future__ import annotations

import functools
from typing import Dict, List

from .deck import FACE_CARDS


class CountingStrategyMissingError(ValueError):
    """No counting strategy has been specified even though aces are present."""


class UnRecognizedCountingStrategyError(ValueError):
    """At least one ace's count is not 1 or 11."""


class MismatchedCountingStrategyError(ValueError):
    """The number of aces and the counts in the strategy do not match"""


class Hand:
    def __init__(self) -> None:
        self.cards: List[str] = []

    @functools.cached_property
    def card_values(cls) -> Dict[str, int]:
        values = {str(card): card for card in range(2, 11)}
        values.update({card: 10 for card in FACE_CARDS if card != "A"})
        return values

    def count(self, aces: List[int] = None) -> int:
        if not self.cards:
            return 0

        if aces is None:
            aces = []

        if "A" in self.cards:
            if not aces:
                raise CountingStrategyMissingError()

            if self.cards.count("A") != len(aces):
                raise MismatchedCountingStrategyError()

            if any(x not in [1, 11] for x in aces):
                raise UnRecognizedCountingStrategyError()

        values, count, ace_count = self.card_values, 0, 0

        for card in self.cards:
            if card == "A":
                count += aces[ace_count]
                ace_count += 1
            else:
                count += values[card]

        return count

    def add_card(self, card: str) -> None:
        self.cards.append(card)
