# Importing 
import pygame, os, sys, time, random


from pygame.constants import K_ESCAPE, MOUSEBUTTONDOWN
from pygame.time import Clock
# Initilize the pygame font library
pygame.font.init()


# Defining a clock so we can call it further down to help set our FPS
clock = pygame.time.Clock()

pause = True


# Setting the game window here
WIDTH, HEIGHT = 900, 500
# Defining the game window as WIN, and telling pygame that we will set the deminsions to the above defined. 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Setting what you see at the top of the window, could be anything you'd like
pygame.display.set_caption("First Game! WOoooWOoooWOoOWOoWOwowoowo")
# Defining our window color so we don't have to type out the RGB every time
GREEN = (0, 200, 0)
LIGHT_GREEN = (63, 217, 117)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (240, 58, 58)
YELLOW = (255, 255, 0)
# Defining our middle border for each player
BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)
# Defining our Spaceship Dimensions -- Initial spaceship was HUGE on the screen. This is scaling down the image
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# User Events for Yellow and Red getting hit with bullets. 
# Multiple User Events, add +1, +2, +3, etc.
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Defining the font you want to use, and the size
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
PAUSED_FONT = pygame.font.SysFont('comicsans', 100)
BUTTON_FONT = pygame.font.SysFont('comicsans', 20)
BUTTON_FONT_HOVER = pygame.font.SysFont('comicsans', 25)

# Our FPS so different Machines can't run the game at different speeds
FPS = 60
# How fast we're going to move, the veloicity 
VEL = 5



# The Bullets being defined 
BULLET_VEL = 7
MAX_BULLETS = 3

# Defining our Assets folder so we don't have to type the directory every time
ASSETS = 'PygameTutorial/Assets'

# Grabbing our yellow spaceship from our Assets folder using os.path.join (helps with various machines playing the game) the folder is Assets, and the image is spaceship_yellow.png
YELLOW_SPACESHIP = pygame.image.load(os.path.join(ASSETS, 'spaceship_yellow.png'))
# Rotating and Scaling down the spaceship.
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Grabbing our red spaceship from our Assets folder using os.path.join (helps with various machines playing the game) the folder is Assets, and the image is spaceship_red.png
RED_SPACESHIP = pygame.image.load(os.path.join(ASSETS, 'spaceship_red.png'))
# Scaling down the spaceship
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
# Grabbing our SPACE background from the Assets folder.
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, 'space.png')), (WIDTH, HEIGHT))

def text_objects(text, font):
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()

# draw_window() is the thing we can call later to update our display, and draw multiple things onto it. Adding "red, yellow" to the main definition allows us to fill in what that means later on in our main game loop.
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, paused):
     # Filling the window with a color/image, so it's not just a black background.
    WIN.blit(SPACE, (0, 0))
    #Drawing our Border on the screen
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Created 2 Text objects for each players health
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    
    # Drawing the text objects on the screen. Dynamically with the WIDTH - How long text is - 10pixels from the right and 10 pixels from the top because it'll be right at the edge if not.
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # BLIT is what you use to add something to the screen or layer it ontop of the screen. Text/Images
    # The yellow/red.x/.y are the coordinates that we will call upon in our main game loop.
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))




    for bullet in red_bullets:
        # What - Rectange / Where - Window / Color - Red / what is it - bullet
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        # What - Rectange / Where - Window / Color - Red / what is it - bullet
        pygame.draw.rect(WIN, YELLOW, bullet)


    # Gotta update the display or else nothing will show.
    pygame.display.update()

# Movement for the Yellow Spaceship
def yellow_handle_movement(keys_pressed, yellow):
    # Saying what each key will do if pressed (Random keys get ignored if not in this list)
            # The "and" statement adds the border to the game. If it comes up to our BORDER it'll just stop. Also with the Height and Width of the game window too.
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - 30: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - 50: # DOWN
        yellow.y += VEL

# Movement for the Red Spaceship
def red_handle_movement(keys_pressed, red):
    # Saying what each key will do if pressed (Random keys get ignored if not in this list)
        # The "and" statement adds the border to the game. If it comes up to our BORDER it'll just stop. Also with the Height and Width of the game window too.
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - 35: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - 50: # DOWN
        red.y += VEL

# Handles moving bullets, Collision of bullets, Remove bullets if they collied or go off screen.
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        # += makes it shoot right -->
        bullet.x += BULLET_VEL
        # If the bullet that is a rec(tangle) collides with ONLY another rectangle (which our spaceships are, technically.), than this works.
        if red.colliderect(bullet):
            # If above, add a user event for yellow, because red was hit.
            pygame.event.post(pygame.event.Event(RED_HIT))
            # If above, then remove bullet.
            yellow_bullets.remove(bullet)
        # If the bullet goes off the screen, remove it so the counter can reset.
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        # += makes it shoot right -->
        bullet.x -= BULLET_VEL
        # If the bullet that is a rec(tangle) collides with ONLY another rectangle (which our spaceships are, technically.), than this works.
        if yellow.colliderect(bullet):
            # If above, add a user event for yellow, because red was hit.
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            # If above, then remove bullet.
            red_bullets.remove(bullet)
        # If the bullet goes off the screen, remove it so the counter can reset.
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(6900)


click = False


def paused():
    draw_text = PAUSED_FONT.render('Paused', 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        mouse_pos = pygame.mouse.get_pos()            
        #gameDisplay.fill(white)
        
        if mouse_pos[0] > 150 and mouse_pos[0] < 250 and mouse_pos[1] > 400 and mouse_pos[1] < 449:
            pygame.draw.rect(WIN, LIGHT_GREEN, (150, 400, 100, 50))
            green_button_text = BUTTON_FONT_HOVER.render('Resume', 1, BLACK)
            WIN.blit(green_button_text, (155, 405))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    unpause() 
                    pygame.time.delay(5)
                    pause = True

        else:
            pygame.draw.rect(WIN, GREEN, (150, 400, 100, 50))
            green_button_text = BUTTON_FONT.render('Resume', 1, BLACK)
            WIN.blit(green_button_text, (155, 405))


        if mouse_pos[0] > 650 and mouse_pos[0] < 750 and mouse_pos[1] > 400 and mouse_pos[1] < 449:
            pygame.draw.rect(WIN, LIGHT_RED, (650, 400, 100, 50))
            red_button_text = BUTTON_FONT_HOVER.render('Q U I T', 1, BLACK)
            WIN.blit(red_button_text, (655, 405))
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    quitgame()

        else:
            pygame.draw.rect(WIN, RED, (650, 400, 100, 50))
            red_button_text = BUTTON_FONT.render('Q U I T', 1, BLACK)
            WIN.blit(red_button_text, (655, 405)) 
        
        pygame.display.update()
        clock.tick(FPS)  

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False
    


# Defining the main game loop.
def main():
    # placing our spaceships, and definig their hitbox
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)


    # Where the number of bullets are being stored for each player
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    # making a run varible, setting it to True.. once it goes False, the loop terminates, and everything shuts down (basically the x button)
    run = True
    # making the actual game loop while run is the same as while run == True
    while run:
        # Setting our FPS, never going over our cap of 60
        clock.tick(FPS)
        # For the new "event" in pygame, we set the new "event" to be gotten with .get() / It's a Queue for events
        for event in pygame.event.get():
            # If we press the x in the top right, we want it to break the loop.
            if event.type == pygame.QUIT:
                run = False

            # If statment for shooting the bullets. Per Press, not hold down and continue to fire.
            if event.type == pygame.KEYDOWN:
                        # len gets how many items are in the yellow_bullets and if it's at 3 it will not add another bullet to the list
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Bullet starts at (width position, height position, how big it is Width, Height)
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                         # len gets how many items are in the red_bullets and if it's at 3 it will not add another bullet to the list
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    # Bullet starts at (width position, height position, how big it is W, H)
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                
                if event.key == pygame.K_ESCAPE:
                    paused()
                    

            # If Red is hit, they loose 1 Health
            if event.type == RED_HIT:
                red_health -= 1
            # If Yellow is hit, they loose 1 Health
            if event.type == YELLOW_HIT:
                yellow_health -= 1
        

        # Winner text is set to blank, and if it doesn't == "" then someone must've won!
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yelow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # Defining a Varible of keys_pressed to get the input of what key is being pressed 
        keys_pressed = pygame.key.get_pressed()
        # Passing our movement to our Game Loop so it we can move around in the game.
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        # Adds the collison to the game loop to make it work properly. 
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Painting what is on the screen in our Main game loop
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, paused)
    # Above turns run to False when the x is pressed. this quits the window itself
    pygame.quit()




# This is so the game can only be ran if we run it ourselves. Any imported things can't launch by themselves with this. 
if __name__ == "__main__":

    main()
