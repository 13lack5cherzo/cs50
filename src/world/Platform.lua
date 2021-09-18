--[[

    Drop Fish
    developed by Dan Chan

    platform class
    * a platform
    
]]

Platform = Class{}

function Platform:init(def)

    -- position
    self.x = def.x
    self.y = VIRTUAL_HEIGHT - 1  -- just above bottom
    -- dimensions
    self.width = PLATFORM_WIDTH
    self.height = PLATFORM_HEIGHT
    -- speed
    self.dx = PLATFORM_SPEED_X * math.random(-1, 1)  -- random x direction
    self.dy = -math.abs(def.dy)  -- always going up

    -- platform graphic
    self.graphic = math.random(1, 2)

end


function Platform:update(dt)
    
    -- position
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt

end


function Platform:render()

    -- do not render picture in debug mode
    if DEBUG_MODE == false then
    
        love.graphics.setColor(1, 1, 1, 1)
        love.graphics.draw(
            gTextures['grassPlatform'],  -- texture
            gFrames['grassPlatform'][self.graphic],  -- quad
            self.x, self.y, 0,  -- position, rotation
            self.width/PLATFORM_GRAPHIC_WIDTH, self.height/PLATFORM_GRAPHIC_HEIGHT  -- scale
        )

    end

    -- black outline
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.rectangle(
        "line",  -- mode
        self.x, self.y,  -- position
        self.width, self.height  -- dimensions
    )

end