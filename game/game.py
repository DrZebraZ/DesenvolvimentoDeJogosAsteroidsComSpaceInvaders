import pygame
import random

from pygame.math import Vector2

from models import Asteroid, Spaceship, EnemySpaceship, BuffBullet, Bomb, Missile, Explosion, CentipedeHead, CentipedeBody
from utils import get_random_position, load_sprite, print_text, print_life


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    round = 1
    buff = 0
    checkpoint = 0
    missilesInv = []
    iventory = []
    timer = 0
    centipedeTimer = 0
    centipedeNextDirection = 0
    centipedeAsset = 1
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
        self.centipede = []
        self.bullets = []
        self.enemyBullets = []
        self.enemys = []
        self.buffs = []
        self.items = []
        self.missiles = []
        self.bullet2 = []
        self.explosion = []
        self.spaceship = Spaceship((400, 300), self.bullets.append, self.bullet2.append)
        
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
            
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT):
                if len(self.missilesInv) > 0:                    
                    self.missilesInv.remove(self.missilesInv[len(self.missilesInv)-1])
                    self.spaceship.missileShoot()

            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL):
                if len(self.iventory) > 0:                    
                    self.iventory.remove(self.iventory[len(self.iventory)-1])
                    self.explosion.append(Explosion(self.spaceship.position, self.explosion.append))
            
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
        if self.centipede:
            if self.timer%5==0:
                for centip in self.centipede:
                    if centip:
                        centip.changeSprite(self.centipedeAsset)
                if self.centipedeAsset==3:
                    self.centipedeAsset= 1
                else:
                    self.centipedeAsset+=1
            if self.centipedeTimer==0:
                self.centipedeNextDirection = random.randint(0,1)
                
            for i in range(0, len(self.centipede)):
                if i*10==self.centipedeTimer:
                    if self.centipede[i]:
                        self.centipede[i].changeClockwise(self.centipedeNextDirection)
                    else:
                        self.centipedeNextDirection = random.randint(0,1)
                else:
                    if self.centipede[i]:
                        self.centipede[i].changeClockwise(-1)
            
            self.centipedeTimer+=1
            if self.centipedeTimer>=(len(self.centipede)*10)+1:
                self.centipedeTimer=0
            
        if self.timer == 120:
            self.timer = 0
            for explode in self.explosion:
                self.explosion.remove(explode)
                    
        for game_object in self._get_game_objects():
            if game_object:
                game_object.move(self.screen)
        
        
        for centi in self.centipede:
            if centi and self.spaceship:
                if centi.collides_with(self.spaceship):
                    self._remove_life()
                    if not self.spaceship:
                        self.message = "You Lost press Z to restart!"
                        break
            
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
                
        for item in self.items[:]:
            if self.spaceship:
                if self.spaceship.collides_with(item):
                    if len(self.iventory)<4:
                        x = len(self.iventory)
                        x = 50*x
                        self.iventory.append(Bomb((750,550-x), self.iventory.append))
                        self.items.remove(item)
                        
        for item in self.missiles[:]:
            if self.spaceship:
                if self.spaceship.collides_with(item):
                    if len(self.missilesInv)<4:
                        x = len(self.missilesInv)
                        x = 50*x
                        self.missilesInv.append(Missile((680,550-x), self.missilesInv.append))
                        self.missiles.remove(item)
                
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
            if self.centipede:
                for i in range(len(self.centipede)):
                    if bullet in self.bullets[:] and self.centipede[i] and self.spaceship:
                        if bullet.collides_with(self.centipede[i]):
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            if self.centipede[i].getType() == 'HEAD':
                                aux = i
                                while(self.centipede[aux]):
                                    aux+=1
                                self.centipede.pop(aux-1)
                                self.spaceship.LIFE+=10
                            else:
                                if len(self.centipede) < 60:
                                    position = self.centipede[i].position
                                    self.centipede.append(CentipedeHead(position))
                                    self.centipede.append(CentipedeBody(Vector2(position.x, position.y+30)))
                                    self.centipede.append(CentipedeBody(Vector2(position.x, position.y+60)))
                                    self.centipede.append(None)
            
        for bullet in self.bullet2[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.explosion.append(Explosion(bullet.position, self.explosion.append))
                    self.bullet2.remove(bullet)
                    break     
            if bullet in self.bullet2[:]:
                for enemy in self.enemys[:]:
                    if enemy.collides_with(bullet):
                        self.explosion.append(Explosion(bullet.position, self.explosion.append))
                        self.bullet2.remove(bullet)
                        break
        
        for explode in self.explosion[:]:
            for enemy in self.enemys[:]:
                if enemy.collides_with(explode):
                    self.enemys.remove(enemy)
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(explode):
                    self.asteroids.remove(asteroid)
            for bullet in self.enemyBullets[:]:
                if bullet.collides_with(explode):
                    self.enemyBullets.remove(bullet)
                    
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
        
        for bullet in self.bullet2[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullet2.remove(bullet)
        
        for bullet in self.enemyBullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.enemyBullets.remove(bullet)                        
            
        print(self.centipede)
        if not self.asteroids and not self.enemys and self.spaceship and len(self.centipede)<2:
            if self.round == 1:
                self.level2()
            elif self.round == 2:
                self.level3()
            elif self.round == 3:
                self.level4()
            elif self.round == 4:
                self.level5()
            elif self.round == 5:
                self.level6()
            elif self.round == 6:
                self.level7()
            elif self.round == 7:
                self.level8()
            elif self.round == 8:
                self.level9()
            elif self.round == 9:
                self.level10()
            elif self.round == 10:
                self.levelBOSS1()
            elif self.round == 11:
                self.levelBOSS2()
            elif self.round == 12:
                self.message = 'YOU WIN!'
        self.timer += 1
        
    def level1(self):
        self.levelBOSS1()
        # self.rount=1
        # for _ in range(4):
        #     while True:
        #         position = get_random_position(self.screen)
        #         if (
        #             position.distance_to(self.spaceship.position)
        #             > self.MIN_ASTEROID_DISTANCE
        #         ):
        #             break
            
        #     self.asteroids.append(Asteroid(position, self.asteroids.append, 1))
        
        # if len(self.missilesInv)<2:
        #     for _ in range(2-len(self.missilesInv)):
        #         while True:
        #             position = get_random_position(self.screen)
        #             if (
        #                 position.distance_to(self.spaceship.position)
        #                 > self.MIN_ASTEROID_DISTANCE
        #             ):
        #                 break
        #         self.missiles.append(Missile(position, self.missiles.append))
        
        # if len(self.iventory)<2:
        #     for _ in range(2-len(self.iventory)):
        #         while True:
        #             position = get_random_position(self.screen)
        #             if (
        #                 position.distance_to(self.spaceship.position)
        #                 > self.MIN_ASTEROID_DISTANCE
        #             ):
        #                 break
        #         self.items.append(Bomb(position, self.items.append))
            
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
        
        if len(self.missilesInv)<2:
            for _ in range(4-len(self.missilesInv)):
                while True:
                    position = get_random_position(self.screen)
                    if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                    ):
                        break
                self.missiles.append(Missile(position, self.missiles.append))
        
        if len(self.iventory)<2:
            for _ in range(4-len(self.iventory)):
                while True:
                    position = get_random_position(self.screen)
                    if (
                        position.distance_to(self.spaceship.position)
                        > self.MIN_ASTEROID_DISTANCE
                    ):
                        break
                self.items.append(Bomb(position, self.items.append))
        
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
        
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.missiles.append(Missile(position, self.missiles.append))
        
        for _ in range(2):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.items.append(Bomb(position, self.items.append))
    
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
    
    def levelBOSS1(self):
        self.round=11
        self.spaceship.LIFE = 100
        while True:
            position = get_random_position(self.screen)
            if (
                position.distance_to(self.spaceship.position)
                > self.MIN_ASTEROID_DISTANCE
            ):
                break
        self.centipede.append(CentipedeHead(position))
        for i in range(1,4):
            self.centipede.append(CentipedeBody(Vector2(position.x, position.y+i*30)))
        self.centipede.append(False)
    
    def levelBOSS2(self):
        self.round=12
        for _ in range(0,4):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.centipede.append(CentipedeHead(position))
            for i in range(1,4):
                self.centipede.append(CentipedeBody(Vector2(position.x, position.y+i*30)))
            self.centipede.append(False)
    
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        
        for game_object in self._get_game_objects():
            if game_object:
                game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
        
        if self.spaceship:
            print_life(self.screen, "Life = "+str(self.spaceship.LIFE), self.font)

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.buffs, *self.iventory, *self.items, *self.enemys, *self.asteroids, *self.bullets, *self.enemyBullets, *self.bullet2, *self.missiles, *self.missilesInv, *self.explosion, *self.explosion, *self.centipede]

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
    