SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 60, 60
BLOCK_SIZE = 60

INTERACTION_DISTANCE = 2

WORLDS = []
CLIENT = None
COIN_IMAGE = None
PARTICLES = []
FONT = None
MIDDLE_FONT = None
LARGE_FONT = None
SOUNDS = {}


def get_world(name: str):
    for i in WORLDS:
        if i.name == name:
            return i
    return None
