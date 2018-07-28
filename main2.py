from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
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
		self.startscrean = BoxLayout(orientation = 'vertical')
		self.gp = GameProcessor()
		self.startscrean.add_widget(Label(text = 'Welcome to chess \n рокировка это R"Ход короля"'))
		self.startscrean.add_widget(Button(text = 'Начать игру', on_press = self.startgame,background_normal = '',background_color = [1,1,1,1], color = [0,0,0,1] ))		
		self.main = BoxLayout(orientation='horizontal')
		self.main.add_widget(self.startscrean)
		return self.main
	def startgame(self,butonobj):
		self.main.remove_widget(self.startscrean)
		self.celllist = [Label(text = '')]
		lineof = ['A','B','C','D','E','F','G','H']
		for i in range(8):
			self.celllist.append(Label(text = lineof[i]))
		
		self.lbllist = []
		for i in range(8):
			row = []
			self.celllist.append(Label(text = str(i+1)))
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
		self.contorls.add_widget(Button(text = 'Следующий Ход',background_color = [0,1,0,.1],background_normal = '',on_press = self.movement))
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
		a = game_result(self.gp)
		if not a[0]:
			self.gameover(a[1])
		value.text = ''
		if (move[0] == 'R') or (move[0] == 'r'):
			rocuemove = move[1:].upper()
			if rocuemove == 'E1G1':
				self.lbllist[0][4].source = NOTHING
				self.lbllist[0][6].source = 'img/w_king.png'
				self.lbllist[0][7].source = NOTHING
				self.lbllist[0][5].source = 'img/w_rook.png'
			if rocuemove == 'E1C1':
				self.lbllist[0][4].source = NOTHING
				self.lbllist[0][2].source = 'img/w_king.png'
				self.lbllist[0][0].source = NOTHING
				self.lbllist[0][3].source = 'img/w_rook.png'
			if rocuemove == 'E8G8':
				self.lbllist[8][4].source = NOTHING
				self.lbllist[8][6].source = 'img/b_king.png'
				self.lbllist[8][7].source = NOTHING
				self.lbllist[8][5].source = 'img/b_rook.png'
			if rocuemove == 'E8C8':
				self.lbllist[8][4].source = NOTHING
				self.lbllist[8][2].source = 'img/b_king.png'
				self.lbllist[8][0].source = NOTHING
				self.lbllist[8][3].source = 'img/b_rook.png'
			 
			move = 'A1A1'
		nowlist = []

		for i in range(8):
			row = []
			for j in range(8):
				row.append(self.lbllist[i][j])
			nowlist.append(row)

		boardlist = movementtolist(nowlist,move)

		for i in range(8):
			for j in range(8):
				self.lbllist[i][j] = boardlist[i][j]

		if move[1:] == 'E1G1':
			self.lbllist[0][4].source = NOTHING
			self.lbllist[0][6].source = 'img/w_king.png'
			self.lbllist[0][7].source = NOTHING
			self.lbllist[0][5].source = 'img/w_rook.png'
		if move[1:] == 'E1C1':
			self.lbllist[0][4].source = NOTHING
			self.lbllist[0][2].source = 'img/w_king.png'
			self.lbllist[0][0].source = NOTHING
			self.lbllist[0][3].source = 'img/w_rook.png'
		if move[1:] == 'E8G8':
			self.lbllist[8][4].source = NOTHING
			self.lbllist[8][6].source = 'img/b_king.png'
			self.lbllist[8][7].source = NOTHING
			self.lbllist[8][5].source = 'img/b_rook.png'
		if move[1:] == 'E8C8':
			self.lbllist[8][4].source = NOTHING
			self.lbllist[8][2].source = 'img/b_king.png'
			self.lbllist[8][0].source = NOTHING
			self.lbllist[8][3].source = 'img/b_rook.png'

	def gameover(self,reason):
		self.main.remove_widget(self.board)
		self.main.remove_widget(self.contorls)
		if reason == WHITE_WIN:
			source = WHITE_WIN_IMAGE
		elif reason == BLACK_WIN:
			source = BLACK_WIN_IMAGE
		else:
			source = TIE_IMAGE
		self.main.add_widget(Image(source = source))
		print(reason)


	def movement(self,instance):
		boardlist = board(self.gp)
		for i in range(8):
			for j in range(8):
				self.lbllist[i][j].source = boardlist[i][j]
		game_result(self.gp)





def movementtolist(nowlist,move):
	Yfrom = move[0]
	Xfrom = int(move[1])-1
	Yto = move[-2]
	Xto = int(move[-1])-1
	Yfrom = LETTER_TO_INDEX.get(Yfrom)
	Yto = LETTER_TO_INDEX.get(Yto)
	whatincell = nowlist[Xfrom][Yfrom].source
	
	figure_color = whatincell[:5]
	figure_type = whatincell[5:]

	if figuretypeback.get(figure_type) == PAWN and Xto==7:
		whatincell = figure_color + figuretype.get(QUEEN)

	nowlist[Xfrom][Yfrom].source = NOTHING
	nowlist[Xto][Yto].source = whatincell
	return nowlist




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