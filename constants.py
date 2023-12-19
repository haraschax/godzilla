from dataclasses import dataclass

MAX_HEALTH = 10
VICTORY_PTS_WIN = 20
DIE_COUNT = 6

class DIESIDE:
    ATTACK = 'Attack'
    HEAL = 'Heal'
    ONE = '1'
    TWO = '2'
    THREE = '3'


@dataclass
class PlayerState:
    health: int = 10
    victory_points: int = 0
    in_tokyo: bool = False