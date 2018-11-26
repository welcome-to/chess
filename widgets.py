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




#Label с изменяемым цветом фона

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



#Добавление свойства цвета клетке
Builder.load_string("""
<Cell>:
    canvas:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
""")
#создание класса клетки
class Cell(FloatLayout):
    bcolor = ListProperty([1,1,1,1])
    def __init__(self,bcolor):
        super().__init__()
        self.bcolor = bcolor
        self.image = Image(source = 'img/nothing.png',
                           size_hint = (1,1),
                           pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.image)
    def updateimage(self,source):
        self.image.source = source



#виджет доски 
class  BoardWidget(GridLayout):
    #создание сетки доски без заполнения
    def __init__(self, initial_objects,button_function):
        super().__init__(
            pos_hint={'center_x':0.5,'center_y':0.5},
            size_hint=(1, 1),
            cols=10,
            rows=10
        )
        self.celllist = []
        self.button_function = button_function

        self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
        for i in range(8):
            self.celllist.append(LabelB(text = listoflaters[i],bcolor = BACKGROUND))
        self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
        cells=[]
        for i in range(8):
            row = []
            for j in range(8):
                if (i + j) % 2 == 0:
                    colorB = COLOROFCELL2
                else:
                    colorB = COLOROFCELL1
                cell = Cell(bcolor = colorB)

                button = Button(text = '',
                                  background_color = [0,0,0,0],
                                  background_normal = '',
                                  on_press = self.InputMove,
                                  size_hint = (1,1),
                                  pos_hint = {'center_x': 0.5, 'center_y': 0.5})
                cell.add_widget(button)
                row.append(cell)
                cells.append(cell)
        for i in range(8):
            self.celllist.append(LabelB(text = str(8-i),bcolor = BACKGROUND))
            for j in range(8):
                self.celllist.append(cells[i*8+j])
            self.celllist.append(LabelB(text = str(8-i),bcolor = BACKGROUND))

        self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))
        for i in range(8):
            self.celllist.append(LabelB(text = listoflaters[i],bcolor = BACKGROUND))
        self.celllist.append(LabelB(text = '',bcolor = BACKGROUND))

        for i in self.celllist:
            self.add_widget(i)
        self.draw(initial_objects)

    #заполнение доски в соответсвии с заданной упорядоченной доской
    def draw(self, orientated_objects):
        k=0
        for i in range(10):
            self.celllist[k].text=orientated_objects[k]
            k+=1
        for i in range(8):
            self.celllist[k].text=orientated_objects[k]
            k+=1
            for i in range(8):
                self.celllist[k].updateimage(orientated_objects[k])
                k+=1
            self.celllist[k].text=orientated_objects[k]
            k+=1
        for i in range(10):
            self.celllist[k].text=orientated_objects[k]
            k+=1

    def InputMove(self,button):
        marked = zip(range(len(self.children)), self.children)
        index = list(
            filter(
                lambda b: b[1].children[0] == button,
                filter(
                    lambda b: isinstance(b[1], Cell),
                    marked
                )
            )
        )[0][0]
        self.button_function(index)

    def LightRed(self,index):
        self.children[index].bcolor = [255, 0, 0, 1]
    def LightGreen(self,index):
        self.children[index].bcolor = [0, 255,0,1]
    def LightBlue(self,index):
        self.children[index].bcolor = [0,0,255,1]
    def UnlightAll(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    colorB = COLOROFCELL2
                else:
                    colorB = COLOROFCELL1
                self.children[10*(i+1)+j+1].bcolor = colorB




    
