--[[

    Drop Fish
    developed by Dan Chan

    constants

]]

-- name
GAME_NAME = "DROP FISH"

-- display
VIRTUAL_WIDTH = 360
VIRTUAL_HEIGHT = 640

-- window
WINDOW_WIDTH = 360
WINDOW_HEIGHT = 640

-- player
PLAYER_SIZE = 24
GRAVITY = 700  -- higher -> faster
PLAYER_ACCEL = 800  -- higher -> faster
PLAYER_ACCEL_YSCALAR = 0.3  -- higher -> more vertical handle
PLAYER_SPEED_CAP = 1000  -- higher -> faster
PLAYER_BOUNCE_LOSS = 0.2  -- [0, 1]. lower -> more bouncy
PLAYER_DOWN_BOUNCE_DAMP = 0.3  -- [0, 1]. lower -> more bouncy
PLAYER_AIR_FRICTION = 3  -- higher -> slower
PLAYER_MIN_BOUNCE = 625  -- higher -> more bouncy
PLAYER_CLIP_TOL = 0.5  -- higher -> safer
PLAYER_SPAWN_X = (VIRTUAL_WIDTH - PLAYER_SIZE) / 2

-- platform
PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 1/2 * PLAYER_SIZE
PLATFORM_SPEED_X = 10  -- higher -> faster
PLATFORM_SPEED_Y = 80  -- higher -> faster
PLATFORM_SPEED_YMAX = 150  -- higher -> faster
PLAT_SPEED_RAND = 0  -- [0, 1]. higher -> more random

-- platform generator
AVE_PLAT_GEN_RATE = 0.8  -- higher -> faster
RAND_PLAT_GEN_RATE = 0.5  -- higher -> more random
PLAT_ROW_CAP = 3  -- higher -> more platforms
PERC_PLAT_MISSING = 90  -- %. higher -> fewer platforms
PERC_PLAT_MISSING_DAMP = 0.3  -- [0, 1]. higher -> more regular platforms
PLAT_INCREMENT = 1  -- %/platform. higher -> faster

-- spike
SPIKE_SIZE = 8
SPIKE_DRAWSIZE_ADD = 2
SPIKE_SPEED_X = PLATFORM_SPEED_X
SPIKE_SPEED_Y = PLATFORM_SPEED_Y
SPIKE_GEN_RATE = 0.05
RAND_SPIKE_GEN_RATE = 0.02

-- score
SCORE_TICK_RATE = 1  -- tick/second
SCORE_TICK_INCR = 1  -- score/tick
SCORE_TICK_RAND = 2

-- font size
FONT_S = 8
FONT_M = 16
FONT_L = 32
FONT_XL = 64

-- text positions
MAINTEXT_Y = VIRTUAL_HEIGHT / 2 - FONT_L
SUBTEXT_Y = VIRTUAL_HEIGHT - FONT_L

-- text platforms information
START_STATE_TEXT_PLAT_INFO = {
    ["subtext"] = {
        x = VIRTUAL_WIDTH / 2 - 81,
        y = SUBTEXT_Y,
        width = VIRTUAL_WIDTH / 2 - 20,
        height = FONT_M
    }
}
GAMEOVER_STATE_TEXT_PLAT_INFO = {
    ["subtext"] = {
        x = VIRTUAL_WIDTH / 2 - 103,
        y = SUBTEXT_Y,
        width = VIRTUAL_WIDTH / 2 + 24,
        height = FONT_M
    }
}

-- player circle graphic
BOWL_R = 0
BOWL_G = 142/255
BOWL_B = 0.8
BOWL_ALPHA = 0.6

-- player fish graphic
FISH_SIZE = 4
FISH_DIMENSIONS = 3
FISH_EYE_SIZE = 1
FISH_EYE_TRANS = 2
FISH_EYE_DIMENSIONS = 3
FISH_BOWL_TOL = 5

-- water particles
PT_NUM = 4
PT_LIFE_BEG = 1
PT_LIFE_END = 2
PT_ACC_X = PLATFORM_SPEED_Y
PT_ACC_YMIN = -PLATFORM_SPEED_Y
PT_ACC_YMAX = -PLATFORM_SPEED_Y
PT_STD_ERR_X = PLAYER_SIZE
PT_STD_ERR_Y = PLAYER_SIZE/2
PT_ALPHA = 1

-- platform graphic
PLATFORM_GRAPHIC_WIDTH = 300  -- pixels
PLATFORM_GRAPHIC_HEIGHT = 100  -- pixels

-- spike graphic
SPIKE_DIMENSIONS = 3
MAX_SPIKE_DIMENSIONS = 6
SPIKE_R = 1
SPIKE_G = 1
SPIKE_B = 0
SPIKE_INNER_SIZE_RATIO = 3/4
SPIKE_WARP_RATE = 8  -- /second. higher -> faster

-- background graphic
BACKGROUND_SCROLL_SPD = 50  -- higher -> faster
BACKGROUND_SCALE_HEIGHT = 1924
BACKGROUND_RESET_POINT = 1024


-- misc
DEBUG_MODE = false
INF = 999999999


