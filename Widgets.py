from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color
from random import randint
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.image import Image
from kivy.graphics import Color
from board import Coordinates
from const import *






Builder.load_string("""
<LabelB>:
	bcolor: 1, 1, 1, 1
	canvas.before:
		Color:
			rgba: self.bcolor
	    Rectangle:
    		pos: self.pos
    		size: self.size
""")
Builder.load_string("""
<Cell>:
    canvas:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
""")

class LabelB(Label):
	bcolor = ListProperty([1,1,1,1])
class Cell(FloatLayout):
	bcolor = ListProperty([1,1,1,1])
class ButtonRC(Button):
	def loadroadandcolumn(self,row,column):
		self.row = row
		self.column = column
	def getrowandcolumn(self):
		return (self.column,self.row)
class  Board(GridLayout):
	def load_board(self,otputlabel):
		self.movelabel = otputlabel
		self.cols = 10
		self.size_hint = (1,1)
		self.celllist = [LabelB(text = '',bcolor = BACKGROUND)]
		self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
		self.r = []
		self.l = []
		self.u = []
		self.b = []
		self.cells = []
		self.countofmove = 0

		for i in range(8):
			label = LabelB(text = lineof[i],bcolor = BACKGROUND, font_size = 20)
			self.celllist.append(label)
			self.u.append(label)
		self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
		
		self.lbllist = []
		for i in range(8):
			labelL = LabelB(text = str(9-(i+1)),bcolor = BACKGROUND, font_size = 20)
			self.l.append(labelL)
		for i in range(8):
			labelR  = LabelB(text = str(9-(i+1)), bcolor = BACKGROUND,font_size = 20)
			self.r.append(labelR)

		for i in range(8):
			row = []
			
			self.celllist.append(self.l[i])
			
			for j in range(8):
				if (i + j) % 2 == 0:
					colorB = COLOROFCELL2
				else:
					colorB = COLOROFCELL1
				cell = Cell(bcolor = colorB)
				image = Image(source = sourcelist[7-i][7-j],
					          size_hint = (1,1),
					          pos_hint = {'center_x': 0.5, 'center_y': 0.5})

				button = ButtonRC(text = '',
					              background_color = [0,0,0,0],
					              background_normal = '',
					              on_press = self.InputMove,
					              size_hint = (1,1),
					              pos_hint = {'center_x': 0.5, 'center_y': 0.5})


				button.loadroadandcolumn(i,j)
				cell.add_widget(image)
				cell.add_widget(button)
				row.append(image)
				self.celllist.append(cell)
				self.cells.append(cell)
			
			self.celllist.append(self.r[i])
			self.lbllist.append(row)
		self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
		for i in range(8):
			label = LabelB(text = lineof[i],bcolor = BACKGROUND, font_size = 20)
			self.celllist.append(label)
			self.b.append(label)
		self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
		for i in range(100):
			self.add_widget(self.celllist[i])
	def InputMove(self,button):
		self.countofmove +=1
		if self.countofmove % 2 == 1:
			self.coord = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
			self.movelabel.text = str(self.coord).upper()+ ' --> '
		else:
			self.coordto = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
			self.movelabel.text = self.movelabel.text + str(self.coordto).upper()
	
		
	