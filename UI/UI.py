import pygame


class UI:

    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def tick(self, keys, events):
        for button in self.buttons:
            button.tick(events)
        return False

    @staticmethod
    # Copilot 写的
    def blur_background(screen: pygame.Surface):
        surface = pygame.Surface(screen.get_size())
        surface.blit(screen, (0, 0))
        for _ in range(5):  # Adjust the range for more/less blur
            surface = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
            surface = pygame.transform.smoothscale(surface, screen.get_size())
        dark_overlay = pygame.Surface(screen.get_size())
        dark_overlay.fill((0, 0, 0))
        dark_overlay.set_alpha(150)  # Adjust the alpha value for more/less darkness
        surface.blit(dark_overlay, (0, 0))
        screen.blit(surface, (0, 0))

    def render(self, screen: pygame.Surface):
        self.blur_background(screen)
        for button in self.buttons:
            button.render(screen)

    def on_close(self):
        pass
