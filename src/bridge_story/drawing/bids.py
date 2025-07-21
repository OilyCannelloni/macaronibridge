from manim import *

from drawing.hands import Suit, Position


class Bid(VMobject):
    def __init__(self, position: Position, bid_str: str):
        super().__init__()
        self.suit: Suit = Suit.from_char(bid_str[1])
        self.level: int = int(bid_str[0])
        self.position: Position = position
        self._create()

    def _create(self):
        box = RoundedRectangle(corner_radius=0.08, height=0.5, width=1, fill_color=WHITE, fill_opacity=1)
        text = Text(f"{self.level}{self.suit.symbol()}", color=self.suit.color(),
                    font_size=18, font="Card Characters")
        text.shift(RIGHT * 0.2)
        box.add(text)

        box.set_opacity(0)
        angle = -PI / 2 * (self.position.value.id - 1)
        box.rotate(angle=angle, about_point=ORIGIN)
        box.move_to(self.position.hand_position())

        self.add(box)

