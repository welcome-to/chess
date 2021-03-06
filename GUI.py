from kivy.app import App
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from const import *
from widgets import LabelB, BoardWidget,Cell
from game_engine import GameProcessor
from board import Coordinates, Move
from Electronic_Kasparov_2 import GameBrains


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
        return [7 - coordinates[0], 7 - coordinates[1]]

    def oriented_board(self,board):
        if self.orientation:
            return board
        return list(reversed(board))


class MainApp(App):
    def build(self):
        self.savelog = False
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
            on_press=self.c_game_mode,
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

    def commit_game_mode(self,button):
        self.game_type = button.text
        self.draw_game_screen(button)

    def c_game_mode(self,button):
        self.start_screen.remove_widget(self.start_screen.children[0])
        self.game_mode = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.3, 0.4),
            pos_hint={'center_x': 0.7, 'center_y': 0.4}
        )
        one_player = Button(
            text='1 Player',
            on_press=self.commit_game_mode,
            background_normal='',
            background_color=INITIAL_BUTTON_COLOR,
            color=[0, 0, 0, 1]
        )
        two_players = Button(
            text='2 Player',
            on_press=self.commit_game_mode,
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
        self.game_mode.add_widget(one_player)
        self.game_mode.add_widget(two_players)
        self.game_mode.add_widget(back_to_start_screen)
        self.start_screen.add_widget(self.game_mode)

    def draw_game_screen(self,button):
        self.main_layout.remove_widget(self.main_layout.children[0])
        if self.game_type == '1 Player':
            self.game_mode = ONEPLAYER
        else:
            self.game_mode = TWOPLAYERS
        self.GameProcessor = GameProcessor()
        self.GameProcessor.savelog(self.savelog)
        self.Algorithm = GameBrains(BLACK)
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
            pos_hint={'center_x':1.25,'center_y':0.66},
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
        self.gameplay.add_widget(Button(
            text='Main menu',
            on_press=self.back_to_main_menu,
            size_hint=[0.35,0.1],
            pos_hint={'center_x':1.25,'center_y':0.78},
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
        #FIXME Make some grouped separate procedure.
        self.start = None
        self.end = None

        self.Orienteer.invert()
        self.board = BoardWidget(self.Orienteer.oriented_board(self.get_board()),self.input_move)
        self.gameplay.add_widget(self.board)
        self.main_layout.add_widget(self.gameplay)

    def leave(self, button):
        exit()

    def back_to_main_menu(self,button):
        self.main_layout.remove_widget(self.main_layout.children[0])
        self.main_layout.add_widget(self.start_screen)

    def gameover(self,reason):
        self.main_layout.remove_widget(self.gameplay)
        if reason != TIE:
            source = WIN_IMAGE
            if reason == WHITE_WIN:
                color = BLACK_WIN
            else:
                color = WHITE_WIN
            text = ' You Lose ('+ color + ') '
        else:
            source = TIE_IMAGE
            text = ' potom '
        del self.GameProcessor 
        self.Gameover = FloatLayout()
        self.Gameover.add_widget(Image(
            source = source,
            size_hint = (1,1),
            pos_hint = {'center_x': 0.5,'center_y':0.5}
        ))
        self.Gameover.add_widget(LabelB(
            bcolor = [0,0,0,0],
            text = text,
            size_hint = (0.3,1),
            pos_hint = {'center_x': 0.5,'center_y':0.7},
            color = [1,0,0,1],
            font_size = 160,
            font_name = FAIL
        ))
        self.Gameover.add_widget(Button(
            text = 'Restart',
            color = [0,0,0,1],
            on_press = self.draw_game_screen,
            background_normal = '',
            background_color = [1,0,0,1],
            pos_hint = {'center_x': 0.20,'center_y':0.15},
            size_hint = (0.20,0.15)
        ))
        self.Gameover.add_widget(Button(
            text = 'Quit',color = [0,0,0,1],
            on_press = self.leave,
            background_normal = '',
            background_color = [1,0,0,1],
            pos_hint = {'center_x': 0.80,'center_y': 0.15},
            size_hint = (0.20,0.15)
        ))
        self.Gameover.add_widget(Button(
            text = 'Main menu',color = [0,0,0,1],
            on_press = self.back_to_start,
            background_normal = '',
            background_color = [1,0,0,1],
            pos_hint = {'center_x': 0.5,'center_y': 0.15},
            size_hint = (0.20,0.15)
        ))
        self.main_layout.add_widget(self.Gameover)
        print(reason)

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
        self.start_screen.remove_widget(self.start_screen.children[0])
        self.start_screen.add_widget(self.buttons)
        self.back_to_main_menu('')

    def crimea(self, button):
        if button.text == 'Whose Crimea?: Russian':
            button.text = 'Whose Crimea?: Ukraine'
        else:
            button.text = 'Whose Crimea?: Russian'

    def loging(self, button):
        if button.text == 'Loging: No':
            button.text = 'Loging: Yes'
            self.savelog = True 
        else:
            button.text = 'Loging: No'
            self.savelog = False

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
                figure = self.GameProcessor.board.data[i][7-j]
                if figure is None:
                    board_list.append(NOTHING)
                else:
                    board_list.append(figurecolor[figure.color]+figuretype[figure.type])
            board_list.append(str(i+1))
        board_list.append('')
        for i in list(reversed(listoflaters)):
            board_list.append(i)
        board_list.append('')
        return board_list

    def figure_input(self):
        self.inputer = BoxLayout(orientation='horizontal',pos_hint={'center_x':0.5, 'center_y': 0.5},size_hint = (1,0.5))
        color = figurecolor[BLACK]
        source_list = [color+figuretype[types] for types in [QUEEN,KNIGHT,ROOK,BISHOP]]
        for source in source_list:
            cell = Cell(COLOROFCELL1)
            cell.add_widget(Button(text = '',
                                   background_color = [0,0,0,0],
                                   background_normal = '',
                                   on_press = self.chooser,
                                   size_hint = (1,1),
                                   pos_hint = {'center_x': 0.5, 'center_y': 0.5}))
            cell.updateimage(source)
            self.inputer.add_widget(cell)
        self.gameplay.add_widget(self.inputer)

    def chooser(self,button):
        for Cell in self.inputer.children:
            if Cell.children[0] == button:
                self.figure_to_create = figuretypeback[Cell.image.source[5:]]
                self.move_label.text += ' figure: '+ self.figure_to_create
                break  
        self.gameplay.remove_widget(self.inputer)

    def input_move(self, index):
        coordinates =  7-((index%10)-1),(index//10)-1
        coordinates = Coordinates(self.Orienteer.oriented_coordinates(coordinates)[0],
                                  self.Orienteer.oriented_coordinates(coordinates)[1]
                                  )
        if self.clicks == 0:
            self.board.UnlightAll()
            self.start = coordinates
            self.board.Light(index,COLORS['RED'])
            self.figure_to_create = None
            self.clicks = 1
            self.move_label.text = (str(coordinates)+' -> ').upper()
            possible_moves = self.GameProcessor.current_allowed_moves()
            possible_moves_from_position = []
            for move in possible_moves:
                if move.start==self.start:
                    possible_moves_from_position.append(move.end)
            self.final_figure_chooser = False
            for move in possible_moves:
                if move.after_conversion is not None:
                    self.final_figure_chooser = True
            for coord in possible_moves_from_position:
                coord = self.Orienteer.oriented_coordinates([coord.x,coord.y])
                coord[0]+=1
                coord[1]+=1
                index1 = (coord[1])*10+(9-coord[0])
                self.board.Light(index1,COLORS['BLUE'])
            self.start_index = index
            return
        self.end = coordinates
        self.board.UnlightAll()
        self.board.Light(self.start_index,COLORS['RED'])
        self.board.Light(index,COLORS['GREEN'])
        self.clicks = 0
        self.move_label.text += str(coordinates).upper()
        if self.final_figure_chooser:
            self.figure_input()

    def commit_move(self, button):
        # do nothing if move is not chosen
        if self.start is None and self.end is None:
            return

        if self.game_mode == TWOPLAYERS:
            self.Orienteer.invert()
        self.board.UnlightAll()
        self.move_label.text = ''
        self.GameProcessor.make_move(self.start,self.end,figure_to_create=self.figure_to_create)
        self.start = None
        self.end = None
        self.figure_to_create = None
        result = self.GameProcessor.game_result()
        if not result == None:
            self.gameover(result)
            return
        if self.game_mode != TWOPLAYERS:
            move_start, move_end, figure_to_create = self.Algorithm.get_move(self.GameProcessor.board,self.GameProcessor.last_move())
            self.GameProcessor.make_move(move_start,move_end,figure_to_create=figure_to_create)
        self.board.draw(self.Orienteer.oriented_board(self.get_board()))
        result = self.GameProcessor.game_result()
        if not result == None:
            self.gameover(result)
