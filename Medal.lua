--[[
    Medal Class

    show medal, as a function of score
]]

Medal = Class{}

local MEDAL0_IMAGE = {
    ["image"] = love.graphics.newImage('medal0.png'),
    ["width"] = 38,
    ["height"] = 38
}
local MEDAL1_IMAGE = {
    ["image"] = love.graphics.newImage('medal1.png'),
    ["width"] = 38,
    ["height"] = 38
}
local MEDAL2_IMAGE = {
    ["image"] = love.graphics.newImage('medal2.png'),
    ["width"] = 38,
    ["height"] = 38
}

local GRAVITY = 40

function Medal:init(score)
    self.x = VIRTUAL_WIDTH / 5
    self.y = VIRTUAL_HEIGHT / 2

    self.score = score
    self.width = 0  -- init with 0
    self.height = 0  -- init with 0

    self.bounceTimer = 0
    self.dx = GRAVITY
end


function Medal:update(dt)
    -- bouncing medal
    self.bounceTimer = self.bounceTimer + dt  -- timer
    
    if self.bounceTimer > 2 then  -- every few seconds,
        self.dx = (self.dx > 0 and -1 or 1) * GRAVITY  -- change direction
        self.bounceTimer = 0  -- reset timer
    end
    self.dx = self.dx + self.dx * dt  -- acceleration
    self.x = self.x + self.dx * dt  -- move
end

function Medal:render()
    -- image dependent on score
    if self.score == 0 then
        self.image = MEDAL0_IMAGE
    elseif self.score == 1 then
        self.image = MEDAL1_IMAGE
    else
        self.image = MEDAL2_IMAGE
    end
    
    self.width = self.image["width"]
    self.height = self.image["height"]
    
    love.graphics.draw(self.image["image"], self.x, self.y - self.height / 2 - 5)
end