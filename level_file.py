from constants import *

class Level():
    TOTAL_LEVEL_SIZE = (len(level_1[0]) * PLATFORM_WIDTH, len(level_1) * PLATFORM_HEIGHT)
    CURRENT_LEVEL = level_1
    CURRENT_POINT_OF_SPAWN = point_spawn_1
    NUM_LEVEL = 0

    def __init__(self):
        pass

    def update(self):
        pass

    @classmethod
    def next_level(cls):
        cls.NUM_LEVEL += 1
        cls.TOTAL_LEVEL_SIZE = (len(LIST_LEVEL[cls.NUM_LEVEL][0]) * PLATFORM_WIDTH, len(LIST_LEVEL[cls.NUM_LEVEL]) * PLATFORM_HEIGHT)
        cls.CURRENT_LEVEL = LIST_LEVEL[cls.NUM_LEVEL]
        cls.CURRENT_POINT_OF_SPAWN = LIST_SPAWN[cls.NUM_LEVEL]