# Support libraries
import pygame
# Scenes
# Game modules
import game
# Enemies
import troll

# Current graphics module to use
currentScene = "forest"

# the backdrop of the scene
backdrop = ""
# Later used to load the backdrop
bg = None

# temp is used to transfer the window dimensions to objects.py
import temp
# Make the image path for the current backdrop
backdrop = "graphics/" + currentScene + ".PNG"
# load the image
bg = pygame.image.load(backdrop)
# get its dimensions
windowWidth = bg.get_width()
windowHeight = bg.get_height()

# place the floor 1 tenth of the window size above the bottom
floor = round((9 / 10) * windowHeight)

# transfer the dimensions to temp
temp.width = windowWidth
temp.height = windowHeight
temp.floor = floor

# import the graphic objects
import objects

# objects.init(windowWidth,windowHeight)
# objects.windowHeight = windowHeight
# objects.windowWidth = windowWidth

# if the scene is forest
if currentScene == "forest":
    # import the scene module
    import forest
    # update knight stats based on window size
    game.knight.speed = round(windowWidth / 30)
    game.knight.jumpHeight = round(windowHeight / 4)

    # initialize player
    player = game.knight("player")
    entities = [player]

    # update troll stats based on window size
    game.troll.speed = round(windowWidth / 60)
    game.troll.jumpHeight = round(windowHeight / 10)

    # initialize enemy1
    enemy1 = game.troll("enemy1")
    game.enemyEntities.append(enemy1)

    # add all game objects to entities array
    for enemy in game.enemyEntities:
        entities.append(enemy)

    # find the player game object
    # store it for quicker access later
    for currentEntity in entities:
        if currentEntity.name == "player":
            playerEntity = currentEntity

    # initialize graphic objects based on window size
    forest.sceneObjects = forest.init(entities,windowWidth,windowHeight)
    # get list of objects
    sceneObjects = forest.sceneObjects

# if the current scene is mainMenu
elif currentScene == "mainMenu":
    # import the module
    import mainMenu
    # initialize the graphic objects based on window size
    mainMenu.sceneObjects = mainMenu.init(windowWidth,windowHeight)
    sceneObjects = mainMenu.sceneObjects

# find the player graphic object
playerObject = None
# by scanning through the list of graphic objects
for currentObject in sceneObjects:
    if currentObject.name == "player":
        playerObject = currentObject
    # if the object's name starts with "enemy" add it a list of enemies
    elif currentObject.name[0:5] == "enemy":
        game.enemyObjects.append(currentObject)

# Initialize pygame
pygame.init()

# Rate of height gain due to jumping (px/s)
jumpSpeed = round(windowHeight * 0.08)

# rate of falling due to gravity (px/s)
gravity = round(windowHeight * 0.07)

# Initialize the game window
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("RPG Game")

# Initialize game clock
gameClock = pygame.time.Clock()
FPS = 15


# Start game loop
def gameLoop():
    key = ""
    # keys currently down
    heldKeys = []

    # Game has is not quitting yet
    gameQuit = False

    # ID of the current attack being run
    attackID = 0

    # While the game is not quitting...
    while not gameQuit:
        # if the player exists
        if playerObject != None:
            # if the player is executing an attack
            if playerObject.state in playerEntity.attackNames:
                # execute the next frame
                playerEntity.attack(playerObject, playerEntity, windowWidth, attackID)

        # Check for events
        for event in pygame.event.get():
            # If the quit button (X) has been pressed
            if event.type == pygame.QUIT:
                # Quit the game
                gameQuit = True
            # If ANY mouse button has pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If it was left click
                if event.button == 1:
                    # Check through all loaded graphic objects
                    for currentObject in range(len(sceneObjects)):
                        # is the object we're checking clickable?
                        if sceneObjects[currentObject].clickable:
                            # Is the mouse over the object?
                            if sceneObjects[currentObject].x - 1 < event.pos[0] < sceneObjects[currentObject].x + \
                                    sceneObjects[currentObject].width + 1 and sceneObjects[currentObject].y - 1 < \
                                    event.pos[1] < sceneObjects[currentObject].y + sceneObjects[
                                currentObject].height + 1:
                                # Say so (will be used later)
                                print("click " + sceneObjects[currentObject].name)

            # If a key has been pressed
            elif event.type == pygame.KEYDOWN:
                # disabled = playerObject.state in ["jump",
                #                                   "drop,knockback"] or playerObject.state in playerEntity.attackNames

                # add it to an array of held keys
                heldKeys.append(event.key)

                    # if event.key == pygame.K_a:
                    #   key = "a"
                    #   if not disabled:
                    #     playerObject.changeState("walk")
                    #     playerObject.face = "l"
                    #   else:
                    #     playerObject.jumpWalk = [True,"l"]
                    # elif event.key == pygame.K_d:
                    #   key = "d"
                    #   if not disabled:
                    #     playerObject.changeState("walk")
                    #     playerObject.face = "r"
                    #   else:
                    #     playerObject.jumpWalk = [True,"r"]
                    #
                    # elif event.key == 257:
                    #   if not disabled:
                    #     playerEntity.attack(playerObject,playerEntity,windowWidth,0)
                    #     key = "KP1"
                    #     attackID = 0
                    #
                    # elif event.key == 258:
                    #   if not disabled:
                    #     playerEntity.attack(playerObject,playerEntity,windowWidth,1)
                    #     key = "KP2"
                    #     attackID = 1
                    #
                    # elif event.key == 259:
                    #   if not disabled:
                    #     playerEntity.attack(playerObject,playerEntity,windowWidth,2)
                    #     key = "KP3"
                    #     attackID = 1
                    #
                    # if event.key == pygame.K_SPACE and playerObject.state in ["walk","stand"]:
                    #   playerObject.changeState("jump")
                    #   if key == "a":
                    #     playerObject.jumpWalk = [True,"l"]
                    #   elif key == "d":
                    #     playerObject.jumpWalk = [True,"r"]

            # if a key was lifted
            elif event.type == pygame.KEYUP:
                # remove it from the array of held keys
                heldKeys.remove(event.key)

                        # if (event.key == pygame.K_a and key == "a") or (event.key == pygame.K_d and key == "d"):
                        #   if not playerObject.state in ["jump","drop"]:
                        #     playerObject.changeState("stand")
                        #   else:
                        #     playerObject.jumpWalk[0] = False
                        #   key = ""

        # default to disabled
        disabled = True
        # if the player exists
        if playerObject is not None:
            # check if the player is in a state where keys should not be pressed
            disabled = playerObject.state in ["jump", "drop", "knockback"] or playerObject.state in playerEntity.attackNames

        # default all recognised keys to not pressed
        found32 = False
        found97 = False
        found100 = False
        found257 = False
        found258 = False
        found259 = False

        #if the player is disabled
        if not disabled:
            # check through all keys currently down
            for key in heldKeys:
                # if it's a
                if key == 97:
                    # note that the key was found
                    found97 = True
                    # if the player isnt walking already
                    if playerObject.state != "walk":
                        # walk
                        playerObject.changeState("walk")
                    # left
                    playerObject.face = "l"
                # if it's d
                if key == 100:
                    found100 = True
                    # walk right
                    if playerObject.state != "walk":
                        playerObject.changeState("walk")
                    playerObject.face = "r"
                # if both a and d are down
                if found97 and found100:
                    # stand
                    if playerObject.state != "stand":
                        playerObject.changeState("stand")
                # if it's space
                if key == 32:
                    found32 = True
                    # jump
                    if playerObject.state != "jump":
                        playerObject.changeState("jump")
                # if it's KP1
                if key == 257:
                    found257 = True
                    # execute attack 1
                    playerEntity.attack(playerObject, playerEntity, windowWidth, 0)
                    key = "KP1"
                    attackID = 0
                # if it's KP2
                if key == 258:
                    found258 = True
                    # execute attack 2
                    playerEntity.attack(playerObject, playerEntity, windowWidth, 1)
                    key = "KP2"
                    attackID = 1
                # if it's KP3
                if key == 259:
                    found259 = True
                    # execute attack 3
                    playerEntity.attack(playerObject, playerEntity, windowWidth, 2)
                    key = "KP3"
                    attackID = 2
            # if no keys were found
            if True not in [found32, found97, found100, found257, found258, found259]:
                # stand
                playerObject.changeState("stand")

        # entity actions
        for currentObject in sceneObjects:
            # if the current graphic object being scanned is an entity
            if currentObject.objectType == "entity":
                # associate entities with their game class counterpart (e.g knight/mage for the player etc)
                for currentEntity in entities:
                    if currentObject.name == currentEntity.name:
                        # if the entity is out of health
                        if currentEntity.health <= 0:
                            # remove them from thr list of objects
                            sceneObjects.remove(currentObject)
                            entities.remove(currentEntity)
                            # remove their health bar
                            for current in sceneObjects:
                                if current.name == currentObject.name + "Health" or current.name == currentObject.name + "Stamina" :
                                    sceneObjects.remove(current)
                        # load the entity's current frame
                        image = pygame.image.load(
                            "graphics/" + currentObject.folder + "/" + currentObject.state + "/" + str(
                                currentObject.current) + ".PNG")
                        # get the y value of the entity's feet
                        feet = currentObject.y + image.get_height()
                                # print(currentObject.name)
                                # if playerObject.state == "swing" and currentObject.name == "player":
                                #   print("---------------------")
                                #   print("Current",playerObject.current)
                                #   print("Y should be",floor - image.get_height())
                                #   print("Y",currentObject.y)
                                #   print("Height",image.get_height())
                                #   print("feet",feet)
                                # print("feet",feet)
                                # print("floor",floor)
                                # print(feet > floor)
                        # Make sure entities are above the ground
                        if feet > floor:
                                      # if currentObject.name == "player":
                                      #   print("RISE TO",floor - image.get_height())
                            currentObject.y = floor - image.get_height()
                        # Make sure entities are on the screen
                        if currentObject.x < 0:
                            currentObject.x = 0
                        elif currentObject.x + image.get_width() > windowWidth:
                            currentObject.x = windowWidth - image.get_width()
                        # gravity
                        # if the wntity is not jumping, dropping or being knocked back AND the feet are above the floor
                        if (currentObject.state not in ["jump", "drop", "knockback"]) and (
                                not currentObject.state in currentEntity.attackNames) and (feet < floor):
                                      # if currentObject.name == "player":
                                      #   print("DROP")
                                      # print(feet)
                                      # print(floor)
                            # make the entity drop
                            currentObject.changeState("drop")
                        # if the entity is dropping
                        if currentObject.state == "drop":
                            # if the distance between the entity's feet and the floor is more than or equal to the distance the entity moves per frame due to gravity
                            if floor - feet >= gravity:
                                # move the entity down at the rate of game gravity
                                currentObject.y += gravity
                            # if the distance is less than the amount needed for normal gravity
                            else:
                                # move the entity down the remaining distance
                                currentObject.y += floor - feet
                        # TODO: this is what's breaking the animations (maybe)
                        # if the entity is attacking and the entity's feet are above the ground
                        if currentObject.state in currentEntity.attackNames and feet < floor:
                            # move them back onto the ground
                            currentObject.y = floor - image.get_height()
                        # if the entity is dropping but they have reached the ground
                        if currentObject.state == "drop" and currentObject.y + image.get_height() == floor:
                            # revert to standing
                            currentObject.changeState("stand")
                        # if the entity is being knocked back
                        if currentObject.state == "knockback":
                            # keep them facing the right way
                            currentObject.face = currentObject.knockbackFace
                            # if the entity is below half way through the knockback sequence
                            if currentObject.knockbackDistance >= round(currentObject.knockbackDistanceMax / 2):
                                # make them gain height at jump rate
                                currentObject.y -= round(jumpSpeed / 2)
                            # if the entity is above half way through the knockback sequence
                            elif currentObject.knockbackDistance != 0:
                                # make them lose weight at jump speed, in the same way as gravity
                                if floor - feet >= round(jumpSpeed / 2):
                                    currentObject.y += round(jumpSpeed / 2)
                                else:
                                    currentObject.y += floor - feet
                            # if the remaining knockback distance is more than 1.5 * the jump speed
                            if currentObject.knockbackDistance >= round(1.5 * jumpSpeed):
                                # add 1.5 * the jump speed to the x position
                                if currentObject.face == "l":
                                    currentObject.x -= round(1.5 * jumpSpeed)
                                else:
                                    currentObject.x += round(1.5 * jumpSpeed)
                                # take the amount moved from the remaining distance
                                currentObject.knockbackDistance -= 1.5 * jumpSpeed
                            # if the remaining distance is less than 1.5 * the jump speed
                            elif currentObject.knockbackDistance != 0:
                                # add the remaining distance
                                if currentObject.face == "l":
                                    currentObject.x -= currentObject.knockbackDistance
                                else:
                                    currentObject.x += currentObject.knockbackDistance
                                # reset knockback
                                currentObject.knockbackDistance = 0
                            # if there is no knockback remaining
                            else:
                                # if the entity is on the ground
                                if currentObject.y == 0:
                                    # stand
                                    currentObject.changeState("stand")
                                # if the entity is in the air
                                else:
                                    # drop
                                    currentObject.changeState("drop")

                        # walking
                        # if:
                        # the entity is walking
                        # OR
                        # they're walking AND they were walking before they jumped
                        # OR
                        # they're dropping AND they were last walking OR the state before last was walk
                        if currentObject.state == "walk" or (
                                        currentObject.state == "jump" and currentObject.previous[-1] == "walk") or (
                                        currentObject.state == "drop" and (
                                                currentObject.previous[-1] == "walk" or currentObject.previous[
                                            -2] == "walk")):
                            # move the entity based on their game entity's walk speed
                            if currentObject.face == "l":
                                currentObject.x -= currentEntity.speed
                            else:
                                currentObject.x += currentEntity.speed
                        # jumping
                        # if the entity is jumping
                        if currentObject.state == "jump":
                            # if the entity is below the jump height
                            if currentObject.y > floor - image.get_height() - currentEntity.jumpHeight:
                                # if the difference between the entity and the jump height is 15 or more
                                if currentObject.y - (
                                                floor - image.get_height() - currentEntity.jumpHeight) >= jumpSpeed:
                                    # move up 15
                                    currentObject.y -= jumpSpeed
                                # if the difference is less than 15
                                else:
                                    # set the y to max jump height
                                    currentObject.y = floor - image.get_height() - currentEntity.jumpHeight
                                    # if the entity is at or above jump height
                            if currentObject.y <= floor - image.get_height() - currentEntity.jumpHeight:
                                # switch to dropping
                                currentObject.changeState("drop")

                # enemy attack continuation and AI call
                # scan through all objects on the scene
                for currentObject in sceneObjects:
                    # associate with game object counterpart
                    for currentEntity in entities:
                        if currentObject.name == currentEntity.name:
                            # if they are not the player and they are not disabled
                            if currentObject.name != "player" and currentObject.state not in ["jump", "drop,knockback"]:
                                # if they are not attacking
                                if not currentObject.state in currentEntity.attackNames:
                                    # call their AI file
                                    troll.react(currentObject, entities, playerObject, playerEntity, windowWidth)
                                # if they are attacking
                                else:
                                    # continue the attack
                                    currentEntity.attack(playerObject, playerEntity, currentObject, windowWidth,
                                                         currentEntity.currentAttack)

        # Wipe the screen
        window.fill(objects.white)
        # If the current scene has a backdrop
        if backdrop != "":
            # blit it onto the screen
            window.blit(bg, [0, 0])

        ########GRAPHIC OBJECT BEHAVIOUR
        # Check through all loaded objects
        for currentObject in range(len(sceneObjects)):
            # If the current object is visible
            if sceneObjects[currentObject].toRender:
                # "shortcut" to the current object's class instance
                workingObject = sceneObjects[currentObject]
                # if the object is a rectangle
                if workingObject.objectType == "rectangle":
                    # draw it
                    pygame.draw.rect(window, workingObject.colour,
                                     [workingObject.x, workingObject.y, workingObject.width, workingObject.height])
                # If it's text
                elif workingObject.objectType == "text":
                    # Render the text
                    shownText = objects.font.render(workingObject.text, workingObject.antialiasing, workingObject.colour)
                    # blit it onto the screen
                    window.blit(shownText, [workingObject.x, workingObject.y])
                # If it's an image
                elif workingObject.objectType == "image":
                    # load
                    image = pygame.image.load(workingObject.file).convert_alpha()
                    # blit
                    window.blit(image, [workingObject.x, workingObject.y])
                # if it's an animated image
                elif workingObject.objectType == "animation":
                    # if the animation is running
                    if workingObject.state == 1:
                        # load its current image, taken from the images array inside of its folder
                        image = pygame.image.load("graphics/" + workingObject.folder + "/" + str(
                            workingObject.current) + ".PNG").convert_alpha()
                        # blit
                        window.blit(image, [workingObject.x, workingObject.y])
                        # increment current image
                        workingObject.current += 1
                        # reset current image id if the last image has been drawn
                        if workingObject.current == workingObject.totalStates - 1:
                            workingObject.current = 0
                # if it's an entity. entities are used for associating the state of an entity with multiple animations
                # entity animations are always running
                elif workingObject.objectType == "entity":
                    # load the current image from it's state folder, from the entity's folder
                    image = pygame.image.load(
                        "graphics/" + workingObject.folder + "/" + workingObject.state + "/" + str(
                            workingObject.current) + ".PNG").convert_alpha()
                    # if the image is facing left, flip it
                    if workingObject.face == "l":
                        image = pygame.transform.flip(image, True, False)
                    # blit
                    window.blit(image, [workingObject.x, workingObject.y])
                    # reset if last image is reached.
                    if workingObject.current == workingObject.totalStates - 1:
                        workingObject.current = 0
                    else:
                        # increment current image
                        workingObject.current += 1
                # if it's a health bar
                elif workingObject.objectType == "healthBar":
                    # update the health bar's position
                    workingObject.update()
                    # draw the green section
                    pygame.draw.rect(window, objects.green,
                                     [workingObject.x, workingObject.y, workingObject.gwidth, workingObject.height])
                    # draw the red section
                    pygame.draw.rect(window, objects.red,
                                     [workingObject.x + workingObject.gwidth, workingObject.y, workingObject.rwidth,
                                      workingObject.height])

                # if it's a stamina bar
                elif workingObject.objectType == "staminaBar":
                    # update the stamina bar's position
                    workingObject.update()
                    # draw the green section
                    pygame.draw.rect(window, objects.lblue,
                                     [workingObject.x, workingObject.y, workingObject.bwidth, workingObject.height])
                    # draw the red section
                    pygame.draw.rect(window, objects.grey,
                                     [workingObject.x + workingObject.bwidth, workingObject.y, workingObject.gwidth,
                                      workingObject.height])

        # update all loaded graphic objects
        pygame.display.flip()

        # tick the game clock
        gameClock.tick(FPS)

    # outside of game loop, so the game must be ending. Quit pygame.
    pygame.quit()


# start the game loop
gameLoop()
