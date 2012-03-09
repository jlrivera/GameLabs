import pygame, sys, pygame.mixer


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_START_X = 10
PADDLE_START_Y = 20
OPADDLE_START_X = SCREEN_WIDTH - 10
OPADDLE_START_Y = SCREEN_HEIGHT/ 2 -20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 10
BALL_WIDTH_HEIGHT = 16

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

pygame.mixer.init()
ysound = pygame.mixer.Sound("pongyou.wav")
osound = pygame.mixer.Sound("pongopp.wav")

# This is a rect that contains the ball at the beginning it is set in the center of the screen
ball_rect = pygame.Rect((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), (BALL_WIDTH_HEIGHT, BALL_WIDTH_HEIGHT))

# Speed of the ball (x, y)
ball_speed = [BALL_SPEED, BALL_SPEED]

#paddles vertically centered on the left side
paddle_rect = pygame.Rect((PADDLE_START_X, PADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
opaddle_rect = pygame.Rect((OPADDLE_START_X, OPADDLE_START_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))


# Scoring: 1 point if you hit the ball, -5 point if you miss the ball
yscore = 0
oscore = 0

# Load the font for displaying the score
font = pygame.font.Font(None, 30)

# Game loop
while True:
	# Event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit(0)
			pygame.quit()
		# Control the paddle with the mouse
		elif event.type == pygame.MOUSEMOTION:
			paddle_rect.centery = event.pos[1]
			# correct paddle position if it's going out of window
			if paddle_rect.top < 0:
				paddle_rect.top = 0
			elif paddle_rect.bottom >= SCREEN_HEIGHT:
				paddle_rect.bottom = SCREEN_HEIGHT

	# This test if up or down keys are pressed; if yes, move the paddle
	if pygame.key.get_pressed()[pygame.K_UP] and paddle_rect.top > 0:
		paddle_rect.top -= BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_DOWN] and paddle_rect.bottom < SCREEN_HEIGHT:
		paddle_rect.top += BALL_SPEED
	elif pygame.key.get_pressed()[pygame.K_ESCAPE]:
		sys.exit(0)
		pygame.quit()
		
	# Update ball position
	ball_rect.left += ball_speed[0]
	ball_rect.top += ball_speed[1]

	# Ball collision with rails
	if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
		ball_speed[1] = -ball_speed[1]
	if ball_rect.right >= SCREEN_WIDTH:
		ball_speed[0] = -ball_speed[0]
		yscore += 1
	if ball_rect.left <= 0:
		ball_speed[0] = -ball_speed[0]
		oscore += 1

	# Test if the ball is hit by the paddle; if yes reverse speed and add a point
	if paddle_rect.colliderect(ball_rect):
		ysound.play()
		ball_speed[0] = -ball_speed[0]
	
	# Clear screen
	screen.fill((255, 255, 255))

	# Render the ball, line, the paddle, and the score
	pygame.draw.rect(screen, (0, 0, 0), paddle_rect) # Your paddle
	pygame.draw.rect(screen, (0, 0, 0), opaddle_rect) # Opponent's paddle
	pygame.draw.circle(screen, (0, 0, 0), ball_rect.center, ball_rect.width / 2) # The ball
	pygame.draw.line(screen, (255,0,0) ,(SCREEN_WIDTH/2 , 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT),5)

	yscore_text = font.render(str(yscore), True, (0, 0, 0))
	oscore_text = font.render(str(oscore), True, (0, 0, 0))
	screen.blit(yscore_text, ((40) - font.size(str(yscore))[0] / 2, 5)) # The score
	screen.blit(oscore_text, ((SCREEN_WIDTH - 40) - font.size(str(oscore))[0] / 2, 5)) # The score

	
	# Update screen and wait 20 milliseconds
	pygame.display.flip()
	pygame.time.delay(20)
