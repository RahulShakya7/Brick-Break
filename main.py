import pygame
import sys
from pygame.locals import *

mainClock = pygame.time.Clock()

pygame.init()
icon = pygame.image.load('bb_icon.png')
pygame.display.set_icon(icon)

screen_width = 600
screen_height = 700

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (600, 700))

pygame.display.set_caption('Brick Break')
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.Font('minecraft_font_by_pwnage_block_d37t6nb.ttf', 25)
font1 = pygame.font.Font('minecraft_font_by_pwnage_block_d37t6nb.ttf', 45)
font2 = pygame.font.Font('minecraft_font_by_pwnage_block_d37t6nb.ttf', 30)

Score = 0
h_score = 1


def high_score():
    with open('high.txt', 'r') as f:
        return f.read()


def text_object(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect = (x, y)
    surface.blit(textobj, textrect)


# Define colours
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Define global variable
clicked = False
counter = 0


class button():
    # Colours for button and text
    button_color = 'grey'
    hover_color = 'orange red1'
    click_color = 'yellow'
    text_color = 'black'
    width = 180
    height = 70

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        pygame.init()
        global clicked
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # Check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_color, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_color, button_rect)
        else:
            pygame.draw.rect(screen, self.button_color, button_rect)

        # Add shading to button
        pygame.draw.line(screen, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        # Add text to button
        text_img = font.render(self.text, True, self.text_color)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action


again = button(210, 210, 'Play')
exit_game = button(210, 410, 'Quit')
about_game = button(210, 310, 'Info')

back1 = button(210, 550, 'back')

click = False


def quit_game():
    pygame.quit()


def back_menu():
    main_menu()


def game_info():
    while True:
        '''Start the game by pressing space-bar or clicking and use the arrow keys to move the paddle and destroy every block without letting the ball fall!'''
        screen.blit(background, (0, 0))
        text_object('Welcome to', font2, 'snow', screen, 210, 70)
        text_object('Brick Break', font1, 'snow', screen, 160, 105)

        text_object('The rules are simple break it', font, 'snow', screen, 90, 200)
        text_object('until you make it.', font, 'snow', screen, 90, 235)

        text_object('Start the game by pressing', font, 'snow', screen, 90, 290)
        text_object('space-bar or clicking the', font, 'snow', screen, 90, 325)
        text_object('mouse. Use the arrow keys to', font, 'snow', screen, 90, 360)
        text_object('navigate the paddle and', font, 'snow', screen, 90, 395)
        text_object('destroy every block without', font, 'snow', screen, 90, 430)
        text_object('letting the the ball fall!', font, 'snow', screen, 90, 465)

        if back1.draw_button():
            back_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)

        pygame.display.update()
        mainClock.tick(60)


def main_menu():
    while True:

        screen.blit(background, (0, 0))
        text_object('Main Menu', font1, 'snow', screen, 175, 110)

        if again.draw_button():
            game()
        if exit_game.draw_button():
            quit_game()
        if about_game.draw_button():
            game_info()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit(0)

        pygame.display.update()
        mainClock.tick(60)


def game():

    # Define colours
    bg = (46, 9, 60)

    # Block colours
    block_stone = 'yellow'
    block_end_stone = 'orange'
    block_obsidian = 'red'
    block_wood = 'green'

    # Paddle colours
    paddle_color = 'navy'
    paddle_outline = 'blue'

    # Sound for wall, paddle and ball
    brick_sound = pygame.mixer.Sound('sounds_brick.wav')
    paddle_sound = pygame.mixer.Sound('sounds_paddle.wav')
    wall_sound = pygame.mixer.Sound('sounds_wall.wav')

    # Text colour
    text_color = 'snow'

    # Define game variables
    cols = 6
    rows = 8
    paddle_size = 6
    clock = pygame.time.Clock()
    fps = 60
    live_ball = False
    game_over = 0

    # Function for outputting text onto the screen
    def draw_text(text, font1, text_column, x, y):
        img = font1.render(text, True, text_column)
        screen.blit(img, (x, y))

    # Brick wall class
    class wall():
        def __init__(self):
            self.blocks = []
            self.width = screen_width // cols
            self.height = 35

        def create_wall(self):
            # Define an empty list for an individual block
            block_individual = []
            for row in range(rows):
                # Reset the block row list
                block_row = []
                # Iterate through each column in that row
                for col in range(cols):
                    # Generate x and y positions for each block and create a rectangle from that
                    block_x = col * self.width
                    block_y = row * self.height + 35
                    rect = pygame.Rect(block_x, block_y, self.width, self.height)
                    # Assign block strength based on row
                    if row < 2:
                        strength = 4
                    elif row < 4:
                        strength = 3
                    elif row < 6:
                        strength = 2
                    elif row < 8:
                        strength = 1
                    # Create a list at this point to store the rect and colour data
                    block_individual = [rect, strength]
                    # Append that individual block to the block row
                    block_row.append(block_individual)
                # Append the row to the full list of blocks
                self.blocks.append(block_row)

        def draw_wall(self):
            for row in self.blocks:
                for block in row:
                    # Assign a colour based on block strength
                    if block[1] == 4:
                        block_col = block_obsidian
                    elif block[1] == 3:
                        block_col = block_end_stone
                    elif block[1] == 2:
                        block_col = block_stone
                    elif block[1] == 1:
                        block_col = block_wood

                    pygame.draw.rect(screen, block_col, block[0])
                    pygame.draw.rect(screen, bg, (block[0]), 2)

    # Paddle class
    class paddle():
        def __init__(self):
            self.reset()

        def move(self):
            # Reset movement direction
            self.direction = 0
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.direction = -1
            if key[pygame.K_RIGHT] and self.rect.right < screen_width:
                self.rect.x += self.speed
                self.direction = 1

        def draw(self):
            pygame.draw.rect(screen, paddle_color, self.rect)
            pygame.draw.rect(screen, paddle_outline, self.rect, 3)

        def reset(self):
            # Define paddle variables
            self.height = 20
            self.width = int(screen_width / paddle_size)
            self.x = int((screen_width / 2) - (self.width / 2))
            self.y = screen_height - (self.height * 2)
            self.speed = 10
            self.rect = Rect(self.x, self.y, self.width, self.height)
            self.direction = 0

    # Ball class
    class game_ball():
        def __init__(self, x, y):
            self.ball_rad = 12
            self.reset(x, y)

        def move(self):
            # Collision threshold
            collision_thresh = 15

            # Start off with the assumption that the wall has been destroyed completely
            wall_destroyed = 1
            row_count = 0
            for row in wall.blocks:
                item_count = 0
                for item in row:
                    # Check collision
                    if self.rect.colliderect(item[0]):
                        brick_sound.play()
                        global Score
                        global h_score
                        Score += 1
                        # Check if collision was from above
                        if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                            self.speed_y *= -1
                        # Check if collision was from below
                        if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                            self.speed_y *= -1
                            # Check if collision was from left
                        if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                            self.speed_x *= -1
                        # Check if collision was from right
                        if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                            self.speed_x *= -1

                        # Reduce the block's strength by doing damage to it
                        if wall.blocks[row_count][item_count][1] > 1:
                            wall.blocks[row_count][item_count][1] -= 1
                        else:
                            wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                    # Check if block still exists, in which case the wall is not destroyed
                    if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                        wall_destroyed = 0

                    # Increase item counter
                    item_count += 1
                # Increase row counter
                row_count += 1
            # After iterating through all the blocks, check if the wall is destroyed
            if wall_destroyed == 1:
                self.game_over = 1

            # Check for collision with walls
            if self.rect.left < 0 or self.rect.right > screen_width:
                self.speed_x *= -1
                wall_sound.play()

            # Check for collision with top and bottom of the screen
            if self.rect.top < 0:
                self.speed_y *= -1
            if self.rect.bottom > screen_height:
                self.game_over = -1

            # Look for collision with paddle
            if self.rect.colliderect(player_paddle):
                # Check if colliding from the top
                if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                    self.speed_y *= -1
                    self.speed_x += player_paddle.direction
                    paddle_sound.play()
                    if self.speed_x > self.speed_max:
                        self.speed_x = self.speed_max
                    elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                        self.speed_x = -self.speed_max
                else:
                    self.speed_x *= -1

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            if game_over == -1:
                Score = 0

            if game_over == 1:
                Score = 0

            return self.game_over

        def draw(self):
            pygame.draw.circle(screen, paddle_color, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                               self.ball_rad)
            pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                               self.ball_rad, 4)

        def reset(self, x, y):
            self.x = x - self.ball_rad
            self.y = y
            self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
            self.speed_x = 4
            self.speed_y = -4
            self.speed_max = 5
            self.game_over = 0

    # Create a wall
    wall = wall()
    wall.create_wall()

    # Create paddle
    player_paddle = paddle()

    # Create ball
    ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

    step = 0

    run = True
    while run:

        clock.tick(fps)
        screen.fill(bg)

        # Draw all objects
        wall.draw_wall()
        player_paddle.draw()
        ball.draw()

        if live_ball:
            # Draw paddle
            player_paddle.move()
            # Draw ball
            game_over = ball.move()
            if game_over != 0:
                live_ball = False

        # Print player instructions
        if not live_ball:
            if game_over == 0:
                draw_text('Click or Press space to start', font, text_color, 90, screen_height // 2 + 100)
            elif game_over == 1:
                draw_text('YOU WON!', font, text_color, 240, screen_height // 2 + 50)
                draw_text('Click anywhere to start', font, text_color, 130, screen_height // 2 + 100)
            elif game_over == -1:
                draw_text('YOU LOST', font, text_color, 240, screen_height // 2 + 50)
                draw_text('Click or Press space to start', font, text_color, 90, screen_height // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and live_ball == False:
                    pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and live_ball == False:
                    live_ball = True
                    ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
                    player_paddle.reset()
                    wall.create_wall()

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
                live_ball = True
                ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
                player_paddle.reset()
                wall.create_wall()

            try:
                global h_score
                h_score = int(high_score())

            except:
                h_score = 0

            if h_score < Score:
                h_score = Score
            with open('high.txt', 'w') as f:
                f.write(str(h_score))

        score_s = font.render(f"Score : {Score}", True, white)
        screen.blit(score_s, (15, 7))

        score_h = font.render(f"Top Score : {h_score}", True, white)
        screen.blit(score_h, (350, 7))

        pygame.display.update()


main_menu()
