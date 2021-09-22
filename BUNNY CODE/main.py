import pygame
from random import randrange, choice
from settings import *
from sprites import *
from os import getcwd

class Game:
	def __init__(self):
		# INIT WINDOW AND ETC.

		# SETUP
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		
		# GAME CONTROL
		self.running = True	
		self.font_name = pygame.font.match_font(FONT_NAME)

		# PLAYER SETTINGS
		self.player = BUNNY[0]

		# FPS CLOCK
		self.clock = pygame.time.Clock()
		self.last_update = pygame.time.get_ticks()

		# LOAD DATA
		self.load_data()
		pygame.display.set_icon(self.gameIcon)

	def load_data(self):
		self.dir = getcwd()
		print(self.dir)
		try:
			with open(self.dir + HIGH_SCORE, 'r') as file:
				self.highscore = int(file.read())
		except:
			self.highscore = 0
		self.spritesheet = SpriteSheet(self.dir + SPRITE_SHEET)
		self.cloud_images = [pygame.image.load(self.dir + CLOUDS_IMAGE.format(x)).convert()\
		 for x in range(1,4)]
		self.jump_sound = pygame.mixer.Sound(self.dir + JUMP_SOUND)
		self.powerup_sound = pygame.mixer.Sound(self.dir + POWERUP_SOUND)
		self.hurt_sound = pygame.mixer.Sound(self.dir + HURT_SOUND)
		self.gameIcon = pygame.image.load(self.dir + GAME_ICON)
		self.raindrop = pygame.image.load(self.dir + RAINDROP)
		self.snowflake = pygame.image.load(self.dir + SNOWFLAKE)

	def save_data(self):
		if self.score > self.highscore:
			self.highscore = self.score
			with open(self.dir + HIGH_SCORE, 'w') as file:
				file.write(str(self.highscore))

	def init_groups(self):
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.platforms = pygame.sprite.Group()
		self.powerups = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		self.clouds = pygame.sprite.Group()
		self.snowflakes = pygame.sprite.Group()
		self.raindrops = pygame.sprite.Group()
		
	def new(self):
		if not self.running:
			return
		# NEW GAME
		self.score = 0
		self.mob_timer = 0
		self.decor_timer = 0
		self.environment = choice(["AFRICA","AFRICA","INDIA","JAPAN","EGYPT"])
		self.init_groups()
		# SPRITES
		self.player = Player(self)
		for platform in PLATFORM_LIST:
			Platform(self, *platform)	
		for index in range(8):
			cloud = Clouds(self)
			cloud.rect.y += 500
		self.all_sprites.add(self.player)
		self.run()

	def run(self):
		# ACTUAL GAMELOOPS
		pygame.mixer.music.load(self.dir + HAPPYTUNES_MUSIC)
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(loops=-1)
		self.playing = True	
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
		pygame.mixer.music.fadeout(500)

	def draw_text(self, text, size, x, y, color=WHITE):
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)

	def update(self):
		# TIME COLLISION
		now = pygame.time.get_ticks()
		# GAMELOOP UPDATE
		self.all_sprites.update()
		# SPAWN MOBS
		if now - self.mob_timer > MOB_FREQ + choice([-1000, 500, 0, 500, 1000]):
			Mob(self)
			self.mob_timer = now
		# CHECK IF PLAYER HITS THE PLATFORM ONLY IF FALLING
		if self.player.vel.y > 0:
			hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
			if hits:
				lowest = hits[0]
				for hit in hits:
					if lowest.rect.bottom > hit.rect.bottom:
						lowest = hit
				if self.player.pos.x < lowest.rect.right + 15 and \
					self.player.pos.x > lowest.rect.left - 15:
					if self.player.pos.y < lowest.rect.centery:			
						self.player.pos.y = hits[0].rect.top
						self.player.vel.y = 0
						self.player.jumping = False 

		# POWERUP COLLECTION
		powhit = pygame.sprite.spritecollide(self.player, self.powerups, True)
		if powhit:
			self.powerup_sound.play()
			self.player.vel.y = -POWERUP_BOOST
			self.player.jumping = False
			for hit in powhit:
				self.all_sprites.remove(hit)
				self.powerups.remove(hit)

		# MOBS COLLISION
		mobshit = pygame.sprite.spritecollide(self.player, self.mobs, False,
			pygame.sprite.collide_mask)
		if mobshit:
			self.hurt_sound.play()
			self.player.dead_meat()
		# IF PLAYER REACHES TOP 1/4 OF THE SCREEN
		if self.player.rect.top <= HEIGHT / 4:
			# SPAWING A CLOUD
			if randrange(100) < 4:
				Clouds(self)
			self.player.pos.y += max(abs(self.player.vel.y), 4)
			for cloud in self.clouds:
				cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
			for mob in self.mobs:
				mob.rect.y += max(abs(self.player.vel.y), 4)
			for platform in self.platforms:
				platform.rect.y += max(abs(self.player.vel.y), 4)
				if platform.rect.top >= HEIGHT:
					platform.kill()
					self.score += 10
			for raindrop in self.raindrops:
				raindrop.rect.y += max(abs(self.player.vel.y), 3)

			for snowflake in self.snowflakes:
				snowflake.rect.y += max(abs(self.player.vel.y), 3)

		# PLATFORMS SPAWING ALGORITHM
		y = -55
		x = randrange(20, WIDTH - randrange(70, 150))
		while len(self.platforms) < 6:
			Platform(self, x, y)
		self.space_check()


		# DIE
		if self.player.rect.bottom > HEIGHT:
			for sprite in self.all_sprites:
				sprite.rect.y -= max(self.player.vel.y, 10)
				if sprite.rect.bottom < 0:
					sprite.kill()
			if len(self.platforms) == 0:
				self.playing = False 

		# DECORATE THE GAME IF AFRICA OR ANTRATICA
		if now - self.decor_timer > 850:
			if self.environment == "AFRICA":
				self.decor_timer = now
				for x_cor in range(0, WIDTH + 120, 120):
					raindrop = RainDrop(self)
					raindrop.rect.x = randrange(x_cor - 60, x_cor)
					raindrop.rect.y = randrange(-40, -10)
			elif self.environment == "ANTARTICA":
				self.decor_timer = now
				for x_cor in range(0, WIDTH + 120, 180):
					snowflake = SnowFlake(self)
					snowflake.rect.x = randrange(x_cor - 60, x_cor)
					snowflake.rect.y = randrange(-40, -10) 

	# DESIGN SPACING ALGORITHM
	def space_check(self):
		platforms_list = self.platforms.sprites()
		for index in range(0, len(platforms_list) - 1):
			if abs(platforms_list[index].rect.y - platforms_list[index + 1].rect.y) < 115:
				platforms_list[index +  1].rect.y -= 60
			if abs(platforms_list[index].rect.x - platforms_list[index + 1].rect.x) < 70:
				platforms_list[index + 1].rect.x += 50

	def events(self):
		# GAMELOOP - events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False	
				self.running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.player.jump()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.player.jump_cut()

	def draw(self):
		# GAMELOOP - draw
		self.screen.fill(BGCOLOR)
		self.all_sprites.draw(self.screen)
		self.draw_text(str(self.score), 22, WIDTH - 40 , 12)
		self.draw_text(self.environment.upper(), 18, 100, 18, color=BLACK)
		pygame.display.flip()

	def show_start_screen(self):
		# GAME SPLASH SCREEN
		pygame.mixer.music.load(self.dir + HAPPYTUNES_MUSIC)
		pygame.mixer.music.set_volume(0.8)
		pygame.mixer.music.play(loops=-1)
		pygame.mixer.music.play(loops=-1)
		self.init_groups()
		self.screen.fill(BGCOLOR)
		for index in range(8):
			cloud = Clouds(self)
			cloud.rect.y += 500
		self.clouds.draw(self.screen)
		self.draw_text(TITLE, 48, WIDTH / 2, HEIGHT / 4, color=BLACK)
		self.draw_text("Arrows to move, Space to Jump", 22, WIDTH / 2, HEIGHT / 2, color=BLACK)
		self.draw_text("Press a key to play", 22, WIDTH / 2, HEIGHT * 3/4, color=BLACK)
		self.draw_text("High Score : "+str(self.highscore), 22, WIDTH / 2, 15, color=BLACK)
		self.draw_text("Developed by : Jesal Shah", 12, 100, HEIGHT - 30, color=BLACK)
		self.draw_text("Art Credits : kenny.nl", 12, WIDTH - 100, HEIGHT - 30, color=BLACK)
		pygame.display.flip()
		self.waiting_for_key()
		self.clouds.empty()
		self.all_sprites.empty()
		pygame.mixer.music.fadeout(500)	

	def waiting_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					self.running = False
				if event.type == pygame.KEYUP:
					waiting = False

	def select_character(self):
		waiting = True
		index = 0
		while waiting:
			self.clock.tick(FPS)
			self.screen.fill(BGCOLOR)
			image = self.spritesheet.get_image(*BUNNY[index]['standing'][0])
			image.set_colorkey(BLACK)
			rect = image.get_rect()
			rect.center = (WIDTH / 2, HEIGHT / 3 + 25)
			self.draw_text("Character Select", 32, WIDTH / 2, 80, color=BLACK)
			self.screen.blit(image, rect)
			if index == 0:
				self.draw_text("Mr. Beer", 28, WIDTH / 2, HEIGHT / 2, color=BLACK)
			else:
				self.draw_text("Ms. Momo", 28, WIDTH / 2, HEIGHT / 2, color=BLACK)
			self.draw_text("Tab   : Change character", 18, WIDTH / 2, HEIGHT - 150, color=BLACK)
			self.draw_text("Space : Start Game       ", 18, WIDTH / 2, HEIGHT - 120, color=BLACK)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_TAB:
						if index == 0:
							index += 1
						else:
							index -= 1
					if event.key == pygame.K_SPACE:
						waiting = False
					self.player = BUNNY[index]
			self.clouds.draw(self.screen)
			pygame.display.flip()
		self.clouds.empty()
		self.all_sprites.empty()

	def show_go_screen(self):
		# GAME OVER/CONTINUE
		if not self.running:
			return
		pygame.mixer.music.load(self.dir + YIPPEE_MUSIC)
		pygame.mixer.music.play(loops=-1)
		pygame.mixer.music.set_volume(0.8)
		self.screen.fill(BGCOLOR)
		self.clouds.empty()
		for index in range(8):
			cloud = Clouds(self)
			cloud.rect.y += 500
		self.clouds.draw(self.screen)
		self.draw_text("GAME OVER", 48, WIDTH / 2, HEIGHT / 4, color=BLACK)
		self.draw_text("Score : "+str(self.score), 22, WIDTH / 2, HEIGHT / 2, color=BLACK)
		self.draw_text("Press a key to play again", 22, WIDTH / 2, HEIGHT * 3/4, color=BLACK)
		self.draw_text("Developed by : Jesal Shah", 12, 100, HEIGHT - 30, color=BLACK)
		self.draw_text("Art Credits : kenny.nl", 12, WIDTH - 100, HEIGHT - 30, color=BLACK)
		self.save_data()
		pygame.display.flip()
		self.waiting_for_key()
		self.clouds.empty()
		self.all_sprites.empty()
		pygame.mixer.music.fadeout(500)

game = Game()
game.show_start_screen()

while game.running:
	game.select_character()
	game.new()
	game.show_go_screen()

pygame.quit()