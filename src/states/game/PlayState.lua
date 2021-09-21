--[[

    Drop Fish
    developed by Dan Chan

    play state
    
]]

PlayState = Class{__includes = BaseState}

function PlayState:init(def)

    -- background
    self.background = def.background

    -- player spawned flag
    self.playerSpawned = false
    self.player = false  -- placeholder

    -- platform generator
    self.platformGenerator = PlatformGenerator {}

    -- spike generator
    self.spikeGenerator = SpikeGenerator {}

    -- scorer object
    self.scorer = Score {}

end


function PlayState:update(dt)

    -- quit
    if love.keyboard.wasPressed('escape') then
        love.event.quit()
    end

    -- spawn player after first platform spawn
    self:spawnPlayer()

    -- update platform generator
    self.platformGenerator:update(dt)

    -- update spike generator
    self.spikeGenerator:update(dt)

    -- update player after platforms and spike (better collision detection)
    if self.playerSpawned then
        -- update player
        self.player:update(dt)

        -- check for game over
        self:checkGameOver()
    end

    -- update background
    self.background:update(dt)

    -- update score
    self.scorer:update(dt)

end


function PlayState:render()

    --render background
    self.background:render()

    -- render platform generator
    self.platformGenerator:render()

    -- render spike
    self.spikeGenerator:render()

    -- render player
    if self.playerSpawned then
        self.player:render()
    end

    -- render score
    self.scorer:render(self.scorer.scoreString, false)

end


function PlayState:spawnPlayer()
    -- function to spawn player after the first platform is spawned

    if not self.playerSpawned and (#self.platformGenerator.platforms > 0) then
        -- spawn player
        self.player = Player {
            x = PLAYER_SPAWN_X,  -- middle
            y = 1,  -- top
            platformGenerator = self.platformGenerator,  -- for collision check
            spikeGenerator = self.spikeGenerator  -- for collision check
        }
        self.playerSpawned = true
    end

end


function PlayState:checkGameOver()

    -- check for game over
    if self.player.offScreen or self.player.collidedSpike then
        -- remove playstate
        gStateStack:pop()
        getRandomTableElement(gDamageSounds):play()
        -- stack game over state
        gStateStack:push(
            GameOverState {
                background = self.background,  -- for smooth transition
                scoreString = self.scorer.scoreString,  -- to display score
            }
        )
    end

end

