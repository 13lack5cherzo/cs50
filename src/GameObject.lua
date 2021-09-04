--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

GameObject = Class{}

function GameObject:init(def, x, y)
    
    -- string identifying this object type
    self.type = def.type

    self.texture = def.texture
    self.frame = def.frame or 1

    -- whether it acts as an obstacle or not
    self.solid = def.solid

    self.defaultState = def.defaultState
    self.state = self.defaultState
    self.states = def.states

    -- dimensions
    self.x = x
    self.y = y
    self.width = def.width
    self.height = def.height
    -- velocity
    self.dx = def.dx or 0
    self.dy = def.dy or 0

    -- collision callback (default empty)
    self.onCollide = def.onCollide or function(_player) end

    -- remove object when collided with
    self.consumable = def.consumable or false

    -- distance for interaction (0 means no interaction allowed)
    self.interactRange = def.interactRange or 0
    -- interaction callback (default empty)
    self.onInteract = def.onInteract or function(_player) end
    -- track player on interaction
    self.interactTrack = def.interactTrack or false
    self.trackOffsetX = def.trackOffsetX or 0
    self.trackOffsetY = def.trackOffsetY or 0

    -- projectile flag
    self.isProjectile = def.isProjectile or false
    -- projectile speed
    self.projectileSpeed = def.projectileSpeed or 0
    --projectile max distance
    self.projectileMaxDist = def.projectileMaxDist or 0
    -- projectile boundaries
    self.projectileBoundLeft = MAP_RENDER_OFFSET_X + TILE_SIZE
    self.projectileBoundRight = VIRTUAL_WIDTH - TILE_SIZE * 2 - self.width
    self.projectileBoundTop = MAP_RENDER_OFFSET_Y + TILE_SIZE
    self.projectileBoundBottom = VIRTUAL_HEIGHT - (VIRTUAL_HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - self.width

end

function GameObject:inRoom()
    -- function to check if object is within the room boundaries
    if (self.x < self.projectileBoundLeft)
        or (self.x > self.projectileBoundRight)
        or (self.y < self.projectileBoundTop)
        or (self.y > self.projectileBoundBottom) 
        then
        return false
    else
        return true
    end
end

function GameObject:projectileDistMax()
    -- function to check if projectile object 
    -- has exceeded maximum distance
    if (math.abs(self.projectileStartX - self.x) > self.projectileMaxDist)
        or (math.abs(self.projectileStartY - self.y) > self.projectileMaxDist) 
        then
        return true
    else
        return false
    end
end


function GameObject:update(dt)
    self.x = self.x + self.dx * dt
    self.y = self.y + self.dy * dt
end

function GameObject:render(adjacentOffsetX, adjacentOffsetY)
    love.graphics.draw(gTextures[self.texture], gFrames[self.texture][self.states[self.state].frame or self.frame],
        self.x + adjacentOffsetX, self.y + adjacentOffsetY)

    
    if DEBUG_MODE then
        
        love.graphics.setColor(255, 0, 255, 255)
        -- object
        love.graphics.rectangle(
            'line', 
            self.x,  -- xloc
            self.y,  -- yloc
            self.width,  -- width
            self.height  -- height
        )

        -- projectile bounds
        love.graphics.rectangle(
            'line', 
            self.projectileBoundLeft,  -- xloc
            self.projectileBoundTop,  -- yloc
            self.projectileBoundRight - self.projectileBoundLeft,  -- width
            self.projectileBoundBottom - self.projectileBoundTop  -- height
        )
        love.graphics.setColor(255, 255, 255, 255)
    end

end