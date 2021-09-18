--[[

    Drop Fish
    developed by Dan Chan

    dependencies
    
]]

-- libraries
Class = require 'lib/class'
Event = require 'lib/knife.event'
push = require 'lib/push'
Timer = require 'lib/knife.timer'

-- utilities
require 'src/util/constants'
require 'src/util/Util'

-- state machine
require 'src/states/BaseState'
require 'src/states/StateStack'

-- game states
require 'src/states/game/StartState'
require 'src/states/game/PlayState'
require 'src/states/game/GameOverState'

-- world
require "src/world/Background"
require "src/world/Platform"
require "src/world/PlatformGenerator"
require "src/world/TextPlatform"
require "src/world/Spike"
require "src/world/SpikeGenerator"
require "src/world/Score"

-- player
require "src/player/Player"
require "src/player/Fish"
require "src/player/Water"

gBackgroundTextures = {
    ["lavaBackground"] = love.graphics.newImage('graphics/lava_background2.jpg'),
    ["iceBackground"] = love.graphics.newImage('graphics/ice_background2.jpg'),
    ["plasmaBackground"] = love.graphics.newImage('graphics/plasma_background2.jpg'),
    ["infernalBackground"] = love.graphics.newImage('graphics/infernal_background2.jpg'),
    ["skyBackground"] = love.graphics.newImage('graphics/sky_background2.jpg'),
    ["candyBackground"] = love.graphics.newImage('graphics/candy_background2.jpg'),
    ["sunsetBackground"] = love.graphics.newImage('graphics/sunset_background2.jpg'),
    ["starBackground"] = love.graphics.newImage('graphics/star_background2.jpg'),
    ["galaxyBackground"] = love.graphics.newImage('graphics/galaxy_background2.jpg'),
    ["jungleBackground"] = love.graphics.newImage('graphics/jungle_background2.jpg'),
    ["autumnBackground"] = love.graphics.newImage('graphics/autumn_background2.jpg')
}

gTextures = {
    ["grassPlatform"] = love.graphics.newImage('graphics/grassLongPlatform2.png'),
    ['particle'] = love.graphics.newImage('graphics/particle.png')
}

gFrames = {
    ["grassPlatform"] = GenerateQuads(
        gTextures["grassPlatform"], 
        PLATFORM_GRAPHIC_WIDTH, 
        PLATFORM_GRAPHIC_HEIGHT
    )
}

gFonts = {
    ['arcade_small'] = love.graphics.newFont('fonts/ArcadeAlternate.ttf', FONT_S),
    ['arcade_medium'] = love.graphics.newFont('fonts/ArcadeAlternate.ttf', FONT_M),
    ['arcade_large'] = love.graphics.newFont('fonts/ArcadeAlternate.ttf', FONT_L),
    ["flappy_small"] = love.graphics.newFont("fonts/flappy.ttf", FONT_S),
    ["flappy_medium"] = love.graphics.newFont("fonts/flappy.ttf", FONT_M),
    ["flappy_large"] = love.graphics.newFont("fonts/flappy.ttf", FONT_L)
}

gSounds = {
    ["music"] = love.audio.newSource('sounds/Cumbia Mamacita by YOKE - Ohzum Beats.mp3', 'static')
}

gCollisionSounds = {
    ["bounce1"] = love.audio.newSource('sounds/bounce1.wav', 'static'),
    ["bounce2"] = love.audio.newSource('sounds/bounce2.wav', 'static'),
    ["bump1"] = love.audio.newSource('sounds/bump1.wav', 'static'),
    ["bump2"] = love.audio.newSource('sounds/bump2.wav', 'static')
}

gDamageSounds = {
    ["damage1"] = love.audio.newSource('sounds/damage1.wav', 'static'),
    ["damage2"] = love.audio.newSource('sounds/damage2.wav', 'static')
}