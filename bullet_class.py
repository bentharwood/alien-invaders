import pygame
from pygame.sprite import Sprite

class bullet(Sprite):
    """A class to manage bullets"""

    def __init__(self, ai_game):
        """create a bullet object at the ships current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create a bullet rect at 0, 0 and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullets position as a float
        self.y = float(self.rect.y)

    def update(self):
        """"move the bullet up the screen"""
        #update the position of the bullet
        self.y -= self.settings.bullet_speed
        #update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    