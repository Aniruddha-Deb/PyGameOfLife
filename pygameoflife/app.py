import pygame
from pygame import Vector2

from pygameoflife.renderer import Renderer, Camera

def run():
	pygame.init()
	pygame.display.set_caption('PyGameOfLife')
	window_surface = pygame.display.set_mode((800,600))
	
	is_running = True
	
	renderer = Renderer(window_surface)
	camera = Camera(Vector2(-0.5,20.234), 50)
	
	renderer.render_grid(camera)
	pygame.display.update()

	dragging = False
	prevMB = None
	while is_running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				is_running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					dragging = True
					prevMB = Vector2(event.pos)
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					dragging = False
			elif event.type == pygame.MOUSEMOTION:
				if dragging:
					loc = Vector2(event.pos)
					delta = (loc - prevMB)
					delta.x *= -1
					camera.pos += delta/camera.get_scale()
					prevMB = loc
					renderer.render_grid(camera)
					pygame.display.update()
			elif event.type == pygame.MOUSEWHEEL:
				camera.add_to_scale(event.y)
				renderer.render_grid(camera)
				pygame.display.update()
