--[[

    Drop Fish
    developed by Dan Chan

    text platform class
    * class to make texts behave like platforms

]]

TextPlatform = Class{}

function TextPlatform:init(def)

    -- init empty platform table
    self.platforms = {}

    -- information of platforms to init
    self.platformInfo = def.platformInfo

    -- working platform placeholder
    self.workingPlatform = {}

end


function TextPlatform:update(dt)
    -- does not update
end


function TextPlatform:render()
    -- for debug only
    for k, platform1 in pairs(self.platforms) do
        platform1:render()
    end
end


function TextPlatform:generate()
    -- function to generate stationary platforms

    for k, info1 in pairs(self.platformInfo) do

        -- init new platform
        self.workingPlatform = Platform {
            x = info1.x,  -- x position
            dy = 0  -- not moving
        }
        
        -- change more platform attributes
        self.workingPlatform.y = info1.y
        self.workingPlatform.width = info1.width
        self.workingPlatform.height = info1.height

        -- add platform to platform table
        table.insert(self.platforms, self.workingPlatform)
        self.workingPlatform = {}  -- clear variable

    end
end


function TextPlatform:despawnAll()
    -- function to despawn all stationary platforms
    self.platforms = {}
end