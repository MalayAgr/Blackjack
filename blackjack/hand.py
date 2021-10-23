from __future__ import annotations

import functools
from collections import UserList
from typing import List

from .deck import Card


class Hand(UserList):
    def get_count(self) -> int:
        if not self:
            return 0

        count = 0

        for card in self:
            count += card.value(current_count=count)

        return count
