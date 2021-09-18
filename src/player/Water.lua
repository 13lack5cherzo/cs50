--[[

    Drop Fish
    developed by Dan Chan

    water class
    (particle rendering)

]]

Water = Class{}

function Water:init(def)

    -- position
    self.x = def.x
    self.y = def.y

    -- init particle settings
    self.psystem = love.graphics.newParticleSystem(
        gTextures['particle'],
        PT_NUM  -- maximum number of particles at once
    )

    -- duration (seconds)
    self.psystem:setParticleLifetime(
        PT_LIFE_BEG,  -- min
        PT_LIFE_END  -- max
    )

    -- particle spread
    self.psystem:setEmissionArea(
        "normal",  -- distribution
        PT_STD_ERR_X, PT_STD_ERR_Y  -- standard deviation (x, y)
    )

end


function Water:update(dt)

    -- set particle accelration
    self.psystem:setLinearAcceleration(
        -PT_ACC_X * dt,  -- minimum acceleration along the x axis
        PT_ACC_YMIN * dt,  -- minimum acceleration along the y axis
        PT_ACC_X * dt,  -- maximum acceleration along the x axis
        PT_ACC_YMAX * dt  -- maximum acceleration along the y axis
    )

    self.psystem:update(dt)
end


function Water:render()
    love.graphics.setColor(BOWL_R, BOWL_G, BOWL_B, PT_ALPHA)
    love.graphics.draw(self.psystem, self.x, self.y)
end


function Water:spill(x, y)

    -- position
    self.x, self.y = x, y

    -- random direction
    self.psystem:setDirection(degToRad(math.random(0, 360)))

    -- colour
    self.psystem:setColors(
        BOWL_R, BOWL_G, BOWL_B, PT_ALPHA,
        BOWL_R, BOWL_G, BOWL_B, PT_ALPHA,
        BOWL_R, BOWL_G, BOWL_B, PT_ALPHA
    )
    self.psystem:emit(math.random(0, PT_NUM))

end
