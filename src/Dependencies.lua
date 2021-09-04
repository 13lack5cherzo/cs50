--
-- libraries
--

Class = require 'lib/class'
Event = require 'lib/knife.event'
push = require 'lib/push'
Timer = require 'lib/knife.timer'

require 'src/Animation'
require 'src/constants'
require 'src/Entity'
require 'src/entity_defs'
require 'src/GameObject'
require 'src/game_objects'
require 'src/Hitbox'
require 'src/Player'
require 'src/StateMachine'
require 'src/Util'

require 'src/world/Doorway'
require 'src/world/Dungeon'
require 'src/world/Room'

require 'src/states/BaseState'

require 'src/states/entity/EntityIdleState'
require 'src/states/entity/EntityWalkState'

require 'src/states/entity/player/PlayerIdleState'
require 'src/states/entity/player/PlayerSwingSwordState'
require 'src/states/entity/player/PlayerWalkState'
require "src/states/entity/player/PlayerLiftState"

require 'src/states/game/GameOverState'
require 'src/states/game/PlayState'
require 'src/states/game/StartState'

gTextures = {
    ['tiles'] = love.graphics.newImage('graphics/tilesheet.png'),
    ['background'] = love.graphics.newImage('graphics/background.png'),
    ['character-walk'] = love.graphics.newImage('graphics/character_walk.png'),
    ['character-swing-sword'] = love.graphics.newImage('graphics/character_swing_sword.png'),
    ["character-pot-walk"] = love.graphics.newImage("graphics/character_pot_walk.png"),
    ['hearts'] = love.graphics.newImage('graphics/hearts.png'),
    ['switches'] = love.graphics.newImage('graphics/switches.png'),
    ['entities'] = love.graphics.newImage('graphics/entities.png')
}

gFrames = {
    ['tiles'] = GenerateQuads(gTextures['tiles'], TILE_SIZE, TILE_SIZE),
    ['character-walk'] = GenerateQuads(gTextures['character-walk'], TILE_SIZE, 2*TILE_SIZE),
    ['character-swing-sword'] = GenerateQuads(gTextures['character-swing-sword'], 2*TILE_SIZE, 2*TILE_SIZE),
    ["character-pot-walk"] = GenerateQuads(gTextures['character-pot-walk'], TILE_SIZE, 2*TILE_SIZE),
    ['entities'] = GenerateQuads(gTextures['entities'], TILE_SIZE, TILE_SIZE),
    ['hearts'] = GenerateQuads(gTextures['hearts'], TILE_SIZE, TILE_SIZE),
    ['switches'] = GenerateQuads(gTextures['switches'], TILE_SIZE, 18)
}

gFonts = {
    ['small'] = love.graphics.newFont('fonts/font.ttf', 8),
    ['medium'] = love.graphics.newFont('fonts/font.ttf', TILE_SIZE),
    ['large'] = love.graphics.newFont('fonts/font.ttf', 2*TILE_SIZE),
    ['gothic-medium'] = love.graphics.newFont('fonts/GothicPixels.ttf', TILE_SIZE),
    ['gothic-large'] = love.graphics.newFont('fonts/GothicPixels.ttf', 2*TILE_SIZE),
    ['zelda'] = love.graphics.newFont('fonts/zelda.otf', 4*TILE_SIZE),
    ['zelda-small'] = love.graphics.newFont('fonts/zelda.otf', 2*TILE_SIZE)
}

gSounds = {
    ['music'] = love.audio.newSource('sounds/music.mp3', 'static'),
    ['sword1'] = love.audio.newSource('sounds/sword1.wav', 'static'),
    ['sword2'] = love.audio.newSource('sounds/sword2.wav', 'static'),
    ['sword3'] = love.audio.newSource('sounds/sword3.wav', 'static'),
    ['hit-enemy'] = love.audio.newSource('sounds/hit_enemy.wav', 'static'),
    ['hit-player'] = love.audio.newSource('sounds/hit_player.wav', 'static'),
    ['door'] = love.audio.newSource('sounds/door.wav', 'static'),
    ["healthup"] = love.audio.newSource('sounds/healthup.wav', 'static'),
    ["lift"] = love.audio.newSource('sounds/lift.wav', 'static'),
    ["throw"] = love.audio.newSource('sounds/throw.wav', 'static'),
    ["projectile_hit"] = love.audio.newSource('sounds/projectile_hit.wav', 'static'),
    ["projectile_drop"] = love.audio.newSource('sounds/projectile_drop.wav', 'static')
}