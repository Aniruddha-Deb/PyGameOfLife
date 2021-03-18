class Game:
	
	def __init__(self):
		self.live_cells = {}
		self.dead_cells = {}
	
	def is_alive(self, cell):
		return cell in self.live_cells

	def get_neighbours(self, cell):
		neighbours = []
		for i in range(cell[0]-1,cell[0]+2):
			for j in range(cell[1]-1,cell[1]+2):
				if (i,j) != cell:
					neighbours.append((i,j))
		return neighbours

	def deactivate_cell(self, cell):
		self.dead_cells[cell] = self.live_cells[cell]
		del self.live_cells[cell]
		if self.dead_cells[cell] == 0:
			del self.dead_cells[cell]
		# update all neighbours
		for nb in self.get_neighbours(cell):
			if nb in self.live_cells:
				self.live_cells[nb] -= 1
			elif nb in self.dead_cells:
				self.dead_cells[nb] -= 1
				if self.dead_cells[nb] == 0:
					del self.dead_cells[nb]

	def activate_cell(self, cell):
		if cell in self.dead_cells:
			self.live_cells[cell] = self.dead_cells[cell]
			del self.dead_cells[cell]
		else:
			self.live_cells[cell] = 0
			# guaranteed to be 0, as dead cells in self.dead_cells all have 
			# atleast one neighobur

		# update all neighbours
		for nb in self.get_neighbours(cell):
			if nb in self.live_cells:
				self.live_cells[nb] += 1
			elif nb in self.dead_cells:
				self.dead_cells[nb] += 1
			elif nb not in self.dead_cells:
				self.dead_cells[nb] = 1

	def toggle_cell(self, cell):
		if cell in self.live_cells:
			self.deactivate_cell(cell)
		else:
			self.activate_cell(cell)

	def update(self):
		old_dead_cells = self.dead_cells
		old_live_cells = self.live_cells

		self.live_cells = {}
		self.dead_cells = {}

		for cell in old_live_cells:
			if old_live_cells[cell] in range(2,4):
				self.activate_cell(cell)
		
		for cell in old_dead_cells:
			if old_dead_cells[cell] == 3:
				self.activate_cell(cell)
