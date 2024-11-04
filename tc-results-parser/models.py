from dataclasses import dataclass


def get_vul(board_n):
    return ["", "NS", "EW", "NSEW", "NS", "EW", "NSEW", "", "EW", "NSEW", "", "NS", "NSEW", "", "NS", "EW"][(board_n - 1) % 16]


def get_dealer(board_n):
    return "NESW"[(board_n - 1) % 4]


@dataclass
class Hand:
    spades: str
    hearts: str
    diamonds: str
    clubs: str

    def __str__(self):
        return f"♠{self.spades} ♥{self.hearts} ♦{self.diamonds} ♣{self.clubs}"

    def to_vhand(self) -> str:
        return f"\\vhand{{{self.spades}}}{{{self.hearts}}}{{{self.diamonds}}}{{{self.clubs}}}"


@dataclass
class BoardData:
    sequence_number: int
    number: int
    west: Hand
    north: Hand
    east: Hand
    south: Hand

    def __str__(self):
        return "\n".join((str(x) for x in (self.west, self.north, self.east, self.south)))

    def to_handdiagramv(self) -> str:
        return (f"\\handdiagramv{{{self.west.to_vhand()}}}\n"
                f"{{{self.north.to_vhand()}}}\n"
                f"{{{self.east.to_vhand()}}}\n"
                f"{{{self.south.to_vhand()}}}\n"
                f"{{{get_vul(self.number)}}}\n")
