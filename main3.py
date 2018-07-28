import os

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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color
from run import GameProcessor

from const import *
import conf


global GameProcessor
GameProcessor = GameProcessor()




Config.set('graphics','resizable','0')
Config.set('graphics','width','800')
Config.set('graphics','height','600')
Config.set('kivy','window_icon','King-black.iso')


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
		self.celllist = []
		self.lbllist = []
		global sourcelist
		for i in range(8):
			row = []
			for j in range(8):
				if (i + j) % 2 == 0:
					colorB = [1,0,0,1]
				else:
					colorB =[0,1,0,1]
				cell = Cell(bcolor = colorB)
				image = Image(source = os.path.join(conf.TILES_DIR, sourcelist[i][j]))
				cell.add_widget(image)
				row.append(image)
				self.celllist.append(cell)
			self.lbllist.append(row)
		self.main = BoxLayout(orientation='horizontal')
		board = GridLayout(cols = 8 , size_hint = (.75,1))
		for i in range(64):
			board.add_widget(self.celllist[i])
		contorls = BoxLayout(orientation='vertical',size_hint = (.25,1))
		contorls.add_widget(Button(text = 'Следующий ход',background_color = [0,1,0,.1],background_normal = '',on_press = self.movement))
		inputpart = BoxLayout(orientation = 'vertical')
		self.textinput =TextInput(multiline = False,font_size = 32)
		self.textinput.bind(on_text_validate = self.on_enter)
		inputpart.add_widget(self.textinput)
		contorls.add_widget(inputpart)
		self.main.add_widget(board)
		self.main.add_widget(contorls)
		return self.main
	def on_enter(instance,value):
		global app
		move = value.text
		make_turn(move)
		a = game_result()
		if a[0] == False:
			instance.gameover(a[1])
			return None
		value.text = ''
		nowlist = []
		for i in range(8):
			row = []
			for j in range(8):
				row.append(app.lbllist[i][j])
			nowlist.append(row)
		boardlist = movementtolist(nowlist,move)
		for i in range(8):
			for j in range(8):
				app.lbllist[i][j] = boardlist[i][j]
	def gameover(self,reason):
		self.stop()
		print(reason)

	def movement(self,instance):
		boardlist = board()
		for i in range(8):
			for j in range(8):
				self.lbllist[i][j].source = boardlist[i][j]
		a = game_result()
		if a[0] == False:
			self.gameover(a[1])
			return None


def movementtolist(nowlist,move):
#	global xdict
	Yfrom=move[0]
	Xfrom=int(move[1])-1
	Yto=move[-2]
	Xto=int(move[-1])-1
	Yfrom = LETTER_TO_INDEX.get(Yfrom)
	Yto = LETTER_TO_INDEX.get(Yto)
	whatincell = nowlist[Xfrom][Yfrom].source
	if ((whatincell == './tiles/w_pawn.png')or(whatincell == './tiles/b_pawn.png')) and Xto==7:
		whatincell = whatincell[0]+'_queen.png' 
	nowlist[Xfrom][Yfrom].source = './tiles/nothing.png'
	nowlist[Xto][Yto].source = whatincell
	return nowlist




def game_result():
	global GameProcessor
	result = GameProcessor.game_result()
	if result == None:
		return [True]
	elif result == WHITE_WIN:
		return [False, 'White win!!!']
	elif result == BLACK_WIN:
		return [False, 'Black win!!!']
	else:
		return [False, 'Tie']


def board():
	global GameProcessor
	datafirstiter =GameProcessor.board.data 
	dataseconditer = []
	for i in range(8):
		row = []
		for j in range(8):
			if datafirstiter[i][j] != None:
				row.append(str(datafirstiter[i][j].type)+str(datafirstiter[i][j].color))
			else:
				row.append(None)
		dataseconditer.append(row)
	finaldata = []
	global figurecolor
	global figuretype
	for i in range(8):
		row =[]
		for j in range(8):
			if dataseconditer[i][j] != None:
				filename = figurecolor.get(int(dataseconditer[i][j][1])) + figuretype.get(dataseconditer[i][j][0])
			else:
				filename = os.path.join(conf.TILES_DIR, 'nothing.png')
			row.append(filename)
		finaldata.append(row)
	return finaldata


def make_turn(move):
	global GameProcessor
	GameProcessor.make_turn(move)


if __name__ == '__main__':
	global app
	app=ChessApp()
	app.run()