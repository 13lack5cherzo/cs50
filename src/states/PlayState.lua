--[[
    GD50
    Breakout Remake

    -- PlayState Class --

    Author: Colton Ogden
    cogden@cs50.harvard.edu

    Represents the state of the game in which we are actively playing;
    player should control the paddle, with the ball actively bouncing between
    the bricks, walls, and the paddle. If the ball goes below the paddle, then
    the player should lose one point of health and be taken either to the Game
    Over screen if at 0 health or the Serve screen otherwise.
]]

PlayState = Class{__includes = BaseState}

--[[
    We initialize what's in our PlayState via a state table that we pass between
    states as we go from playing to serving.
]]
function PlayState:enter(params)
    self.paddle = params.paddle
    self.bricks = params.bricks
    self.health = params.health
    self.score = params.score
    self.highScores = params.highScores
    self.balls = params.balls
    self.level = params.level

    self.recoverPoints = params.recoverPoints

    -- give first ball random starting velocity
    self.ballsCount = 1  -- start with 1 ball
    self.balls[0].dx = math.random(-200, 200)
    self.balls[0].dy = math.random(-50, -60)
    
    self.powerup = Powerup()  -- only 1 powerup

    self.bricksLocked = true  -- bricks start locked

    self.autoplay = false  -- autoplay
end

function PlayState:update(dt)
    if self.paused then
        if love.keyboard.wasPressed('space') then
            self.paused = false
            gSounds['pause']:play()
        else
            return
        end
    elseif love.keyboard.wasPressed('space') then
        self.paused = true
        gSounds['pause']:play()
        return
    end

    -- update positions based on velocity
    self.paddle:update(dt, self.score, self.health)  -- modified to rely on score and health
    for bidx = 0, 2 do  -- update all balls
        self.balls[bidx]:update(dt)
    end

    -- powerup update
    if (self.ballsCount > 1) and (self.bricksLocked == true) then
        -- if more than 1 ball in play and bricks are locked
        self.powerup:update(dt, 2)  -- only spawn key powerup
    elseif self.ballsCount == 1 then
        self.powerup:update(dt, 1)  -- only spawn ball powerup
    end

    if self.autoplay then
        self.paddle.dx = -1

        lowestY = 0  -- get ball at the lowest position
        for bidx = 0, 2 do
            if self.balls[bidx].y > lowestY then
                lowestY = self.balls[bidx].y
                lowestBallIdx = bidx
            end
        end
        self.paddle.x =  math.min(  -- match paddle position
            VIRTUAL_WIDTH - self.paddle.width, 
            self.balls[lowestBallIdx].x
        ) -- toggle autoplay
        if love.keyboard.wasPressed('a') then
            self.autoplay = false
        end
    elseif love.keyboard.wasPressed('a') then
            self.autoplay = true
    end

    for bidx = 0, 2 do
        if self.balls[bidx]:collides(self.paddle) then
            -- raise ball above paddle in case it goes below it, then reverse dy
            self.balls[bidx].y = self.paddle.y - 8
            self.balls[bidx].dy = -self.balls[bidx].dy

            --
            -- tweak angle of bounce based on where it hits the paddle
            --

            -- if we hit the paddle on its left side while moving left...
            if self.balls[bidx].x < self.paddle.x + (self.paddle.width / 2) and self.paddle.dx < 0 then
                self.balls[bidx].dx = -50 + -(8 * (self.paddle.x + self.paddle.width / 2 - self.balls[bidx].x))
            
            -- else if we hit the paddle on its right side while moving right...
            elseif self.balls[bidx].x > self.paddle.x + (self.paddle.width / 2) and self.paddle.dx > 0 then
                self.balls[bidx].dx = 50 + (8 * math.abs(self.paddle.x + self.paddle.width / 2 - self.balls[bidx].x))
            end

            gSounds['paddle-hit']:play()
        end
    end

    -- detect collision across all bricks with the ball
    for k, brick in pairs(self.bricks) do
        for bidx = 0, 2 do  -- for each ball
            -- only check collision if we're in play
            if brick.inPlay and self.balls[bidx]:collides(brick) then
                
                if brick.locked == false then  -- no points if brick is locked
                    -- add to score
                    self.score = self.score + (brick.tier * 200 + brick.color * 25)
                end

                -- trigger the brick's hit function, which removes it from play
                brick:hit()

                -- if we have enough points, recover a point of health
                if self.score > self.recoverPoints then
                    -- can't go above 3 health
                    self.health = math.min(3, self.health + 1)

                    -- multiply recover points by 2
                    self.recoverPoints = self.recoverPoints + math.min(100000, self.recoverPoints * 2)

                    -- play recover sound effect
                    gSounds['recover']:play()
                end

                -- go to our victory screen if there are no more bricks left
                if self:checkVictory() then
                    gSounds['victory']:play()

                    gStateMachine:change('victory', {
                        level = self.level,
                        paddle = self.paddle,
                        health = self.health,
                        score = self.score,
                        highScores = self.highScores,
                        balls = self.balls,
                        recoverPoints = self.recoverPoints
                    })
                end

                --
                -- collision code for bricks
                --
                -- we check to see if the opposite side of our velocity is outside of the brick;
                -- if it is, we trigger a collision on that side. else we're within the X + width of
                -- the brick and should check to see if the top or bottom edge is outside of the brick,
                -- colliding on the top or bottom accordingly 
                --

                -- left edge; only check if we're moving right, and offset the check by a couple of pixels
                -- so that flush corner hits register as Y flips, not X flips
                if self.balls[bidx].x + 2 < brick.x and self.balls[bidx].dx > 0 then
                    
                    -- flip x velocity and reset position outside of brick
                    self.balls[bidx].dx = -self.balls[bidx].dx
                    self.balls[bidx].x = brick.x - 8
                
                -- right edge; only check if we're moving left, , and offset the check by a couple of pixels
                -- so that flush corner hits register as Y flips, not X flips
                elseif self.balls[bidx].x + 6 > brick.x + brick.width and self.balls[bidx].dx < 0 then
                    
                    -- flip x velocity and reset position outside of brick
                    self.balls[bidx].dx = -self.balls[bidx].dx
                    self.balls[bidx].x = brick.x + 32
                
                -- top edge if no X collisions, always check
                elseif self.balls[bidx].y < brick.y then
                    
                    -- flip y velocity and reset position outside of brick
                    self.balls[bidx].dy = -self.balls[bidx].dy
                    self.balls[bidx].y = brick.y - 8
                
                -- bottom edge if no X collisions or top collision, last possibility
                else
                    
                    -- flip y velocity and reset position outside of brick
                    self.balls[bidx].dy = -self.balls[bidx].dy
                    self.balls[bidx].y = brick.y + 16
                end

                -- slightly scale the y velocity to speed up the game, capping at +- 150
                if math.abs(self.balls[bidx].dy) < 150 then
                    self.balls[bidx].dy = self.balls[bidx].dy * 1.02
                end

                -- only allow colliding with one brick, for corners
                break
            end
        end
    end

    -- collide with powerup
    if self.powerup:collides(self.paddle) then
        self.powerup:despawn()
        if self.powerup.type == 1 then  -- ball powerup
            self.ballsCount = self.ballsCount + 2  -- increase ball count
            for bidx = 0, 2 do  -- get location of ball currently in play
                if self.balls[bidx].inPlay then
                    ballsLocationX = self.balls[bidx].x
                    ballsLocationY = self.balls[bidx].y
                end
            end
            for bidx = 0, 2 do
                -- give all balls a random velocity
                self.balls[bidx].dx = math.random(100, 200) * (math.random(0, 1) == 0 and -1 or 1)
                self.balls[bidx].dy = math.random(100, 200) * (math.random(0, 1) == 0 and -1 or 1)
                -- all at the same location
                self.balls[bidx].x = ballsLocationX
                self.balls[bidx].y = ballsLocationY
                self.balls[bidx].inPlay = true  -- set in play
            end
        elseif self.powerup.type == 2 then  -- brick powerup
            self.bricksLocked = false  -- change flag
            for k, brick in pairs(self.bricks) do  -- unlock all bricks
                brick:unlock()
            end
        end
    end


    -- if ball goes below bounds, despawn
    for bidx = 0, 2 do
        if self.balls[bidx].y >= VIRTUAL_HEIGHT then
            self.balls[bidx]:despawn()
            self.ballsCount = self.ballsCount - 1
        end
    end

    -- if ball goes below bounds, revert to serve state and decrease health
    if self.ballsCount <= 0 then
        self.health = self.health - 1
        gSounds['hurt']:play()

        if self.health == 0 then
            gStateMachine:change('game-over', {
                score = self.score,
                highScores = self.highScores
            })
        else
            gStateMachine:change('serve', {
                paddle = self.paddle,
                bricks = self.bricks,
                health = self.health,
                score = self.score,
                highScores = self.highScores,
                level = self.level,
                recoverPoints = self.recoverPoints
            })
        end
    end

    -- for rendering particle systems
    for k, brick in pairs(self.bricks) do
        brick:update(dt)
    end

    if love.keyboard.wasPressed('escape') then
        love.event.quit()
    end
end

function PlayState:render()
    -- render bricks
    for k, brick in pairs(self.bricks) do
        brick:render()
    end

    -- render all particle systems
    for k, brick in pairs(self.bricks) do
        brick:renderParticles()
    end

    self.paddle:render()
    for bidx = 0, 2 do  -- for each ball
        self.balls[bidx]:render()
    end
    self.powerup:render()

    renderScore(self.score)
    renderHealth(self.health)

    -- pause text, if paused
    if self.paused then
        love.graphics.setFont(gFonts['large'])
        love.graphics.printf("PAUSED", 0, VIRTUAL_HEIGHT / 2 - 16, VIRTUAL_WIDTH, 'center')
    end

    -- pause text, if paused
    if self.autoplay then
        love.graphics.setFont(gFonts['small'])
        love.graphics.printf("autoplay: on", 16, VIRTUAL_HEIGHT - 16, VIRTUAL_WIDTH, 'left')
    end

end

function PlayState:checkVictory()
    for k, brick in pairs(self.bricks) do
        if brick.inPlay then
            return false
        end 
    end

    return true
end