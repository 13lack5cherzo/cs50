--[[

    Drop Fish
    developed by Dan Chan

    spike class
    * a spike

]]

Spike = Class{}

function Spike:init(def)

    -- position (spike center)
    self.x = def.x
    self.y = VIRTUAL_HEIGHT - 1  -- just above bottom
    -- dimensions
    self.width = SPIKE_SIZE
    self.height = SPIKE_SIZE
    -- drawsize (draw is larger than actual size for "close calls")
    self.drawWidth = self.width + math.abs(SPIKE_DRAWSIZE_ADD)
    self.drawHeight = self.height + math.abs(SPIKE_DRAWSIZE_ADD)
    -- center position
    self.centerX = self.x + self.width/2
    self.centerY = self.y + self.height/2
    -- speed
    self.dx = SPIKE_SPEED_X * math.random(-1, 1)  -- random x direction
    self.dy = -math.abs(SPIKE_SPEED_Y)  -- always going up

    -- segments (aesthetic)
    self.segments = SPIKE_DIMENSIONS
    -- rate at which segments change (times per second)
    self.segRate = SPIKE_WARP_RATE  -- /second. higher -> faster

    -- inner shape (aesthetic)
    self.innerSize = self.drawWidth * SPIKE_INNER_SIZE_RATIO
    -- timer
    self.timer = 0

end


function Spike:update(dt)

    -- update position
    self:updatePosition(dt)

    -- warp spike shape
    self:warp(dt)

end


function Spike:render()

    love.graphics.setColor(SPIKE_R, SPIKE_G, SPIKE_B, 1)
    love.graphics.circle(  -- body
        "fill", 
        self.centerX, self.centerY,  -- center pos
        self.drawWidth,  -- radius
        self.segments  -- segments
    )
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.circle(  -- inner body
        "fill", 
        self.centerX, self.centerY,  -- center pos
        self.innerSize,  -- radius
        self.segments  -- segments
    )

end


function Spike:updatePosition(dt)

    -- update collision position
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt

    -- update centre position
    self.centerX = self.x + self.width/2
    self.centerY = self.y + self.height/2

end


function Spike:warp(dt)
    -- function to warp spike (aesthetic)

    if self.timer > 1 then

        -- change segments
        if self.segments == SPIKE_DIMENSIONS then
            self.segments = math.random(SPIKE_DIMENSIONS, MAX_SPIKE_DIMENSIONS)
        else
            self.segments = SPIKE_DIMENSIONS
        end

        -- reset timer
        self.timer = self.timer - 1  
        -- add randomness to period between platform spawn
        self.timer = self.timer

    end

    -- update timer
    self.timer = self.timer + dt * self.segRate

end