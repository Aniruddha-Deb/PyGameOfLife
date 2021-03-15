import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

FG_COLOR = pygame.Color('white')
BG_COLOR = pygame.Color('black')

class Ball:
	
	def __init__(self, pos, r):
		[self.x, self.y] = pos
		self.r = r
	
	def getPos(self):
		return (self.x, self.y)

	def render(self, surface):
		pygame.draw.circle(surface, FG_COLOR, self.getPos(), self.r, width=1)
	
	def clear(self, surface):
		pygame.draw.circle(surface, BG_COLOR, self.getPos(), self.r, width=1)

pygame.init()
pygame.display.set_caption('PyGameOfLife')
window_surface = pygame.display.set_mode((800,600))

background = pygame.Surface((800, 600))
background.fill(BG_COLOR)

is_running = True

pygame.draw.rect(window_surface, FG_COLOR, pygame.Rect(0,0,800,600), 1)

ball = Ball([30,30], 20)
ball.render(window_surface)
speed = [3,3]

pygame.display.update()

while is_running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			is_running = False
	
	ball.clear(window_surface)
	if (ball.x >= 800-ball.r or ball.x <= ball.r):
		speed[0] *= -1
		pygame.draw.rect(window_surface, FG_COLOR, pygame.Rect(0,0,800,600), 1)
	if (ball.y >= 600-ball.r or ball.y <= ball.r):
		speed[1] *= -1
		pygame.draw.rect(window_surface, FG_COLOR, pygame.Rect(0,0,800,600), 1)
	
	ball.x += speed[0]
	ball.y += speed[1]
	ball.render(window_surface)
	pygame.display.update()
	pygame.time.delay(10)
	
