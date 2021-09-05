--[[
    GD50
    Pokemon

    Author: Colton Ogden
    cogden@cs50.harvard.edu
]]

BattleLevelupState = Class{__includes = BaseState}

function BattleLevelupState:init(battleState, statIncrease)
    self.battleState = battleState

    self.menuWidth = 14*TILE_SIZE
    self.menuHeight = 8*TILE_SIZE

    self.statNames = {  -- pokemon stat names
        [1] = "HP",
        [2] = "attack",
        [3] = "defense",
        [4] = "speed"
    }

    self.statAfter = {  -- pokemon stats after level up
        ["HP"] = self.battleState.player.party.pokemon[1].HP,
        ["attack"] = self.battleState.player.party.pokemon[1].attack,
        ["defense"] = self.battleState.player.party.pokemon[1].defense,
        ["speed"] = self.battleState.player.party.pokemon[1].speed
    }

    -- function to go back to field (on select)
    self.backToField = function()
        -- pop battle menu
        gStateStack:pop()

        -- resume field music
        gSounds['victory-music']:stop()
        gSounds['field-music']:play()

        -- pop battle state
        gStateStack:pop()

        gStateStack:push(FadeOutState({
            r = 1, g = 1, b = 1
        }, 1, function()
        -- do nothing after fade out ends
        end))
    end

    self.LevelupMenu = Menu {

        width = self.menuWidth,
        height = self.menuHeight,
        x = VIRTUAL_WIDTH - self.menuWidth,  -- top
        y = VIRTUAL_HEIGHT - self.menuHeight - 4*TILE_SIZE,  -- right, adjusted down slightly

        noCursor = true,
        items = {
            {
                text = self.statNames[1] .. ": " .. 
                    self.statAfter[self.statNames[1]] - statIncrease[self.statNames[1]] .. " + " .. 
                    statIncrease[self.statNames[1]] .. " = " .. 
                    self.statAfter[self.statNames[1]],
                onSelect = self.backToField
            },
            {
                text = self.statNames[2] .. ": " .. 
                    self.statAfter[self.statNames[2]] - statIncrease[self.statNames[2]] .. " + " .. 
                    statIncrease[self.statNames[2]] .. " = " .. 
                    self.statAfter[self.statNames[2]],
                onSelect = self.backToField
            },
            {
                text = self.statNames[3] .. ": " .. 
                    self.statAfter[self.statNames[3]] - statIncrease[self.statNames[3]] .. " + " .. 
                    statIncrease[self.statNames[3]] .. " = " .. 
                    self.statAfter[self.statNames[3]],
                onSelect = self.backToField
            },
            {
                text = self.statNames[4] .. ": " .. 
                    self.statAfter[self.statNames[4]] - statIncrease[self.statNames[4]] .. " + " .. 
                    statIncrease[self.statNames[4]] .. " = " .. 
                    self.statAfter[self.statNames[4]],
                onSelect = self.backToField
            },
        }
    }
end


function BattleLevelupState:update(dt)
    self.LevelupMenu:update(dt)
end

function BattleLevelupState:render()
    self.LevelupMenu:render()
end