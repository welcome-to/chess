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
		self.column = 7- column
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
		self.numberofmoves = 0
		self.coord = Coordinates(9,9)
		self.coordto = Coordinates(9,9)

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
		if self.numberofmoves % 2 != 0:
			if self.countofmove % 2 == 1:
				self.coord = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
				self.movelabel.text = str(self.coord).upper()+ ' --> '
			else:
				self.coordto = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
				self.movelabel.text = self.movelabel.text + str(self.coordto).upper()
		else:
			if self.countofmove % 2 == 1:
				self.coord = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
				self.movelabel.text = str(self.inverted()[0]).upper() + ' --> '
			else:
				self.coordto = Coordinates(button.getrowandcolumn()[0],button.getrowandcolumn()[1])
				self.movelabel.text = self.movelabel.text + str(self.inverted()[1]).upper()
				
	def get_move(self):
		if self.numberofmoves % 2 == 0:
			return self.normal()
		else:
			return self.inverted()
	def normal(self):
		return self.coord, self.coordto
	def inverted(self):
		coord = Coordinates(7-self.coord.x,7-self.coord.y)
		coordto = Coordinates(7-self.coordto.x,7-self.coordto.y)
		return coord ,coordto
	def invertboard(self):
		if self.numberofmoves % 2 != 0:
			for i in range(8):
				self.u[i].text = lineof[7-i]
				self.b[i].text = lineof[7-i]
				self.l[i].text = str(i+1)
				self.r[i].text = str(i+1)
		else:
			for i in range(8):
				self.u[i].text = lineof[i]
				self.b[i].text = lineof[i]
				self.l[i].text = str(9 - (i + 1))
				self.r[i].text = str(9 - (i + 1))
	def del_move(self):
		self.coord = Coordinates(9,9)
		self.coordto = Coordinates(9,9)