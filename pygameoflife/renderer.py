import math
import pygame
from pygame import Vector2, Surface

BG_COLOR = pygame.Color('white')
GRID_COLOR = pygame.Color('grey80')
ACTIVE_CELL_COLOR = pygame.Color('grey95')

class Renderer:
	
	def __init__(self, surface: Surface):
		self.surface = surface
	
	def render_grid(self, camera):
		w, h = self.surface.get_size()
		self.surface.fill(BG_COLOR)
		# draw vertical lines
		i = math.ceil(camera.pos.x)
		vlpos = (i-camera.pos.x)*camera.scale
		while vlpos < w:
			pygame.draw.line(self.surface, GRID_COLOR, (vlpos,0), (vlpos,h), width=1)
			vlpos += camera.scale

		j = math.floor(camera.pos.y)
		hlpos = (camera.pos.y-j)*camera.scale
		while hlpos < h:
			pygame.draw.line(self.surface, GRID_COLOR, (0,hlpos), (w,hlpos), width=1)
			hlpos += camera.scale
	
class Camera:
	
	def __init__(self, top_left: Vector2, scale: float):
		self.pos = top_left
		self.scale = scale
