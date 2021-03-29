import math
import pygame
import pygame_gui
from pygame import Vector2, Surface
from pygame_gui import UIManager

from pygameoflife.game import Game

BG_COLOR = pygame.Color('white')
GRID_COLOR = pygame.Color('#c6c6c6')
ACTIVE_CELL_COLOR = pygame.Color('black')

BTN_HEIGHT = 50
HDR_HEIGHT = 100

class MenuBar(UIManager):
	
	def __init__(self, bg: Surface):
		super().__init__((800,600))
		self.bg = bg
		self.create_components()
	
	def create_components(self):
		cx, cy = Vector2(self.bg.get_size())/2
		self.pp_btn = pygame_gui.elements.UIButton(
				relative_rect=pygame.Rect((cx-100,25),(100, 50)),
                text='Play/Pause',
                manager=self)
		self.clear_btn = pygame_gui.elements.UIButton(
				relative_rect=pygame.Rect((cx+5, 25), (80, 50)),
                text='Clear',
                manager=self)
		self.speed_reduce_btn = pygame_gui.elements.UIButton(
				relative_rect=pygame.Rect((700,30),(40,40)),
				text='-',
				manager=self)
	
	def update_on_resize(self):
		w,h = self.bg.get_size()
		self.window_resolution = (w,h) 
		self.pp_btn.set_position((w/2-100,25))
		self.clear_btn.set_position((w/2+5,25))
		self.speed_reduce_btn.set_position((w-100,30))
		print(self.window_resolution)

	def render(self):
		w = self.bg.get_size()[0]
		pygame.draw.rect(self.bg, BG_COLOR, pygame.Rect(0,0,w,HDR_HEIGHT))
		super().draw_ui(self.bg)

class Renderer():
	
	def __init__(self, surface: Surface):
		self.surface = surface
		self.surface.fill(BG_COLOR)
		self.surface_changed = False;
	
	def render_grid(self, camera):
		w, h = self.surface.get_size()
			
		pygame.draw.rect(self.surface, BG_COLOR, 
			pygame.Rect(0,HDR_HEIGHT,w,h-HDR_HEIGHT) )
		scale = camera.get_scale()

		i = math.ceil(camera.pos.x)
		vlpos = (i-camera.pos.x)*scale
		while vlpos < w:
			pygame.draw.line(self.surface, GRID_COLOR, (vlpos,HDR_HEIGHT), (vlpos,h), width=1)
			vlpos += scale

		j = math.floor(camera.pos.y)
		hlpos = HDR_HEIGHT + (camera.pos.y-j)*scale
		while hlpos < h:
			pygame.draw.line(self.surface, GRID_COLOR, (0,hlpos), (w,hlpos), width=1)
			hlpos += scale

		self.surface_changed = True
	
	# Convention is that cell (x,y) is the TOP RIGHT cell ie it spans the range
	# (x->x+1, y->y+1)
	def render_cells(self, camera, game):
		w, h = self.surface.get_size()
		scale = camera.get_scale()

		camx, camy = camera.pos
		x = math.floor(camx)
		y = math.floor(camy)
		nx = math.floor(w/scale + 2)
		ny = math.floor((h-HDR_HEIGHT)/scale + 2)
		rx, ry = (0,0)
		cx, cy = ((x-camx)*scale, HDR_HEIGHT-(y+1-camy)*scale)
		while rx < nx:
			while ry > -ny:
				if game.is_alive((x+rx, y+ry)):
					# render cell
					cell_tlx, cell_tly = cx+1, cy+1
					diff_x, diff_y = (0,0)
					if cell_tly < HDR_HEIGHT:
						diff_y = HDR_HEIGHT-cell_tly
						cell_tly = HDR_HEIGHT
					pygame.draw.rect(
						self.surface, 
						ACTIVE_CELL_COLOR,
						pygame.Rect(cell_tlx, cell_tly, scale-diff_x-1, scale-diff_y-1)
					)
				ry -= 1
				cy += scale
			rx += 1
			cx += scale
			cy = HDR_HEIGHT-(y+1-camy)*scale
			ry = 0

		self.surface_changed = True
	
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
