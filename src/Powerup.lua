--[[
    GD50
    Breakout Remake

    -- Powerup Class --

    Represents a powerup
    including inherited classes:
    - BallPowerup
    - KeyPowerup
]]

Powerup = Class{
    init = function(self)
        -- placed outside screen
        self.x = VIRTUAL_WIDTH  -- right
        self.y = VIRTUAL_HEIGHT  -- bottom

        -- simple positional and dimensional variables
        self.width = 16
        self.height = 16

        -- these variables are for keeping track of our velocity on both the
        -- X and Y axis, since the ball can move in two dimensions
        self.dy = 0
        self.dx = 0

        --[[
        powerup type
        - 1: extra ball
        - 2: key
        ]]
        self.type = 1

        self.inPlay = false  -- init not in play
        self.spawnTimer = 0  -- spawn timer counter
        self.spawnProbability = 100  -- % chance
        self.spawnPeriod = 5  -- to spawn every self.spawnPeriod frames
        
    end;
}

--[[
    Expects an argument with a bounding box, be that a paddle or a brick,
    and returns true if the bounding boxes of this and the argument overlap.
]]
function Powerup:collides(target)
    -- first, check to see if the left edge of either is farther to the right
    -- than the right edge of the other
    if self.x > target.x + target.width or target.x > self.x + self.width then
        return false
    end

    -- then check to see if the bottom edge of either is higher than the top
    -- edge of the other
    if self.y > target.y + target.height or target.y > self.y + self.height then
        return false
    end 

    -- if the above aren't true, they're overlapping
    gSounds['powerup']:stop()
    gSounds['powerup']:play()
    return true
end

--[[
    Places the powerup in the middle of the screen, falling.
]]
function Powerup:spawn(type)
    self.x = VIRTUAL_WIDTH * math.random(1, 7) / 8  -- random width (height fixed)
    self.y = VIRTUAL_HEIGHT / 4  -- y is in the top quarter
    self.dy = 10
    self.type = type  -- random type
    self.inPlay = true  -- flag as in play
end

--[[
    Places the powerup in the off-screen, not moving.
]]
function Powerup:despawn()
    self.x = VIRTUAL_WIDTH  -- right
    self.y = VIRTUAL_HEIGHT  -- bottom
    self.dy = 0
    self.inPlay = false  -- flag as not in play
end

function Powerup:update(dt, powerupType)
    -- update positions
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt

    -- spawn
    if self.inPlay == false then  -- if powerup not spawned
        self.spawnTimer = self.spawnTimer + dt  -- start spawnTimer
        if self.spawnTimer > self.spawnPeriod then  -- after spawnPeriod,
            self.spawnTimer = 0  -- reset timer
            if math.random(0, 100) <= self.spawnProbability then
                self:spawn(powerupType)  -- spawn with self.spawnProbability
            end
        end
    else  -- powerup is spawned
        if self.y > VIRTUAL_HEIGHT then  -- if off screen
            self:despawn()  -- despawn
        end
    end
end

function Powerup:render()
    -- gTexture is our global texture
    love.graphics.draw(gTextures['main'], gFrames['powerups'][self.type],
        self.x, self.y)
end