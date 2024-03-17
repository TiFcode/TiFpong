
# PROGRAM: TiFpong

import pygame
import random


# Initialize Pygame
pygame.init()

# Set window dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minimal Pong")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Font for score display
score_font = pygame.font.Font(None, 36)  # Use default font

# Scorekeeping
player_score = 0  # Initialize player_score
computer_score = 0  # Initialize computer_score

# Paddle settings
paddle_width = 15
paddle_height = 80

# Player paddle
player_x = 10
player_y = height // 2 - paddle_height // 2

# Computer paddle
computer_x = width - paddle_width - 10
computer_y = height // 2 - paddle_height // 2

# Paddle speeds
player_speed = 0
computer_speed = 7 

# Ball Settings
ball_x = width // 2
ball_y = height // 2
ball_radius = 16
ball_speed_x = 5  
ball_speed_y = 5  

# Make the computer to make mistakes
computer_percent_of_moving_correctly = 0.8 # 0.8 == 80%
computer_reaction_delay_maximum = 3  # Counter for delay
computer_reaction_delay = computer_reaction_delay_maximum

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Player paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -7
            if event.key == pygame.K_DOWN:
                player_speed = 7
        if event.type == pygame.KEYUP:
            player_speed = 0

    # Move paddles
    player_y += player_speed
    computer_y += computer_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Basic AI (move towards ball)
    # if computer_y + paddle_height//2 < ball_y:
    #     computer_speed = 7
    # elif computer_y + paddle_height//2 > ball_y:
    #     computer_speed = -7
        
    # Basic AI with randomness and delay
    if computer_reaction_delay > 0:
        computer_reaction_delay -= 1
    else:
        if computer_y + paddle_height//2 < ball_y:
            if random.random() < computer_percent_of_moving_correctly:
                computer_speed = 7
        elif computer_y + paddle_height//2 > ball_y:
            if random.random() < computer_percent_of_moving_correctly:  
                computer_speed = -7
        computer_reaction_delay = computer_reaction_delay_maximum  # Reset the delay

    # Collision and bounce 
    # (Add more refined collision handling for accurate bounces)
    if ball_y <= 0 or ball_y + ball_radius >= height:
        ball_speed_y *= -1
    if ball_x <= 0 or ball_x + ball_radius >= width:
        ball_speed_x *= -1  
      #      ball_x = width // 2  # Reset ball on score
      #      ball_y = height // 2
        
    
    # Collision with paddles
    if ball_x - ball_radius <= player_x + paddle_width and \
       player_y <= ball_y <= player_y + paddle_height:
      ball_speed_x *= -1
      
    if ball_x + ball_radius >= computer_x and \
       computer_y <= ball_y <= computer_y + paddle_height:
       ball_speed_x *= -1
       
    # Score Updates
    if ball_x <= 0: 
        computer_score += 1
        ball_x = width // 2  
        ball_y = height // 2
        ball_speed_x *= -1  # Optionally reverse after a point
    elif ball_x + ball_radius >= width:  
        player_score += 1
        ball_x = width // 2  
        ball_y = height // 2
        ball_speed_x *= -1 
  

    # Keep paddles within screen bounds
    if player_y < 0:
        player_y = 0
    if player_y + paddle_height > height:
        player_y = height - paddle_height 
    # (Do the same for computer paddle)

    # Drawing
    screen.fill(black)  # Clear the screen
    
    
    # Draw scores
    player_score_text = score_font.render(str(player_score), True, white)
    computer_score_text = score_font.render(str(computer_score), True, white)
    screen.blit(player_score_text, (20, 10))
    screen.blit(computer_score_text, (width - player_score_text.get_width() - 20, 10))


    # Draw paddles
    pygame.draw.rect(screen, white, (player_x, player_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (computer_x, computer_y, paddle_width, paddle_height))
    # Draw ball
    pygame.draw.circle(screen, white, (ball_x, ball_y), ball_radius)

    pygame.display.flip()  # Update the display
    clock = pygame.time.Clock()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
