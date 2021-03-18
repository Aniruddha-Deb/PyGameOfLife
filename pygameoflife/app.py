import pygame
from pygame import Vector2

from pygameoflife.renderer import Renderer, Camera

class App:
	
	def __init__(self):
		pygame.init()
		pygame.display.set_caption('PyGameOfLife')

		self.win_surf = pygame.display.set_mode((800,600))
		self.is_running = True

		self.renderer = Renderer(self.win_surf)
		self.camera = Camera(Vector2(0,0), 50)

		self.renderer.render_grid(self.camera)
		pygame.display.update()

		self.dragging = False
		self.shift_pressed = False
		self.prev_mouse_loc = None

	def handle_mouse_down_event(self, evt):
		if evt.button == 1:
			self.dragging = True
			self.prev_mouse_loc = Vector2(evt.pos)
						
	def handle_mouse_up_event(self, evt):
		if evt.button == 1:
			self.dragging = False

	def handle_mouse_motion_event(self, evt):
		if self.dragging:
			loc = Vector2(evt.pos)
			delta = (loc - self.prev_mouse_loc)
			delta.x *= -1
			self.camera.pos += delta/self.camera.get_scale()
			self.prev_mouse_loc = loc
			self.renderer.render_grid(self.camera)

	def handle_mouse_wheel_event(self, evt):
		self.camera.add_to_scale(evt.y)
		self.renderer.render_grid(self.camera)

	def handle_quit_event(self, evt):
		self.is_running = False

	def run(self):
		evt_dict = {
			pygame.MOUSEBUTTONDOWN: self.handle_mouse_down_event,
			pygame.MOUSEBUTTONUP: self.handle_mouse_up_event,
			pygame.MOUSEMOTION: self.handle_mouse_motion_event,
			pygame.MOUSEWHEEL: self.handle_mouse_wheel_event,
			pygame.QUIT: self.handle_quit_event,
		}

		while self.is_running:
			evts = [e for e in pygame.event.get() if e.type in evt_dict]
			for evt in evts:
				evt_dict[evt.type](evt) # run method corresponsing to event

			if self.renderer.surface_changed:
				pygame.display.update()
				self.renderer.surface_changed = False
