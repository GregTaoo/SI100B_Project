from typing import Tuple

import pygame
from pygame import Rect

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE
from dimension import Dimension


class Player:

    def __init__(self, name: str, pos: Tuple[int, int], image: pygame.Surface):
        self.name = name
        self.x, self.y = pos
        self.image = image
        self.size = image.get_size()

    def move(self, direction, dimension: Dimension, speed=4):
        block_x, block_y = dimension.get_block_index((self.x, self.y))
        block2_x, block2_y = block_x, block_y
        if direction == 1:
            self.x += speed
            block_x += 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 2:
            self.x -= speed
            block_x -= 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 3:
            self.y += speed
            block_y += 1
            block2_x, block2_y = block_x + 1, block_y
        elif direction == 4:
            self.y -= speed
            block_y -= 1
            block2_x, block2_y = block_x + 1, block_y

        limit_x, limit_y = dimension.get_render_size()
        self.x = max(0, min(limit_x - self.size[0], self.x))
        self.y = max(0, min(limit_y - self.size[1], self.y))

        rect = self.image.get_rect()
        rect.x, rect.y = self.x, self.y
        if ((rect.colliderect(Rect(block_x * BLOCK_SIZE, block_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
                dimension.get_block_from_index((block_x, block_y)).path) or
                (rect.colliderect(Rect(block2_x * BLOCK_SIZE, block2_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) and
                 dimension.get_block_from_index((block2_x, block2_y)).path)):
            if direction == 1:
                self.x -= self.x + self.size[0] - block_x * BLOCK_SIZE
            elif direction == 2:
                self.x += block_x * BLOCK_SIZE - self.x + BLOCK_SIZE
            elif direction == 3:
                self.y -= self.y + self.size[1] - block_y * BLOCK_SIZE
            elif direction == 4:
                self.y += block_y * BLOCK_SIZE - self.y + BLOCK_SIZE

    def get_camera(self, limit: Tuple[int, int]):
        return (max(0, min(limit[0] - SCREEN_WIDTH, self.x + self.size[0] // 2 - SCREEN_WIDTH // 2)),
                max(0, min(limit[1] - SCREEN_HEIGHT, self.y + self.size[1] // 2 - SCREEN_HEIGHT // 2)))

    def render(self, screen: pygame.Surface, camera):
        screen.blit(self.image, (self.x - camera[0], self.y - camera[1]))
