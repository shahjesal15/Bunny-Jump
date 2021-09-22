import pygame
from settings import *

# SETUP
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# FPS CLOCK
clock = pygame.time.Clock()

# SPRITES
all_sprites = pygame.sprite.Group()

# GAME LOOP
running = True
while running:
	clock.tick(FPS)
	# EVENT LOOP
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False	

pygame.quit()