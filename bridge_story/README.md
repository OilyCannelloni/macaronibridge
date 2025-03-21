# BridgeStory
### A [Manim](https://github.com/ManimCommunity/manim) based framefork to create cute bridge movies.

## Installation
1. Install [ffmpeg](https://www.ffmpeg.org/)
2. Install manim:  
`pip install manim`
This might not work with python newer then 3.10.
3. Install the [Card Characters](https://font.download/font/card-characters) font

## Usage
Create a file named example.py:  
```py
from manim import Scene
from drawing.hands import Deal, Position, HandData
from drawing.deal_animator import DealAnimator

class Example(Scene):
    def construct(self):
        deal = Deal(
            west=HandData("QJT98", "Q872", "KQ96", ""),
            north=HandData("43", "AKJ65", "A872", "62"),
            east=HandData("A762", "T", "JT43", "AKQ8"),
            south=HandData("K5", "943", "5", "JT97543")
        )
        
        animator = DealAnimator(self)
        animator.initialize(deal)
        animator.create_hands(*Position.all())
        self.wait(3)
```

Build the animation:  
`manim -p -qh example.py Example`

What happened here?  
- Manim is based on Scenes. To create one, you utilise a class with a `construct()` method.
- Then, we defined a Deal and passed it to the DealAnimator. It did all the hard work for you!

### Playing the cards

At the bottom of the file, before the final `wait()`, add  
```py
animator.animate_trick(Position.NORTH, Position.NORTH, "Ah", "Th", "3h", "7h")
animator.animate_trick(Position.NORTH, Position.EAST, "xs", "As", "xs", "xs")
animator.animate_trick(Position.EAST, Position.SOUTH, "xs", "xs", "xs", "xs")
```

Animating a trick requires you to specify the player on lead, the player taking the trick
and the cards played from each hand. You can use 'xs' as the smallest spade, even if it's a face card!

### Savestates

As you can see here, South blundered by not giving correct suit preference on the first trick.
Let's give him another chance! Add the following lines:
```py
self.wait(2)
animator.restore_state("start")
animator.animate_trick(Position.NORTH, Position.NORTH, "Ah", "xh", "9h", "xh")
animator.animate_trick(Position.NORTH, Position.NORTH, "Ad", "xd", "xd", "xd")
animator.animate_trick(Position.NORTH, Position.SOUTH, "xd", "xd", "xs", "xd")
```

Now if declarer takes the spade hook, the contract is down!

The start of the deal is saved under the tag "start"
You can create custom savestates using `animator.save_state([tag])`

