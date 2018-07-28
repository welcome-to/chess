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
Config.set('graphics','width','800')
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
class Cell(BoxLayout):
	bcolor = ListProperty([1,1,1,1])






class ChessApp(App):
	def build(self):
		self.startscrean = FloatLayout()
		self.gp = GameProcessor()
		self.startscrean.add_widget(LabelB(text = 'Welcome to Chess' , size_hint = [2,2], pos_hint = {'center_x': 0.5, 'center_y': 0.6} , bcolor = [.8,.7,.6,1] ) )
		self.startscrean.add_widget(Button(text = 'Start game', on_press = self.startgame,background_normal = '',background_color = BUTTONCOLOR, color = [0,0,0,1],size_hint = [0.15,0.1],pos_hint = {'center_x': 0.5, 'center_y': 0.4} ))
		self.startscrean.add_widget(Button(text = 'Exit', on_press = self.leave ,background_normal = '',background_color = BUTTONCOLOR, color = [0,0,0,1],size_hint = [0.15,0.1],pos_hint = {'center_x': 0.5, 'center_y': 0.29} ))		
		self.main = BoxLayout(orientation='horizontal')
		self.main.add_widget(self.startscrean)
		return self.main
	def leave(self,obj):
		self.stop()
	def startgame(self,butonobj):
		self.main.remove_widget(self.startscrean)
		self.celllist = [LabelB(text = '',bcolor = [.1,.1,.1,1])]
		lineof = ['A','B','C','D','E','F','G','H']
		for i in range(8):
			self.celllist.append(LabelB(text = lineof[i],bcolor = BUTTONCOLOR, font_size = 20))
		
		self.lbllist = []
		for i in range(8):
			row = []
			self.celllist.append(LabelB(text = str(i+1),bcolor = BUTTONCOLOR, font_size = 20))
			for j in range(8):
				if (i + j) % 2 == 0:
					colorB = COLOROFCELL1
				else:
					colorB = COLOROFCELL2
				cell = Cell(bcolor = colorB)
				image = Image(source = sourcelist[i][j])
				cell.add_widget(image)
				row.append(image)
				self.celllist.append(cell)
			self.lbllist.append(row)
		
		self.board = GridLayout(cols = 9 , size_hint = (.75,1))
		for i in range(81):
			self.board.add_widget(self.celllist[i])
		self.contorls = BoxLayout(orientation='vertical',size_hint = (.25,1))
		self.contorls.add_widget(Button(text = 'Next Move',background_color = [.1,.1,.1,1],background_normal = '',on_press = self.movement))
		inputpart = BoxLayout(orientation = 'vertical')
		self.textinput = TextInput(multiline = False, font_size = 32)
		self.textinput.bind(on_text_validate = self.on_enter)
		inputpart.add_widget(self.textinput)
		self.contorls.add_widget(inputpart)
		self.main.add_widget(self.board)
		self.main.add_widget(self.contorls)


	def on_enter(self,value):
		move = value.text
		make_turn(self.gp, move)
		value.text = ''
		boardlist = board(self.gp)
		for i in range(8):
			for j in range(8):
				self.lbllist[i][j].source = boardlist[i][j]
		a = game_result(self.gp)
		if not a[0]:
			self.gameover(a[1])

	def gameover(self,reason):
		self.main.remove_widget(self.board)
		self.main.remove_widget(self.contorls)
		if reason == WHITE_WIN:
			source = WHITE_WIN_IMAGE
			text = 'You win like a real white man'
		elif reason == BLACK_WIN:
			source = BLACK_WIN_IMAGE
			text = 'pridumay sama'
		else:
			source = TIE_IMAGE
			text = 'potom'
		self.main.orientation = 'vertical'
		self.main.add_widget(LabelB(text = text, size_hint  = (1,.3), bcolor = [0,0,0,1], color = [1,0,0,1], font_size = 32))
		self.main.add_widget(Image(source = source, size_hint = (1,.7)))
		print(reason)


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


if __name__ == '__main__':
	ChessApp().run()