import sys
from time import sleep
import pygame as pg
from settings_class import settings
from game_stats_class import gamestats
from ship_class import Ship
from bullet_class import bullet
from aliens_class import Alien
from button_class import Button
from scoreboard_class import Scoreboard

class alienInvasion:
    """overall class to manage game assets and behavior"""

    def __init__(self):
        """initialize the game and create game resources"""
        pg.init()
        self.clock = pg.time.Clock()
        self.settings = settings()

        self.screen = pg.display.set_mode((
            self.settings.screen_width, self.settings.screen_height
        ))
        pg.display.set_caption("Alien Invasion")
        self.stats = gamestats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()
        #start alien invasion in active state
        self.game_active = False

        #make the play button
        self.play_button = Button(self, 'play')


    def run_game(self):
        """start game loop"""
        while True:
            self._check_events()
            if self.game_active:
              self.ship.update()
              self._update_bullets()
              self._update_aliens()
              
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """respond to keypress and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
               self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """start new game when the player clicks the button"""
        button_clicked =  self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.settings.initialize_dynamic_settings()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pg.mouse.set_visible(False)
            self.game_active = True
            self.sb.prep_ships()
            self.sb.prep_level()

    def _check_keydown_events(self, event): 
        """Respond to keypress"""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        if event.key == pg.K_UP:
            self.ship.moving_up = True
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False
        if event.key == pg.K_UP:
            self.ship.moving_up = False
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = False

    
    def _update_bullets(self):
        """manage bullets"""
        #update bullet position
        self.bullets.update()

        #get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        #check for bullets that have hit aliens
        collisions = pg.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if not self.aliens:
            #destroy bullets create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

        if collisions:
            for aliens in collisions.values():
              self.stats.score += self.settings.alien_points * len(aliens)
              self.sb.check_high_score()
            self.sb.prep_score()
            self.sb.prep_level()


    def _update_screen(self):
        """update images on the screen and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        pg.display.flip()

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = bullet(self)
            self.bullets.add(new_bullet) 

    
    def _create_fleet(self):
        """create the fleet of aliens"""
        #create an alien and keep adding aliens until there no room left.
        #space between aliens is one aliens width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
          while current_x < (self.settings.screen_width - 2 * alien_width):
            self._create_alien(current_x, current_y)
            current_x += 2 * alien_width
          #finished a row; reset x value increment y value
          current_x = alien_width
          current_y += 2 * alien_height
        self.aliens.add(alien)


    def _create_alien(self, x_position, y_position):
        """create an alien and place it on the row"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens hitting the bottom of the screen
        self._check_aliens_bottom() 
        

    def _check_fleet_edges(self):
        """respond if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
    def _ship_hit(self):
        """responds to the ship being hit by an alien"""
        if self.stats.ships_left >= 0:
          #decrease number of ships left
          self.stats.ships_left -= 1
          self.sb.prep_ships()

          #get rid of any remaining bullets and aliens
          self.bullets.empty()
          self.aliens.empty()

          #new fleet and center the fleet 
          self._create_fleet()
          self.ship.center_ship()
          #pause
          sleep(0.5)
        else:
            self.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #treat this the same as if the ship got hit
                self._ship_hit()
                break

if __name__ == '__main__':
    #make a game instance and run the game
    ai = alienInvasion()
    ai.run_game()