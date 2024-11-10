from drawing.hands import *
from drawing.deal_animator import DealAnimator


config.max_files_cached = 200


class Test(Scene):
    def construct(self):
        deal = Deal(
            west=HandData("AKJ974", "7", "Q962", "96"),
            north=HandData("T6", "KQ92", "A3", "J8532"),
            east=HandData("Q82", "A8643", "J74", "A4"),
            south=HandData("53", "JT5", "KT85", "KQT7")
        )

        animator = DealAnimator(self)
        animator.initialize(deal)

        animator.create_deal()
        animator.set_caption("4♠ by West")
        self.wait(3)
        animator.remove_caption()

        animator.animate_trick(NORTH, EAST, "Kh", "Ah", "5h", "7h")
        animator.animate_trick(EAST, WEST, "xh", "xh", "xs", "xh")
        animator.animate_trick(WEST, EAST, "xc", "xc", "Ac", "xc")
        animator.animate_trick(EAST, WEST, "xh", "xh", "xs", "xh")
        animator.animate_trick(WEST, EAST, "xs", "xs", "Qs", "xs")
        animator.animate_trick(EAST, WEST, "xh", "Qc", "xs", "xh")
        animator.animate_trick(WEST, WEST, "As", "xs", "xs", "xs")
        animator.animate_trick(WEST, SOUTH, "xc", "xc", "xc", "xc")

        animator.save_state("endplay")

        animator.set_caption("S is now endplayed.")
        self.wait(2)
        animator.set_caption("If he leads a diamond, \nhe breaks a frozen suit")
        self.wait(1)
        animator.animate_trick(SOUTH, NORTH, "xd", "xd", "Ad", "xd")
        animator.animate_trick(NORTH, WEST, "xd", "xd", "xd", "Qd")
        animator.animate_trick(WEST, SOUTH, "xd", "xc", "Jd", "Kd")
        animator.animate_trick(SOUTH, EAST, "xd", "xd", "xc", "xs")
        self.wait(2)

        animator.restore_state("endplay")
        animator.set_caption("If he leads a club, \nhe gives declarer a ruff-sluff \nand an entry to the "
                             "established heart")
        self.wait(1)
        animator.animate_trick(SOUTH, EAST, "xc", "xd", "xc", "xs")
        animator.animate_trick(EAST, EAST, "xh", "xd", "xd", "xc")

        self.wait(5)

