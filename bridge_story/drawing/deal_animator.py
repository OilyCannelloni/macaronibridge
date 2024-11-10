from copy import deepcopy
from .hands import *


class DealAnimator:
    """
    This class contains the methods which can be used to animate a bridge deal.
    :param scene: Manim Scene.
    """
    def __init__(self, scene: Scene):
        self.scene = scene
        self.hands: dict[Position, Hand] = {}
        self.cached_states: dict[str, Deal] = {}
        self.active_trick = {}
        self.caption = None
        self.hidden: dict[Position, bool] = {p: True for p in Position.all()}

        circle = Circle(0.1, WHITE).center()
        self.scene.play(Create(circle))

    def initialize(self, deal: Deal):
        """
        Initializes the Animator with a Deal. It is saved as a state with name 'start'.
        """
        self.create_state("start", deal)
        self.hands = deal.to_hands()

    def create_hand(self, hand: Hand):
        """
        Creates a given hand at the Scene.
        """
        self.hidden[hand.position] = False
        self.scene.play(Create(hand), run_time=0.8)

    def create_hands(self, *positions: Position):
        """
        Creates all hands at the scene. All hands must be registered using initialize(deal)
        """
        for position in positions:
            self.create_hand(self.hands[position])

    def hide_hands(self, *positions_to_hide: Position):
        hiding_hands = []
        for pos in positions_to_hide:
            if not self.hidden[pos]:
                hiding_hands.append(self.hands[pos])
            self.hidden[pos] = True
        self.scene.play(
            *[FadeOut(hand) for hand in hiding_hands]
        )

    def reveal_hands(self, *positions_to_reveal: Position):
        revealing_hands = []
        for pos in positions_to_reveal:
            if self.hidden[pos]:
                revealing_hands.append(self.hands[pos])
            self.hidden[pos] = False
        self.scene.play(
            *[FadeIn(hand) for hand in revealing_hands]
        )

    def create_state(self, tag: str, deal: Deal):
        """
        Creates a state from a given Deal (might not use all 13 cards per player).
        :param tag: A name of the state to be saved.
        :param deal: A Deal object containing the players' cards.
        """
        self.cached_states[tag] = deal

    def save_state(self, tag: str):
        """
        Stores the current state of the deal in memory.
        :param tag: A name of the state to be saved.
        """
        self.cached_states[tag] = Deal(
            *(deepcopy(self.hands[pos].hand_data) for pos in Position.all())
        )

    def restore_state(self, tag: str):
        """
        Restores a previously saved state of the deal.
        :param tag: A name of the saved state.
        """
        new_hands = self.cached_states[tag].to_hands()

        self.scene.play(*[
            Transform(self.hands[pos], new_hands[pos], replace_mobject_with_target_in_scene=True)
            for pos in Position.trick(Position.WEST)
        ])

        self.hands = new_hands

    def play_card(self, hand: Hand, card_value: str) -> None:
        """
        Animates the play of a single card.
        :param hand: Player's hand
        :param card_value: Value of the card to be played in short-notation,
                           ex. 'Qc' for the Queen of clubs. Use 'x' for smallest card.
        """
        holding = hand.get_holding(card_value[1])
        card = holding.get_card(card_value[0])
        self.active_trick[hand.position] = card
        holding.remove(card)  # remove card from screen
        new_holding_str = hand.hand_data.remove_card(card_value)  # remove card from memory

        new_holding = Holding(holding.suit, new_holding_str)
        new_holding.move_to(holding.get_left())
        new_holding.shift(new_holding.width / 2 * RIGHT)

        if self.hidden[hand.position]:
            hand.remove(holding)  # silent transform
            hand.add(new_holding)
            card.move_to(hand.position.hand_position())
            self.scene.play(
                card.animate.move_to(hand.position.card_target())
                            .set(font_size=24)
                            .set_opacity(1),
                run_time=0.8
            )
            return

        self.scene.play(
            card.animate.move_to(hand.position.card_target())
                        .set(font_size=24)
                        .set_opacity(1),
            Transform(holding, new_holding, replace_mobject_with_target_in_scene=True),
            run_time=0.8
        )

    def play_trick(self, on_lead: Position, *sequence):
        """
        Animates the play of a trick.
        :param on_lead: The player who starts the trick.
        """
        assert len(sequence) <= 4
        for i, position in enumerate(on_lead.trick()):
            self.play_card(self.hands[position], sequence[i])

    def give_trick_to(self, winner: Position):
        """
        Animates the disappearing of the trick.
        :param winner: The player towards whom the trick goes.
        """
        trick = Group(*self.active_trick.values())
        self.scene.play(
            FadeOut(trick, target_position=winner.hand_position(), scale=0.5)
        )
        self.active_trick = {}

    def animate_trick(self, on_lead: Position, winner: Position, *sequence):
        """
        Animates the playing and disappearing of a trick.
        :param on_lead: The player who starts the trick.
        :param winner: The player towards whom the trick goes.
        """
        self.play_trick(on_lead, *sequence)
        self.scene.wait(0.5)
        self.give_trick_to(winner)
        self.scene.wait(0.5)

    def set_caption(self, str):
        """
        Creates a caption on lower-right of the screen.
        """
        CAPT = DOWN * 2 + RIGHT * 1.5
        text = Text(str, font_size=24, font="Cambria").shift(CAPT)
        text.shift(text.width / 2 * RIGHT)
        if self.caption is None:
            self.scene.play(Create(text))
        else:
            self.scene.play(Transform(self.caption, text, replace_mobject_with_target_in_scene=True))
        self.caption = text

    def remove_caption(self):
        """
        Removes the caption from the screen.
        """
        self.scene.play(FadeOut(self.caption))
        self.caption = None


