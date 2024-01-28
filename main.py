import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set a timer for the special square event
SPECIAL_SQUARE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPECIAL_SQUARE_EVENT, 30000)  # 30,000 milliseconds = 30 seconds

# Constants
WIDTH, HEIGHT = 1150, 475
SCOREBOARD_HEIGHT = 50 
CHART_HEIGHT = 150
CHART_MARGIN = 20
WINDOW_HEIGHT = HEIGHT + SCOREBOARD_HEIGHT + CHART_MARGIN + CHART_HEIGHT 
BALL_SIZE = 24
BALL_SPEED = 8
SQUARE_SIZE = 20
MAX_SCORE_HISTORY = 50

# Colors
COLOR1 = (128, 0, 128)  
COLOR2 = (255, 165, 0)  
COLOR3 = (0, 255, 0)
COLOR4 = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Capture")

class Button:
    def __init__(self, x, y, width, height, text=None, color=(73, 73, 73), highlighted_color=(189, 189, 189), function=None, params=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.highlighted_color = highlighted_color
        self.function = function
        self.params = params
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 20)

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text:
            text = self.font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        return self.rect.collidepoint(pos)

    def update_color(self, pos):
        if self.is_over(pos):
            self.color = self.highlighted_color
        else:
            self.color = (73, 73, 73)

    def click(self):
        if self.params:
            self.function(*self.params)
        else:
            self.function()

# Initialize game_started variable
game_started = False

def start_game():
    global game_started
    game_started = True
    # Add code here to start the game

def reset_game():
    global game_started
    game_started = False
    # Add code here to reset the game state

# Create start and reset buttons
start_button = Button(WIDTH - 150, HEIGHT + (SCOREBOARD_HEIGHT - 30) // 2, 70, 30, 'Start', function=start_game)
reset_button = Button(WIDTH - 70, HEIGHT + (SCOREBOARD_HEIGHT - 30) // 2, 70, 30, 'Reset', function=reset_game)

# In your main game loop, update the button color based on mouse position
for event in pygame.event.get():
    pos = pygame.mouse.get_pos()
    start_button.update_color(pos)
    reset_button.update_color(pos)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.is_over(pos):
            start_button.click()
        if reset_button.is_over(pos):
            reset_button.click()


class Ball:
    def __init__(self, x, y, color, paint_color):
        self.x = x
        self.y = y
        self.color = WHITE  # Set the ball color to be white
        self.paint_color = paint_color
        self.dx = BALL_SPEED if color == COLOR1 else -BALL_SPEED
        self.dy = BALL_SPEED if random.choice([True, False]) else -BALL_SPEED

    def bounce(self, collision_type):
        # If the ball is in the special state, it should not slow down
        if abs(self.dx) != 11 and abs(self.dy) != 11:
            if collision_type == 'horizontal':
                self.dx = -self.dx
                self.dy += random.choice([-1, 1])  # vertical deviation
            elif collision_type == 'vertical':
                self.dy = -self.dy
                self.dx += random.choice([-1, 1])  # horizontal deviation

            # Ensure that the ball's speed doesn't exceed a maximum value
            self.dx = max(-BALL_SPEED, min(self.dx, BALL_SPEED))
            self.dy = max(-BALL_SPEED, min(self.dy, BALL_SPEED))
        else:
            # If the ball is in the special state, it should only change direction
            if collision_type == 'horizontal':
                self.dx = -self.dx
            elif collision_type == 'vertical':
                self.dy = -self.dy

    def move(self, squares):
        # Predict the next position
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        # Check for collision with the walls
        if new_x < 0 or new_x > WIDTH - BALL_SIZE:
            self.bounce('horizontal')
        if new_y < 0 or new_y > HEIGHT - BALL_SIZE:
            self.bounce('vertical')

        # Update the position
        self.x += self.dx
        self.y += self.dy

        # Check for collision with squares
        for row in squares:
            for square in row:
                if square['rect'].colliderect(self.x, self.y, BALL_SIZE, BALL_SIZE):
                    if square['color'] != self.paint_color:
                        square['color'] = self.paint_color
                        # Determine collision type (horizontal/vertical)
                        collision_type = self.determine_collision_type(square['rect'])
                        self.bounce(collision_type)
                        # Check if the square is special
                        if square.get('special'):
                            self.increase_speed()
                            square['special'] = False
                            pygame.time.set_timer(SPECIAL_SQUARE_EVENT, 30000)  # Reset the timer for the special square event
                        return

    def draw(self, squares):
        # Calculate the number of squares of the ball's color
        num_squares = sum(square['color'] == self.paint_color for row in squares for square in row)
        
        # Adjust the ball size based on the number of squares
        adjusted_ball_size = BALL_SIZE + num_squares // 100  # Adjust the denominator to control the rate of size increase

        # Draw a larger circle behind the ball
        pygame.draw.ellipse(screen, self.paint_color, (self.x - 5, self.y - 5, adjusted_ball_size + 10, adjusted_ball_size + 10))
        
        # Draw the ball
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, adjusted_ball_size, adjusted_ball_size))
        
        # Render the size text
        font = pygame.font.Font(None, 15)  # Adjust the font size as needed
        text = font.render(str(adjusted_ball_size), True, BLACK)
        text_rect = text.get_rect(center=(self.x + adjusted_ball_size // 2, self.y + adjusted_ball_size // 2))
        
        # Draw the size text on the ball
        screen.blit(text, text_rect)

    def increase_speed(self):
        self.dx = 11 if self.dx > 0 else -11
        self.dy = 11 if self.dy > 0 else -11
        self.color = GREEN
        pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

    def reset_speed(self):
        self.dx = BALL_SPEED if self.dx > 0 else -BALL_SPEED
        self.dy = BALL_SPEED if self.dy > 0 else -BALL_SPEED
        self.color = WHITE  # Change color back to white

    def determine_collision_type(self, rect):
        # Check if collision is more likely horizontal or vertical
        if abs(self.x + BALL_SIZE / 2 - rect.centerx) > abs(self.y + BALL_SIZE / 2 - rect.centery):
            return 'horizontal'
        else:
            return 'vertical'

# create squares
def create_squares():
    squares = []
    for y in range(0, HEIGHT, SQUARE_SIZE):
        row = []
        for x in range(0, WIDTH, SQUARE_SIZE):
            if x < WIDTH / 4:
                color = COLOR1
            elif x < WIDTH / 2:
                color = COLOR2
            elif x < 3 * WIDTH / 4:
                color = COLOR3
            else:
                color = COLOR4
            square = {'rect': pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE), 'color': color, 'last_change': pygame.time.get_ticks()}
            row.append(square)
        squares.append(row)
    # Randomly choose one square to be the special square
    special_row = random.choice(squares)
    special_square = random.choice(special_row)
    special_square['special'] = True
    special_square['color'] = GREEN 
    return squares

# initialize balls and squares
ball1 = Ball(WIDTH // 8, HEIGHT // 2, WHITE, COLOR1)
ball2 = Ball(3 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR2)
ball3 = Ball(5 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR3)
ball4 = Ball(7 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR4)
squares = create_squares()

# initialize score history
score_history1 = []
score_history2 = []
score_history3 = []
score_history4 = []

# calculate scores
def calculate_scores(squares):
    score1 = 0
    score2 = 0
    score3 = 0
    score4 = 0
    for row in squares:
        for square in row:
            if square['color'] == COLOR1:
                score1 += 1
            elif square['color'] == COLOR2:
                score2 += 1
            elif square['color'] == COLOR3:
                score3 += 1
            elif square['color'] == COLOR4:
                score4 += 1
    return score1, score2, score3, score4

# draw the scoreboard
def draw_scoreboard(score1, score2, score3, score4):
    scoreboard_rect = pygame.Rect(0, HEIGHT, WIDTH, SCOREBOARD_HEIGHT)
    pygame.draw.rect(screen, BLACK, scoreboard_rect)
    font = pygame.font.Font(None, 36)
    
    # Get the current time since pygame.init() was called
    current_time = pygame.time.get_ticks()
    
    # Convert the time to minutes and seconds
    minutes = current_time // 60000  # 1 minute = 60,000 milliseconds
    seconds = (current_time % 60000) // 1000
    
    # Create the timer string
    timer_string = f"{int(minutes)}:{int(seconds):02d}"
    
    score_text1 = font.render(f"{score1}", True, COLOR1)
    score_text2 = font.render(f"{score2}", True, COLOR2)
    score_text3 = font.render(f"{score3}", True, COLOR3)
    score_text4 = font.render(f"{score4}", True, COLOR4)
    timer_text = font.render(timer_string, True, WHITE)
    
    screen.blit(score_text1, (WIDTH // 4 - score_text1.get_width() // 2, HEIGHT + (SCOREBOARD_HEIGHT - score_text1.get_height()) // 2))
    screen.blit(score_text2, (WIDTH // 2 - score_text2.get_width() // 2, HEIGHT + (SCOREBOARD_HEIGHT - score_text2.get_height()) // 2))
    screen.blit(score_text3, (3 * WIDTH // 4 - score_text3.get_width() // 2, HEIGHT + (SCOREBOARD_HEIGHT - score_text3.get_height()) // 2))
    screen.blit(score_text4, (WIDTH - score_text4.get_width(), HEIGHT + (SCOREBOARD_HEIGHT - score_text4.get_height()) // 2))  # Adjusted position for blue score
    screen.blit(timer_text, (10, HEIGHT + (SCOREBOARD_HEIGHT - timer_text.get_height()) // 2)) 

# update and draw the line chart using Pygame's drawing functions
def draw_line_chart_pygame(score_history1, score_history2, score_history3, score_history4):
    # Limit the history size
    score_history1 = score_history1[-MAX_SCORE_HISTORY:]
    score_history2 = score_history2[-MAX_SCORE_HISTORY:]
    score_history3 = score_history3[-MAX_SCORE_HISTORY:]
    score_history4 = score_history4[-MAX_SCORE_HISTORY:]

    # Calculate the maximum score to normalize the chart scale
    max_score = max(max(score_history1, default=0), max(score_history2, default=0), max(score_history3, default=0), max(score_history4, default=0), 1)

    # Calculate the spacing between points on the x-axis
    x_spacing = WIDTH / MAX_SCORE_HISTORY

    # Starting position for the chart on the y-axis
    chart_base = HEIGHT + SCOREBOARD_HEIGHT + CHART_MARGIN

    # Draw the chart background and grid lines
    chart_rect = pygame.Rect(0, chart_base, WIDTH, CHART_HEIGHT)
    pygame.draw.rect(screen, BLACK, chart_rect)
    for x in range(0, WIDTH, int(x_spacing)):
        pygame.draw.line(screen, (50, 50, 50), (x, chart_base), (x, chart_base + CHART_HEIGHT))
    for y in range(chart_base, chart_base + CHART_HEIGHT, CHART_HEIGHT // 10):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

    # Draw the score history lines
    for i in range(1, len(score_history1)):
        start_pos = ((i - 1) * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history1[i - 1] / max_score))
        end_pos = (i * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history1[i] / max_score))
        pygame.draw.line(screen, COLOR1, start_pos, end_pos, 2)

    for i in range(1, len(score_history2)):
        start_pos = ((i - 1) * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history2[i - 1] / max_score))
        end_pos = (i * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history2[i] / max_score))
        pygame.draw.line(screen, COLOR2, start_pos, end_pos, 2)

    for i in range(1, len(score_history3)):
        start_pos = ((i - 1) * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history3[i - 1] / max_score))
        end_pos = (i * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history3[i] / max_score))
        pygame.draw.line(screen, COLOR3, start_pos, end_pos, 2)

    for i in range(1, len(score_history4)):
        start_pos = ((i - 1) * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history4[i - 1] / max_score))
        end_pos = (i * x_spacing, chart_base + CHART_HEIGHT - (CHART_HEIGHT / 2) * (score_history4[i] / max_score))
        pygame.draw.line(screen, COLOR4, start_pos, end_pos, 2)

# Set a timer for the board rotation event
ROTATE_BOARD_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(ROTATE_BOARD_EVENT, 60000)  # 60,000 milliseconds = 60 seconds

def rotate_board(squares):
    return [list(reversed(col)) for col in zip(*squares)]

def reset_game():
    global game_started, squares, ball1, ball2, ball3, ball4, score_history1, score_history2, score_history3, score_history4
    game_started = False
    # Reset squares to their original state
    squares = create_squares()
    # Reset balls to their original state
    ball1 = Ball(WIDTH // 8, HEIGHT // 2, WHITE, COLOR1)
    ball2 = Ball(3 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR2)
    ball3 = Ball(5 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR3)
    ball4 = Ball(7 * WIDTH // 8, HEIGHT // 2, WHITE, COLOR4)
    # Reset score histories
    score_history1 = []
    score_history2 = []
    score_history3 = []
    score_history4 = []

# Main game loop
running = True
while running:
    screen.fill(WHITE)  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT + 1:  
            ball1.reset_speed()
            ball2.reset_speed()
            ball3.reset_speed()
            ball4.reset_speed()
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)  
        elif event.type == SPECIAL_SQUARE_EVENT:  
            # Remove the special status from all squares
            for row in squares:
                for square in row:
                    square['special'] = False

            # Randomly choose one square to be the new special square
            special_row = random.choice(squares)
            special_square = random.choice(special_row)
            special_square['special'] = True
            special_square['color'] = GREEN 
            pygame.time.set_timer(SPECIAL_SQUARE_EVENT, 30000)  
        elif event.type == ROTATE_BOARD_EVENT: 
            squares = rotate_board(squares)

        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            start_button.update_color(pos)
            reset_button.update_color(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if start_button.is_over(pos) and not game_started:
                start_button.click()
            if reset_button.is_over(pos):
                reset_button.click()

    # Draw squares
    for row in squares:
        for square in row:
            pygame.draw.rect(screen, square['color'], square['rect'])

    # Move and draw balls
    ball1.move(squares)
    ball2.move(squares)
    ball3.move(squares)
    ball4.move(squares)
    ball1.draw(squares)
    ball2.draw(squares)
    ball3.draw(squares)
    ball4.draw(squares)

    # Calculate scores and draw scoreboard
    score1, score2, score3, score4 = calculate_scores(squares)
    draw_scoreboard(score1, score2, score3, score4)

    # Update score history and draw the line chart using Pygame
    score_history1.append(score1)
    score_history2.append(score2)
    score_history3.append(score3)
    score_history4.append(score4)
    draw_line_chart_pygame(score_history1, score_history2, score_history3, score_history4)  



    # Update the display
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()