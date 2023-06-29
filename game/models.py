from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import get_random_velocity, load_sound, load_sprite, wrap_position

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class CentipedeBody(GameObject):
    CLOCKWISE = 0
    CLOCKWISENUM = 0
    MANEUVERABILITY = 45
    ACCELERATION = 3
    
    def __init__(self, position):
        self.spriteName = "head1.png"
        self.velocity = 3
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite(self.spriteName), Vector2(0,-1))
        
    def rotate(self):
        angle = self.MANEUVERABILITY * self.CLOCKWISE
        self.direction.rotate_ip(angle)
        self.velocity = self.direction * self.ACCELERATION
        
    def changeSprite(self, num):
        super().__init__(self.position, load_sprite(self.spriteName), self.velocity)
        if num ==1:
            self.spriteName="body1.png"
        elif num == 2:
            self.spriteName="body2.png"
        else:
            self.spriteName="body3.png"
            
    def getClockwise(self):
        return self.CLOCKWISENUM
    
    def getType(self):
        return 'BODY'
    
    def changeClockwise(self, num):
        if num == -1:
            self.CLOCKWISENUM = -1
            self.CLOCKWISE = 0
        elif num == 1:
            self.CLOCKWISENUM = 1
            self.CLOCKWISE = 1
        elif num == 0:
            self.CLOCKWISENUM = 0
            self.CLOCKWISE = -1
            
    def draw(self, surface):
        self.rotate()
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class CentipedeHead(GameObject):
    CLOCKWISE = 0
    CLOCKWISENUM = 0
    MANEUVERABILITY = 45
    ACCELERATION = 3
    
    def __init__(self, position):
        self.spriteName = "head1.png"
        self.velocity = 3
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite(self.spriteName), Vector2(0,-1))
    
    def rotate(self):
        angle = self.MANEUVERABILITY * self.CLOCKWISE
        self.direction.rotate_ip(angle)
        self.velocity = self.direction * self.ACCELERATION
        
    def getType(self):
        return 'HEAD'
        
    def changeSprite(self, num):
        super().__init__(self.position, load_sprite(self.spriteName), self.velocity)
        if num ==1:
            self.spriteName="head1.png"
        elif num == 2:
            self.spriteName="head2.png"
        else:
            self.spriteName="head3.png"
    
    def getClockwise(self):
        return self.CLOCKWISENUM
    
    def changeClockwise(self, num):
        if num == -1:
            self.CLOCKWISENUM = -1
            self.CLOCKWISE = 0
        elif num == 1:
            self.CLOCKWISENUM = 1
            self.CLOCKWISE = 1
        elif num == 0:
            self.CLOCKWISENUM = 0
            self.CLOCKWISE = -1
            
    def draw(self, surface):
        self.rotate()
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class EnemySpaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.10
    BULLET_SPEED = 2
    CLOCKWISE = True
    ACCELERATEDTIMES = 0
    
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("enemy.png"), Vector2(1))

    def changeClockwise(self):
        if self.CLOCKWISE:
            self.CLOCKWISE = False
        else:
            self.CLOCKWISE = True
            
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.ACCELERATEDTIMES += 1
        self.velocity += self.direction * self.ACCELERATION
        if self.ACCELERATEDTIMES > 5:
            self.velocity = self.direction * self.ACCELERATION * 10
        if self.ACCELERATEDTIMES > 10:
            self.ACCELERATEDTIMES=0
            self.velocity = Vector2(0)
        
    def draw(self, surface):
        self.rotate(clockwise=self.CLOCKWISE)
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = BulletEnemy(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        #self.laser_sound.play()


class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=1):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size

        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("asteroid.png"), 0, scale)

        super().__init__(position, sprite, get_random_velocity(1, 2))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)
            
            
class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.15
    BULLET_SPEED = 4
    MISSILE_SPEED = 1
    LIFE = 3

    def __init__(self, position, create_bullet_callback, create_missile_callback):
        self.create_bullet_callback = create_bullet_callback
        self.create_missile_callback = create_missile_callback
        self.laser_sound = load_sound("laser")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)

        super().__init__(position, load_sprite("spaceship1.png"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
    
    def desaccelerate(self):
        self.velocity -= self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        #self.laser_sound.play()
        
    def missileShoot(self):
        missile_velocity = self.direction * self.MISSILE_SPEED + self.velocity
        missile = Bullet2(self.position, missile_velocity)
        self.create_missile_callback(missile)


class BuffBullet(GameObject):
    def __init__(self, position, create_buff_callback):
        self.create_buff_callback = create_buff_callback
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("minigun.png"), Vector2(0))

    def getBuff(self):
        return 1
    
class Bomb(GameObject):
    def __init__(self, position, create_item_callback):
        self.create_item_callback = create_item_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("bomb1.png"), Vector2(0))

class Explosion(GameObject):
    def __init__(self, position, create_explosion_callback):
        self.create_explosion_callback = create_explosion_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("explosion.png"), Vector2(0))

class Missile(GameObject):
    def __init__(self, position, create_item_callback):
        self.create_item_callback = create_item_callback
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("missile.png"), Vector2(0))

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet.png"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
        
class BulletEnemy(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bulletEnemy.png"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity



class Bullet2(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet2.png"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity
