--[[
    GD50
    Legend of Zelda

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

Player = Class{__includes = Entity}

function Player:init(def)
    Entity.init(self, def)
end

function Player:update(dt)
    Entity.update(self, dt)
end

function Player:collides(target)
    local selfY, selfHeight = self.y + self.height / 2, self.height - self.height / 2
    
    return not (self.x + self.width < target.x or self.x > target.x + target.width or
                selfY + selfHeight < target.y or selfY > target.y + target.height)
end

function Player:displace(target)
    --[[
        function to displace player when colliding with a solid object
    ]]
    -- stop player from moving through solid object
    -- displace player so there is no more collision
    if self.direction == "right" then  -- left collision
        self.x = self.x - 1
    elseif self.direction == "left" then  --right collision
        self.x = self.x + 1
    elseif self.direction == "up" then  -- bottom collision
        self.y = self.y + 1
    elseif self.direction == "down" then  -- top collision
        self.y = self.y - 1  
    else  -- force player out
        self.x = self.x - 1
        self.y = self.y + 1
    end
end

function Player:canInteract(target)
    --[[
        function to returning true if 
            * object can be interacted with
            * player is in object's interaction range
    ]]
    if target.interactRange == 0 then
        return false
    else
        local selfY, selfHeight = self.y + self.height / 2, self.height - self.height / 2
        canInteract = not (
            self.x + self.width < target.x - target.interactRange 
            or self.x > target.x + target.width + target.interactRange  
            or selfY + selfHeight < target.y - target.interactRange  
            or selfY > target.y + target.height + target.interactRange 
        )
        return canInteract
    end
end

function Player:render()
    Entity.render(self)
    
    -- love.graphics.setColor(255, 0, 255, 255)
    -- love.graphics.rectangle('line', self.x, self.y, self.width, self.height)
    -- love.graphics.setColor(255, 255, 255, 255)
end