--[[

    Drop Fish
    developed by Dan Chan

    platform generator class
    * spawn platforms
    * despawn platforms
    
]]

PlatformGenerator = Class{}

function PlatformGenerator:init()

    -- init empty platform table
    self.platforms = {}

    -- timer
    self.timer = 0

    -- average platform generation rate (per second)
    self.generationRate = AVE_PLAT_GEN_RATE  -- higher -> faster
    -- random change to platform generation rate
    self.genRand = RAND_PLAT_GEN_RATE  -- higher -> more random

    -- platform speed
    self.platSpeedY = PLATFORM_SPEED_Y  -- higher -> faster
    -- platform speed randomness
    self.speedRand = PLAT_SPEED_RAND  -- higher -> more random

    -- maximum platforms in a row
    self.rowMaxPlatforms = VIRTUAL_WIDTH / PLATFORM_WIDTH
    -- cap on number of platforms in a row
    self.PlatRowCap = PLAT_ROW_CAP  -- higher -> more platforms
    -- percentage of missing platforms (init as zero for starting midpoint platforms)
    self.percPlatMissing = 0  -- %  higher -> fewer platforms
    -- spawn more platforms if less were spawned previously
    self.percPlatDamp = PERC_PLAT_MISSING_DAMP  -- [0, 1]. higher -> more regular platforms
    -- array to keep track of previous x horizontal spawn position
    self:initStartPlatforms()

    -- speed increment
    self.speedIncrement = 1 + PLAT_INCREMENT/100

end


function PlatformGenerator:update(dt)

    -- generate platforms
    self:generate(dt)

    -- update platforms
    for k, platform1 in pairs(self.platforms) do
        platform1:update(dt)
    end

    -- despawn platforms that are off screen
    self:despawn(dt)

end


function PlatformGenerator:render(dt)
    for k, platform1 in pairs(self.platforms) do
        platform1:render()
    end
end


function PlatformGenerator:initStartPlatforms()
    -- function to identify middle platforms

    self.prevSpawnX = {}  -- init empty

    local midPointStart = 0
    local midPointEnd = 0

    midPointStart, midPointEnd = returnMidPoint(self.rowMaxPlatforms)

    for xIdx = 0, self.rowMaxPlatforms - 1 do
        if (xIdx == midPointStart-1) or (xIdx == midPointEnd-1) then
            self.prevSpawnX[xIdx] = false  -- init midpoints as false
        else
            self.prevSpawnX[xIdx] = true
        end
    end
end


function PlatformGenerator:generate(dt)

    if self.timer > 1 then  -- time to spawn a platform row

        --
        -- row spawn start
        --

        -- init to keep track of platforms spawned for the row
        local rowPlatformsSpawned = 0

        -- at all the possible platform positions,
        for xIdx = 0, self.rowMaxPlatforms - 1 do

            --
            -- column spawn start
            --

            -- if not at the platform cap and no platform was spawned in the same column
            if (rowPlatformsSpawned < self.PlatRowCap) and (not self.prevSpawnX[xIdx]) then

                -- at randomly selected positions,
                if (math.random(0, 100) > self.percPlatMissing) then

                    -- generate platform
                    table.insert(
                        self.platforms, 
                        Platform {
                            x = xIdx * PLATFORM_WIDTH,
                            dy = self.platSpeedY * (1 + math.random(-100, 100)/100 * self.speedRand)
                        }
                    )

                    -- increase speed of generation and platform after a platform spawns
                    if self.platSpeedY < PLATFORM_SPEED_YMAX then
                        self.platSpeedY = self.platSpeedY * self.speedIncrement
                        self.generationRate = self.generationRate * self.speedIncrement
                    end

                    -- keep track of that platform was spawned at x horizontal position
                    self.prevSpawnX[xIdx] = true
                    -- increment number of platforms spawned for the row
                    rowPlatformsSpawned = rowPlatformsSpawned + 1

                    if DEBUG_MODE then 
                        print(
                            "platform spawn: position=" .. tostring(xIdx) 
                            .. ", prob=" .. tostring(self.percPlatMissing) 
                            .. ", speed=" .. tostring(self.platSpeedY))
                    end

                end
            
            else

                -- keep track of that no platform was spawned at x horizontal position
                self.prevSpawnX[xIdx] = false
                
            end

            --
            -- column spawn end
            --

            -- increase probability of platform spawn if none spawned for the row
            if rowPlatformsSpawned == 0 then
                self.percPlatMissing = self.percPlatMissing * (1 - self.percPlatDamp)
            else  -- return probability back to normal
                self.percPlatMissing = PERC_PLAT_MISSING
            end

        end

        --
        -- row spawn end
        --

        -- reset timer
        self.timer = self.timer - 1  
        -- add randomness to period between platform spawn
        self.timer = self.timer + math.random(-100, 100)/100 * self.genRand

    end

    -- update timer
    self.timer = self.timer + dt * self.generationRate  

end


function PlatformGenerator:despawn(dt)

    for k, platform1 in pairs(self.platforms) do
        -- check if platform is off screen and
        if Background:offScreen(platform1) then
            table.remove(self.platforms, k)  -- remove if so
            if DEBUG_MODE then print("platform despawned") end
        end
    end

end