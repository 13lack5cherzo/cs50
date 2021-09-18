# DROP FISH
---

## A fish in a bowl plummets to uncertain doom.

## But, by bouncing on platforms and avoiding spikes, it may live!

---

<div style="text-align: right"> Developed by Dan Chan </div>

## Description

The game is an endless 2D platformer, where the player is in control of a fish in a fish bowl.
> **Goal**: Survive as long as possible. <br/>
> **Losing Conditions**: Fish bowl leaves the game area or hits a spike. <br/>
> **Scoring**: Points are awarded based on the time survived. <br/>
> **Controls**: Left/right arrow keys to steer, up/down arrow keys to control fall. <br/>

---

## Repository Structure
```
./
    fonts/
    graphics/
    lib/
        knife/
        class.lua
        push.lua
    sounds/
    src/
        player/
            Fish.lua
            Player.lua
            Water.lua
        states/
            game/
                GameOverState.lua
                PlayState.lua
                StartState.ua
            BaseState.lua
            StateStack.lua
        util/
            Constants.lua
            Dependencies.lua
            Util.lua
        world/
            Background.lua
            Platform.lua
            PlatformGenerator.lua
            Score.lua
            Spike.lua
            SpikeGenerator.lua
            TextPlatform.lua
    main.lua
    README.md
```

---

## Features and Design

### Intuitive Movement Control

A crucial feature of the game is movement control that feels intuitive to the player, yet fun to interact with. Components of the player's movement are elaborated below.
1. **Gravity**. Gravity is simulated by a constant acceleration on the player's downward velocity. Gravity is implemented in the `Player:naturalForces` function.
2. **Air friction**. Friction is applied along the player's horizontal velocity. It is a constant deceleration, applied in the opposing direction of the player's movement. This force is capped at the player's horizontal velocity to prevent the force from making the player move in the opposite direction. For example, if the player is moving leftward, air friction is acting rightward, by a constant amount, until the player's leftward velocity falls below that constant amount. At which point, the rightward friction will equal the player's leftward velocity and zero the player's horizontal movement. This feature creates a sense of inertia, which not only feels more realistic, but also makes it easier for the player to manoeuvre; behaving like a brake when the player is moving too quickly. Air friction is implemented in the `Player:naturalForces` function.
3. **Bouncing**. When the player collides with a platform, the player's vertical velocity is reversed. The player is also displaced out of the collided platform to prevent clipping. Bouncing is implemented in the `Player:bounce` function.
4. **Bounce Energy Loss**. Upon bouncing, the player loses a percentage of vertical velocity, to simulate energy loss. The effect is that the player will reach a lower height than from where the player's drop started, similar to bouncing a ball in reality. Bounce energy loss is implemented in the `Player:bounce` function.
5. **Minimum Upward Bounciness**. Since bouncing energy loss subtracts a fixed percentage of the player's vertical velocity at every bounce, the player loses velocity very quicly (like how a real bouncing ball would behave). With the exception of infrequent scenarios where the player is dropped from a significant height, the player commonly ends up sliding on the surface of the platforms. When the bouncing stops, so does the fun. Continuous collision with a platform also creates a higher risk of the player clipping into it. Hence, a minimum bounciness is given to the player, such that the player, when bouncing up, will have at least a substantial amount of vertical velocity. Minimum bounciness is implemented in the `Player:bounce` function.
6. **Downward Bounce Damping**. An opposite issue arises for downward bounces; cases when the player travels upwards, and bounces off the underside of a platform toward the downward direction. These cases always occur after the player bounces upward, from the topside of a lower platform, into the underside of a higher platform. The 2 consecutive bounces leaves the player with a high downward vertical velocity, which when paired with gravity, launches the player very quickly in the downward direction. Unless the player is particularly adept, the scenario typically ends with the player losing, which is not fun. Hence, an addition damp is applied on downward bounces, behaving in a similar manner to bouncing energy loss. Downward bounce damping is implemented in the `Player:bounce` function.
7. **Speed Cap**. A cap on the player's velocity is applied, so that the player's velocity does not become too fast for the player to control. The speed cap is implemented in the `Player:capSpeed` function.
8. **Steering**. The player steers using the left and right arrow keys, that when held down, apply a constant amount of horizontal acceleration to the player in the corresponding direction. Steering is implemented in the `Player:userInputMove` function.
9. **Floating and Diving**. The player can also apply a certain amount of vertical acceleration using the up and down arrow keys. This allows the player to interact more with the game, giving the player the option to fall faster or slower, both of which can be used to the player's advantage depending on the scenario. Floating and diving is implemented in the `Player:userInputMove` function.

### Constrained Procedural Generation

The game level is an endless platformer, wherein game world objects are procedurally generated. There are 2 objects classes that are procedurally generated:
1. **Platforms** are for the player to use to stay within the game area. They are initialised with a constant vertical upwards velocity. The initialised vertical velocity increases over time (to a limit), and has some random variability. Horizontal velocity is randomised to be zero or a fixed constant for all platforms, and in a random horizontal direction. Platforms are implemented in the `Platform` class, and generated in the `PlatformGenerator` class.
2. **Spikes** are obstacles for the player to avoid. They are all initialised with the same vertical velocity. Like platforms, horizontal velocity is randomised to be zero or a fixed constant, and in a random horizontal direction. Spikes are implemented in the `Spike` class, and generated in the `SpikeGenerator` class.

Unconstrained random procedural generation has its limitations in creating fun scenarios for the player. Hence, several constraints were put in place, that are elaborated below.
1. Each row of platforms are generated as a grid of columns, helping to prevent them from bunching together.
2. The first platforms are generated underneath the player, so that the player does not lose the game immediately.
3. The number of platforms spawned per row is limited, so that the player has room to go below the platform row.
4. A platform cannot spawn in a column position, if there was a platform spawned in that column position in the previous row. This prevents the generation of long columns of platforms that are hard for the player to navigate around.
5. If no platforms were spawned in a row, the probability of platforms spawning increases. The probability increases exponentially with the number of rows without any platforms. This prevents scenarios where there are no platforms for the player to jump on.
6. Spikes are generated infrequently because they tend to limit the player's jumping options.

### Interactive Start Screen

The start screen is designed to also function as a tutorial. With the *arrow keys*, the player can control the perpetually falling fish bowl. When the *space key* is pressed, instructions will appear, and an invisible `Platform` object will be generated at the bottom of the screen where the "Press Enter to Play" text is. This invisible `Platform` will catch the player, as if the player were bouncing on the text. Now bouncing on the text, the player can try out the controls. The start screen is implemented in the `StartState` class, while the invisible text platforms are generated in the `TextPlatform` class.

### Aesthetic Finishes

Additional aesthetic features in the game are elaborated below.
1. **Session High Score**. The player's current score is displayed in the `PlayState` on the top right hand corner. The score increases as a function of time, with a small amount of random variation. The session high score is stored in a global variable `highScore`, to keep track of the player's best score. This is reset when the game stops running. In the `GameOverState`, the high score is displayed. Scoring is implemented in the `Score` object.
2. **Moving Backgrounds**. The recurring background image is perpetually looping upwards at a constant rate, that is slower than the platforms'. This is to create the illusion that the player is always falling and the background is a distance away. To ensure a smooth transition out of the `StartState`, that is, to enter the other states with the same image and vertical position, the `Background` object is passed between states. A random background image is chosen every time the `StartState` is entered. The player can also shuffle the background by pressing the *space key* in the `StartState`. When the background image is shuffled, the vertical position is also stored, so that for some pairs of backgrounds images it creates the illusion of a colour swap rather than the entire background changing. The background is implemented in the `Background` class.
3. **Fish in Bowl**. Within the draw area of the player controlled bowl, a small triangle (representing a fish) with a black dot (an eye) is drawn. This fish is a separate object that can move within the bowl as the bowl moves, as if the fish is "swimming" in the bowl. The fish is confined to the draw area of the bowl by checking for reverse collision. When the player loses and enters the `GameOverState`, the bowl is not rendered, only the fish, implying that the fish had lost the bowl. However, the player can still control the invisible bowl, which feels like the player is controlling the now bowl-less fish. The fish is implemented in the `Fish` class.
4. **Water Particles Effects**. Particle effects are managed using the engine's particle system. Particle effects are triggered when the player collides with platforms, like water is spilling out of the fish bowl. Particle effects are implemented in the `Water` class.
5. **Conservative Losing Conditions**. The losing conditions are more conservative that what the player can see visually. The player triggers game over when the player fully leaves the screen (not just colliding with the edge of the screen). Futhermore, the spike draw area is slightly larger than its collision box. Besides making the game less punitive, it also allows the player to experience "close calls".

---





