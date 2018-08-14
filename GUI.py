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
from run import GameProcessor
from const import *
from Widgets import LabelB,Cell,ButtonRC,Board
from board import Coordinates


# Window configuration
Config.set('graphics','resizable','0')
Config.set('graphics','width','1200')
Config.set('graphics','height','600')



		
class MainApp(App):
	def build(self):
		self.gp = GameProcessor()


		self.startscrean = FloatLayout(size_hint = (1,1),
		                               pos_hint = {'center_x': 0.5, 'center_y': 0.5})

		background   = Image(source = FON,
		                   size_hint = [1,1],
		                   pos_hint = {'center_x': 0.5, 'center_y': 0.5},
		                   allow_stretch = True)

		game = LabelB(text = 'Chess game',
			          size_hint = [0.15,0.1],
			          pos_hint ={'center_x': 0.7, 'center_y': 0.8},
			          color = [0,0,0,1],
			          bcolor = [0,0,0,0],
			          font_name = FONT,
			          font_size = 100)
		startgame = Button(text = 'Start game',
		                   on_press = self.startgame,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.70, 'center_y': 0.5})

		self.loging= Button(text = 'Save game log',
		                   on_press = self.log,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.70, 'center_y': 0.39})

		exit      = Button(text = 'Exit',
		                   on_press = self.leave,
		                   background_normal = '',
		                   background_color = BUTTONCOLOR,
		                   color = [0,0,0,1],
		                   size_hint = [0.25,0.1],
		                   pos_hint = {'center_x': 0.70, 'center_y': 0.28})

		self.startscrean.add_widget(background)
		self.startscrean.add_widget(game)
		self.startscrean.add_widget(startgame)
		self.startscrean.add_widget(exit)
		self.startscrean.add_widget(self.loging)
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
		try:
			self.main.remove_widget(self.startscrean)
		except:
			pass
		try:
			self.main.remove_widget(self.Gameover)
		except:
			pass
		self.numberofmoves = 0
		self.countofmove = 0



		self.gameplay = FloatLayout(size_hint = [0.5,1], pos_hint = {'center_x': 0.5, 'center_y': 0.5})
		self.gameplay.add_widget(Image(source = FON2,size_hint = [2,2],pos_hint = {'center_x': 0.5, 'center_y': 0.5},allow_stretch = True))
		self.gameplay.add_widget(Button(text = 'Next Move',on_press = self.movement,size_hint = [0.35,0.1], pos_hint = {'center_x':1.25,'center_y':0.9},background_color = BUTTONCOLOR1,background_normal = ''))
		self.gameplay.add_widget(Button(text = 'Quit',on_press = self.leave,size_hint = [0.35,0.1], pos_hint = {'center_x':1.25,'center_y':0.66},background_color = BUTTONCOLOR1,background_normal = ''))		
		self.gameplay.add_widget(Button(text = 'Restart',on_press = self.Restart,size_hint = [0.35,0.1], pos_hint = {'center_x':1.25,'center_y':0.78},background_color = BUTTONCOLOR1,background_normal = ''))
		self.movelabel = LabelB(text = '',bcolor = BUTTONCOLOR1,size_hint = [.35,.1],pos_hint = {'center_x':-0.25,'center_y':0.9})
		self.gameplay.add_widget(self.movelabel)
		self.gameplay.add_widget(Button(text = 'Cancel selection',on_press = self.CancelMove,size_hint = [0.35,0.1], pos_hint = {'center_x':-0.25,'center_y':0.66},background_color = BUTTONCOLOR1,background_normal = ''))
		self.gameplay.add_widget(Button(text = 'Make movement',on_press = self.ComitMove,size_hint = [0.35,0.1], pos_hint = {'center_x':-0.25,'center_y':0.78},background_color = BUTTONCOLOR1,background_normal = ''))
		self.board = Board()
		self.board.load_board(self.movelabel)
		self.gameplay.add_widget(self.board)




		self.main.add_widget(self.gameplay)
	def Restart(self,btn):
		del self.gp
		self.gp = GameProcessor()
		self.main.remove_widget(self.gameplay)
		self.startgame(Button())

	def reversfildadres(self):
		if (int(self.board.l[0].text)) != 8:
			for i in range(8):
				self.board.l[i].text = str(9 - (i+1))
				self.board.r[i].text = str(9 - (i+1))
				self.board.u[i].text = lineof[7-i]
				self.board.b[i].text = lineof[7-i]
			for i in range(8):
				for j in range(8):
					if (i+j) % 2 == 0:
						colorB = COLOROFCELL2
					else:
						colorB = COLOROFCELL1
					self.board.cells[i*8+j].bcolor = colorB
		else:
			for i in range(8):
				self.board.l[i].text = str(i+1)
				self.board.r[i].text = str(i+1)
				self.board.u[i].text = lineof[i]
				self.board.b[i].text = lineof[i]
			for i in range(8):
				for j in range(8):
					if (i+j) % 2 != 0:
						colorB = COLOROFCELL2
					else:
						colorB = COLOROFCELL1
					self.board.cells[i*8+j].bcolor = colorB
		


	def CancelMove(self,button):
		self.countofmove = 0 
		self.movelabel.text = ''

	def ComitMove(self,button):
		self.gp.make_turn(self.board.coord, self.board.coordto)
		boardlist = board(self.gp)
		self.reversfildadres()
		self.numberofmoves += 1
		if self.numberofmoves%2 != 0:
			for i in range(8):
				for j in range(8):
					self.board.lbllist[i][j].source = boardlist[i][j]
		else:
			for i in range(8):
				for j in range(8):
					self.board.lbllist[7-i][7-j].source = boardlist[i][j]
		a = game_result(self.gp)
		if not a[0]:
			self.gameover(a[1])
		self.movelabel.text = ''





	def gameover(self,reason):
		self.main.remove_widget(self.gameplay)
		if reason != TIE:
			source = BLACK_WIN_IMAGE
			text = 'You Lose'
		else:
			source = TIE_IMAGE
			text = 'potom'
		self.Gameover = FloatLayout()
		self.Gameover.add_widget(Image(source = source, size_hint = (1,1),pos_hint = {'center_x': 0.5,'center_y':0.5}))
		self.Gameover.add_widget(LabelB(bcolor = [0,0,0,0],text = text,size_hint = (0.3,1),pos_hint = {'center_x': 0.5,'center_y':0.7}, color = [1,0,0,1],font_size = 160,font_name = FAIL))
		self.Gameover.add_widget(Button(text = 'Restart',color = [0,0,0,1],on_press = self.Restart,background_normal = '', background_color = [1,0,0,1],pos_hint = {'center_x': 0.25,'center_y':0.15},size_hint = (0.25,0.15)))
		self.Gameover.add_widget(Button(text = 'Quit',color = [0,0,0,1],on_press = self.leave,background_normal = '', background_color = [1,0,0,1],pos_hint = {'center_x': 0.75,'center_y': 0.15},size_hint = (0.25,0.15)))
		self.main.add_widget(self.Gameover)
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
		
  

