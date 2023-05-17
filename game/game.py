import pygame
import random
import time

from models import Asteroid, Spaceship, EnemySpaceship, BuffBullet
from utils import get_random_position, load_sprite, print_text, print_life


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    round = 1
    buff = 0
    checkpoint = 0

    def __init__(self):
        self.start()
    
    def start(self):
        self.round = 1
        self.buff = 0
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 600))
        self.background = (load_sprite("space.png", False))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.enemyBullets = []
        self.enemys = []
        self.buffs = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)
        
        if self.checkpoint == 1:
            self.level5()
        elif self.checkpoint == 2:
            self.level9()
        else:
            self.level1()
            


    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Game")

    def _handle_input(self):
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
                
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spaceship.shoot()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and not self.spaceship:
                self.start()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.desaccelerate()

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self._remove_life()
                    self.asteroids.remove(asteroid)
                    if not self.spaceship:
                        self.message = "You Lost press Z to restart!"
                        break
                
        for buff in self.buffs[:]:
            if self.spaceship:
                if self.spaceship.collides_with(buff):
                    self.buff = buff.getBuff()
                    self.buffs.remove(buff)
                    break
                
        if self.buff == 1:
            if self.spaceship:
                self.spaceship.shoot()
        
        if self.enemys:
            for enemy in self.enemys:
                willacelerate = random.randint(0,5)
                shoot = random.randint(0,30)
                rotate = random.randint(0,40)
                if shoot==1:
                    enemy.shoot()
                if willacelerate==1:
                    enemy.accelerate()
                if rotate ==1:
                    enemy.changeClockwise()
        
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break     
            if bullet in self.bullets[:]:
                for enemy in self.enemys[:]:
                    if enemy.collides_with(bullet):
                        self.enemys.remove(enemy)
                        self.bullets.remove(bullet)
                        break
        if self.spaceship:
            for bullet in self.enemyBullets[:]:
                if bullet.collides_with(self.spaceship):
                    self._remove_life()
                    self.enemyBullets.remove(bullet)
                    if not self.spaceship:
                        self.message = "You Lost press Z to restart!"
                        break
                            
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)
        
        for bullet in self.enemyBullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.enemyBullets.remove(bullet)                        
            

        if not self.asteroids and self.round == 1 and self.spaceship:
            self.level2()
        if not self.asteroids and self.round == 2 and self.spaceship and not self.enemys:
            self.level3()
        if not self.asteroids and self.round == 3 and self.spaceship and not self.enemys:
            self.level4()
        if not self.asteroids and self.round == 4 and self.spaceship and not self.enemys:
            self.level5()
        if not self.asteroids and self.round == 5 and self.spaceship and not self.enemys:
            self.level6()
        if not self.asteroids and self.round == 6 and self.spaceship and not self.enemys:
            self.level7()
        if not self.asteroids and self.round == 7 and self.spaceship and not self.enemys:
            self.level8()
        if not self.asteroids and self.round == 8 and self.spaceship and not self.enemys:
            self.level9()
            
    def level1(self):
        self.rount=1
        for _ in range(4):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            
            self.asteroids.append(Asteroid(position, self.asteroids.append, 1))
            
    def level2(self):
        self.round = 2
        for _ in range(8):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, 1))
        while True:
            position = get_random_position(self.screen)
            if (
                position.distance_to(self.spaceship.position)
                > self.MIN_ASTEROID_DISTANCE+30
            ):
                break
        
    def level3(self):
        self.round = 3
        for _ in range(4):
            size = random.randint(1, 2)
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, size))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))

    def level4(self):
        self.round = 4
        for _ in range(3):
            size = random.randint(2,3)
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, size))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
        
    def level5(self):
        self.round = 5
        self.buffs.append(BuffBullet((400, 300), self.buffs.append))
        self.checkpoint=1
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
   
    def level6(self):
        self.round = 6
        for _ in range(5):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, 3))
            self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
    
    def level7(self):
        self.round = 7
        for _ in range(10):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, 3))
            self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
       
    def level8(self):
        self.round = 8
        for _ in range(20):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, 3))
            self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
           
    def level9(self):
        self.round=9
        self.checkpoints = 2
        self.buff = 0
        for _ in range(3):
            size = random.randint(2,3)
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, size))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))

    def level10(self):
        self.round=10
        for _ in range(3):
            size = random.randint(2,3)
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE+30
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append, size))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
        self.enemys.append(EnemySpaceship(position, self.enemyBullets.append))
    
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
        
        if self.spaceship:
            print_life(self.screen, "Life = "+str(self.spaceship.LIFE), self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets, *self.enemys, *self.enemyBullets, *self.buffs]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def _remove_life(self):
        self.spaceship.LIFE -= 1
        if self.spaceship.LIFE == 0:
            self.spaceship = None
            
def applybuff(self, value):
    if value==1:
        self.buff = 1
    