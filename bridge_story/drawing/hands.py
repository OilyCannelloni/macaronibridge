from .common import load_config

import abc
import dataclasses
from copy import copy
from typing import cast
from abc import ABC
from enum import Enum, EnumMeta
from collections.abc import Iterable

import numpy.typing
from manim import *

config = load_config()

class Position(Enum):
    """
    Represents properties of compass positions, including:
    - vector: a 3D numpy.NDArray of a unit vector directed towards the position.
    - HAND_MPL: a multiplier for the vector describing the position of the player's hand.
    - TARGET_MPL: a multiplier for the vector describing the position of the place, where a played card lands.
    """
    @dataclasses.dataclass
    class PositionData:
        vector: numpy.typing.NDArray
        id: int = -1
        HAND_MPL = 2
        TARGET_MPL = 0.5

        def __eq__(self, other):
            return self.id == other.id  # Must be so, because NDArrays do not define __eq__, which is necessary in Enums

    WEST = PositionData(LEFT, 0)
    NORTH = PositionData(UP, 1)
    EAST = PositionData(RIGHT, 2)
    SOUTH = PositionData(DOWN, 3)

    def card_target(self):
        """
        Returns the vector pointing to the place, where a played card lands.
        """
        return self.value.vector * self.value.TARGET_MPL

    def hand_position(self):
        """
        Returns the vector pointing to the position of the player's hand.
        """
        return self.value.vector * self.value.HAND_MPL

    def next(self):
        """
        Returns the position following the current one in clockwise order.
        """
        match self:
            case Position.WEST:
                return Position.NORTH
            case Position.NORTH:
                return Position.EAST
            case Position.EAST:
                return Position.SOUTH
            case Position.SOUTH:
                return Position.WEST

    def trick(self):
        """
        Iterates around the compass for exactly one revolution.
        """
        base = copy(self)
        for _ in range(4):
            yield base
            base = base.next()

    @classmethod
    def all(cls):
        return tuple(cls.trick(cls.WEST))


WEST = Position.WEST
NORTH = Position.NORTH
EAST = Position.EAST
SOUTH = Position.SOUTH


class Suit(Enum):
    """
    Describes the properties of card suits.
    """
    @dataclasses.dataclass
    class SuitData:
        symbol: str
        color: tuple[int, int, int]

    if config.get("use_alternative_font", False):
        CLUBS = SuitData('c', (20, 220, 20))
        DIAMS = SuitData('1', (255, 160, 20))
        HEARTS = SuitData('2', (255, 26, 26))
        SPADES = SuitData('s', (50, 183, 255))
    else:
        CLUBS = SuitData(']', (20, 220, 20))  # what
        DIAMS = SuitData('[', (255, 160, 20))
        HEARTS = SuitData('{', (255, 26, 26))
        SPADES = SuitData('}', (50, 183, 255))  # see README if still confused lol

    @classmethod
    def suits(cls) -> Iterable[SuitData]:
        """
        Iterates over all suits in SHDC order.
        """
        yield from (cls.SPADES, cls.HEARTS, cls.DIAMS, cls.CLUBS)

    def symbol(self) -> str:
        """
        Returns the symbol of the suit.
        """
        return self.value.symbol

    def color(self) -> tuple[int, int, int]:
        """
        Returns the color of the suit
        """
        return self.value.color

    @classmethod
    def from_char(cls, char: str):
        """
        Transforms a short-notation char (s, h, d, c) into a Suit object.
        Suit.from_char('h') -> Suit.HEARTS
        """
        match char:
            case "c":
                return cls.CLUBS
            case "d":
                return cls.DIAMS
            case "h":
                return cls.HEARTS
            case "s":
                return cls.SPADES
        return None


class Card(Text):
    """
    Represents a single card on the animation.
    """
    def __init__(self, value, **kwargs):
        self.value = value
        if config.get("use_alternative_font", False):
            super().__init__(value, font="Cards", **kwargs)
        else:
            super().__init__(value, font="Card Characters", **kwargs)
        # There is the answer, this font encodes '=' as a single-space 10, '[' as ♦, '}' as ♠ etc.


CARD_SPACING = 0.20
CARD_SYMBOL_OFFSET = 0.30


class Holding(VMobject):
    """
    Describes a set of cards within a suit, ex. ♥AKJ9653
    """
    def __init__(self, suit: Suit, cards_str: str, **kwargs):
        self.cards_str = cards_str
        self.suit = suit
        self.font_size = kwargs.get("font_size", 20)
        super().__init__()
        self._create()

    def _create(self):
        # Choose font for suit symbol
        suit_font = "Cards" if config.get("use_alternative_font", False) else "Card Characters"
        # Choose font for card values
        card_font = "Arial" if config.get("use_alternative_font", False) else "Card Characters"

        # Create the suit symbol text
        symbol = Text(
            self.suit.symbol(),
            font_size=self.font_size,
            color=self.suit.color(),
            font=suit_font
        )
        self.add(symbol)

        for i, card_value in enumerate(self.cards_str):
            if not config.get("use_alternative_font", True):
                text = card_value.replace("T", "=")
            else:
                text = card_value
            
            card = Text(
                text,
                font_size=self.font_size,
                color=self.suit.color(),
                font=card_font
            )

            offset = CARD_SYMBOL_OFFSET + i * CARD_SPACING
            card.shift(offset * RIGHT)
            self.add(card)

    def cards(self):
        """
        Iterates over all cards in the Holding
        """
        yield from (x for x in self.submobjects if x.__class__ == Card)

    def get_card(self, card_value: str):
        """
        Gets the Card object from a short-notation string.
        :param card_value: The value of the card to get, ex. 9 or Q. Use 'x' for smallest available card.
        :return: Card object corresponding to the value.
        """
        if not config.get("use_alternative_font", True) and card_value == "T":
            value = "="
        else:
            value = card_value

        if value == 'x':
            return max(enumerate(self.cards()))[1]  # what
        return next(c for c in self.cards() if c.value == value)


class HandData(dict):
    """
    Describes the contents of a hand. Reference using
    hand_data = HandData("AKQJ", "T98", "76543", "2")
    hand_data[Suit.HEARTS]  # "T98"
    """
    def __init__(self, spades, hearts, diams, clubs):
        super().__init__()
        self[Suit.SPADES] = spades
        self[Suit.HEARTS] = hearts
        self[Suit.DIAMS] = diams
        self[Suit.CLUBS] = clubs

    def __str__(self):
        return " ".join(self[s] for s in Suit.suits())

    def str_holdings(self) -> Iterable[str]:
        """
        Iterates over the holdings in SHDC order.
        """
        yield from (self[s] for s in Suit.suits())

    def remove_card(self, card_str) -> str:
        """
        Removes a card from a string holding.
        :param card_str: A card in short-notation, ex. Qd for the Queen of diamonds. 'xh' = smallest heart.
        """
        pos = Suit.from_char(card_str[1])
        try:
            if card_str[0] == "x":
                self[pos] = self[pos][:-1]
            else:
                self[pos] = self[pos].replace(card_str[0], "")
            return self[pos]

        except Exception:
            raise ValueError(f"Hand {str(self)} does not contain {card_str}")


class Hand(VMobject, ABC):
    """
    An abstract class defining a Hand as a set of 4 Holdings.
    """
    def __init__(self, spades: str, hearts: str, diams: str, clubs: str):
        self.hand_data = HandData(spades, hearts, diams, clubs)
        self.position = None
        super().__init__()
        self._create()

    def get_holding(self, char: str) -> Holding:
        """
        Returns a Holding marked by the suit in short-notation ('s' for spades etc.)
        """
        suit = Suit.from_char(char)
        holding = next(h for h in self.submobjects if h.suit == suit)
        return cast(Holding, holding)

    @abc.abstractmethod
    def _create(self):
        """
        Creates the Hand object on the Scene.
        """
        pass


V_HOLDING_SPACING = 0.40


class VerticalHand(Hand):
    def _create(self):
        """
        Creates a Vertical Hand on the scene. The Holdings are stacked on top of each other.
        """
        super()._create()
        for i, suit, cards in zip(range(4), Suit.suits(), self.hand_data.str_holdings()):
            holding = Holding(suit, cards)
            holding.shift(i * V_HOLDING_SPACING * DOWN)
            self.add(holding)
        self.shift(-self.get_center())
        """ 
        TODO: ^^ It's just slightly imprecise for some reason. 
        Probably the starting position is at the center of ♠ pip rather than the top-left corner.
        """


class Deal(dict):
    """
    dict[Position, HandData]
    Represents the properties of a bridge deal.
    Used to store savestates for a later rollback.
    """
    def __init__(self, west: HandData, north: HandData, east: HandData, south: HandData):
        super().__init__()
        self[Position.WEST] = west
        self[Position.NORTH] = north
        self[Position.EAST] = east
        self[Position.SOUTH] = south

    def to_hands(self) -> dict[Position, Hand]:
        """
        Creates a dict of Hand objects.
        """
        hands = {}
        for pos, hand_data in self.items():
            hands[pos] = VerticalHand(*hand_data.str_holdings())
            hands[pos].position = pos
            hands[pos].shift(pos.hand_position())
        return hands

