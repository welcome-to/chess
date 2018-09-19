from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from const import *
from widgets import LabelB, BoardWidget
from run import GameProcessor
from copy import copy

from board import Coordinates


# Window configuration
Config.set('graphics','resizable','0')
Config.set('graphics','width','1200')
Config.set('graphics','height','600')


def another_orientation(orientation):
    if orientation == REGULAR:
        return INVERSE
    return REGULAR


class Orienteer(object):
    def __init__(self, initial_color=WHITE):
        if initial_color == WHITE:
            self.orientation = REGULAR
        else:
            self.orientation = INVERSE

    def invert(self):
        self.orientation = another_orientation(self.orientation)

    def oriented_coordinates(self,coordinates):
        if not self.orientation:
            return coordinates
        return 7 - coordinates[0], 7 - coordinates[1]

    def oriented_board(self,board):
        if self.orientation:
            return board
        return list(reversed(board))


class MainApp(App):
    def build(self):
        self.start_screen = FloatLayout(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        background_image = Image(
            source=INITIAL_BACKGROUND,
            size_hint=[1, 1],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True
        )

        game_label = LabelB(
            text='Chess game',
            size_hint=[0.15, 0.1],
            pos_hint={'center_x': 0.7, 'center_y': 0.8},
            color=[0, 0, 0, 1],
            bcolor=[0, 0, 0, 0],
            font_name=FONT,
            font_size=100
        )
        
        self.buttons = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.7, 'center_y': 0.4}
        )

        start_game_button = Button(
            text='Start game',
            on_press=self.draw_game_screen,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )

        settings_button = Button(
            text='Settings',
            on_press=self.show_settings,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )
                           
        exit_button = Button(
            text='Quit',
            on_press=self.leave,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )

        self.buttons.add_widget(start_game_button)
        self.buttons.add_widget(settings_button)
        self.buttons.add_widget(exit_button)

        self.start_screen.add_widget(background_image)
        self.start_screen.add_widget(game_label)

        self.start_screen.add_widget(self.buttons)
        self.main_layout = FloatLayout()
        self.main_layout.add_widget(self.start_screen)

        return self.main_layout



    def draw_game_screen(self,button):
        self.main_layout.remove_widget(self.main_layout.children[0])
        self.GameProcessor = GameProcessor()
        self.Orienteer = Orienteer()
        self.clicks = 0


        self.gameplay = FloatLayout(
            size_hint=[0.5,1],
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        self.gameplay.add_widget(Image(
            source=GAME_BACKGROUND,
            size_hint=[2,2],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            allow_stretch=True
        ))

        self.gameplay.add_widget(Button(
            text='Quit',
            on_press=self.leave,
            size_hint=[0.35,0.1],
            pos_hint={'center_x':1.25,'center_y':0.78},
            background_color=GAME_BUTTON_COLOR,
            background_normal=''
        ))

        self.gameplay.add_widget(Button(
            text='Restart',
            on_press=self.draw_game_screen,
            size_hint=[0.35,0.1],
            pos_hint={'center_x':1.25,'center_y':0.90},
            background_color=GAME_BUTTON_COLOR,
            background_normal=''
        ))
        self.move_label=LabelB(
            text='',
            bcolor=GAME_BUTTON_COLOR,
            size_hint=[.35,.1],
            pos_hint={'center_x':-0.25,'center_y':0.9}
        )
        self.gameplay.add_widget(self.move_label)
        self.gameplay.add_widget(Button(
            text='Cancel selection',
            on_press=self.cancel_move,
            size_hint=[0.35,0.1],
            pos_hint={'center_x':-0.25,'center_y':0.66},
            background_color=GAME_BUTTON_COLOR,
            background_normal=''
        ))
        self.gameplay.add_widget(Button(
            text='Make movement',
            on_press=self.commit_move,
            size_hint=[0.35,0.1],
            pos_hint={'center_x':-0.25,'center_y':0.78},
            background_color=GAME_BUTTON_COLOR,
            background_normal=''
        ))
        self.Orienteer.invert()
        self.board = BoardWidget(self.Orienteer.oriented_board(self.get_board()),self.input_move)
        self.gameplay.add_widget(self.board)
        self.main_layout.add_widget(self.gameplay)

    def leave(self, button):
        self.stop()

    def show_settings(self, button):
        self.start_screen.remove_widget(self.buttons)

        self.settings = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.7, 'center_y': 0.4})
        crimea = Button(
            text='Whose Crimea?: Russian',
            on_press=self.crimea,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )

        log = Button(
            text='Loging: No',
            on_press=self.loging,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )

        back_to_start_screen = Button(
            text='Back',
            on_press=self.back_to_start,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )
        self.settings.add_widget(crimea)
        self.settings.add_widget(log)
        self.settings.add_widget(back_to_start_screen)
        self.start_screen.add_widget(self.settings)

    def back_to_start(self, button):

        self.start_screen.remove_widget(self.settings)
        self.start_screen.add_widget(self.buttons)

    def crimea(self, button):
        if button.text == 'Whose Crimea?: Russian':
            button.text = 'Whose Crimea?: Ukraine'
        else:
            button.text = 'Whose Crimea?: Russian'

    def loging(self, button):
        if button.text == 'Loging: No':
            button.text = 'Loging: Yes'
        else:
            button.text = 'Loging: No'
    def cancel_move(self, button):
        self.clicks = 0
        self.move_label.text = ''
        self.start = None
        self.end = None
        self.board.UnlightAll()

    def get_board(self):
        board_list = []
        board_list.append('')
        for i in list(reversed(listoflaters)):
            board_list.append(i)
        board_list.append('')
        for i in range(8):
            board_list.append(str(i+1))
            for j in range(8):
                figure = self.GameProcessor.board.data[i][j]
                if figure is None:
                    board_list.append('img/nothing.png')
                else:
                    board_list.append(figurecolor[figure.color]+figuretype[figure.type])
            board_list.append(str(i+1))
        board_list.append('')
        for i in list(reversed(listoflaters)):
            board_list.append(i)
        board_list.append('')
        return board_list

    def input_move(self, index):
        coordinates =  7-((index%10)-1),(index//10)-1
        coordinates = Coordinates(self.Orienteer.oriented_coordinates(coordinates)[0],self.Orienteer.oriented_coordinates(coordinates)[1])
        print(str(coordinates).upper())
        if self.clicks == 0:
            self.start = coordinates
            self.board.LightRed(index)
            self.clicks = 1
            self.move_label.text = (str(coordinates)+' -> ').upper()
        else:
            self.end = coordinates
            self.board.LightGreen(index)
            self.clicks = 0
            self.move_label.text += str(coordinates).upper()

    def commit_move(self, button):
        self.Orienteer.invert()
        self.board.UnlightAll()
        self.move_label.text = ''
        self.GameProcessor.make_turn(self.start,self.end)
        self.board.draw(self.Orienteer.oriented_board(self.get_board()))

    def restart(self, button):
        print(self.main_layout.children)


if __name__ == "__main__":
    app = MainApp()
    app.run()
