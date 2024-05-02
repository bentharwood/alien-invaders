import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship and get its rect
        self.image = pg.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #store a decimal value for the rockets horizontal and vertical positions.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #movemnet flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """update the ships position based on movement flags"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.rocket_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.rocket_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.setting.rocket_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.setting.rocket_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """center the ship on screen"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.x)
