--[[

    Drop Fish
    developed by Dan Chan

    background class

    texture specification:
    * aspect ratio: 9:16 (1080p)
    * repeat at BACKGROUND_RESET_POINT (in pixels)
    
]]

Background = Class{}

function Background:init(def)

    -- texture
    self.texture = getRandomTableElement(gBackgroundTextures)
    -- position
    self.x = 0
    self.y = def.y and def.y or 0
    -- scaling dimensions
    self.width = VIRTUAL_WIDTH / self.texture:getWidth()
    self.height = VIRTUAL_HEIGHT / BACKGROUND_SCALE_HEIGHT

    -- background scroll speed (upwards)
    self.scrollSpeed = -math.abs(BACKGROUND_SCROLL_SPD)  -- higher -> faster
    -- background reset point
    self.resetPoint = BACKGROUND_RESET_POINT * self.height


end


function Background:update(dt)

    self.y = (self.y - self.scrollSpeed * dt) % self.resetPoint

end


function Background:render()

    -- clear background
    love.graphics.setColor(0, 0, 0, 1)
    love.graphics.rectangle("fill", self.x, self.y, self.width, self.height)

    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.draw(
        self.texture,  -- texture
        self.x, -self.y, 0,  -- position, rotation
        self.width, self.height  -- scale
    )


end


function Background:offScreen(entity)
    -- function to detect if an entity is off-screen
    if (
        (entity.x > VIRTUAL_WIDTH)  -- right
        or (entity.x + entity.width < 0)  -- left
        or (entity.y > VIRTUAL_HEIGHT) -- bottom
        or (entity.y + entity.height < 0)  -- top
    ) then
        return true
    else
        return false
    end
end
