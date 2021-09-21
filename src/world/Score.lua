--[[

    Drop Fish
    developed by Dan Chan

    score class

]]

Score = Class{}

-- global variable for high score
highScore = 0  -- init zero

function Score:init()

    -- keep track of score
    self.score = 0  -- init zero
    -- timer
    self.timer = 0  -- init zero
    -- score increment tick rate (per second)
    self.scoreRate = SCORE_TICK_RATE  -- tick/second
    -- score increment amount
    self.scoreIncrement = SCORE_TICK_INCR  -- score/tick
    -- score tick randomness (possible random extra points per tick)
    self.scoreRand = SCORE_TICK_RAND

    -- score as string format to display
    self.scoreString = formatInt(self.score)

end


function Score:update(dt)

    if self.timer > 1 then

        -- increment score
        self.score = self.score + self.scoreIncrement
        -- add randomness (rounded to nearest int)
        self.score = self.score + math.floor(math.random(0, 100)/100 * self.scoreRand + 0.5)
        -- format into string
        self.scoreString = formatInt(self.score)

        -- update high score
        if self.score > highScore then
            highScore = self.score
        end

        -- reset timer
        self.timer = self.timer - 1  
        -- add randomness to period between platform spawn
        self.timer = self.timer

    end

    -- update timer
    self.timer = self.timer + dt * self.scoreRate

end


function Score:render(scoreString, renderScoreText)

    local printString = scoreString

    -- additional text to render
    if renderScoreText then  
        printString = "SCORE " .. printString

    -- print high score
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_large'])
    love.graphics.printf(
        "BEST ".. formatInt(highScore),  -- text
        0,  -- x
        FONT_L,  -- y
        VIRTUAL_WIDTH,  -- limit
        'right'  -- align
    )

    end

    -- print current score string
    love.graphics.setColor(1, 1, 1, 1)
    love.graphics.setFont(gFonts['flappy_large'])
    love.graphics.printf(
        printString,  -- text
        0,  -- x
        0,  -- y
        VIRTUAL_WIDTH,  -- limit
        'right'  -- align
    )
    

end


