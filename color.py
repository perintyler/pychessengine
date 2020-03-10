from enum import Enum

class Color(Enum):

	WHITE = 0
	BLACK = 1


	def other(self):
		return Color.BLACK if self.value == 0 else Color.WHITE

	def __str__(self):
		return 'white' if self.value == 0 else 'black'

WHITE = Color.WHITE 
BLACK = Color.BLACK