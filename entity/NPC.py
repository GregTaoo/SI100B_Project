import random
from typing import Tuple

import pygame

import AIHelper
import Config
import I18n
from render import Renderer, Particle
from ui.BattleUI import BattleUI
from ui.TradeUI import TradeUI
from entity import Entity


class NPC(Entity.Entity):

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer):
        # 初始化 NPC，设置名字、位置和渲染器。
        super().__init__(name, pos, renderer)
        self.dialog_timer = 0  # 对话计时器，用于控制对话显示的持续时间。
        self.hp = self.max_hp = 11451419198101212  # 设置 NPC 的生命值。
        self.battle = False  # 标记 NPC 是否参与战斗。
        self.interact = True  # 标记 NPC 是否可互动。

    def dialog(self):
        # 表示 NPC 的对话。
        return I18n.text('npc_dialog').format(self.name)

    def tick(self, dimension, player=None):
        # 每一帧更新 NPC 状态。
        super().tick(dimension, player)
        if self.is_nearby(player, 2):  # 检查玩家是否在 NPC 附近（范围为 2）。
            self.start_dialog(270)  # 启动对话，持续时间为 270 帧。
        if self.dialog_timer > 0:
            self.dialog_timer -= 1

    def start_dialog(self, duration):
        # 启动对话并设置对话持续时间。
        self.dialog_timer = duration

    def render(self, layers: list[pygame.Surface], camera: Tuple[int, int]):
        # 渲染对话框到屏幕上。
        super().render(layers, camera)
        self.render_dialog(layers[1], camera)  # 如果有对话，绘制对话框。

    def render_dialog(self, screen, camera):
        # 如果对话计时器大于 0，则渲染对话框。
        dialog_text = self.dialog()
        if self.dialog_timer > 0 and len(dialog_text) > 0:
            Entity.render_dialog_at_absolute_pos(dialog_text, screen,
                                                 (self.x - camera[0] + self.size[0] // 2,
                                                  self.y - camera[1] - 40),
                                                 Config.FONT)

    def on_battle(self, player):
        pass


class TraderNPC(NPC):

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer, trade_list=None):
        # 初始化 TraderNPC，设置名称、位置、渲染器以及可交易的物品列表（默认为空列表）。
        super().__init__(name, pos, renderer)
        self.trade_list = trade_list if trade_list is not None else []

    def on_interact(self, player):
        # 处理玩家与 TraderNPC 的互动。
        AIHelper.add_event(f'player interacted with {self.name}')  # 记录互动事件。
        Config.CLIENT.open_ui(TradeUI(player, self))  # 打开交易界面。


class VillagerNPC(TraderNPC):
    # VillagerNPC 是 TraderNPC 的子类，代表一个村民 NPC，村民可以进行交易和战斗。

    def __init__(self, pos):
        # 初始化 VillagerNPC，设置其名称、渲染器和交易选项。
        super().__init__(I18n.text('villager'), pos, Renderer.image_renderer('entities/villager.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.literal("购买"), 999, lambda player, npc, opt: print("购买")),
                             TradeOption(I18n.literal("购买1"), 1099, lambda player, npc, opt: print("购买1")),
                             TradeOption(I18n.literal("购买2"), 1990, lambda player, npc, opt: print("购买2")),
                         ])
        self.battle = True  # 启用战斗模式。

    def tick(self, dimension, player=None):
        super().tick(dimension, player)
        if self.is_nearby(player, 4) and random.randint(0, 180) == 0:
            x = self.x + random.randint(0, 50)
            y = self.y + random.randint(0, 50)
            Particle.ENV_PARTICLES.add(Particle.GlintParticle((x, y), 90))

    def on_battle(self, player):
        # 当玩家与村民 NPC 战斗时触发。
        for trade in self.trade_list:
            trade.price *= 2  # 将所有交易选项的价格加倍。
        # 召唤一个铁傀儡来与玩家战斗。
        iron_golem = Entity.Entity(I18n.text('iron_golem'), self.get_right_bottom_pos(),
                                   Renderer.image_renderer('entities/iron_golem.png', (50, 50)), atk=8, sp=3)
        Config.CLIENT.spawn_entity(iron_golem)  # 生成铁傀儡。
        Config.CLIENT.open_ui(BattleUI(player, iron_golem))  # 打开战斗界面。


class MedicineTraderNPC(TraderNPC):
    # MedicineTraderNPC代表一个药剂商 NPC，可以出售药品和增强物品。

    def __init__(self, pos):
        # 初始化 MedicineTraderNPC，设置其名称、渲染器和交易选项。
        super().__init__(I18n.text('witch'), pos, Renderer.image_renderer('entities/witch.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.literal("锻炼"), 10, self.buy_1),
                             TradeOption(I18n.literal("健身"), 20, self.buy_2),
                             TradeOption(I18n.literal("test"), 1, self.buy_3),
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        # 购买选项 1，增加玩家最大生命值 50。
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')  # 如果玩家的金币不足，返回提示信息。
        player.max_hp += 50  # 增加最大生命值 50。
        player.coins -= opt.price  # 扣除玩家金币。
        return I18n.literal("效果显著，增加50体力上限")

    @staticmethod
    def buy_2(player, npc, opt):
        # 购买选项 2，增加玩家最大生命值 50。
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')  # 如果玩家金币不足，返回提示信息。
        player.max_hp *= 2
        player.hp *= 2
        player.coins -= opt.price  # 扣除玩家金币。
        return I18n.literal("十分强大的，发生了一些变化")

    @staticmethod
    def buy_3(player, npc, opt):
        # 购买选项 3，玩家发生随机变化
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        rd = random.randint(-50, 100)
        player.max_hp += rd
        player.hp += rd
        player.coins -= opt.price
        return I18n.literal("发生了一些神秘变化")




class WeaponTraderNPC(TraderNPC):
    # WeaponTraderNPC，代表一个武器商 NPC，出售各种武器给玩家。

    def __init__(self, pos):
        # 初始化 WeaponTraderNPC，设置其名称、渲染器和交易选项。
        super().__init__(I18n.text('weapon_trader'), pos,
                         Renderer.image_renderer('entities/weapon_trader.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('charged_fist'), 10, self.buy_1),
                             TradeOption(I18n.text('iron_sword'), 10, self.buy_2),
                             TradeOption(I18n.text("infinite_sword"), 10, self.buy_3),
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        # 购买选项 1，增加玩家暴击几率 0.15。
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')  # 如果玩家金币不足，返回提示信息。
        player.crt += 0.15  # 增加暴击几率。
        player.coins -= opt.price  # 扣除玩家金币。
        return I18n.literal(I18n.text('bought').format(I18n.text('charged_fist')))

    @staticmethod
    def buy_2(player, npc, opt):
        # 购买选项 2，增加玩家攻击力 0.1。
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')  # 如果玩家金币不足，返回提示信息。
        player.atk += 0.1  # 增加攻击力。
        player.coins -= opt.price  # 扣除玩家金币。
        return I18n.literal(I18n.text('bought').format(I18n.text('iron_sword')))

    @staticmethod
    def buy_3(player, npc, opt):
        # 购买选项 3，增加玩家暴击伤害 0.25，但要求玩家拥有至少 1 个铁矿石。
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')  # 如果玩家金币不足，返回提示信息。
        if player.iron < 1:  # 检查玩家是否有至少 1 个铁矿石。
            return I18n.text("no_iron")
        player.crt_damage += 0.25

        player.coins -= opt.price
        return I18n.literal(I18n.text('bought').format(I18n.text('infinite_sword')))


class TradeOption:
    # TradeOption代表交易选择，物品名字和价格
    def __init__(self, name: I18n.Text, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade  # 是否在售
        self.available = True  # 是否可获得
