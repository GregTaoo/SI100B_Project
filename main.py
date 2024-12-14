import sys

import pygame

from NPC import NPC
from block import Blocks
import client
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
from dimension import Dimension
from player import Player


def main():
    pygame.init()
    pygame.display.set_caption("Minecraft (FAKE)")
    pygame.display.set_icon(Blocks.GRASS_BLOCK.image)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/simhei.ttf", 16)

    player = Player("Steve", (600, 600), (600, 600),
                    pygame.transform.scale(pygame.image.load("assets/player.png"), (50, 50)))
    dimension = Dimension(MAP_WIDTH, MAP_HEIGHT, Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [
        Blocks.GRASS_BLOCK, Blocks.LAVA, Blocks.STONE, Blocks.WATER
    ], [80, 1, 1, 1]))

    client.CLIENT = client.Client(screen, clock, font, player, dimension, player.get_camera(dimension.get_render_size()))

    client.CLIENT.spawn_entity(
        NPC("刁民", (500, 500), pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50)))
    )
    client.CLIENT.spawn_entity(
        NPC("丧尸", (700, 700), pygame.transform.scale(pygame.image.load("assets/zombie.png"), (50, 50)))
    )

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        client.CLIENT.tick(events)

        # 执行渲染
        pygame.display.flip()
        clock.tick(90)


if __name__ == "__main__":
    main()
