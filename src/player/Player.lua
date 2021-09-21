--[[

    Drop Fish
    developed by Dan Chan

    player class
    
]]

Player = Class{}

function Player:init(def)

    -- position
    self.x = def.x
    self.y = def.y
    -- dimensions
    self.width = PLAYER_SIZE
    self.height = PLAYER_SIZE
    -- center position
    self.centerX = self.x + self.width/2
    self.centerY = self.y + self.height/2
    -- speed
    self.dx = 0
    self.dy = 0
    -- gravity
    self.gravity = math.abs(GRAVITY)  -- higher -> faster
    -- air friction on x horizontal direction
    self.airFriction = PLAYER_AIR_FRICTION  -- higher -> slower
    -- user input movement acceleration
    self.inputSpeed = math.abs(PLAYER_ACCEL)  -- higher -> faster
    -- player speed scalar for floating
    self.inputYScalar = PLAYER_ACCEL_YSCALAR  -- higher -> more vertical handle
    -- player speed cap
    self.speedCap = PLAYER_SPEED_CAP
    -- player speed loss from bounce
    self.bounceLoss = PLAYER_BOUNCE_LOSS  -- % lower -> more bouncy
    -- player speed loss from down bounce (up-to-down)
    self.downBounceDamp = PLAYER_DOWN_BOUNCE_DAMP

    -- player minimum bounce 
    self.bounceMin = PLAYER_MIN_BOUNCE  -- higher -> more bouncy

    -- tolerance for player clipping into platform
    self.clipTol = PLAYER_CLIP_TOL  -- higher -> safer

    -- platform generator object to check collisions
    self.platformGenerator = def.platformGenerator
    -- placeholder for platform object collided with
    self.collidedPlatform = false

    -- spike generator object to check collisions
    self.spikeGenerator = def.spikeGenerator
    -- player-spike collision flag
    self.collidedSpike = false

    -- player off screen flag
    self.offScreen = false

    -- fish aesthetic object
    -- pass player object to sync position
    self.fish = Fish {player = self}

    -- water particles
    self.water = Water {}

    -- render bowl flag
    self.renderBowl = true

end


function Player:update(dt)

    self:getCenter()

    self:capSpeed(dt)

    self:updatePosition(dt)

    self:naturalForces(dt)

    self:userInputMove(dt)

    self.collidedPlatform = self:checkPlatformCollision(dt)

    self.collidedSpike = self:checkSpikeCollision(dt)

    if self.collidedPlatform ~= false then  -- collision
        
        if DEBUG_MODE then print("bounce player") end

        self.water:spill(self.centerX, self.centerY)
        getRandomTableElement(gCollisionSounds):play()

        self:bounce(dt)
        
    end

    if Background:offScreen(self) then
        if DEBUG_MODE then print("player offscreen") end
        self.offScreen = true
    end

    self.fish:update(dt)
    self.water:update(dt)

end


function Player:render()

    if self.renderBowl then

        -- blue circle
        love.graphics.setColor(BOWL_R, BOWL_G, BOWL_B, BOWL_ALPHA)
        love.graphics.circle(
            "fill", 
            self.centerX, self.centerY,  -- center pos
            self.width/2,  -- radius
            100  -- segments
        )
        -- white border
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.circle(
            "line", 
            self.centerX, self.centerY,  -- center pos
            self.width/2,  -- radius
            100  -- segments
        )

    end

    self.fish:render()
    self.water:render()

end


function Player:getCenter()
    -- function to get centre of the player
    self.centerX = self.x + self.width/2
    self.centerY = self.y + self.height/2
end


function Player:capSpeed(dt)
    -- cap player speed
    self.dx = math.min(self.dx, self.speedCap)
    self.dy = math.min(self.dy, self.speedCap)
end


function Player:updatePosition(dt)
    -- update position
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt
end


function Player:naturalForces(dt)
    -- gravity on y vertical direction
    self.dy = self.dy + self.gravity * dt

    -- air friction on x horizontal direction (cap at x horizontal speed)
    local airFriction = math.min(math.abs(self.dx), PLAYER_AIR_FRICTION)
    self.dx = self.dx - sign(self.dx) * self.airFriction  -- opposite sign

end


function Player:collides(target)
    -- function to check if player collided with target

    return not (
        self.x + self.width < target.x 
        or self.x > target.x + target.width 
        or self.y + self.height < target.y 
        or self.y > target.y + target.height
    )
end


function Player:checkPlatformCollision(dt)
    -- function to check if player collided with any platforms

    for k, platform1 in pairs(self.platformGenerator.platforms) do
        if self:collides(platform1) then

            if DEBUG_MODE then print("player platform collision") end
            return platform1
 
        end
    end
    return false
    
end


function Player:checkSpikeCollision(dt)
    -- function to check if player collided with any spikes

    for k, spike1 in pairs(self.spikeGenerator.spikes) do
        if self:collides(spike1) then

            if DEBUG_MODE then print("player spike collision") end
            return true
 
        end
    end
    return false
    
end


function Player:bounce(dt)
    -- function to bounce player

    -- different logic for collision on top and below platform
    if self.dy > 0 then  -- on top of platform
        
        -- push player out of the platform (to prevent clipping)
        self.y = self.collidedPlatform.y - (self.height + self.clipTol)

        -- maintain minimum bounciness
        if math.abs(self.dy) < self.bounceMin then
            self.dy = sign(self.dy) * self.bounceMin
        end

        -- reverse vertical speed, with energy loss
        self.dy = -self.dy * (1 - self.bounceLoss)

    else  -- below platform

        -- push player out of the platform (to prevent clipping)
        self.y = self.collidedPlatform.y + (self.collidedPlatform.height + self.clipTol)

        -- reverse vertical speed, with energy loss and reduced down bounce
        self.dy = -self.dy * (1 - self.bounceLoss - self.downBounceDamp)

    end


    -- lower horizontal speed based on energy loss
    self.dx = self.dx * (1 - self.bounceLoss)

    -- reset collided platform to placeholder
    self.collidedPlatform = false
end


function Player:userInputMove(dt)
    -- function to translate user input to movement

    -- left
    if love.keyboard.isDown('left') then
        self.dx = self.dx - self.inputSpeed * dt
    end
    -- right
    if love.keyboard.isDown('right') then
        self.dx = self.dx + self.inputSpeed * dt
    end
    -- float (capped at gravity, and only whilstgoing downwards)
    if love.keyboard.isDown('up') and (self.dy > 0) then
        self.dy = self.dy - self.inputSpeed * self.inputYScalar * dt
    end
    -- fall faster
    if love.keyboard.isDown('down') then
        self.dy = self.dy + self.inputSpeed * self.inputYScalar * dt
    end
    -- debug reset to middle
    if DEBUG_MODE and love.keyboard.isDown('r') then
        self.x = PLAYER_SPAWN_X
        self.y = (VIRTUAL_HEIGHT - PLAYER_SIZE) / 2
        self.dx, self.dy = 0, 0
    end
end

