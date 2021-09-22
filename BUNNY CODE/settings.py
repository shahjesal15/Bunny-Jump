# GAME OPTIONS/ SETTINGS

WIDTH = 600
HEIGHT = 600
FPS = 60
TITLE = "Bunny!"
HIGH_SCORE = "\\gamedata\\highscore.txt"
SPRITE_SHEET = "\\images\\spritesheet.png"
JUMP_SOUND = "\\sounds\\Jump.wav"
HAPPYTUNES_MUSIC = "\\sounds\\Happy Tunes.mp3"
YIPPEE_MUSIC = "\\sounds\\Yippee.wav"
POWERUP_SOUND = "\\sounds\\PowerUp.wav"
HURT_SOUND = "\\sounds\\Hurt.wav"
CLOUDS_IMAGE = "\\images\\cloud{}.png"
GAME_ICON = "\\bunny.ico"
RAINDROP = "\\images\\raindrop.png"
SNOWFLAKE = "\\images\\snowflake.png"

# PLAYER PROPERTIES
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# BLITING PROPERTIES
CLOUDS_LAYER = 0
POWERUP_LAYER = 1
PLATFORM_LAYER = 1
MOB_LAYER = 3
PLAYER_LAYER = 2
ANIMATED_BACKGROUND = 0

# GAME PROPERTIES
POWERUP_BOOST = 60
POWER_SPAWN_PERCENT = 4
MOB_FREQ = 5000

BUNNY = [
	# MALE_BUNNY : BEER
	{
		"standing": [(614, 1063, 120, 191), (690, 406, 120, 201)],
		"walking": [(678, 860, 120, 201), (692, 1458, 120, 207)],
		"hurt": [(382, 946, 150, 174)],
		"jump": [(382, 763, 150, 181)]
	},

	# FEMALE_BUNNY : CUDDLES
	{
		"standing": [(581, 1265, 121, 191), (584, 0, 121, 201)],
		"walking": [(584, 203, 121, 201), (678, 651, 121, 207)],
		"hurt": [(411, 1866, 150, 174)],
		"jump": [(416, 1660, 150, 181)]
	}
]

PLATFORMS = {
	"AFRICA": [(0, 384, 380, 94), (382, 204, 200, 100)],
	"EGYPT": [(0, 672, 380, 94), (208, 1879, 201, 100)],
	"ANTARTICA": [(0, 768, 380, 94), (213, 1764, 201, 100)],
	"INDIA": [(0, 96, 380, 94), (382, 408, 200, 100)],
	"JAPAN": [(0, 960, 380, 94), (218, 1558, 200, 100)]
}
# TEXT 
FONT_NAME = 'arial'

# PLATFORM LOCATIONS
PLATFORM_LIST = [
				(0, HEIGHT - 50),
				(WIDTH / 2 - 50, HEIGHT * 3/4 - 50),
				(105, HEIGHT- 350),
				(350, 200),
				(175, 100)
]

PLATFORM_MAP = [
				((0, 45), (HEIGHT - 70, HEIGHT - 50)),
				((WIDTH - 70, WIDTH - 50), (HEIGHT - 120, HEIGHT - 80)),
				((150, 190), (400, 460)),
				((90, 125), (215, 350)),
				((50, 175), (120, 190))
]

# DEFINE COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (0, 255 ,255)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE