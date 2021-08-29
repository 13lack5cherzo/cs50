
Lock = Class{__includes = GameObject}

function Lock:init(def)
    self.name = "lock"
    self.x = def.x
    self.y = def.y
    self.texture = 'keysLocks'
    self.width = def.width
    self.height = def.height
    self.frame = def.frame + 4  -- lock texture is 4 away from key
    self.solid = true
    self.collidable = true
    self.consumable = false
    self.hit = false
    self.renderFlag = true

    self.onCollide = function(obj)  -- placeholder
        return 0
    end
    self.onConsume = function(player1)  -- placeholder
        return 0
    end




end





Key = Class{__includes = GameObject}

function Key:init(def)
    self.x = def.x
    self.y = def.y
    self.texture = 'keysLocks'
    self.width = def.width
    self.height = def.height
    self.frame = def.frame
    self.solid = false
    self.collidable = true
    self.consumable = true
    self.hit = false
    self.renderFlag = true

    self.onCollide = function(obj)
        return 0
    end
    self.onConsume = function(player1)
        gSounds['key']:play()
        -- remove the lock block
        for k1, object in pairs(player1.level.objects) do
            if object.name == "lock" then  -- remove the locked block
                player1.level.objects[k1] = nil
            elseif object.name == "post" then  -- make the post:
                player1.level.objects[k1].renderFlag = true  -- render
                player1.level.objects[k1].collidable = true  -- consumable
                player1.level.objects[k1].consumable = true  -- consumable
            elseif object.name == "flag" then  -- make the flag:
                player1.level.objects[k1].renderFlag = true  -- render
            end  -- key is "consumed" as per implementation in player.lua
        end
    end


end

