import pygame

import I18n
import Config
from Dialog import Dialog
from entity.NPC import NPC
from render import Renderer
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton


class DialogUI(UI):

    def __init__(self, npc: NPC, dialogs: Dialog, after_dialog):
        super().__init__()
        self.npc = npc
        self.dialogs = dialogs
        self.after_dialog = after_dialog
        self.npc_text = I18n.text(self.dialogs.current['npc']).get()
        self.options = self.dialogs.current['player']
        self.typing_index = 1
        Config.CLOCKS.append((10, self.typer_animate))

    def on_close(self):
        Config.CLOCKS.remove((15, self.typer_animate))
        super().on_close()

    def typer_animate(self):
        self.typing_index = min(len(self.npc_text), self.typing_index + 1)
        if self.typing_index == len(self.npc_text) - 1:
            self.update_buttons(self.options)

    def update_buttons(self, options):
        for i, option in enumerate(options):
            self.add_button(ClassicButton(I18n.text(option['str']),
                                          (Config.SCREEN_WIDTH // 2 - 150, Config.SCREEN_HEIGHT // 2 + 10 + i * 50),
                                          (300, 45), (0, 0, 0, 150), (255, 255, 255),
                                          lambda index=i: self.next_dialog(index), (0, 0, 0, 150),
                                          (0, 0, 0, 200), (255, 255, 255), border_radius=1))

    def next_dialog(self, choice: int):
        nxt = self.dialogs.next(choice)
        if isinstance(nxt, str):
            self.after_dialog(nxt)
            return
        self.options = nxt['player']
        self.buttons.clear()
        self.npc_text = I18n.text(self.dialogs.current['npc']).get()
        self.typing_index = 1

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render(self.npc_text[:self.typing_index], True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 75))
        Config.CLIENT.player.render_at_absolute_pos(screen, (20, Config.SCREEN_HEIGHT - 70), False, False)
        self.npc.render_at_absolute_pos(screen, (Config.SCREEN_WIDTH - 70, 20), True, False)

    def tick(self, keys, events):
        super().tick(keys, events)
        Renderer.PLAYER.tick()
        return True
