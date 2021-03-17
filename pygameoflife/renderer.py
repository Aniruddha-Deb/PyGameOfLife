import math
import pygame
from pygame import Vector2, Surface

from pygameoflife.game import Game

BG_COLOR = pygame.Color('white')
GRID_COLOR = pygame.Color('grey80')
ACTIVE_CELL_COLOR = pygame.Color('grey95')

class Renderer:
	
	def __init__(self, surface: Surface):
		self.surface = surface
	
	def render_grid(self, camera):
		w, h = self.surface.get_size()
		self.surface.fill(BG_COLOR)
		scale = camera.get_scale()
		# draw vertical lines
		i = math.ceil(camera.pos.x)
		vlpos = (i-camera.pos.x)*scale
		while vlpos < w:
			pygame.draw.line(self.surface, GRID_COLOR, (vlpos,0), (vlpos,h), width=1)
			vlpos += scale

		j = math.floor(camera.pos.y)
		hlpos = (camera.pos.y-j)*scale
		while hlpos < h:
			pygame.draw.line(self.surface, GRID_COLOR, (0,hlpos), (w,hlpos), width=1)
			hlpos += scale
	
	def render_cells(self, camera, game):
		# TODO implement
	
class Camera:
	
	def __init__(self, top_left: Vector2, scale: float):
		self.pos = top_left
		self._scale = scale
	
	def set_scale(self, scale: float):
		if scale >= 2:
			self._scale = scale
	
	def get_scale(self):
		return self._scale
	
	def add_to_scale(self, addend: float):
		if (self._scale + addend >= 2):
			self._scale += addend
