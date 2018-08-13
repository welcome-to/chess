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
	