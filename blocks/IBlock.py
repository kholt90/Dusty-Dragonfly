import numpy as np
from blocks.BaseBlock import BaseBlock

class IBlock(BaseBlock):
	def __init__(self, scale = 1, color=[0,0,0]):
		super().__init__(scale=scale,color=color)

		self.verts = np.asfarray([
			(-1, -1, -1),	# left-far-bottom
			(1, -1, -1),	# right-far-bottom
			(1, 1, -1),		# right-close-bottom
			(-1, 1, -1),	# left-close-bottom
			
			(-1, -1, 1),	# left-far-top
			(1, -1, 1),		# right-far-top
			(1, 1, 1),		# right-close-top
			(-1, 1, 1),		# left-close-top
		])

		# If you move the vertices around, remember to update this.
		# self.ang = 0: top is facing us
		# self.ang = 90: close is facing us
		self.surfaces = np.array([
			(0,1,2,3),	# bottom
			(0,3,7,4),	# left
			(0,1,5,4),	# far
			(1,2,6,5),	# right
			(3,2,6,7),	# close
			(4,5,6,7)	# top
		])

		self.normals = np.asfarray([
			(0,0,-1),	# center -> bottom
			(-1,0,0),	# center -> left
			(0,-1,0),	# center -> far
			(1,0,0),	# center -> right
			(0,1,0),	# center -> close
			(0,0,1)		# center -> top
		])

		self.colors =  np.asfarray([
			(1,0,0),
			(0,1,1),
			(1,1,0),
			(0,1,1),
			(1,0,1),
			(1,1,1)
			])