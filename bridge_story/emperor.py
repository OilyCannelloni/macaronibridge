from manim import Scene
from drawing.hands import Deal, Position, HandData
from drawing.deal_animator import DealAnimator

class Example(Scene):
    def construct(self):
        deal = Deal(
            west=HandData("AQ3", "QJ4", "K542", "KQ8"),
            north=HandData("T982", "T9", "QT", "A9654"),
            east=HandData("J65", "AK", "J9876", "T32"),
            south=HandData("K74", "876532", "A3", "J7"),
        )
        
        animator = DealAnimator(self)
        animator.initialize(deal)
        animator.create_hands(*Position.all())

        animator.set_contract_info("contract: 3ntW\n1d - 3d - 3nt\nopps play Better Minor, 1nt=11-14")

        animator.animate_trick(Position.NORTH, Position.SOUTH, "5c", "Tc", "Jc", "xc")
        animator.animate_trick(Position.SOUTH, Position.NORTH, "xc", "Qc", "Ac", "xc")
        comment1 = "From the first two tricks we know,\nthat  partner has 5 clubs,\nand declarer has KQx."
        comment2 = "Declarer would not let Jc hold,\nif he had KQxx."
        comment3 = "Therefore there is no need to\nshow count signal by 4c,\nand it should be interpreted\nas Lavinthal"
        comment4 = "We can deduce partner having Qxd."
        comment5 = "If we now play any low card..."
        
        animator.save_state("imperator")
        
        animator.animate_trick_with_comments(
            Position.NORTH, Position.WEST, 
            4, 2, "4c", "xc", "3h", "Kc",
            comment1, comment2, comment3, comment4, comment5)
        comment6 = "Declarer will easily guess the\ndiamond suit,\nas he must keep our partner off lead."
        animator.print_caption(comment6)

        animator.animate_trick(Position.WEST, Position.EAST, "xh", "xh", "Ah", "xh")
        animator.animate_trick(Position.EAST, Position.WEST, "xd", "xd", "Kd", "xd")
        animator.animate_trick(Position.WEST, Position.SOUTH, "xd", "xd", "Jd", "xd")

        comment7 = "Now the defense is hopeless."
        animator.print_caption(comment7)

        animator.restore_state("imperator")

        comment8 = "The only winning play here\nis to discard Ad!"
        animator.animate_trick_with_comments(
            Position.NORTH, Position.WEST, 
            4, 2, "4c", "xc", "Ad", "Kc",
            comment8)
        comment9 = "Declarer has no chance to play\ndiamonds without givind a trick to\nour partner\nand the contract will go down."
        animator.print_caption(comment9)

        comment10 = "This play is called Emperor's Coup.\nThis contract occured in\n1982 World Championships in France\nand was played by Jean Besse."
        animator.print_caption(comment10)

        self.wait(2)
