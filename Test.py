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
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color
from run import GameProcessor
from const import *

Config.set('graphics','resizable','0')
Config.set('graphics','width','600')
Config.set('graphics','height','600')


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
		return (self.row,self.column)
		
class MainApp(App):
	def build(self):
		self.gp = GameProcessor()


		self.startscrean = FloatLayout(size_hint = (1,1),
		                               pos_hint = {'center_x': 0.5, 'center_y': 0.5})

		welcome   = LabelB(text = 'Welcome to Chess',
		                   size_hint = [2,2],
		                   pos_hint = {'center_x': 0.5, 'center_y': 0.6},
		                   bcolor = [.8,.7,.6,1])

		startgame = Button(text = 'Start game',
		                   on_press = self.startgame,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.5, 'center_y': 0.5})

		loging    = Button(text = 'Save game log',
		                   on_press = self.log,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.5, 'center_y': 0.39})

		exit      = Button(text = 'Exit',
		                   on_press = self.leave,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.5, 'center_y': 0.28})

		self.startscrean.add_widget(welcome)
		self.startscrean.add_widget(startgame)
		self.startscrean.add_widget(exit)
		self.startscrean.add_widget(loging)
		self.main = FloatLayout()
		self.main.add_widget(self.startscrean)
		
		return self.main



	def leave(self,obj):
		self.stop()



	def log(self,button):
		if button.text == 'Save game log':
			self.gp.savelog(True)
			self.loging.text = 'Don\'t save log'
		else:
			self.gp.savelog(False)
			self.loging.text = 'Save game log'



	def startgame(self,button):
		self.main.remove_widget(self.startscrean)
		self.countofmove = 0
		celllist = [Button(text = 'Next',background_color = [.1,.1,.1,1])]

		for i in range(8):
			celllist.append(LabelB(text = lineof[i],bcolor = BUTTONCOLOR, font_size = 20))
		
		self.lbllist = []
		for i in range(8):
			row = []
			celllist.append(LabelB(text = str(i+1),bcolor = BUTTONCOLOR, font_size = 20))
			for j in range(8):
				if (i + j) % 2 == 0:
					colorB = COLOROFCELL1
				else:
					colorB = COLOROFCELL2
				cell = Cell(bcolor = colorB)
				image = Image(source = sourcelist[i][j], size_hint = (1,1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
				button = ButtonRC(text = '',background_color = [0,0,0,0],background_normal = '', on_press = self.update,size_hint = (1,1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
				button.loadroadandcolumn(i,j)
				cell.add_widget(image)
				cell.add_widget(button)
				row.append(image)
				celllist.append(cell)
			self.lbllist.append(row)
		
		self.board = GridLayout(cols = 9,size_hint = (1,1),pos_hint = {'center_x': 0.5, 'center_y': 0.5})

		for i in range(81):
			self.board.add_widget(celllist[i])

		self.main.add_widget(self.board)

	def gameover(self,reason):
		self.main.remove_widget(self.board)
		if reason == WHITE_WIN:
			source = WHITE_WIN_IMAGE
			text = 'You win like a real white man'
		elif reason == BLACK_WIN:
			source = BLACK_WIN_IMAGE
			text = 'pridumay sama'
		else:
			source = TIE_IMAGE
			text = 'potom'
		self.main.add_widget(Image(source = source, size_hint = (1,1)))
		print(reason)


	def update(self,button):
		self.countofmove += 1
		if self.countofmove % 2 == 1:
			cord =button.getrowandcolumn()
			self.row = cord[0]
			self.column = cord[1]
		else:
			cord = button.getrowandcolumn()

			move = INDEX_TO_LATTER.get(self.column)+str(self.row + 1) + INDEX_TO_LATTER.get(cord[1])+ str(cord[0]+1)
			make_turn(self.gp, move)
			boardlist = board(self.gp)
			for i in range(8):
				for j in range(8):
					self.lbllist[i][j].source = boardlist[i][j]
			a = game_result(self.gp)
			if not a[0]:
				self.gameover(a[1])
	def movement(self,instance):
		boardlist = board(self.gp)
		for i in range(8):
			for j in range(8):
				self.lbllist[i][j].source = boardlist[i][j]
		game_result(self.gp)


def game_result(GameProcessor):
	result = GameProcessor.game_result()
	if result == None:
		return [True]
	elif result == WHITE_WIN:
		return[False, WHITE_WIN]
	elif result == BLACK_WIN:
		return [False, BLACK_WIN]
	else:
		return [False, TIE]


def board(GameProcessor):
	datafirstiter = GameProcessor.board.data 
	finaldata = []
	for i in range(8):
		row = []
		for j in range(8):
			if datafirstiter[i][j] != None:
				row.append(figurecolor[(datafirstiter[i][j].color)]+figuretype[datafirstiter[i][j].type])
			else:
				row.append(NOTHING)
		finaldata.append(row)
	return finaldata


def make_turn(GameProcessor, move):
	GameProcessor.make_turn(move)
		


MainApp().run()  

