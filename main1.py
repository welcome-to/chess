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
class LabelB(Label):
  bcolor = ListProperty([1,1,1,1])


class MyApp(App):
	def build(self):
		self.lbllist = []
		for i in range(8):
			for j in range(8):
				if (i + j) % 2 == 0:
					colorB = [0,0,0,1]
					color =[1,1,1,1]
				else:
					color = [0,0,0,1]
					colorB =[1,1,1,1]
				textlist = startupdate()
				text = textlist[i][j]
				self.lbllist.append(LabelB(text = text,color = color,bcolor = colorB))
		main = BoxLayout(orientation='horizontal')
		board = GridLayout(cols = 8 , size_hint = (.75,1))
		for i in range(64):
			board.add_widget(self.lbllist[i])
		contorls = BoxLayout(orientation='vertical',size_hint = (.25,1))
		contorls.add_widget(Button(text = 'Следующий ход',background_color = [0,1,0,.1],background_normal = '',on_press = self.movement2))
		contorls.add_widget(Button(text = 'Ввести ход',background_color = [1,0,0,.1],background_normal = '',on_press = self.movement))
		main.add_widget(board)
		main.add_widget(contorls)
		return main
	def movement(self,instance):
		move = input()
		nowlist = []
		for i in range(8):
			row = []
			for j in range(8):
				row.append(self.lbllist[i*8+j].text)
			nowlist.append(row)
		boardlist = movementtolist(nowlist,move)
		for i in range(8):
			for j in range(8):
				self.lbllist[i*8+j].text = boardlist[i][j]

	def movement2(self,instance):
		self.lbllist[22].text +=('\n' + str(2))

def startupdate():
	boardlist = [['E','H','O','Q','K','O','H','E'],
	             ['S','S','S','S','S','S','S','S'],
	             ['','','','','','','',''],
	             ['','','','','','','',''],
	             ['','','','','','','',''],
	             ['','','','','','','',''],
	             ['S','S','S','S','S','S','S','S'],
	             ['1','1','1','1','1','1','1','1']]
	return boardlist
def movementtolist(nowlist,move):
	Xfrom=int(move[0])
	Yfrom=int(move[1])
	Xto=int(move[2])
	Yto=int(move[3])
	whatincell = nowlist[Xfrom][Yfrom]
	nowlist[Xfrom][Yfrom] = ''
	nowlist[Xto][Yto]=whatincell
	return nowlist

if __name__ == '__main__':
	MyApp().run()
