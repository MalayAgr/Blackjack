from __future__ import annotations

from typing import List, Optional, Union

from rich.prompt import FloatPrompt

from .console import console
from .deck import Card


class _GenericPlayer:
    """Class which represents a generic player.

    Attributes
    ----------
    hand: list of Card instances
        Current hand of the player.

    Methods
    ----------
    count() -> int:
        Computes the count value of the current hand.

    add_card_to_hand(card: Card) -> None:
        Adds the given card to the hand.

    clear_hand() -> None:
        Clears the hand.

    has_blackjack() -> bool:
        Returns True if the count of value of the current hand is 21.

    has_busted() -> bool:
        Returns True if the count of value of the current hand
        is greater than 21.
    """

    def __init__(self) -> None:
        self.hand: List[Card] = []

    def count(self, ace_limit: int = 21) -> int:
        """Method to compute the count value of the current hand.

        This uses a greedy approach where all aces are counted as 11
        as long as the count does not exceed ace_limit. All remaining aces
        are counted as 1.

        Arguments
        ----------
        ace_limit: Count value up to which aces should be counted as 11.
        Defaults to 21.
        """
        hand = self.hand

        if not hand:
            return 0

        # First count all non-ace cards since their value is fixed
        count = sum(card.value() for card in hand if not card.is_ace())

        for ace in (card for card in hand if card.is_ace()):
            # Greedily add aces
            count += ace.value(ace=11 if count + 11 < ace_limit else 1)

        return count

    def add_card_to_hand(self, card: Card) -> None:
        """Method to add a card to the hand of the player.

        Arguments
        ---------
        card: Card to be added.
        """
        self.hand.append(card)

    def has_blackjack(self) -> bool:
        """Method to check if the player has a count value of 21."""
        return self.count() == 21

    def has_busted(self) -> bool:
        """Method to check if the player has exceeded a count value of 21."""
        return self.count() > 21

    def clear_hand(self) -> None:
        """Method to reset the player's hand to an empty hand."""
        self.hand.clear()


class Player(_GenericPlayer):
    """Class to represent a non-dealer player.

    Inherits from
    ----------
    _GenericPlayer

    Attributes
    ----------
    name: str
        Name of the player.

    bankroll: float
        Amount of money (in dollars) the player has with them.

    Methods
    ----------
    from_input() -> Player:
        Class method which creates a Player instance from user-input.

    pay(amount: float) -> None:
        Pays the given amount to the player.

    bet(amount: float) -> None:
        Deducts the given amount from the player's bankroll.
    """

    def __init__(self, name: str, bankroll: float) -> None:
        """
        Arguments
        ----------
        name: Name of the player.

        bankroll: Amount of money player has with them.
        """
        self.name = name
        self.bankroll = bankroll
        super().__init__()

    @classmethod
    def from_input(cls) -> Player:
        """Class method which creates a Player instance from user-input

        Returns
        ----------
        A Player instance with the inputted name and bankroll.
        """
        name = console.input("What should we call you? ")
        console.print(f"[green]Hi, {name}![/green]")

        bankroll = FloatPrompt.ask("How much money will you be playing with? ($)")

        return cls(name=name, bankroll=bankroll)

    def pay(self, amount: float) -> None:
        """Method which pays the given amount to the player,
        adding it to their bankroll.

        Arguments
        ----------
        amount: Amount to be paid.
        """
        self.bankroll += amount

    def bet(self, amount: float) -> None:
        """Method which deducts the given amount from the player's bankroll.

        Arguments
        ----------
        amount: Amount that should be deducted.
        """
        self.bankroll -= amount


class Dealer(_GenericPlayer):
    """Class which represents a dealer.

    Inherits from
    ----------
    _GenericPlayer

    Attributes
    ---------
    face_up: Card
        Face-up card of the dealer.

    face_down: Card or None
        Face-down card of the dealer. It is None when there is no such card.

    has_face_down: bool
        Denotes whether the dealer has a face-down card. True when this is the case.
        False otherwise. Defaults to True.
    """

    def __init__(self) -> None:
        self._face_up = 0
        self.has_face_down = True
        self._face_down = -1
        super().__init__()

    @property
    def face_up(self) -> Card:
        """Face-up card of the dealer."""
        return self.hand[self._face_up]

    @property
    def face_down(self) -> Optional[Card]:
        """Face-down card of the dealer."""
        if self.has_face_down:
            return self.hand[self._face_down]

    def count(self) -> int:
        """Method to compute the dealer's count."""
        # Limit is 17 since dealers must count an ace as 11
        # If it puts their count above 17.
        return super().count(ace_limit=17)

    def clear_hand(self) -> None:
        self.has_face_down = True
        return super().clear_hand()


# Type alias for a player since _GenericPlayer is internal
PlayerType = Union[Player, Dealer]
