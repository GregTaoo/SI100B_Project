import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import TraderNPC, TradeOption, NPC
from render import Renderer
from ui.DialogUI import DialogUI
from ui.TradeUI import TradeUI


class NetherNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc1'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        # 玩家与NPC交互时触发
        if self.interact:
            # 打开对话框UI，调用process_choice方法处理玩家选择
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc1'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.NETHERITE_BLOCK)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.NETHERITE_BLOCK)
            return 'b2'
        else:
            return '!#'


class NetherNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc2'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((7, 11), Block.NETHERITE_BLOCK)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((8, 10), Block.NETHERITE_BLOCK)
            return 'b2'
        else:
            return '!#'


class NetherNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc3'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            return 'b1'
        else:
            return '!#'


class NetherNPC4(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc4'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc4_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc4_option2'), 0, self.buy_2)
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        # 玩家选择交易选项1时触发，关闭UI并返回购买成功的提示
        npc.interact = False
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        # 玩家选择交易选项2时触发，关闭UI并返回购买成功的提示
        npc.interact = False
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option2')))

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc5'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))
    
    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            return 'b1'
        else:
            return '!#'



class NetherNPC5(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc5'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc4_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc4_option2'), 0, self.buy_2)
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        # 玩家选择交易选项1时触发，关闭UI并返回购买成功的提示
        npc.interact = False
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        # 玩家选择交易选项2时触发，关闭UI并返回购买成功的提示
        npc.interact = False
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option2')))

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc5'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))
            
    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            return 'b1'
        else:
            return '!#'

