import math
import pygame
import pygame_gui
from pygame import Vector2, Surface
from pygame_gui import UIManager

from pygameoflife.game import Game

BG_COLOR = pygame.Color('white')
BUTTON_COLOR = pygame.Color('#aaabab')
GRID_COLOR = pygame.Color('#c6c6c6')
ACTIVE_CELL_COLOR = pygame.Color('black')

BTN_HEIGHT = 50
HDR_HEIGHT = 100

class Button():
	
	def __init__(self, text: str, pos: pygame.Rect, color: pygame.Color, rel: int):
		self.FONT = pygame.font.SysFont('Menlo', 20)
		self.text = text
		self.pos = pos
		self.color = color
		self.rel = rel
	
	def render(self, surf: Surface):
		text_surf = self.FONT.render(self.text, True, ACTIVE_CELL_COLOR)
		w, h = surf.get_size()
		x = self.pos.x
		y = self.pos.y
		if self.rel == 0:
			# (centre,centre) relative
			x = w/2+self.pos.x
			y = h/2+self.pos.y
		elif self.rel == 1:
			# (right,centre) relative
			x = w+self.pos.x
			y = h/2+self.pos.y
		pygame.draw.rect(surf, self.color, pygame.Rect(x, y, self.pos.w, self.pos.h))
		surf.blit(text_surf, (x, y))

class MenuBar():
	
	def __init__(self):
		self.FONT = pygame.font.SysFont('Menlo', 20)
		self.buttons = [
			Button("Play/Pause", pygame.Rect(-105,-25,100,50), BUTTON_COLOR, 0),
			Button("Clear", pygame.Rect(5,-25,100,50), BUTTON_COLOR, 0),
			Button("-", pygame.Rect(-50,-20,40,40), BUTTON_COLOR, 1),
			Button("+", pygame.Rect(-20,-20,40,40), BUTTON_COLOR, 1)
		]
		self.gen = 0
		self.pop = 0
		
	def update(self, game: Game):
		self.gen = game.gen
		self.pop = len(game.live_cells)

	def render(self, surf: Surface):
		w, h = surf.get_size()
		surf.fill(BG_COLOR)
		for button in self.buttons:
			button.render(surf)

		gen_text = self.FONT.render(f"Generation: {self.gen}", True, ACTIVE_CELL_COLOR)
		pop_text = self.FONT.render(f"Population: {self.pop}", True, ACTIVE_CELL_COLOR)

		surf.blit(gen_text, (20,20))
		surf.blit(pop_text, (20,50))

class Renderer():
	
	def __init__(self, surface: Surface):
		self.surface = surface
		self.surface.fill(BG_COLOR)
		self.surface_changed = False;
	
	def render_menubar(self, menubar: MenuBar):
		w, h = self.surface.get_size()

		surf = pygame.Surface((w,HDR_HEIGHT))

		menubar.render(surf)
		self.surface.blit(surf, (0,0))

		self.surface_changed = True

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
