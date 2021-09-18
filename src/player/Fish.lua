--[[

    Drop Fish
    developed by Dan Chan

    fish class
    
]]

Fish = Class{}

function Fish:init(def)

    -- player object to sync position
    self.player = def.player

    -- position (centre of fish)
    self.x = self.player.centerX
    self.y = self.player.centerY
    -- dimensions
    self.width = FISH_SIZE
    self.height = FISH_SIZE
    self.segments = FISH_DIMENSIONS
    -- speed
    self.dx = 0
    self.dy = 0

    -- indicator if out of bowl
    self.outOfBowl = false

    -- fish eye size
    self.eyeSize = FISH_EYE_SIZE
    -- fish eye dimensions
    self.eyeDim = FISH_EYE_DIMENSIONS
    -- fish eye transpose
    self.eyeTrans = FISH_EYE_TRANS
    -- fish bowl tolerance to maker sure that fish 
    -- looks like it is inside bowl
    self.bowlTol = FISH_BOWL_TOL

end


function Fish:update(dt)

    self:updatePosition(dt)

    -- check collision with bowl 
    -- then reverse equation to prevent fish from going out
    -- and add tolerance
    if (  -- right
        self.x + self.width/2  -- fish right
        > self.player.x + self.player.width  -- bowl right
        - self.bowlTol  -- tol
    ) then  
        self.x = self.player.x + self.player.width - self.width/2
        self.x = self.x - self.bowlTol  -- tol
    end

    if (  -- left
        self.x - self.width/2  -- fish left
        < self.player.x  -- bowl left
        + self.bowlTol  -- tol
    ) then  
        self.x = self.player.x + self.width/2 
        self.x = self.x + self.bowlTol  -- tol
    end

    if (  -- bottom
        self.y + self.height/2  -- fish bottom
        > self.player.y + self.player.height  -- bowl bottom
        - self.bowlTol  -- tol
    ) then  
        self.y = self.player.y + self.player.height - self.height/2
        self.y = self.y - self.bowlTol  -- tol
    end

    if (  -- top
        self.y - self.height/2  -- fish top
        < self.player.y  -- bowl top
        + self.bowlTol  -- tol
    ) then  
        self.y = self.player.y + self.height/2
        self.y = self.y + self.bowlTol  -- tol
    end

end


function Fish:updatePosition(dt)
    -- update position
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt
end


function Fish:render()

    -- fish
    love.graphics.setColor(1, 1, 0, 1)
    love.graphics.circle(  -- body
        "fill", 
        self.x, self.y,  -- center pos
        self.width,  -- radius
        self.segments  -- segments
    )
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.circle(  -- eye
        "fill", 
        self.x + self.eyeTrans, self.y,  -- center pos
        self.eyeSize,  -- radius
        self.eyeDim  -- segments
    )

end


function Fish:checkOutOfBowl()
    -- function to detect if an fish is out of bowl
    if (
        (self.x + self.width/2 > self.player.x + self.player.width)  -- right
        or (self.x - self.width/2 < self.player.x)  -- left
        or (self.y + self.height/2 > self.player.y + self.player.height) -- bottom
        or (self.y - self.height/2 < self.player.y)  -- top
    ) then
        return true
    else
        return false
    end
end
