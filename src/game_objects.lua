--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

GAME_OBJECT_DEFS = {
    ['switch'] = {
        type = 'switch',
        texture = 'switches',
        frame = 2,
        width = 16,
        height = 16,
        solid = false,
        defaultState = 'unpressed',
        states = {
            ['unpressed'] = {
                frame = 2
            },
            ['pressed'] = {
                frame = 1
            }
        }
    },

    ["healthDrop"] = {
        type = "healthDrop",
        texture = "hearts",
        frame = 5,
        width = TILE_SIZE,
        height = TILE_SIZE,
        solid = false,
        defaultState = "heart",
        states = {
            ["heart"] = {
                frame = 5
            }
        },
        onCollide = function(_player)
            -- function to increment player's health
            _player.health = math.min(_player.health + 2, 6)
            gSounds['healthup']:play()
        end,
        consumable = true,
    },

    ['pot'] = {
        type = "pot",
        texture = "tiles",
        frame = 14,
        width = TILE_SIZE,
        height = TILE_SIZE,
        solid = true,
        defaultState = "pot",
        states = {
            ["pot"] = {
                frame = 14
            }
        },
        interactRange = 5,
        onInteract = function(_player)
            _player:changeState("lift")
        end,
        interactTrack = false,
        trackOffsetY = -10,
        isProjectile = false,
        projectileSpeed = 2*PLAYER_WALK_SPEED,
        projectileMaxDist = 4*TILE_SIZE
    },
}