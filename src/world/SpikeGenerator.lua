--[[

    Drop Fish
    developed by Dan Chan

    spike generator class
    * spawn spikes
    * despawn spikes

]]


SpikeGenerator = Class{}

function SpikeGenerator:init()

    -- init empty spike table
    self.spikes = {}

    -- timer
    self.timer = 0

    -- average spike generation rate (per second)
    self.generationRate = SPIKE_GEN_RATE  -- higher -> faster    
    -- random change to spike generation rate
    self.genRand = RAND_SPIKE_GEN_RATE  -- higher -> more random

end


function SpikeGenerator:update(dt)


    self:generate(dt)

    -- update platforms
    for k, spike1 in pairs(self.spikes) do
        spike1:update(dt)
    end



end


function SpikeGenerator:render(dt)
    for k, spike1 in pairs(self.spikes) do
        spike1:render()
    end
end


function SpikeGenerator:generate(dt)

    if self.timer > 1 then

        -- generate spike
        table.insert(
            self.spikes, 
            Spike {
                x = math.random(0, VIRTUAL_WIDTH - SPIKE_SIZE)
            }
        )

        if DEBUG_MODE then print("spike spawned") end

        -- reset timer
        self.timer = self.timer - 1  
        -- add randomness to period between spike spawn
        self.timer = self.timer + math.random(-100, 100)/100 * self.genRand

    end

    -- update timer
    self.timer = self.timer + dt * self.generationRate

end


function SpikeGenerator:despawn(dt)

    for k, spike1 in pairs(self.spikes) do
        -- check if platform is off screen and
        if Background:offScreen(spike1) then
            table.remove(self.spikes, k)  -- remove if so
            if DEBUG_MODE then print("spike despawned") end
        end
    end

end