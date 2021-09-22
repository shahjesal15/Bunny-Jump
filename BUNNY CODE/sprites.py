# SPRITE CLASSES FOR PLATFORMER GAME

import pygame
from settings import *
from random import choice, randrange
from math import sin

vec = pygame.math.Vector2

# ADDING THE GROUPS TO THE SPRITES SUPER CLASS MAKES IT THE MEMBER OF THE GROUP INTERNALLY

class SpriteSheet:

	# UTILIY CLASS FOR LOADING AND PARSING THE SPRITESHEETS
	def __init__(self, filename):
		self.spritesheet = pygame.image.load(filename).convert()

	def get_image(self, x, y, width, height, scale=(55, 85)):
		# GRAB AN IMAGE OUT OF THE LARGE SPRITESHEET
		image = pygame.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		if not scale is None:
			image = pygame.transform.scale(image, scale)
		return image

class Player(pygame.sprite.Sprite):
	def __init__(self, game):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.player = self.game.player
		self.load_images()
		self.image = self.standing_frames[0]
		self.rect = self.image.get_rect()
		self.walking = False
		self.jumping = False
		self.current_frame = 0
		self.last_update = 0	
		self.image.set_colorkey(BLACK)
		self.rect.center = (40, HEIGHT - 100)
		self.pos = vec(WIDTH / 2, HEIGHT / 2)
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
	
	def load_images(self):
		self.standing_frames = [
			self.game.spritesheet.get_image(*self.player['standing'][0]),
			self.game.spritesheet.get_image(*self.player['standing'][1])
		]
		self.walk_frames_r = [
			self.game.spritesheet.get_image(*self.player['walking'][0]),
			self.game.spritesheet.get_image(*self.player['walking'][1])
		]
		self.walk_frames_l = [
			pygame.transform.flip(image, True, False) for image in self.walk_frames_r
		]
		for index in range(0,2):
			self.standing_frames[index].set_colorkey(BLACK)
			self.walk_frames_r[index].set_colorkey(BLACK)
			self.walk_frames_l[index].set_colorkey(BLACK)

		self.jump_frame = self.game.spritesheet.get_image(*self.player['jump'][0])
		self.hurt_frame = self.game.spritesheet.get_image(*self.player['hurt'][0])
		self.jump_frame.set_colorkey(BLACK)
		self.hurt_frame.set_colorkey(BLACK)
	
	def animate(self):
		now = pygame.time.get_ticks()
		
		if self.vel.x != 0:
			self.walking = True
		else:
			self.walking = False

		if self.walking:
			if now - self.last_update > 300:
				self.last_update = now 
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				bottom = self.rect.bottom
				if self.vel.x > 0:
					self.image = self.walk_frames_r[self.current_frame]
				else:
					self.image = self.walk_frames_l[self.current_frame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom	


		if not self.jumping and not self.walking:
			if now - self.last_update > 300:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				self.image = self.standing_frames[self.current_frame]
				bottom = self.rect.bottom
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

	def jump_cut(self):
		if self.jumping:
			if self.vel.y < -3:
				self.vel.y = -3

	def jump(self):
		self.rect.x += 2
		hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
		self.rect.x -= 2
		if hits and not self.jumping:
			self.game.jump_sound.play()
			self.jumping = True
			self.vel.y = -PLAYER_JUMP

	def dead_meat(self):
		center = self.rect.center
		self.vel.y = -25
		self.image = self.hurt_frame
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.game.playing = False

	def update(self):
		self.animate()
		self.acc = vec(0, PLAYER_GRAV)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.acc.x = -PLAYER_ACC
		if keys[pygame.K_RIGHT]:
			self.acc.x = PLAYER_ACC

		# APPLY FRICTION
		self.acc.x += self.vel.x * PLAYER_FRICTION
		# EQUATIONS OF MOTION
		self.vel += self.acc
		if abs(self.vel.x) < 0.1:
			self.vel.x = 0
		self.pos += self.vel + 0.5 * self.acc
		# 	WRAP THE SIDES OF THE SCREEN
		if self.pos.x > WIDTH + self.rect.width / 2:
			self.pos.x = 0 - self.rect.width / 2
		if self.pos.x < 0 - self.rect.width / 2:
			self.pos.x = WIDTH + self.rect.width / 2

		self.rect.midbottom = self.pos
		self.mask = pygame.mask.from_surface(self.image)

class Platform(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLATFORM_LAYER
		self.groups = game.all_sprites, game.platforms
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = [
			self.game.spritesheet.get_image(*PLATFORMS[self.game.environment][0], scale=(200, 55)),
			self.game.spritesheet.get_image(*PLATFORMS[self.game.environment][1], scale=(140, 55))
		]
		self.image = choice(self.image)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		if randrange(100) < POWER_SPAWN_PERCENT:
			PowerUp(self.game, self)

class PowerUp(pygame.sprite.Sprite):
	def __init__(self, game, platform):
		self._layer = POWERUP_LAYER
		self.groups = game.all_sprites, game.powerups
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.platform = platform
		self.image = self.game.spritesheet.get_image(820, 1805, 71, 70)
		self.image = pygame.transform.scale(self.image, (30, 30))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.platform.rect.centerx - 10
		self.rect.bottom = self.platform.rect.top - 5

	def update(self):
		self.rect.bottom = self.platform.rect.top - 5
		if not self.game.platforms.has(self.platform):
			self.kill()

class Mob(pygame.sprite.Sprite):
	def __init__(self, game):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image_set = [self.game.spritesheet.get_image(566, 510, 122, 139),
					self.game.spritesheet.get_image(568, 1534, 122, 135)
		]
		for index, image in enumerate(self.image_set):
			self.image_set[index] = pygame.transform.scale(image, (60,60))
			self.image_set[index].set_colorkey(BLACK)

		self.image = self.image_set[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = choice([-100, WIDTH + 100])
		self.vx = randrange(1, 4)
		if self.rect.centerx > WIDTH:
			self.vx *= -1
		self.rect.y = randrange(HEIGHT / 2)
		self.vy = 0
		self.dy = 0.5

	def update(self):
		self.rect.x += self.vx
		self.vy += self.dy
		if self.vy > 3 or self.vy < -3:
			self.dy *= -1
		center = self.rect.center
		if self.dy < 0:
			self.image = self.image_set[0]
		else:
			self.image = self.image_set[1]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.rect.y += self.vy
		self.mask = pygame.mask.from_surface(self.image)
		if self.rect.left >  WIDTH + 100 or self.rect.right < -100:
			self.kill()

class Clouds(pygame.sprite.Sprite):
	"""docstring for Clouds"""
	def __init__(self, game):
		self._layer = CLOUDS_LAYER
		self.groups = game.all_sprites, game.clouds
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = choice(game.cloud_images)
		self.rect = self.image.get_rect()
		self.image.set_colorkey(BLACK)
		scale = randrange(50, 100) / 100
		self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
		 int(self.rect.height * scale)))
		self.rect.x = randrange(WIDTH - self.rect.width)
		self.rect.y = randrange(-500, -50)

	def update(self):
		if self.rect.top > HEIGHT * 2:
			self.kill()

class SnowFlake(pygame.sprite.Sprite):
	def __init__(self, game):
		self._layer = ANIMATED_BACKGROUND
		self.groups = game.all_sprites, game.snowflakes
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image_original = self.game.snowflake
		self.image = self.image_original.copy()
		self.rect = self.image.get_rect()
		self.vy = 1
		self.vx =  randrange(-1, 2)
		self.rotate_timer = 0
		self.rot = 0
		self.rot_speed = 5

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.rotate_timer > 50:
			self.rot = (self.rot + self.rot_speed) % 360
			center = self.rect.center
			self.image = pygame.transform.rotate(self.image_original, self.rot)
			self.rect = self.image.get_rect()
			self.rect.center = center
			self.rotate_timer = now
		
	def update(self):
		self.rotate()
		self.rect.y += self.vy
		self.rect.x += self.vx
		if self.rect.x >= WIDTH - 25 or self.rect.x <= -25:
			self.rect.y = -10
		if self.rect.y >= HEIGHT:
			self.kill()

class RainDrop(pygame.sprite.Sprite):
	def __init__(self, game):
		self._layer = ANIMATED_BACKGROUND
		self.groups = game.all_sprites, game.raindrops
		self.game = game
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = self.game.raindrop
		self.image = pygame.transform.rotate(self.image, 6)
		self.rect = self.image.get_rect()
		self.vy = randrange(1, 3)

	def update(self):
		self.rect.y += self.vy
		if self.rect.y >= HEIGHT:
			self.kill()
