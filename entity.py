from typing import Tuple

import pygame
from pygame import Rect

import action
import animation
import client
from config import BLOCK_SIZE, INTERACTION_DISTANCE


class Entity:
    fire_image = pygame.transform.scale(pygame.image.load("assets/fire.png"), (BLOCK_SIZE, BLOCK_SIZE))

    def __init__(self, name: str, pos: Tuple[int, int], image: pygame.Surface, actions=None, atk=1.0):
        self.name = name
        self.x, self.y = pos
        self.image, self.image_mirrored = image, pygame.transform.flip(image, True, False)
        self.size = image.get_size()
        self.mirror = False
        self.hp = 100
        self.fire_tick = 0
        self.atk = atk
        self.actions = actions if actions is not None else [action.Actions.ATTACK_LEFT]

    def move(self, direction, dimension, speed=4):
        if not (1 <= direction <= 4):
            return

        # 获取移动方向的左右两格方块，并判断碰撞箱，如果该方块被标记为障碍物则无法通过
        block_x, block_y = dimension.get_block_index((self.x, self.y))
        block2_x, block2_y = block_x, block_y

        if direction == 1:
            self.x += speed
            self.mirror = False
            block_x += 1
            block2_x, block2_y = block_x, block_y + 1
        elif direction == 2:
            self.x -= speed
            self.mirror = True
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

        # 地图边界
        limit_x, limit_y = dimension.get_render_size()
        self.x = max(0, min(limit_x - self.size[0], self.x))
        self.y = max(0, min(limit_y - self.size[1], self.y))

        # 障碍物处理
        rect = self.get_rect()
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

    def tick(self, dimension, player=None):
        for i in {dimension.get_block_index(self.get_left_top_pos()),
                  dimension.get_block_index(self.get_left_bottom_pos()),
                  dimension.get_block_index(self.get_right_top_pos()),
                  dimension.get_block_index(self.get_right_bottom_pos())}:
            blk = dimension.get_block_from_index(i)
            if blk is not None:
                blk.on_entity(dimension.get_pos_from_index(i), self)
        if self.fire_tick > 0:
            self.fire_tick -= 1
            self.hp -= 1 / 12
        if self.hp <= 0 and self in client.CLIENT.dimension.entities:
            client.CLIENT.dimension.entities.remove(self)
            del self

    def respawn_at_pos(self, pos: Tuple[int, int]):
        self.x, self.y = pos
        self.hp = 100
        self.fire_tick = 0

    def get_rect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.x, self.y
        return rect

    def get_left_top_pos(self):
        return self.x, self.y

    def get_left_bottom_pos(self):
        return self.x, self.y + self.size[1] - 1

    def get_right_top_pos(self):
        return self.x + self.size[0] - 1, self.y

    def get_right_bottom_pos(self):
        return self.x + self.size[0] - 1, self.y + self.size[1] - 1

    def is_nearby(self, entity):
        return abs(self.x - entity.x) + abs(self.y - entity.y) < INTERACTION_DISTANCE * BLOCK_SIZE

    def render(self, screen: pygame.Surface, camera: Tuple[int, int], font=None):
        screen.blit(self.image_mirrored if self.mirror else self.image, (self.x - camera[0], self.y - camera[1]))
        if self.fire_tick > 0:
            animation.Animations.FIRE.render(screen, (self.x - camera[0], self.y - camera[1]))
        self.render_hp_bar(screen, (self.x - camera[0], self.y - camera[1] - 10), font)

    def render_at_absolute_pos(self, screen: pygame.Surface, pos: Tuple[int, int], font=None, use_mirror=False):
        screen.blit(self.image_mirrored if use_mirror else self.image, pos)
        self.render_hp_bar(screen, (pos[0], pos[1] - 10), font)

    def render_hp_bar(self, screen: pygame.Surface, pos: Tuple[int, int], font=None):
        bar_width, bar_height = self.size[0], 5
        hp_rect = pygame.Rect(pos[0], pos[1], bar_width * self.hp / 100, bar_height)
        border_rect = pygame.Rect(pos[0], pos[1], bar_width, bar_height)
        pygame.draw.rect(screen, ((0, 255, 0) if self.hp >= 60 else (255, 255, 0)) if self.hp >= 30 else (255, 0, 0),
                         hp_rect)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 1)

        # hp_text = f"HP: {self.hp} / 100"
        # text_surface = font.render(hp_text, True, (255, 255, 255))
        # text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        # screen.blit(text_surface, text_rect)
