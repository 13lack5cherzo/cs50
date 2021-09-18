--[[

    Drop Fish
    developed by Dan Chan

    start state
    
]]

StartState = Class{__includes = BaseState}

function StartState:init(def)

    -- background
    if def == nil then  -- nil on first init
        self.backgroundY = nil
    else  -- smoother transition if background is the same
        self.backgroundY = def.backgroundY
    end
    self.background = Background {
        y = self.backgroundY
    }

    -- text platform generator
    self.platformGenerator = TextPlatform {
        platformInfo = START_STATE_TEXT_PLAT_INFO
    }

    -- spike generator (for player init; not updated)
    self.spikeGenerator = SpikeGenerator {}

    -- player
    self.player = Player {
        x = PLAYER_SPAWN_X,  -- middle
        y = 1,  -- top
        platformGenerator = self.platformGenerator,
        spikeGenerator = self.spikeGenerator
    }

    -- flag to track help mode
    self.helpMode = false

end

function StartState:update(dt)

    -- handle user input
    self:inputHandler()

    -- update background
    self.background:update(dt)

    -- update platform generator
    self.platformGenerator:update(dt)

    -- update player
    self.player:update(dt)
    -- if player is offscreen, reset
    if self.player.offScreen then
        self.player.x = math.random(
            PLAYER_SIZE, VIRTUAL_WIDTH - PLAYER_SIZE
        )
        self.player.y = 1
        self.player.offScreen = false
    end

end

function StartState:render()

    -- render background
    self.background:render()

    -- render platform generator (debug only)
    if DEBUG_MODE then
        self.platformGenerator:render()
    end

    -- render player (behind text)
    self.player:render()

    -- texts
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.setFont(gFonts['flappy_large'])
    love.graphics.printf(
        GAME_NAME,  -- text
        2, MAINTEXT_Y+2,  -- x, y
        VIRTUAL_WIDTH,  -- limit
        'center'  -- align
    )
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_large'])
    love.graphics.printf(
        GAME_NAME,  -- text
        0, MAINTEXT_Y,  -- x, y
        VIRTUAL_WIDTH,  -- limit
        'center'  -- align
    )
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_medium'])
    love.graphics.printf(
        'Press Enter to Play',  -- text
        0, SUBTEXT_Y,  -- x, y
        VIRTUAL_WIDTH,  -- limit
        'center'  -- align
    )


    -- help mode off
    if self.helpMode == false then  
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.setFont(gFonts['flappy_medium'])
        love.graphics.printf(
            "Press Space for Help",  -- text
            0, FONT_M,  -- x, y
            VIRTUAL_WIDTH,  -- limit
            'left'  -- align
        )
    -- help mode on
    else  

        -- black background (easier to see text)
        love.graphics.setColor(0, 0, 0, BOWL_ALPHA)
        love.graphics.rectangle(
            "fill",  -- mode
            0, FONT_M,  -- position
            VIRTUAL_WIDTH, 3*FONT_M  -- dimensions
        )
        
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.setFont(gFonts['arcade_medium'])
        love.graphics.printf(
            "Stay in View and Avoid Spikes!",  -- text
            0, FONT_M,  -- x, y
            VIRTUAL_WIDTH,  -- limit
            'left'  -- align
        )
        love.graphics.printf(
            "Left-Right Keys to Steer",  -- text
            0, 2*FONT_M,  -- x, y
            VIRTUAL_WIDTH,  -- limit
            'left'  -- align
        )
        love.graphics.printf(
            "Up-Down Keys to Control Drop",  -- text
            0, 3*FONT_M,  -- x, y
            VIRTUAL_WIDTH,  -- limit
            'left'  -- align
        )

        love.graphics.setFont(gFonts['flappy_medium'])
        love.graphics.printf(
            "Press Space to Hide This",  -- text
            0, 4*FONT_M,  -- x, y
            VIRTUAL_WIDTH,  -- limit
            'left'  -- align
        )
    end

end


function StartState:inputHandler()
    -- function to handle user input

    -- quit
    if love.keyboard.wasPressed('escape') then
        love.event.quit()
    end

    -- play
    if (
        love.keyboard.wasPressed('enter') 
        or love.keyboard.wasPressed('return')
    ) then
        -- remove start state
        gStateStack:pop()
        -- stack playstate
        gStateStack:push(
            PlayState {
                background = self.background  -- for smooth transition
            }
        )

    end

    -- help mode
    if love.keyboard.wasPressed('space') then

        -- toggle help mode
        if self.helpMode == false then
            self.platformGenerator:generate()
            self.helpMode = true

            -- change background 
            -- (only when helpmode is turned on)
            self.background = Background {
                y = self.background.y
            }

        else
            self.platformGenerator:despawnAll()
            self.helpMode = false
        end

    end

end