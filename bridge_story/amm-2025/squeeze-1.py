from drawing.hands import *
from drawing.deal_animator import DealAnimator

config.max_files_cached = 200


class Test(Scene):
    def construct(self):
        deal = Deal(
            west=HandData.from_str("AK82 KQ2 2 JT932"),
            north=HandData.from_str("T9 654 JT64 AKQ5"),
            east=HandData.from_str("Q543 T987 9853 4"),
            south=HandData.from_str("J76 AJ3 AKQ7 876")
        )

        animator = DealAnimator(self)
        animator.initialize(deal)
        animator.reveal_hands(Position.NORTH, Position.SOUTH)
        self.wait(1)
        animator.bid(NORTH, "1h")
        self.wait(0.5)
        animator.bid(EAST, "1s")
        self.wait(0.5)
        animator.bid(SOUTH, "2c")
        self.wait(0.5)
        animator.bid(WEST, "3d")
        self.wait(3)



