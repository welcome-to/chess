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
global xdict
xdict = {'A' : 0,
         'B' : 1,
         'C' : 2,
         'D' : 3,
         'E' : 4,
         'F' : 5,
         'G' : 6,
         'H' : 7}

Config.set('graphics','resizable','0')
Config.set('graphics','width','800')
Config.set('graphics','height','600')

global sourcelist
sourcelist = [
['w_rook.png','w_knight.png','w_bishop.png','w_queen.png','w_king.png','w_bishop.png','w_knight.png','w_rook.png'],
['w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png','w_pawn.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png','nothing.png'],
['b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png','b_pawn.png'],
['b_rook.png','b_knight.png','b_bishop.png','b_queen.png','b_king.png','b_bishop.png','b_knight.png','b_rook.png']]
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
				image = Image(source = sourcelist[i][j])
				cell.add_widget(image)
				row.append(image)
				self.celllist.append(cell)
			self.lbllist.append(row)
		self.main = BoxLayout(orientation='horizontal')
		board = GridLayout(cols = 8 , size_hint = (.75,1))
		for i in range(64):
			board.add_widget(self.celllist[i])
		contorls = BoxLayout(orientation='vertical',size_hint = (.25,1))
		contorls.add_widget(Button(text = 'Следующий ход',background_color = [0,1,0,.1],background_normal = '',on_press = self.movement2))
		inputpart = BoxLayout(orientation = 'vertical')
		self.textinput =TextInput(multiline = False)
		self.textinput.bind(on_text_validate = self.on_enter)
		inputpart.add_widget(self.textinput)
		contorls.add_widget(inputpart)
		self.main.add_widget(board)
		self.main.add_widget(contorls)
		return self.main
	def on_enter(instance,value):
		global app
		move = value.text
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
	def gameover(self):
		self.stop()

	def movement2(self,instance):
		self.gameover()

def movementtolist(nowlist,move):
	global xdict
	Yfrom=move[0]
	Xfrom=int(move[1])-1
	Yto=move[2]
	Xto=int(move[3])-1
	Yfrom = xdict.get(Yfrom)
	Yto = xdict.get(Yto)
	whatincell = nowlist[Xfrom][Yfrom].source
	if ((whatincell == 'w_pawn.png')or(whatincell == 'b_pawn.png')) and Xto==7:
		whatincell = whatincell[0]+'_queen.png' 
	nowlist[Xfrom][Yfrom].source = 'nothing.png'
	nowlist[Xto][Yto].source = whatincell
	return nowlist

if __name__ == '__main__':
	global app
	app=ChessApp()
	app.run()
	print('YYYY')
