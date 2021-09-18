--[[

    Drop Fish
    developed by Dan Chan

    game over state
    
]]

GameOverState = Class{__includes = BaseState}

function GameOverState:init(def)

    -- background
    self.background = def.background

    -- score
    self.scoreString = def.scoreString

    -- text platform generator
    self.platformGenerator = TextPlatform {
        platformInfo = GAMEOVER_STATE_TEXT_PLAT_INFO
    }
    self.platformGenerator:generate()  -- generate text platforms

    -- spike generator (for player init; not updated)
    self.spikeGenerator = SpikeGenerator {}

    -- player
    self.player = Player {
        x = PLAYER_SPAWN_X,  -- middle
        y = 1,  -- top
        platformGenerator = self.platformGenerator,
        spikeGenerator = self.spikeGenerator
    }
    self.player.renderBowl = false  -- turn off bowl render

end

function GameOverState:update(dt)

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
            PLAYER_SIZE, 
            VIRTUAL_WIDTH - PLAYER_SIZE
        )
        self.player.y = 1
        self.player.offScreen = false
    end

end

function GameOverState:render()

    -- render background
    self.background:render()

    -- render platform generator (debug only)
    if DEBUG_MODE then
        self.platformGenerator:render()
    end

    -- render player (behind text)
    self.player:render()

    -- render score
    Score:render(self.scoreString, true)

    -- texts
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_large'])
    love.graphics.printf(
        'GAME OVER',  -- text
        0, MAINTEXT_Y,  -- x, y
        VIRTUAL_WIDTH,  -- limit
        'center'  -- align
    )

    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_medium'])
    love.graphics.printf(  
        'Press Enter to Try Again',   -- text
        0, SUBTEXT_Y,   -- x, y
        VIRTUAL_WIDTH,  -- limit
        'center'  -- align
    )

end


function GameOverState:inputHandler()
    -- function to handle user input

    if love.keyboard.wasPressed('escape') then
        love.event.quit()
    end

    if (
        love.keyboard.wasPressed('enter') 
        or love.keyboard.wasPressed('return')
    ) then
        -- remove game over state
        gStateStack:pop()
        -- stack start state
        gStateStack:push(
            StartState {  -- reset game
                backgroundY = self.background.y  -- for smoother transition
            }
        )

    end

end