import functools
from typing import Dict, List

from .deck import FACE_CARDS


class Hand:
    def __init__(self) -> None:
        self.cards: List[str] = []
        self.count = 0

    @functools.cached_property
    def card_values(cls) -> Dict[str, int]:
        values = {str(card): card for card in range(2, 11)}
        values.update({card: 10 for card in FACE_CARDS if card != "A"})
        return values

    def update_count(self, card, ace=11) -> None:
        self.count += self.card_values[card] if card != "A" else ace

    def add_card(self, card: str, ace=11) -> None:
        self.cards.append(card)
        self.update_count(card, ace=ace)
