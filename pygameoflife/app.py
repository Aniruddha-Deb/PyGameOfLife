import pygame
import pygame_gui
import math
from pygame import Vector2

import pygameoflife.renderer
from pygameoflife.renderer import MenuBar, Renderer, Camera
from pygameoflife.game import Game

MIN_SIZE = (800, 600)
FRAMERATE = 60

class App:
	
	def __init__(self):
		pygame.init()
		print("Init pygame")
		pygame.font.init()
		print("Init pygame font")
		pygame.display.set_caption('PyGameOfLife')

		self.win_surf = pygame.display.set_mode(MIN_SIZE, pygame.RESIZABLE)
		self.is_running = True
		self.game_paused = True
		
		self.game = Game()
		# testing only
		self.game.activate_cell((5,-5))
		self.game.activate_cell((6,-5))
		self.game.activate_cell((6,-6))
		self.game.activate_cell((6,-4))
		self.game.activate_cell((7,-4))

		self.renderer = Renderer(self.win_surf)
		self.camera = Camera(Vector2(-9,5), 25)
		print("Made everything else")
		self.menubar = MenuBar(self)
		print("Made menubar")
		self.menubar.update(self.game)

		self.renderer.render_grid(self.camera)
		self.renderer.render_cells(self.camera, self.game)
		self.renderer.render_menubar(self.menubar)
		pygame.display.update()

		self.dragging = False
		self.shift_pressed = False
		self.btn_active = None
		self.prev_mouse_loc = None

	def get_cell_at(self, pos: Vector2):
		x = pos.x/self.camera.get_scale()
		y = (pos.y-pygameoflife.renderer.HDR_HEIGHT)/self.camera.get_scale()

		cx = math.floor(self.camera.pos.x+x)
		cy = math.floor(self.camera.pos.y-y)

		return (cx, cy)
	
	def get_cell_at_lazy(self, pos: Vector2):
		x = pos.x/self.camera.get_scale()
		y = (pos.y-pygameoflife.renderer.HDR_HEIGHT)/self.camera.get_scale()

		cxf = self.camera.pos.x+x
		cyf = self.camera.pos.y-y
		cx = math.floor(cxf)
		cy = math.floor(cyf)

		if cxf-cx < 0.2:
			cx -= 1
		elif cxf-cx > 0.8:
			cx += 1

		if cyf-cy < 0.2:
			cy -= 1
		elif cyf-cy > 0.8:
			cy += 1

		return (cx, cy)
			
	def toggle_cell_at(self, pos: Vector2):
		self.game.toggle_cell(self.get_cell_at(pos))
	
	def activate_cell_at(self, pos: Vector2):
		cell = self.get_cell_at(pos)
		if not self.game.is_alive(cell):
			self.game.activate_cell(cell)

	def deactivate_cell_at(self, pos: Vector2):
		cell = self.get_cell_at(pos)
		if self.game.is_alive(cell):
			self.game.deactivate_cell(cell)
	
	def play_pause(self):
		self.game_paused = not self.game_paused 
	
	def reset(self):
		self.game.reset()
		self.menubar.update(self.game)
		self.renderer.render_menubar(self.menubar)
		self.renderer.render_grid(self.camera)
		self.renderer.render_cells(self.camera, self.game)

	def handle_mouse_down_event(self, evt):
		if evt.button == pygame.BUTTON_LEFT:
			self.prev_mouse_loc = Vector2(evt.pos)
			self.drag_start_loc = Vector2(evt.pos)
			if self.btn_active:
				self.btn_active.color = pygameoflife.renderer.BTN_CLICK_COLOR
				self.renderer.render_menubar(self.menubar)
				self.btn_active.onclick()

	def handle_mouse_up_event(self, evt):
		if evt.button == pygame.BUTTON_LEFT:
			if not self.dragging and evt.pos[1] > pygameoflife.renderer.HDR_HEIGHT:
				# just a click
				self.toggle_cell_at(self.prev_mouse_loc)
				self.menubar.update(self.game)
				self.renderer.render_menubar(self.menubar)
				self.renderer.render_grid(self.camera)
				self.renderer.render_cells(self.camera, self.game)
			elif self.btn_active:
				self.btn_active.color = pygameoflife.renderer.ACTIVE_BTN_COLOR
				self.renderer.render_menubar(self.menubar)
			self.dragging = False
		
	def handle_mouse_motion_event(self, evt):
		curr_pos = Vector2(evt.pos)
		if evt.buttons[0]:
			if (self.drag_start_loc - curr_pos).length() > 5:
				self.dragging = True

			if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
				self.activate_cell_at(curr_pos)
			elif pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]:
				self.deactivate_cell_at(curr_pos)
			elif self.dragging:
				delta = Vector2(curr_pos - self.prev_mouse_loc)
				delta.x *= -1
				self.camera.pos += delta/self.camera.get_scale()
			self.menubar.update(self.game)
			self.renderer.render_menubar(self.menubar)
			self.renderer.render_grid(self.camera)
			self.renderer.render_cells(self.camera, self.game)
			self.prev_mouse_loc = curr_pos
		elif curr_pos.y < pygameoflife.renderer.HDR_HEIGHT and not self.btn_active:
			for button in self.menubar.buttons:
				if button.has_coord(curr_pos):
					button.color = pygameoflife.renderer.ACTIVE_BTN_COLOR
					self.renderer.render_menubar(self.menubar)
					self.btn_active = button
					break
		elif self.btn_active and not self.btn_active.has_coord(curr_pos):
			self.btn_active.color = pygameoflife.renderer.BUTTON_COLOR
			self.renderer.render_menubar(self.menubar)
			self.btn_active = None

	def handle_mouse_wheel_event(self, evt):
		self.camera.add_to_scale(evt.y)
		self.renderer.render_grid(self.camera)
		self.renderer.render_cells(self.camera, self.game)

	def handle_quit_event(self, evt):
		self.is_running = False
	
	def handle_video_resize_event(self, evt):
		# video resize events are only fired after resizing is complete, 
		# so the picture on screen is linearly scaled while the frame is
		# being resized. This is a known bug, and for now I'll stick
		# with it because there's no way of changing it in SDL atleast.
		# bug @ https://github.com/libsdl-org/SDL/issues/1059
		w, h = evt.size
		if w < MIN_SIZE[0]:
			w = MIN_SIZE[0]
		if h < MIN_SIZE[1]:
			h = MIN_SIZE[1]
		self.win_surf = pygame.display.set_mode((w,h), pygame.RESIZABLE)
		self.renderer.surface = self.win_surf
		self.renderer.render_grid(self.camera)
		self.renderer.render_menubar(self.menubar)
		self.renderer.render_cells(self.camera, self.game)
	
	def run(self):
		evt_dict = {
			pygame.MOUSEBUTTONDOWN: self.handle_mouse_down_event,
			pygame.MOUSEBUTTONUP: self.handle_mouse_up_event,
			pygame.MOUSEMOTION: self.handle_mouse_motion_event,
			pygame.MOUSEWHEEL: self.handle_mouse_wheel_event,
			pygame.QUIT: self.handle_quit_event,
			pygame.VIDEORESIZE: self.handle_video_resize_event,
		}

		clock = pygame.time.Clock()
		nticks = 0

		while self.is_running:
			time_elapsed = clock.tick(FRAMERATE)
			nticks += 1
			evts = [e for e in pygame.event.get() if e.type in evt_dict]
			for evt in evts:
				evt_dict[evt.type](evt) # run method corresponsing to event

			nticks %= FRAMERATE/2
			if nticks == 0 and not self.game_paused:
				self.game.update()
				self.menubar.update(self.game)
				self.renderer.render_menubar(self.menubar)
				self.renderer.render_grid(self.camera)
				self.renderer.render_cells(self.camera, self.game)

			if self.renderer.surface_changed:
				self.renderer.surface_changed = False
				pygame.display.update()
