import pygame

import NPC
import UI
import animation
import config
import i18n
from block import Blocks
from config import MAP_WIDTH, MAP_HEIGHT
from dimension import Dimension
from hud import MainHud


def generate_the_world():
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [
        Blocks.GRASS_BLOCK, Blocks.LAVA, Blocks.STONE, Blocks.WATER
    ], [150, 1, 2, 1])
    for i in range(3):
        mp[MAP_WIDTH - 10 + i][MAP_HEIGHT - 10] = mp[MAP_WIDTH - 10 + i][MAP_HEIGHT - 8] = Blocks.OBSIDIAN
    mp[MAP_WIDTH - 10][MAP_HEIGHT - 9] = mp[MAP_WIDTH - 8][MAP_HEIGHT - 9] = Blocks.OBSIDIAN
    mp[MAP_WIDTH - 9][MAP_HEIGHT - 9] = Blocks.NETHER_PORTAL
    # mp[10][10] = Blocks.NETHER_PORTAL
    return mp


def generate_the_end():
    mp = Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [Blocks.END_STONE], [1])
    mp[MAP_WIDTH // 2][MAP_HEIGHT // 2] = Blocks.NETHER_BACK_PORTAL
    return mp


def generate_the_nether():
    mp = [[Blocks.NETHERITE_BLOCK] * 17 + [Blocks.WARPED_PLANKS] * 3 + [Blocks.NETHERITE_BLOCK] * 40]
    with open('assets/maps/nether.txt', 'r') as f:
        for line in f.readlines():
            mp.append([Blocks.WARPED_PLANKS if i == 'A' else Blocks.NETHERITE_BLOCK
                       for i in line.strip()] + [Blocks.NETHERITE_BLOCK] * 39)
    for i in range(38):
        mp.append([Blocks.NETHERITE_BLOCK] * MAP_WIDTH)
    mp[2][17] = mp[3][19] = Blocks.REDSTONE_BLOCK
    mp[7][11] = mp[8][10] = Blocks.REDSTONE_BLOCK
    mp[18][18] = mp[19][19] = Blocks.REDSTONE_BLOCK

    return mp


def change_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


def pause_music():
    pygame.mixer.music.pause()


class Client:

    def __init__(self, screen, clock, player, dimension):
        self.screen = screen
        self.clock = clock
        self.tick_counter = 0
        self.player = player
        self.current_ui = None
        self.current_hud = MainHud(player)
        config.WORLDS['the_world'] = Dimension('the_world', MAP_WIDTH, MAP_HEIGHT, generate_the_world())
        config.WORLDS['the_nether'] = Dimension('the_nether', MAP_WIDTH, MAP_HEIGHT, generate_the_nether(),
                                                'assets/sounds/music_terribly.mp3')
        nether_npc1 = NPC.NetherNPC1((2 * config.BLOCK_SIZE + 5, 18 * config.BLOCK_SIZE + 5))
        nether_npc1.mirror = True
        config.WORLDS['the_nether'].spawn_entity(nether_npc1)
        nether_npc2 = NPC.NetherNPC2((8 * config.BLOCK_SIZE + 5, 11 * config.BLOCK_SIZE + 5))
        config.WORLDS['the_nether'].spawn_entity(nether_npc2)
        nether_npc3 = NPC.NetherNPC3((18 * config.BLOCK_SIZE + 5, 19 * config.BLOCK_SIZE + 5))
        config.WORLDS['the_nether'].spawn_entity(nether_npc3)
        nether_npc4 = NPC.NetherNPC4((12 * config.BLOCK_SIZE + 5, 2 * config.BLOCK_SIZE + 5))
        config.WORLDS['the_nether'].spawn_entity(nether_npc4)
        nether_npc5 = NPC.NetherNPC3((20 * config.BLOCK_SIZE + 5, 1 * config.BLOCK_SIZE + 5))
        config.WORLDS['the_nether'].spawn_entity(nether_npc5)
        config.WORLDS['the_end'] = Dimension('the_end', MAP_WIDTH, MAP_HEIGHT, generate_the_end())
        config.SOUNDS['hit'] = pygame.mixer.Sound("assets/sounds/hit.mp3")
        config.SOUNDS['hit'].set_volume(0.5)
        config.SOUNDS['player_death'] = pygame.mixer.Sound("assets/sounds/player_death.mp3")
        config.SOUNDS['player_death'].set_volume(0.5)
        config.SOUNDS['zeus'] = pygame.mixer.Sound("assets/sounds/zeus.mp3")
        config.SOUNDS['zeus'].set_volume(0.25)
        config.SOUNDS['button1'] = pygame.mixer.Sound("assets/sounds/button1.mp3")
        config.SOUNDS['button1'].set_volume(0.75)
        config.SOUNDS['button2'] = pygame.mixer.Sound("assets/sounds/button2.mp3")
        config.SOUNDS['button2'].set_volume(0.75)
        self.dimension = config.WORLDS[dimension]
        self.camera = self.player.get_camera(self.dimension.get_render_size())

    def spawn_entity(self, entity):
        self.dimension.spawn_entity(entity)

    def set_dimension(self, dimension):
        self.dimension = dimension
        if dimension.music is not None:
            change_music(dimension.music)

    def open_ui(self, ui):
        self.current_ui = ui

    def open_message_box(self, text: i18n.Text, father_ui):
        self.open_ui(UI.MessageBoxUI(text, father_ui))

    def close_ui(self):
        ui = self.current_ui
        self.current_ui = None
        if ui is not None:
            ui.on_close()
        del ui

    def open_death_ui(self):
        self.player.coins //= 2
        self.current_ui = UI.DeathUI()

    def player_respawn(self):
        self.player.respawn()
        self.close_ui()

    def tick_second(self):
        self.player.tick_second(self.dimension, self.player)
        for i in self.dimension.entities:
            i.tick_second(self.dimension, self.player)

    def tick(self, events):
        # 务必先渲染背景
        self.screen.fill((50, 50, 50))
        self.dimension.render(self.screen, self.camera)
        for i in self.dimension.entities:
            i.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)

        if self.current_ui is None:
            # 玩家移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SLASH]:
                self.open_ui(UI.InputTextUI())
            if keys[pygame.K_w]:  # 向上移动
                self.player.move(4, self.dimension)
            if keys[pygame.K_s]:  # 向下移动
                self.player.move(3, self.dimension)
            if keys[pygame.K_a]:  # 向左移动
                self.player.move(2, self.dimension)
            if keys[pygame.K_d]:  # 向右移动
                self.player.move(1, self.dimension)
            if keys[pygame.K_f] or keys[pygame.K_b]:
                nearest = self.dimension.nearest_entity(self.player.get_pos())
                if nearest.is_nearby(self.player):
                    if keys[pygame.K_f]:
                        nearest.on_interact(self.player)
                    if keys[pygame.K_b]:
                        nearest.on_battle(self.player)

            # 踩岩浆扣血
            # for k in range(50):
            #     if (dimension.get_block_from_pos((player.x + k, player.y + k)) == Blocks.LAVA or
            #             dimension.get_block_from_pos((player.x + 50 - k, player.y + k)) == Blocks.LAVA):
            #         player.hp -= 1 / 90
            # player.hp = max(0, player.hp)
            self.player.tick(self.dimension)
            for i in animation.get_all_animations():
                i.tick()
            for i in self.dimension.entities:
                if i.hp <= 0:
                    self.dimension.entities.remove(i)
                    del i
                else:
                    i.tick(self.dimension, self.player)

            # 更新摄像机位置
            self.camera = self.player.get_camera(self.dimension.get_render_size())

            if self.player.hp <= 0:
                config.SOUNDS['player_death'].play()
                self.open_death_ui()

            self.tick_counter = (self.tick_counter + 1) % 90
            if self.tick_counter == 0:
                self.tick_second()

            self.current_hud.tick(keys, events)
            self.current_hud.render(self.screen)
        else:
            self.current_ui.render(self.screen)
            if not self.current_ui.tick(pygame.key.get_pressed(), events):
                self.close_ui()
