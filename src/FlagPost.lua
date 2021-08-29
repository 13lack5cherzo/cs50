

Post = Class{__includes = GameObject}

function Post:init(def)

    self.name = "post"
    self.x = def.x
    self.y = (GROUND_BLOCK_N - 1 - 3) * TILE_SIZE  -- pole at ground level
    self.texture = "posts"
    self.width = TILE_SIZE
    self.height = 3 * TILE_SIZE
    self.frame = math.random(1, 6)  -- random flag colour
    self.solid = false
    self.collidable = false
    self.consumable = false
    self.hit = false
    self.renderFlag = false

    self.onCollide = function(obj)  -- placeholder
        return 0
    end
    self.onConsume = function(player1)  -- go to next level
        player1.nextLevelFlag = true  -- change player object flag
    end


end

--[[
    function to get right-most coordinate with solid ground (not column)
]]
function Post:getPoleLoc(tiles, objects, width, blankHeight, maxSearchx)
    spawn_x = 1
    for x = 1, maxSearchx do  -- iterate horizontally through game grid (column-wise search)
        if (tiles[GROUND_BLOCK_N][width - x].id == TILE_ID_GROUND) then  -- check that ground-level is ground
            requiredBlanks = true  -- then ensure that, from blankHeight (top) to just above GROUND_BLOCK_N,
            for y = blankHeight, (GROUND_BLOCK_N-1) do  -- is all blank
                if (tiles[y][width - x].id ~= TILE_ID_EMPTY) then
                    requiredBlanks = false
                    break
                end
            end
            for k, object in pairs(objects) do  -- no objects in the way
                if (object.x - (width - x - 1) * TILE_SIZE >= 0) 
                and (object.x - (width - x - 1) * TILE_SIZE < 2*TILE_SIZE) -- 1 space left also
                then
                    requiredBlanks = false
                    break
                end
            end
            if requiredBlanks then
                spawn_x = x
                break
            end
        end
    end
    return (width - spawn_x - 1) * TILE_SIZE  -- multiply by tile size
end




Flag = Class{__includes = GameObject}

function Flag:init(def)
    self.name = "flag"
    self.x = def.x + TILE_SIZE/2  -- offset flag location slightly (looks nicer)
    self.y = (GROUND_BLOCK_N - 1 - 3) * TILE_SIZE + 3  -- flag slightly lower
    self.texture = "flags"
    self.width = TILE_SIZE
    self.height = 3 * TILE_SIZE
    self.frame = math.random(1, 4)*9 - 2  -- use indices 7, 16, 25, 34
    self.solid = false
    self.collidable = false
    self.hit = false
    self.renderFlag = false

    self.onCollide = function(obj)  -- placeholder
        return 0
    end
    self.onConsume = function(player1)  -- placeholder
        return 0
    end
end

