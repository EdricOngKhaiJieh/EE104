#CITE: base code from Python_All-in-one_for_dummies


from random import randint
import time
import pgzrun
from pgzero.builtins import Actor, Rect

# Constants
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Global variables
game_over = False
finalized = False
garden_happy = True
fangflower_collision = False
start_time = time.time()
time_elapsed = 0
raining = False  # Variable to control rain in the garden
rain_duration_start = None  # Track when rain starts
character_selected = False  # Track if a character has been selected
selected_character = None  # Holds the selected character
show_play_again_prompt = False  # Track if we're showing the "Play Again?" prompt
zap_actor = Actor("zap")  # Zap image for collision effect
zap_displayed = False  # Track if zap image is displayed

# Actors and positions
cow = Actor("cow")
cow.pos = 100, 500
pig = Actor("pig")
pig.pos = 300, 500
flower_list = []
wilted_list = []
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []

# Define play again options as Rect objects for Yes/No
yes_box = Rect((CENTER_X - 100, CENTER_Y), (100, 50))
no_box = Rect((CENTER_X + 10, CENTER_Y), (100, 50))

# Character selection screen
def draw_character_selection():
    screen.clear()
    screen.fill((0, 255, 255))  # Cyan background
    screen.draw.text("Choose Your Character", center=(CENTER_X, CENTER_Y - 100), fontsize=50, color="black")
    cow.draw()
    pig.draw()
    screen.draw.text("Cow", center=(cow.x, cow.y + 50), color="black")
    screen.draw.text("Pig", center=(pig.x, pig.y + 50), color="black")

# Draw function
def draw():
    global game_over, time_elapsed, finalized, show_play_again_prompt
    if not character_selected:
        draw_character_selection()  # Show character selection screen
    elif not game_over:
        screen.clear()
        if raining:
            screen.blit("garden-raining", (0, 0))  # Rain background
        else:
            screen.blit("garden", (0, 0))  # Default background
        selected_character.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        time_elapsed = int(time.time() - start_time)
        screen.draw.text(
            "Garden happy for: " + str(time_elapsed) + " seconds",
            topleft=(10, 10), color="black"
        )
    else:
        # Game over screen
        if not finalized:
            screen.clear()
            screen.fill((255, 0, 0))  # Bright red background
            if zap_displayed:
                zap_actor.draw()  # Display zap image at character's position
            else:
                selected_character.draw()
            screen.draw.text("Oops! Game Over!", center=(CENTER_X, CENTER_Y - 50), fontsize=60, color="white")
            finalized = True
            clock.schedule(show_play_again_screen, 3)  # Delay before showing play again screen

# Show "Play Again?" screen with Yes/No options
def show_play_again_screen():
    global show_play_again_prompt
    screen.clear()
    screen.fill((255, 255, 255))  # White background
    screen.draw.text("Play Again?", center=(CENTER_X, CENTER_Y - 100), fontsize=50, color="black")

    # Draw Yes option
    screen.draw.filled_rect(yes_box, (0, 0, 0))
    screen.draw.text("Yes", center=yes_box.center, color="white", fontsize=40)

    # Draw No option
    screen.draw.filled_rect(no_box, (0, 0, 0))
    screen.draw.text("No", center=no_box.center, color="white", fontsize=40)

    show_play_again_prompt = True

# Functions to add flowers and fangflowers
def new_flower():
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")

def add_flowers():
    if not game_over:
        new_flower()
        clock.schedule(add_flowers, 4)

def reset_character():
    if not game_over:
        selected_character.image = selected_character.image.split("-")[0]  # Reset to base image

def wilt_flower():
    if not game_over and not raining:  # Flowers do not wilt in the rain
        if flower_list:
            rand_flower = randint(0, len(flower_list) - 1)
            if flower_list[rand_flower].image == "flower":
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
        clock.schedule(wilt_flower, 3)

def check_flower_collision():
    global selected_character, flower_list, wilted_list
    index = 0
    for flower in flower_list:
        if flower.colliderect(selected_character) and flower.image == "flower-wilt":
            flower.image = "flower"
            wilted_list[index] = "happy"
            break
        index += 1

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if wilted_list:
        for wilted_since in wilted_list:
            if wilted_since != "happy":
                time_wilted = int(time.time() - wilted_since)
                if time_wilted > 9.0:  # Game over if wilted for more than 9 seconds
                    garden_happy = False
                    game_over = True
                    break

# Fangflower-related functions
def mutate():
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        fangflower_pos_x = flower_list[rand_flower].x
        fangflower_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        fangflower = Actor("fangflower")
        fangflower.pos = fangflower_pos_x, fangflower_pos_y
        fangflower_vx = velocity()
        fangflower_vy = velocity()
        fangflower_list.append(fangflower)
        fangflower_vx_list.append(fangflower_vx)
        fangflower_vy_list.append(fangflower_vy)
        clock.schedule(mutate, 10 if raining else 20)

def velocity():
    random_dir = randint(0, 1)
    random_velocity = randint(3, 5)  # Adjust the speed range here
    return -random_velocity if random_dir == 0 else random_velocity

def update_fangflowers():
    global fangflower_list, game_over
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx
            fangflower.y += fangflower_vy

            # Bounce off edges
            if fangflower.left < 0 or fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150 or fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy

            index += 1

def check_fangflower_collision():
    global selected_character, fangflower_list, fangflower_collision, game_over, zap_displayed
    for fangflower in fangflower_list:
        if fangflower.colliderect(selected_character):
            zap_actor.pos = selected_character.pos  # Position zap image where the character is
            zap_displayed = True
            selected_character.image = "zap"  # Show 'zap' image on collision
            game_over = True
            break

# Update function for player controls and game logic
def update():
    global score, game_over, fangflower_collision, raining, time_elapsed, rain_duration_start
    global flower_list, fangflower_list, character_selected, selected_character

    if not character_selected:
        return  # Skip game logic if character has not been selected

    # Update time elapsed
    time_elapsed = int(time.time() - start_time)

    # Start the rain after 20 seconds of gameplay and set rain start time
    if time_elapsed >= 20 and not raining:
        raining = True
        rain_duration_start = time.time()  # Record the exact time when rain starts

    # Turn off rain after 8 seconds of raining
    if raining and (time.time() - rain_duration_start >= 8):
        raining = False  # Turn off rain after 8 seconds

    fangflower_collision = check_fangflower_collision()
    check_wilt_times()

    if not game_over:
        # Character watering behavior
        if keyboard.space:
            selected_character.image = f"{selected_character.image.split('-')[0]}-water"
            clock.schedule(reset_character, 0.5)
            check_flower_collision()

        # Character movement
        if keyboard.left and selected_character.x > 0:
            selected_character.x -= 5
        elif keyboard.right and selected_character.x < WIDTH:
            selected_character.x += 5
        elif keyboard.up and selected_character.y > 150:
            selected_character.y -= 5
        elif keyboard.down and selected_character.y < HEIGHT:
            selected_character.y += 5

        update_fangflowers()

# Mouse click handler for character selection and "Play Again?" prompt
def on_mouse_down(pos):
    global character_selected, selected_character, game_over, show_play_again_prompt
    if not character_selected:
        if cow.collidepoint(pos):
            selected_character = Actor("cow", (100, 500))
            character_selected = True
        elif pig.collidepoint(pos):
            selected_character = Actor("pig", (100, 500))
            character_selected = True
    elif game_over and show_play_again_prompt:
        if yes_box.collidepoint(pos):
            reset_game()  # Restart the game if "Yes" is clicked
        elif no_box.collidepoint(pos):
            exit()  # Exit the game if "No" is clicked

# Reset the game
def reset_game():
    global game_over, finalized, garden_happy, fangflower_collision, start_time
    global time_elapsed, raining, rain_duration_start, character_selected, selected_character
    global flower_list, wilted_list, fangflower_list, fangflower_vy_list, fangflower_vx_list, show_play_again_prompt, zap_displayed

    game_over = False
    finalized = False
    garden_happy = True
    fangflower_collision = False
    start_time = time.time()
    time_elapsed = 0
    raining = False
    rain_duration_start = None
    character_selected = False
    selected_character = None
    flower_list.clear()
    wilted_list.clear()
    fangflower_list.clear()
    fangflower_vy_list.clear()
    fangflower_vx_list.clear()
    show_play_again_prompt = False
    zap_displayed = False

    add_flowers()
    wilt_flower()
    mutate()  # Start fangflower mutation

# Initialize game elements
add_flowers()
wilt_flower()
mutate()  # Start fangflower mutation

# Run the game
pgzrun.go()
